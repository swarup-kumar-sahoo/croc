from typing import Callable, Dict, Optional
from .components.base import Component


class Router:
    """
    Simple path-based router for croc apps.

    Usage:
        router = Router()

        @router.page("/")
        def home():
            return VStack([Heading("Home")])

        @router.page("/about")
        def about():
            return VStack([Heading("About")])
    """

    def __init__(self):
        self._routes: Dict[str, Callable] = {}
        self._not_found: Optional[Callable] = None

    def page(self, path: str):
        """Decorator to register a page at the given path."""
        def decorator(fn: Callable):
            self._routes[path] = fn
            return fn
        return decorator

    def not_found(self, fn: Callable):
        """Register a 404 page."""
        self._not_found = fn
        return fn

    def resolve(self, path: str) -> Optional[Component]:
        """Resolve a path to a rendered component."""
        handler = self._routes.get(path)
        if handler is None:
            if self._not_found:
                return self._not_found()
            return None
        return handler()

    @property
    def paths(self):
        return list(self._routes.keys())