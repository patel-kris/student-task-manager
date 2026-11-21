import json
import os
from datetime import date


def load_tasks(filepath="tasks.json"):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_tasks(tasks, filepath="tasks.json"):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def add_task(title, filepath="tasks.json"):
    clean_title = title.strip()
    if not clean_title:
        return None
    tasks = load_tasks(filepath)
    next_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {
        "id": next_id,
        "title": clean_title,
        "completed": False,
        "created_at": date.today().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks, filepath)
    return new_task


def complete_task(task_id, filepath="tasks.json"):
    tasks = load_tasks(filepath)
    updated = False
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            updated = True
            break
    if updated:
        save_tasks(tasks, filepath)
    return updated


def delete_task(task_id, filepath="tasks.json"):
    tasks = load_tasks(filepath)
    remaining = [task for task in tasks if task["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    save_tasks(remaining, filepath)
    return True


def get_pending_tasks(filepath="tasks.json"):
    return [task for task in load_tasks(filepath) if not task["completed"]]


def get_completed_tasks(filepath="tasks.json"):
    return [task for task in load_tasks(filepath) if task["completed"]]
