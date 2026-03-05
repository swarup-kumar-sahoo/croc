"""
Layout components for croc-ui.
"""
from ..base import Element
from typing import Any, Dict, List, Optional, Union


class Div(Element):
    tag = "div"


class Container(Element):
    tag = "div"

    def __init__(self, *children, fluid=False, **kwargs):
        kwargs.setdefault("classes", [])
        if isinstance(kwargs["classes"], str):
            kwargs["classes"] = kwargs["classes"].split()
        if fluid:
            kwargs["classes"] = list(kwargs["classes"]) + ["croc-container-fluid"]
        else:
            kwargs["classes"] = list(kwargs["classes"]) + ["croc-container"]
        super().__init__(*children, **kwargs)


class Row(Element):
    tag = "div"

    def __init__(self, *children, **kwargs):
        classes = kwargs.pop("classes", [])
        if isinstance(classes, str):
            classes = classes.split()
        kwargs["classes"] = list(classes) + ["croc-row"]
        super().__init__(*children, **kwargs)


class Column(Element):
    tag = "div"

    def __init__(self, *children, span: Optional[int] = None, **kwargs):
        classes = kwargs.pop("classes", [])
        if isinstance(classes, str):
            classes = classes.split()
        col_classes = list(classes) + ["croc-col"]
        if span:
            col_classes.append(f"croc-col-{span}")
        kwargs["classes"] = col_classes
        super().__init__(*children, **kwargs)


class Section(Element):
    tag = "section"


class Header(Element):
    tag = "header"


class Footer(Element):
    tag = "footer"


class Nav(Element):
    tag = "nav"


class Main(Element):
    tag = "main"


class Aside(Element):
    tag = "aside"


class Article(Element):
    tag = "article"


class Figure(Element):
    tag = "figure"


class Figcaption(Element):
    tag = "figcaption"
