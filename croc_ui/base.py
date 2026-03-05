"""
Base element class for all croc-ui components.
"""
from typing import Any, Dict, List, Optional, Union


class Element:
    """Base class for all HTML elements in croc-ui."""

    tag: str = "div"

    def __init__(
        self,
        *children,
        id: Optional[str] = None,
        classes: Optional[Union[str, List[str]]] = None,
        style: Optional[Union[str, Dict[str, str]]] = None,
        attrs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.children = list(children)
        self.id = id
        self._classes = self._normalize_classes(classes)
        self._style = style
        self._attrs = attrs or {}
        self._extra_attrs = kwargs

    def _normalize_classes(self, classes) -> List[str]:
        if classes is None:
            return []
        if isinstance(classes, str):
            return classes.split()
        return list(classes)

    def add_class(self, *cls):
        for c in cls:
            if c not in self._classes:
                self._classes.append(c)
        return self

    def remove_class(self, cls: str):
        self._classes = [c for c in self._classes if c != cls]
        return self

    def set_style(self, **styles):
        if isinstance(self._style, dict):
            self._style.update(styles)
        elif self._style is None:
            self._style = styles
        return self

    def add(self, *children):
        self.children.extend(children)
        return self

    def _render_style(self) -> str:
        if not self._style:
            return ""
        if isinstance(self._style, str):
            return f' style="{self._style}"'
        css = "; ".join(
            f"{k.replace('_', '-')}: {v}" for k, v in self._style.items()
        )
        return f' style="{css}"'

    def _render_attrs(self) -> str:
        parts = []
        all_attrs = {**self._attrs, **self._extra_attrs}
        for k, v in all_attrs.items():
            k = k.rstrip("_").replace("_", "-")
            if v is True:
                parts.append(k)
            elif v is not False and v is not None:
                parts.append(f'{k}="{v}"')
        return (" " + " ".join(parts)) if parts else ""

    def _render_classes(self) -> str:
        if not self._classes:
            return ""
        return f' class="{" ".join(self._classes)}"'

    def _render_id(self) -> str:
        return f' id="{self.id}"' if self.id else ""

    def _render_child(self, child) -> str:
        if isinstance(child, Element):
            return child.render()
        return str(child)

    def render(self) -> str:
        attrs = (
            self._render_id()
            + self._render_classes()
            + self._render_style()
            + self._render_attrs()
        )
        inner = "".join(self._render_child(c) for c in self.children)
        return f"<{self.tag}{attrs}>{inner}</{self.tag}>"

    def __str__(self):
        return self.render()


class VoidElement(Element):
    """Self-closing HTML elements (img, input, br, hr, etc.)"""

    def render(self) -> str:
        attrs = (
            self._render_id()
            + self._render_classes()
            + self._render_style()
            + self._render_attrs()
        )
        return f"<{self.tag}{attrs} />"
