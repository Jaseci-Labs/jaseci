"""MkDocs development server with file watching and automatic rebuilds.

This module provides a custom HTTP server for serving an MkDocs site locally,
with file system watching to trigger rebuilds when source files change.
It uses a debounced rebuild mechanism to avoid excessive rebuilds during rapid file changes.
"""

import http.server
import os
import socketserver
import subprocess
import threading
from typing import Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class CustomHeaderHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with custom security headers for MkDocs site serving."""

    def end_headers(self) -> None:
        """Add security headers to HTTP responses."""
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

    def send_error(
        self, code: int, message: Optional[str] = None, explain: Optional[str] = None
    ) -> None:
        """Serve custom 404.html page for 404 errors."""
        if code == 404:
            try:
                with open("404.html", "rb") as f:
                    content = f.read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception:
                super().send_error(code, message, explain)
        else:
            super().send_error(code, message, explain)


class DebouncedRebuildHandler(FileSystemEventHandler):
    """File system event handler for debounced MkDocs site rebuilding."""

    def __init__(self, root_dir: str, debounce_seconds: int = 10) -> None:
        """Initialize the handler with root directory and debounce time."""
        self.root_dir = root_dir
        self.debounce_seconds = debounce_seconds
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

    def debounced_rebuild(self, event_type: str, path: str) -> None:
        """Schedule a debounced rebuild on file system events."""
        print(f"Change detected: {event_type} — {path}")
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce_seconds, self.rebuild)
            self._timer.start()

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory and "site" not in event.src_path:
            self.debounced_rebuild("modified", str(event.src_path))

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and "site" not in event.src_path:
            self.debounced_rebuild("created", str(event.src_path))

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion events."""
        if not event.is_directory and "site" not in event.src_path:
            self.debounced_rebuild("deleted", str(event.src_path))

    def rebuild(self) -> None:
        """Rebuild the MkDocs site."""
        print("\nRebuilding MkDocs site...")
        try:
            subprocess.run(["mkdocs", "build"], check=True, cwd=self.root_dir)
            print("Rebuild complete.")
        except subprocess.CalledProcessError as e:
            print(f"Rebuild failed: {e}")


def serve_with_watch() -> None:
    """Serve MkDocs site and watch for file changes to trigger rebuilds."""
    port = 8000
    root_dir = os.path.dirname(os.path.dirname(__file__))

    print("Initial build of MkDocs site...")
    subprocess.run(["mkdocs", "build"], check=True, cwd=root_dir)

    # Set up file watcher
    event_handler = DebouncedRebuildHandler(root_dir=root_dir, debounce_seconds=20)
    observer = Observer()

    # Watch everything except the site directory
    observer.schedule(event_handler, root_dir, recursive=True)
    observer.start()

    # Change working dir to 'site' and start server
    site_dir = os.path.join(root_dir, "site")
    os.chdir(site_dir)
    print(f"Serving at http://localhost:{port}")

    try:
        with socketserver.ThreadingTCPServer(("", port), CustomHeaderHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    serve_with_watch()
