import html


def render_task_item(task, is_completed):
    safe_title = html.escape(task["title"])
    safe_date = html.escape(task.get("created_at", ""))
    task_id = task["id"]

    if is_completed:
        action_button = ""
        title_class = "task-title completed"
    else:
        action_button = (
            f'<form method="POST" action="/complete" class="inline-form">'
            f'<input type="hidden" name="id" value="{task_id}">'
            f'<button type="submit" class="btn-secondary">Complete</button>'
            f"</form>"
        )
        title_class = "task-title"

    delete_button = (
        f'<form method="POST" action="/delete" class="inline-form">'
        f'<input type="hidden" name="id" value="{task_id}">'
        f'<button type="submit" class="btn-ghost" title="Delete task">Delete</button>'
        f"</form>"
    )

    return (
        f'<li class="task-row">'
        f'<div class="task-info">'
        f'<span class="{title_class}">{safe_title}</span>'
        f'<span class="task-date">{safe_date}</span>'
        f"</div>"
        f'<div class="task-actions">{action_button}{delete_button}</div>'
        f"</li>"
    )


def render_page(pending_tasks, completed_tasks):
    if pending_tasks:
        pending_html = "".join(render_task_item(t, False) for t in pending_tasks)
        pending_section = f'<ul class="task-list">{pending_html}</ul>'
    else:
        pending_section = '<p class="empty-state">No pending tasks. Add one above to get started.</p>'

    if completed_tasks:
        completed_html = "".join(render_task_item(t, True) for t in completed_tasks)
        completed_section = (
            f'<section class="card muted-card">'
            f'<div class="section-header">'
            f"<h2>Completed</h2>"
            f'<span class="badge">{len(completed_tasks)}</span>'
            f"</div>"
            f'<ul class="task-list">{completed_html}</ul>'
            f"</section>"
        )
    else:
        completed_section = ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Task Manager</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #F8F9FA;
      color: #1A2238;
      line-height: 1.5;
      padding: 48px 16px;
    }}
    .container {{
      max-width: 640px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }}
    h1 {{
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      font-size: 14px;
      color: #5A6478;
    }}
    .card {{
      background-color: #FFFFFF;
      border: 1px solid #E5E7EB;
      border-radius: 12px;
      padding: 24px;
    }}
    .muted-card {{
      background-color: #F3F4F6;
    }}
    .add-form {{
      display: flex;
      gap: 12px;
    }}
    input[type="text"] {{
      flex: 1;
      padding: 12px 16px;
      font-size: 15px;
      font-family: inherit;
      color: #1A2238;
      background-color: #F8F9FA;
      border: 1px solid #D1D5DB;
      border-radius: 8px;
      outline: none;
    }}
    input[type="text"]:focus {{
      border-color: #2563EB;
      background-color: #FFFFFF;
    }}
    button {{
      font-family: inherit;
      font-size: 14px;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      border: none;
      transition: background-color 0.15s ease;
    }}
    .btn-primary {{
      background-color: #2563EB;
      color: #FFFFFF;
      padding: 12px 20px;
    }}
    .btn-primary:hover {{
      background-color: #1D4ED8;
    }}
    .btn-secondary {{
      background-color: #EFF6FF;
      color: #2563EB;
      padding: 8px 12px;
    }}
    .btn-secondary:hover {{
      background-color: #DBEAFE;
    }}
    .btn-ghost {{
      background-color: transparent;
      color: #6B7280;
      padding: 8px 12px;
    }}
    .btn-ghost:hover {{
      background-color: #FEE2E2;
      color: #DC2626;
    }}
    .section-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }}
    h2 {{
      font-size: 16px;
      font-weight: 600;
    }}
    .badge {{
      background-color: #E5E7EB;
      color: #1A2238;
      font-size: 12px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 999px;
    }}
    .task-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .task-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding: 12px 16px;
      background-color: #F8F9FA;
      border-radius: 8px;
      border: 1px solid #E5E7EB;
    }}
    .muted-card .task-row {{
      background-color: #FFFFFF;
    }}
    .task-info {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .task-title {{
      font-size: 15px;
      font-weight: 500;
    }}
    .task-title.completed {{
      text-decoration: line-through;
      color: #6B7280;
    }}
    .task-date {{
      font-size: 12px;
      color: #6B7280;
    }}
    .task-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .inline-form {{
      display: inline;
    }}
    .empty-state {{
      font-size: 14px;
      color: #6B7280;
      padding: 16px 0 4px;
    }}
  </style>
</head>
<body>
  <main class="container">
    <header>
      <h1>Student Task Manager</h1>
      <span class="subtitle">{len(pending_tasks)} pending</span>
    </header>

    <section class="card">
      <form method="POST" action="/add" class="add-form">
        <input type="text" name="title" placeholder="Add a daily task (e.g., Revise Python loops)" required autofocus>
        <button type="submit" class="btn-primary">Add Task</button>
      </form>
    </section>

    <section class="card">
      <div class="section-header">
        <h2>Pending Tasks</h2>
        <span class="badge">{len(pending_tasks)}</span>
      </div>
      {pending_section}
    </section>

    {completed_section}
  </main>
</body>
</html>"""
