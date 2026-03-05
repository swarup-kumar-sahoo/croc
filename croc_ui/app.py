"""
App class for croc-ui — runs a local dev server.
"""
import os
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Dict, Optional, Union

from .page import Page


class _CrocHandler(BaseHTTPRequestHandler):
    """Internal HTTP request handler."""

    routes: Dict[str, Union[str, "Page", Callable]] = {}
    static_dir: Optional[str] = None

    def log_message(self, format, *args):
        # Suppress default server logs; we print our own
        pass

    def _serve_content(self, content: str, status: int = 200, content_type: str = "text/html"):
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", len(encoded))
        self.end_headers()
        self.wfile.write(encoded)

    def _serve_file(self, filepath: str):
        ext = os.path.splitext(filepath)[1].lower()
        mime = {
            ".css": "text/css", ".js": "application/javascript",
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml", ".ico": "image/x-icon",
            ".woff": "font/woff", ".woff2": "font/woff2",
            ".ttf": "font/ttf", ".otf": "font/otf",
            ".json": "application/json", ".txt": "text/plain",
        }.get(ext, "application/octet-stream")

        try:
            mode = "rb" if mime.startswith("image") or mime.startswith("font") or mime == "application/octet-stream" else "r"
            with open(filepath, mode) as f:
                data = f.read()
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self._serve_content(f"Error reading file: {e}", 500)

    def do_GET(self):
        path = self.path.split("?")[0]

        # Try exact route match
        if path in self.routes:
            handler = self.routes[path]
            if callable(handler) and not isinstance(handler, Page):
                result = handler()
            else:
                result = handler
            if isinstance(result, Page):
                self._serve_content(result.render())
            else:
                self._serve_content(str(result))
            return

        # Try static files
        if self.static_dir:
            static_path = os.path.join(self.static_dir, path.lstrip("/"))
            if os.path.isfile(static_path):
                self._serve_file(static_path)
                return

        # 404
        not_found_html = f"""<!DOCTYPE html>
<html><head><title>404 Not Found</title>
<style>
  body {{ font-family: system-ui; display: flex; align-items: center; justify-content: center;
         height: 100vh; margin: 0; background: #0f172a; color: #f1f5f9; }}
  .box {{ text-align: center; }}
  h1 {{ font-size: 5rem; margin: 0; color: #3b82f6; }}
  p {{ color: #94a3b8; }}
  a {{ color: #60a5fa; }}
</style></head>
<body><div class="box">
  <h1>404</h1>
  <p>Page <code>{path}</code> not found.</p>
  <p><a href="/">← Go Home</a></p>
</div></body></html>"""
        self._serve_content(not_found_html, 404)


class App:
    """
    croc-ui development server.

    Usage:
        app = App()

        @app.route("/")
        def home():
            page = Page(title="Home")
            page.add(H1("Hello World!"))
            return page

        app.run()
    """

    def __init__(self, static_dir: Optional[str] = None, debug: bool = True):
        self._routes: Dict[str, Union[str, Page, Callable]] = {}
        self.static_dir = static_dir
        self.debug = debug
        self._server: Optional[HTTPServer] = None

    def route(self, path: str):
        """Decorator to register a route."""
        def decorator(fn: Callable):
            self._routes[path] = fn
            return fn
        return decorator

    def add_route(self, path: str, handler: Union[str, Page, Callable]):
        """Programmatically add a route."""
        self._routes[path] = handler
        return self

    def add_page(self, path: str, page: Page):
        """Add a Page directly to a route."""
        self._routes[path] = page
        return self

    def _make_handler(self):
        routes = self._routes
        static_dir = self.static_dir

        class Handler(_CrocHandler):
            pass
        Handler.routes = routes
        Handler.static_dir = static_dir
        return Handler

    def run(self, host: str = "127.0.0.1", port: int = 3000,
            open_browser: bool = True, reload: bool = False):
        """
        Start the croc-ui development server.

        Args:
            host: Host to bind (default: 127.0.0.1)
            port: Port to listen on (default: 3000)
            open_browser: Open browser automatically (default: True)
            reload: Auto-reload on file changes (default: False, future feature)
        """
        handler = self._make_handler()
        self._server = HTTPServer((host, port), handler)

        url = f"http://{host}:{port}"

        CYAN    = "\033[1;36m"
        GREEN   = "\033[0;32m"
        YELLOW  = "\033[1;33m"
        MAGENTA = "\033[1;35m"
        DIM     = "\033[2m"
        RESET   = "\033[0m"

        logo = f"""
{CYAN} ██████╗██████╗  ██████╗  ██████╗ {RESET}
{CYAN}██╔════╝██╔══██╗██╔═══██╗██╔════╝{RESET}
{CYAN}██║     ██████╔╝██║   ██║██║     {RESET}
{CYAN}██║     ██╔══██╗██║   ██║██║     {RESET}
{CYAN}╚██████╗██║  ██║╚██████╔╝╚██████╗{RESET}
{CYAN} ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝{RESET}
{DIM}  Python UI Library  v1.0.2{RESET}"""

        bar = f"{DIM}  {'━' * 36}{RESET}"

        print(logo)
        print(bar)
        print(f"  {GREEN}▶  Server{RESET}    {CYAN}{url}{RESET}")
        print(f"  {GREEN}▶  Routes{RESET}    {YELLOW}{len(self._routes)} registered{RESET}")
        for p in self._routes:
            print(f"       {DIM}│{RESET}  {GREEN}{p}{RESET}")
        if self.static_dir:
            print(f"  {GREEN}▶  Static{RESET}    {self.static_dir}")
        print(bar)
        print(f"  {DIM}Press Ctrl+C to stop{RESET}\n")

        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            print("\n  🛑  Server stopped.")
            self._server.server_close()

    def stop(self):
        """Stop the server."""
        if self._server:
            self._server.shutdown()
            self._server.server_close()