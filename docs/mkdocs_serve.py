import os
import http.server
import socketserver
import subprocess


class CustomHeaderHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


def serve_with_headers():
    PORT = 8000

    # Step 1: Build MkDocs site
    print("Building MkDocs site...")
    subprocess.run(["mkdocs", "build"], check=True)

    # Step 2: Change working directory to the 'site/' folder
    site_dir = os.path.join(os.getcwd(), "site")
    os.chdir(site_dir)

    # Step 3: Start the custom server
    with socketserver.TCPServer(("", PORT), CustomHeaderHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    serve_with_headers()
