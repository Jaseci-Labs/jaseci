"""Custom MkDocs server with additional HTTP headers and build step."""

import http.server
import os
import socketserver
import subprocess


class CustomHeaderHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that adds custom headers for CORS and embedding policies."""

    def end_headers(self) -> None:
        """Add custom HTTP headers before ending headers."""
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


def serve_with_headers() -> None:
    """Build the MkDocs site and serve it with custom headers."""
    port = 8000

    # Step 1: Build MkDocs site
    print("Building MkDocs site...")
    subprocess.run(["mkdocs", "build"], check=True)

    # Step 2: Change working directory to the 'site/' folder
    site_dir = os.path.join(os.getcwd(), "site")
    os.chdir(site_dir)

    # Step 3: Start the custom server
    with socketserver.ThreadingTCPServer(("", port), CustomHeaderHandler) as httpd:
        print(f"Serving on http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    serve_with_headers()
