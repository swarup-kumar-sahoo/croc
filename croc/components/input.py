from croc.components.base import Component
from typing import Callable, List, Optional, Tuple


class Button(Component):
    """Clickable button."""
    def __init__(self, label: str = "Button", on_click: Optional[Callable] = None,
                 variant: str = "primary", disabled: bool = False, **props):
        super().__init__(children=[label], variant=variant, disabled=disabled, **props)
        if on_click:
            self._event_handlers["click"] = on_click


class Input(Component):
    """Text input field."""
    def __init__(self, placeholder: str = "", value: str = "",
                 on_change: Optional[Callable] = None, input_type: str = "text",
                 label: Optional[str] = None, **props):
        super().__init__(children=[], placeholder=placeholder, value=value,
                         input_type=input_type, label=label, **props)
        if on_change:
            self._event_handlers["change"] = on_change


class Textarea(Component):
    """Multi-line text input."""
    def __init__(self, placeholder: str = "", value: str = "",
                 on_change: Optional[Callable] = None, rows: int = 4,
                 label: Optional[str] = None, **props):
        super().__init__(children=[], placeholder=placeholder, value=value,
                         rows=rows, label=label, **props)
        if on_change:
            self._event_handlers["change"] = on_change


class Select(Component):
    """Dropdown select."""
    def __init__(self, options: List[Tuple[str, str]] = None,
                 value: str = "", on_change: Optional[Callable] = None,
                 label: Optional[str] = None, **props):
        super().__init__(children=[], options=options or [], value=value,
                         label=label, **props)
        if on_change:
            self._event_handlers["change"] = on_change


class Checkbox(Component):
    """Checkbox input."""
    def __init__(self, label: str = "", checked: bool = False,
                 on_change: Optional[Callable] = None, **props):
        super().__init__(children=[], label=label, checked=checked, **props)
        if on_change:
            self._event_handlers["change"] = on_change


class Switch(Component):
    """Toggle switch."""
    def __init__(self, label: str = "", checked: bool = False,
                 on_change: Optional[Callable] = None, **props):
        super().__init__(children=[], label=label, checked=checked, **props)
        if on_change:
            self._event_handlers["change"] = on_change


class Slider(Component):
    """Range slider."""
    def __init__(self, min: int = 0, max: int = 100, value: int = 50,
                 on_change: Optional[Callable] = None, label: Optional[str] = None, **props):
        super().__init__(children=[], min=min, max=max, value=value, label=label, **props)
        if on_change:
            self._event_handlers["change"] = on_change
