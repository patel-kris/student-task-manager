# Student Task Manager — Technical Documentation

This document explains how the **Student Task Manager** works internally, including its architecture, data format, HTTP routes, and every Python function.

---

## 1. Architecture Overview

The application uses **only Python's built-in standard library** (`http.server`, `json`, `urllib.parse`, `html`, `os`, `datetime`, `threading`, `webbrowser`).

| Layer | File | Responsibility |
| :--- | :--- | :--- |
| Web Server & Routing | `app.py` | Handles browser `GET` and `POST` requests on `http://127.0.0.1:8000` |
| Business Logic & Storage | `task_manager.py` | Reads, writes, adds, completes, deletes, and filters tasks in `tasks.json` |
| User Interface | `ui.py` | Generates the HTML/CSS web page as a Python string |
| Verification | `test_task_manager.py` | Runs automated `unittest` checks on all task functions |

### Request Flow (POST-Redirect-GET)

1. The user opens `http://127.0.0.1:8000/` (`GET /`).
2. `app.py` fetches pending and completed tasks from `task_manager.py` and passes them to `ui.py` to render the HTML page.
3. When the user clicks **Add Task**, **Complete**, or **Delete**, the browser sends a `POST` request (`/add`, `/complete`, or `/delete`).
4. `app.py` updates `tasks.json` via `task_manager.py` and responds with `303 See Other` redirecting back to `/`, so refreshing the page never resubmits a form.

---

## 2. Data Storage (`tasks.json`)

Tasks are stored as a JSON array in `tasks.json` (created automatically on first task addition). Each task object has four fields:

```json
{
  "id": 1,
  "title": "Revise Python loops",
  "completed": false,
  "created_at": "2026-11-21"
}
```

---

## 3. Function Reference

### `task_manager.py`

#### `load_tasks(filepath="tasks.json")`
- **Purpose:** Loads all saved tasks from the JSON file.
- **How it works:** Checks if `filepath` exists using `os.path.exists`. If not, returns an empty list `[]`. Otherwise opens the file, parses JSON safely, and returns `[]` if the file is empty or malformed.

#### `save_tasks(tasks, filepath="tasks.json")`
- **Purpose:** Writes the updated list of task dictionaries back to disk.
- **How it works:** Opens `filepath` in write mode (`"w"`) with UTF-8 encoding and serializes `tasks` using `json.dump(..., indent=2)`.

#### `add_task(title, filepath="tasks.json")`
- **Purpose:** Creates and saves a new pending task.
- **How it works:** Trims leading/trailing spaces from `title`. If empty, returns `None`. Otherwise loads existing tasks, computes `next_id` as `max(existing_ids) + 1` (or `1` if empty), creates the new task dictionary with `completed=False` and today's ISO date, appends it, saves, and returns the new task.

#### `complete_task(task_id, filepath="tasks.json")`
- **Purpose:** Marks a specific task as completed.
- **How it works:** Loads tasks, loops through to find the task matching `task_id`, sets `task["completed"] = True`, saves if found, and returns `True` (or `False` if the ID was not found).

#### `delete_task(task_id, filepath="tasks.json")`
- **Purpose:** Permanently removes a task by its ID.
- **How it works:** Loads tasks and builds a new list excluding the matching `task_id`. If the list length changed, saves the remaining tasks and returns `True`; otherwise returns `False`.

#### `get_pending_tasks(filepath="tasks.json")`
- **Purpose:** Returns only tasks where `completed` is `False`.

#### `get_completed_tasks(filepath="tasks.json")`
- **Purpose:** Returns only tasks where `completed` is `True`.

---

### `ui.py`

#### `render_task_item(task, is_completed)`
- **Purpose:** Builds the HTML `<li>` row for a single task.
- **How it works:** Escapes `task["title"]` and `task["created_at"]` with `html.escape()` to prevent HTML injection, renders a **Complete** button form only for pending tasks, and renders a **Delete** button form for every task.

#### `render_page(pending_tasks, completed_tasks)`
- **Purpose:** Builds the complete HTML5 + CSS page returned to the browser.
- **How it works:** Uses `render_task_item()` to populate the **Pending Tasks** card (or an empty-state message) and the **Completed** card when completed tasks exist.

---

### `app.py`

#### `TaskHandler.do_GET(self)`
- **Purpose:** Serves the main web page on `/`.
- **How it works:** Returns `404` for unknown paths; otherwise calls `render_page(get_pending_tasks(), get_completed_tasks())` and sends it with `200 OK`.

#### `TaskHandler.do_POST(self)`
- **Purpose:** Handles form submissions for `/add`, `/complete`, and `/delete`.
- **How it works:** Reads `Content-Length` bytes from `self.rfile`, parses URL-encoded form fields with `urllib.parse.parse_qs`, dispatches to the matching `task_manager` function, and sends a `303` redirect back to `/`.

#### `run_server(host="127.0.0.1", port=8000, open_browser=True)`
- **Purpose:** Starts the local Python HTTP server.
- **How it works:** Instantiates `HTTPServer`, optionally launches the default browser after 0.5 seconds via `threading.Timer`, and runs `serve_forever()` until `Ctrl+C` is pressed.
