"""
Media components for croc-ui.
"""
from ..base import Element, VoidElement
from typing import Optional


class Img(VoidElement):
    tag = "img"

    def __init__(self, src: str, alt: str = "", width: Optional[str] = None,
                 height: Optional[str] = None, loading: str = "lazy", **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["src"] = src
        attrs["alt"] = alt
        attrs["loading"] = loading
        if width:
            attrs["width"] = width
        if height:
            attrs["height"] = height
        super().__init__(attrs=attrs, **kwargs)


class Video(Element):
    tag = "video"

    def __init__(self, src: Optional[str] = None, *sources, controls: bool = True,
                 autoplay: bool = False, loop: bool = False, muted: bool = False,
                 poster: Optional[str] = None, width: Optional[str] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if src:
            attrs["src"] = src
        if controls:
            attrs["controls"] = True
        if autoplay:
            attrs["autoplay"] = True
        if loop:
            attrs["loop"] = True
        if muted:
            attrs["muted"] = True
        if poster:
            attrs["poster"] = poster
        if width:
            attrs["width"] = width
        children = list(sources)
        super().__init__(*children, attrs=attrs, **kwargs)


class Audio(Element):
    tag = "audio"

    def __init__(self, src: Optional[str] = None, *sources, controls: bool = True,
                 autoplay: bool = False, loop: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if src:
            attrs["src"] = src
        if controls:
            attrs["controls"] = True
        if autoplay:
            attrs["autoplay"] = True
        if loop:
            attrs["loop"] = True
        children = list(sources)
        super().__init__(*children, attrs=attrs, **kwargs)


class Source(VoidElement):
    tag = "source"

    def __init__(self, src: str, type: Optional[str] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["src"] = src
        if type:
            attrs["type"] = type
        super().__init__(attrs=attrs, **kwargs)


class Iframe(Element):
    tag = "iframe"

    def __init__(self, src: str, width: str = "100%", height: str = "400",
                 frameborder: str = "0", allow: Optional[str] = None,
                 allowfullscreen: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["src"] = src
        attrs["width"] = width
        attrs["height"] = height
        attrs["frameborder"] = frameborder
        if allow:
            attrs["allow"] = allow
        if allowfullscreen:
            attrs["allowfullscreen"] = True
        super().__init__(attrs=attrs, **kwargs)


class Icon(Element):
    """
    Icon using popular icon libraries.
    Supports: Font Awesome, Material Icons, Bootstrap Icons.
    """
    tag = "i"

    def __init__(self, name: str, library: str = "fa", size: Optional[str] = None,
                 color: Optional[str] = None, **kwargs):
        classes = kwargs.pop("classes", [])
        if isinstance(classes, str):
            classes = classes.split()

        if library == "fa":
            classes = [f"fa", f"fa-{name}"] + list(classes)
        elif library == "fas":
            classes = [f"fas", f"fa-{name}"] + list(classes)
        elif library == "fab":
            classes = [f"fab", f"fa-{name}"] + list(classes)
        elif library == "material":
            super().__init__(name, classes=["material-icons"] + list(classes), **kwargs)
            return
        elif library == "bi":
            classes = [f"bi", f"bi-{name}"] + list(classes)
        else:
            classes = [name] + list(classes)

        style = kwargs.pop("style", {})
        if isinstance(style, dict):
            if size:
                style["font-size"] = size
            if color:
                style["color"] = color
        elif isinstance(style, str):
            if size:
                style += f"; font-size: {size}"
            if color:
                style += f"; color: {color}"

        super().__init__(classes=classes, style=style, **kwargs)


class SVG(Element):
    tag = "svg"

    def __init__(self, *children, viewbox: str = "0 0 24 24",
                 width: str = "24", height: str = "24",
                 fill: str = "currentColor", **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["viewBox"] = viewbox
        attrs["width"] = width
        attrs["height"] = height
        attrs["fill"] = fill
        attrs["xmlns"] = "http://www.w3.org/2000/svg"
        super().__init__(*children, attrs=attrs, **kwargs)

    def render(self) -> str:
        attrs = (
            self._render_id()
            + self._render_classes()
            + self._render_style()
            + self._render_attrs()
        )
        inner = "".join(self._render_child(c) for c in self.children)
        return f"<svg{attrs}>{inner}</svg>"


class Path(Element):
    tag = "path"

    def __init__(self, d: str, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["d"] = d
        super().__init__(attrs=attrs, **kwargs)

    def render(self) -> str:
        attrs = self._render_id() + self._render_classes() + self._render_style() + self._render_attrs()
        return f"<path{attrs} />"
