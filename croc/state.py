import asyncio
from typing import Any, Callable, Dict, List, Optional, Set


class State:
    """
    Reactive state container for croc apps.

    Usage:
        state = State(count=0, name="world")
        state.count += 1  # triggers re-render
    """

    def __init__(self, **initial):
        object.__setattr__(self, "_data", dict(initial))
        object.__setattr__(self, "_listeners", [])
        object.__setattr__(self, "_dirty", False)

    def __getattr__(self, key: str) -> Any:
        data = object.__getattribute__(self, "_data")
        if key in data:
            return data[key]
        raise AttributeError(f"State has no attribute '{key}'")

    def __setattr__(self, key: str, value: Any):
        data = object.__getattribute__(self, "_data")
        data[key] = value
        object.__setattr__(self, "_dirty", True)
        self._notify()

    def _notify(self):
        listeners = object.__getattribute__(self, "_listeners")
        for callback in listeners:
            if asyncio.iscoroutinefunction(callback):
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.ensure_future(callback())
                    else:
                        loop.run_until_complete(callback())
                except RuntimeError:
                    pass
            else:
                callback()

    def subscribe(self, callback: Callable):
        """Subscribe to state changes."""
        listeners = object.__getattribute__(self, "_listeners")
        listeners.append(callback)

    def unsubscribe(self, callback: Callable):
        """Unsubscribe from state changes."""
        listeners = object.__getattribute__(self, "_listeners")
        if callback in listeners:
            listeners.remove(callback)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to dict."""
        data = object.__getattribute__(self, "_data")
        return {k: v for k, v in data.items() if not callable(v)}

    def update(self, **kwargs):
        """Batch update multiple state values at once."""
        data = object.__getattribute__(self, "_data")
        data.update(kwargs)
        object.__setattr__(self, "_dirty", True)
        self._notify()