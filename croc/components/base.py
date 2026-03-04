import uuid
from typing import Any, Callable, Dict, List, Optional


class Component:
    """Base class for all croc UI components."""

    def __init__(self, children=None, **props):
        self.id = str(uuid.uuid4())[:8]
        self.children = children or []
        if isinstance(self.children, Component):
            self.children = [self.children]
        self.props = props
        self._event_handlers: Dict[str, Callable] = {}

    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        self._event_handlers[event] = handler
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Serialize component to dict for sending to client."""
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "props": self._serialize_props(),
            "children": [
                c.to_dict() if isinstance(c, Component) else {"type": "text", "value": str(c)}
                for c in self.children
            ],
            "events": list(self._event_handlers.keys()),
        }

    def _serialize_props(self) -> Dict[str, Any]:
        """Serialize props, excluding non-serializable values."""
        result = {}
        for k, v in self.props.items():
            if callable(v):
                self._event_handlers[k.replace("on_", "").lower()] = v
                result[k] = True  # Signal to client that handler exists
            else:
                result[k] = v
        return result

    def collect_handlers(self) -> Dict[str, Callable]:
        """Recursively collect all event handlers in this subtree."""
        handlers = {f"{self.id}:{event}": fn for event, fn in self._event_handlers.items()}
        for child in self.children:
            if isinstance(child, Component):
                handlers.update(child.collect_handlers())
        return handlers
