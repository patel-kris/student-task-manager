import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from task_manager import (
    add_task,
    complete_task,
    delete_task,
    get_completed_tasks,
    get_pending_tasks,
)
from ui import render_page


class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return

        html_content = render_page(get_pending_tasks(), get_completed_tasks())
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form_data = urllib.parse.parse_qs(raw_body)

        if self.path == "/add":
            title = form_data.get("title", [""])[0]
            add_task(title)
        elif self.path == "/complete":
            raw_id = form_data.get("id", [""])[0]
            if raw_id.isdigit():
                complete_task(int(raw_id))
        elif self.path == "/delete":
            raw_id = form_data.get("id", [""])[0]
            if raw_id.isdigit():
                delete_task(int(raw_id))

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run_server(host="127.0.0.1", port=8000, open_browser=True):
    server = HTTPServer((host, port), TaskHandler)
    url = f"http://{host}:{port}"
    print(f"Student Task Manager running at {url}")
    print("Press Ctrl+C to stop the server.")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
