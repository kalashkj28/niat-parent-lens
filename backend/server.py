"""
Production HTTP Server for NIAT Parent Decision Lens
Runs completely on Python 3.12 standard libraries with zero external dependencies.
Serves REST API endpoints and static frontend files.
"""

import http.server
import socketserver
import json
import os
import sys
import mimetypes
from urllib.parse import urlparse, parse_qs

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import init_db, get_leads, add_feedback, get_metrics
from backend.agent import run_growth_agent
from backend.learning_loop import compute_conversion_analytics

PORT = int(os.environ.get("PORT", 8080))
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

class GrowthSystemHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, status_code: int, data: dict):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/metrics":
            metrics = get_metrics()
            self._send_json(200, metrics)
            return

        elif path == "/api/leads":
            leads = get_leads()
            self._send_json(200, {"leads": leads})
            return

        elif path == "/api/learning":
            learning_data = compute_conversion_analytics()
            self._send_json(200, learning_data)
            return

        # Static File Serving
        if path == "/" or path == "":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            clean_path = path.lstrip("/")
            file_path = os.path.join(FRONTEND_DIR, clean_path)

        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", f"{content_type}; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self._send_json(500, {"error": f"Failed reading file: {str(e)}"})
        else:
            self._send_json(404, {"error": "File not found", "path": path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)

        try:
            payload = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception:
            self._send_json(400, {"error": "Invalid JSON payload in request"})
            return

        if path == "/api/analyze":
            try:
                result = run_growth_agent(payload)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": f"Agent execution error: {str(e)}"})

        elif path == "/api/feedback":
            try:
                fb_id = add_feedback(payload)
                self._send_json(200, {"status": "FEEDBACK_LOGGED", "feedback_id": fb_id})
            except Exception as e:
                self._send_json(500, {"error": f"Feedback logging error: {str(e)}"})

        else:
            self._send_json(404, {"error": "Endpoint not recognized", "path": path})

def run_server(port=PORT):
    init_db()
    server_address = ("", port)
    httpd = socketserver.TCPServer(server_address, GrowthSystemHandler)
    print(f"NIAT Parent Decision Lens server running on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
