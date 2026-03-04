from croc.components.base import Component
from typing import Any, Dict, List, Optional


class Card(Component):
    """Content card with optional title."""
    def __init__(self, children=None, title: Optional[str] = None,
                 subtitle: Optional[str] = None, **props):
        super().__init__(children=children, title=title, subtitle=subtitle, **props)


class Image(Component):
    """Image display."""
    def __init__(self, src: str = "", alt: str = "", width: Optional[str] = None,
                 height: Optional[str] = None, **props):
        super().__init__(children=[], src=src, alt=alt, width=width, height=height, **props)


class Table(Component):
    """Data table."""
    def __init__(self, columns: List[str] = None, rows: List[List[Any]] = None,
                 striped: bool = True, **props):
        super().__init__(children=[], columns=columns or [], rows=rows or [],
                         striped=striped, **props)


class Alert(Component):
    """Alert / notification banner."""
    def __init__(self, message: str = "", variant: str = "info",
                 title: Optional[str] = None, **props):
        super().__init__(children=[message], variant=variant, title=title, **props)


class Spinner(Component):
    """Loading spinner."""
    def __init__(self, size: str = "md", **props):
        super().__init__(children=[], size=size, **props)


class Progress(Component):
    """Progress bar."""
    def __init__(self, value: int = 0, max: int = 100,
                 label: Optional[str] = None, **props):
        super().__init__(children=[], value=value, max=max, label=label, **props)


class Avatar(Component):
    """User avatar image or initials."""
    def __init__(self, src: Optional[str] = None, name: str = "",
                 size: str = "md", **props):
        super().__init__(children=[], src=src, name=name, size=size, **props)


class Stat(Component):
    """Statistic display with label and value."""
    def __init__(self, label: str = "", value: str = "",
                 delta: Optional[str] = None, **props):
        super().__init__(children=[], label=label, value=value, delta=delta, **props)
