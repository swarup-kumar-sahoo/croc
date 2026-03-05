"""
Typography components for croc-ui.
"""
from ..base import Element
from typing import Optional


class H1(Element):
    tag = "h1"


class H2(Element):
    tag = "h2"


class H3(Element):
    tag = "h3"


class H4(Element):
    tag = "h4"


class H5(Element):
    tag = "h5"


class H6(Element):
    tag = "h6"


class P(Element):
    tag = "p"


class Span(Element):
    tag = "span"


class Text(Element):
    """Alias for Span — for inline text."""
    tag = "span"


class Strong(Element):
    tag = "strong"


class Em(Element):
    tag = "em"


class Code(Element):
    tag = "code"


class Pre(Element):
    tag = "pre"


class Blockquote(Element):
    tag = "blockquote"


class Label(Element):
    tag = "label"

    def __init__(self, *children, for_: Optional[str] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if for_:
            attrs["for"] = for_
        super().__init__(*children, attrs=attrs, **kwargs)


class Small(Element):
    tag = "small"


class Mark(Element):
    tag = "mark"


class Del(Element):
    tag = "del"


class Ins(Element):
    tag = "ins"


class Sub(Element):
    tag = "sub"


class Sup(Element):
    tag = "sup"


class Abbr(Element):
    tag = "abbr"


class Cite(Element):
    tag = "cite"


class Kbd(Element):
    tag = "kbd"


class Var(Element):
    tag = "var"


class A(Element):
    tag = "a"

    def __init__(self, *children, href: str = "#", target: Optional[str] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["href"] = href
        if target:
            attrs["target"] = target
        super().__init__(*children, attrs=attrs, **kwargs)


class Br(Element):
    tag = "br"

    def render(self) -> str:
        return "<br />"


class Hr(Element):
    tag = "hr"

    def render(self) -> str:
        attrs = self._render_id() + self._render_classes() + self._render_style() + self._render_attrs()
        return f"<hr{attrs} />"
