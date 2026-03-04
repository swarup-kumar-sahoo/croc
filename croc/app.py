import logging
import uvicorn

from .router import Router
from .server import CrocServer
from .state import State
from .components import *  # re-export all components

logger = logging.getLogger("croc")


class App:
    """
    The main entry point for a croc application.

    Usage:
        import croc

        app = croc.App(title="My App")
        state = croc.State(count=0)

        @app.page("/")
        def home():
            def increment():
                state.count += 1

            return croc.Page([
                croc.Heading("Counter"),
                croc.Text(f"Count: {state.count}"),
                croc.Button("Increment", on_click=increment),
            ])

        app.run()
    """

    def __init__(self, title: str = "croc app", theme: str = "light"):
        self.title = title
        self.theme = theme
        self.router = Router()
        self._server: CrocServer = None

    def page(self, path: str):
        """Decorator to register a page route."""
        return self.router.page(path)

    def not_found(self, fn):
        """Register a custom 404 page."""
        return self.router.not_found(fn)

    def _get_server(self) -> CrocServer:
        if self._server is None:
            self._server = CrocServer(
                router=self.router,
                title=self.title,
                theme=self.theme,
            )
        return self._server

    @property
    def fastapi(self):
        """Access the underlying FastAPI app (for custom routes, middleware, etc.)."""
        return self._get_server().fastapi_app

    def run(self, host: str = "127.0.0.1", port: int = 8000, reload: bool = False,
            log_level: str = "info"):
        """Start the croc development server."""
        print(f"\n🐊 croc v0.1 — running at http://{host}:{port}\n")
        server = self._get_server()
        uvicorn.run(server.fastapi_app, host=host, port=port, log_level=log_level)