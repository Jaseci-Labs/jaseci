import http.server
import os
import socketserver
import subprocess


class CustomHeaderHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


def serve_with_headers() -> None:
    port = 8000

    # Step 1: Build MkDocs site from project root
    root_dir = os.path.dirname(os.path.dirname(__file__))
    print("Building MkDocs site...")
    subprocess.run(["mkdocs", "build"], check=True, cwd=root_dir)

    # Step 2: Change to the 'site' directory in project root
    site_dir = os.path.join(root_dir, "site")
    os.chdir(site_dir)

    # Step 3: Serve the site
    with socketserver.ThreadingTCPServer(("", port), CustomHeaderHandler) as httpd:
        print(f"Serving on http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    serve_with_headers()
