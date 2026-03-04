from croc.components.base import Component
from typing import List, Optional, Union


class VStack(Component):
    """Vertical stack layout."""
    def __init__(self, children=None, gap: str = "4", align: str = "stretch", **props):
        super().__init__(children=children, gap=gap, align=align, **props)


class HStack(Component):
    """Horizontal stack layout."""
    def __init__(self, children=None, gap: str = "4", align: str = "center", **props):
        super().__init__(children=children, gap=gap, align=align, **props)


class Grid(Component):
    """CSS Grid layout."""
    def __init__(self, children=None, cols: int = 2, gap: str = "4", **props):
        super().__init__(children=children, cols=cols, gap=gap, **props)


class Box(Component):
    """Generic container box."""
    def __init__(self, children=None, padding: str = "4", **props):
        super().__init__(children=children, padding=padding, **props)


class Divider(Component):
    """Horizontal rule / divider."""
    def __init__(self, **props):
        super().__init__(children=[], **props)


class Spacer(Component):
    """Flexible spacer."""
    def __init__(self, size: str = "4", **props):
        super().__init__(children=[], size=size, **props)


class Center(Component):
    """Centers its children."""
    def __init__(self, children=None, **props):
        super().__init__(children=children, **props)


class Page(Component):
    """Top-level page wrapper."""
    def __init__(self, children=None, title: str = "croc app", **props):
        super().__init__(children=children, title=title, **props)
