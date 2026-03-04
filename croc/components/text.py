from croc.components.base import Component
from typing import Optional


class Text(Component):
    """Plain text / paragraph."""
    def __init__(self, content: str = "", size: str = "base", color: str = "default",
                 weight: str = "normal", **props):
        super().__init__(children=[content], size=size, color=color, weight=weight, **props)


class Heading(Component):
    """Heading element (h1–h6)."""
    def __init__(self, content: str = "", level: int = 1, **props):
        super().__init__(children=[content], level=level, **props)


class Label(Component):
    """Small label, often used with inputs."""
    def __init__(self, content: str = "", for_id: Optional[str] = None, **props):
        super().__init__(children=[content], for_id=for_id, **props)


class Badge(Component):
    """Small status badge."""
    def __init__(self, content: str = "", variant: str = "default", **props):
        super().__init__(children=[content], variant=variant, **props)


class Code(Component):
    """Inline code or code block."""
    def __init__(self, content: str = "", block: bool = False, language: str = "", **props):
        super().__init__(children=[content], block=block, language=language, **props)


class Link(Component):
    """Hyperlink."""
    def __init__(self, content: str = "", href: str = "#", external: bool = False, **props):
        super().__init__(children=[content], href=href, external=external, **props)
