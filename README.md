# Student Task Manager

A beginner-friendly **Student Task Manager** web application built using **100% pure Python** (standard library only — no `pip install` or external frameworks required).

## Features

- **Add daily tasks** with automatic date stamping
- **Display pending tasks** in a clean, distraction-free list
- **Mark tasks as completed** with one click
- **Delete tasks** from either the pending or completed list
- **Automatic local storage** in `tasks.json`

## Project Structure

```text
student-task-manager/
├── .vscode/
│   └── launch.json          # Enables pressing F5 in VS Code to run
├── app.py                   # Built-in Python HTTP web server & router
├── task_manager.py          # Core task CRUD & JSON storage functions
├── ui.py                    # Pure-Python HTML/CSS page renderer
├── test_task_manager.py     # Automated unit tests
├── DOCUMENTATION.md         # Detailed function-by-function documentation
└── README.md                # Setup & VS Code deployment guide
```

## How to Run in VS Code

1. **Unzip** `student-task-manager.zip` to a folder on your computer.
2. Open **VS Code**, click **File → Open Folder...**, and select the `student-task-manager` folder.
3. Make sure the **Python** extension is installed in VS Code and Python 3 is selected.
4. Start the app using either method:
   - **Shortcut:** Press `F5` (uses `.vscode/launch.json`), **or**
   - **Terminal:** Open the integrated terminal (`Ctrl + ~`) and run:
     ```bash
     python app.py
     ```
5. Your browser will open automatically at **`http://127.0.0.1:8000`**.

## Running the Automated Tests

In the VS Code terminal, run:

```bash
python -m unittest test_task_manager.py -v
```
