"""
Navigation components for croc-ui.
"""
from ..base import Element
from ..components.typography import A
from typing import List, Optional, Tuple, Union


class Navbar(Element):
    """Responsive navigation bar."""
    tag = "nav"

    def __init__(self, brand: Optional[str] = None, brand_href: str = "/",
                 links: Optional[List[Tuple[str, str]]] = None,
                 sticky: bool = False, transparent: bool = False, **kwargs):
        classes = kwargs.pop("classes", [])
        if isinstance(classes, str):
            classes = classes.split()

        style_parts = [
            "display: flex",
            "align-items: center",
            "justify-content: space-between",
            "padding: 0.75rem 1.5rem",
            "background: var(--croc-bg)",
            "border-bottom: 1px solid var(--croc-border)",
            "font-weight: 600",
        ]
        if sticky:
            style_parts += ["position: sticky", "top: 0", "z-index: 1000"]
        if transparent:
            style_parts[4] = "background: transparent"
            style_parts[5] = "border-bottom: none"

        children = []

        if brand:
            brand_el = A(brand, href=brand_href,
                         style="font-size: 1.25rem; font-weight: 700; color: var(--croc-primary); text-decoration: none;")
            children.append(brand_el)

        if links:
            nav_links = []
            for text, href in links:
                link = A(text, href=href, style=(
                    "color: var(--croc-text); text-decoration: none; "
                    "padding: 0.5rem 0.75rem; border-radius: 4px; "
                    "transition: var(--croc-transition); "
                ))
                nav_links.append(link)
            nav_el = Element.__new__(Element)
            nav_el.tag = "div"
            nav_el.children = nav_links
            nav_el.id = None
            nav_el._classes = ["croc-nav-links"]
            nav_el._style = "display: flex; gap: 0.25rem; align-items: center;"
            nav_el._attrs = {}
            nav_el._extra_attrs = {}
            children.append(nav_el)

        super().__init__(*children,
                         classes=list(classes) + ["croc-navbar"],
                         style="; ".join(style_parts),
                         **kwargs)


class Sidebar(Element):
    """Vertical sidebar navigation."""
    tag = "aside"

    def __init__(self, links: Optional[List[Tuple[str, str]]] = None,
                 width: str = "240px", **kwargs):
        style = kwargs.pop("style", {})
        if isinstance(style, str):
            style += f"; width: {width}; min-height: 100vh; background: var(--croc-bg-secondary); padding: 1rem; border-right: 1px solid var(--croc-border);"
        else:
            style = {"width": width, "min-height": "100vh",
                     "background": "var(--croc-bg-secondary)",
                     "padding": "1rem", "border-right": "1px solid var(--croc-border)"}

        children = []
        if links:
            for text, href in links:
                link = A(text, href=href, style=(
                    "display: block; padding: 0.5rem 0.75rem; "
                    "color: var(--croc-text); text-decoration: none; "
                    "border-radius: 6px; margin-bottom: 2px; "
                    "transition: var(--croc-transition);"
                ))
                children.append(link)

        super().__init__(*children, style=style, **kwargs)


class Breadcrumb(Element):
    """Breadcrumb navigation."""
    tag = "nav"

    def __init__(self, items: List[Tuple[str, Optional[str]]], separator: str = "/", **kwargs):
        """
        items: list of (label, href) tuples. href=None for current page.
        """
        crumb_els = []
        for i, (label, href) in enumerate(items):
            if href and i < len(items) - 1:
                crumb_els.append(A(label, href=href,
                                   style="color: var(--croc-primary); text-decoration: none;"))
            else:
                span = Element.__new__(Element)
                span.tag = "span"
                span.children = [label]
                span.id = None
                span._classes = ["croc-breadcrumb-active"]
                span._style = "color: var(--croc-text-muted);"
                span._attrs = {}
                span._extra_attrs = {}
                crumb_els.append(span)

            if i < len(items) - 1:
                sep = Element.__new__(Element)
                sep.tag = "span"
                sep.children = [f" {separator} "]
                sep.id = None
                sep._classes = []
                sep._style = "color: var(--croc-text-muted); margin: 0 0.25rem;"
                sep._attrs = {}
                sep._extra_attrs = {}
                crumb_els.append(sep)

        ol = Element.__new__(Element)
        ol.tag = "ol"
        ol.children = crumb_els
        ol.id = None
        ol._classes = ["croc-breadcrumb"]
        ol._style = "display: flex; align-items: center; list-style: none; padding: 0; gap: 0.25rem;"
        ol._attrs = {}
        ol._extra_attrs = {}

        super().__init__(ol, attrs={"aria-label": "breadcrumb"}, **kwargs)


class Tabs(Element):
    """Tab navigation component."""
    tag = "div"

    def __init__(self, tabs: List[Tuple[str, "Element"]], active: int = 0, **kwargs):
        """
        tabs: list of (label, content_element) tuples.
        active: index of the active tab (0-based).
        """
        tab_buttons = []
        tab_panels = []

        for i, (label, content) in enumerate(tabs):
            is_active = i == active
            btn_style = (
                f"padding: 0.5rem 1rem; border: none; cursor: pointer; "
                f"border-bottom: 2px solid {'var(--croc-primary)' if is_active else 'transparent'}; "
                f"color: {'var(--croc-primary)' if is_active else 'var(--croc-text-muted)'}; "
                f"background: transparent; font-weight: {'600' if is_active else '400'}; "
                f"transition: var(--croc-transition);"
            )
            btn = Element.__new__(Element)
            btn.tag = "button"
            btn.children = [label]
            btn.id = f"croc-tab-btn-{i}"
            btn._classes = ["croc-tab-btn"]
            btn._style = btn_style
            btn._attrs = {"onclick": f"crocActivateTab({i})", "type": "button"}
            btn._extra_attrs = {}
            tab_buttons.append(btn)

            panel = Element.__new__(Element)
            panel.tag = "div"
            panel.children = [content]
            panel.id = f"croc-tab-panel-{i}"
            panel._classes = ["croc-tab-panel"]
            panel._style = f"display: {'block' if is_active else 'none'}; padding: 1rem 0;"
            panel._attrs = {}
            panel._extra_attrs = {}
            tab_panels.append(panel)

        tab_bar = Element.__new__(Element)
        tab_bar.tag = "div"
        tab_bar.children = tab_buttons
        tab_bar.id = None
        tab_bar._classes = ["croc-tab-bar"]
        tab_bar._style = "display: flex; border-bottom: 1px solid var(--croc-border); gap: 0.25rem;"
        tab_bar._attrs = {}
        tab_bar._extra_attrs = {}

        tab_content = Element.__new__(Element)
        tab_content.tag = "div"
        tab_content.children = tab_panels
        tab_content.id = None
        tab_content._classes = ["croc-tab-content"]
        tab_content._style = ""
        tab_content._attrs = {}
        tab_content._extra_attrs = {}

        script_content = f"""
<script>
function crocActivateTab(index) {{
  document.querySelectorAll('.croc-tab-btn').forEach(function(btn, i) {{
    btn.style.borderBottomColor = i === index ? 'var(--croc-primary)' : 'transparent';
    btn.style.color = i === index ? 'var(--croc-primary)' : 'var(--croc-text-muted)';
    btn.style.fontWeight = i === index ? '600' : '400';
  }});
  document.querySelectorAll('.croc-tab-panel').forEach(function(panel, i) {{
    panel.style.display = i === index ? 'block' : 'none';
  }});
}}
</script>
"""
        raw = Element.__new__(Element)
        raw.tag = "span"
        raw.children = []
        raw.id = None
        raw._classes = []
        raw._style = None
        raw._attrs = {}
        raw._extra_attrs = {}
        raw.render = lambda: script_content

        super().__init__(tab_bar, tab_content, raw, **kwargs)


class Pagination(Element):
    """Pagination component."""
    tag = "nav"

    def __init__(self, total_pages: int, current_page: int = 1,
                 base_url: str = "?page=", **kwargs):
        items = []

        def make_link(label, page, active=False, disabled=False):
            btn_style = (
                f"display: inline-flex; align-items: center; justify-content: center; "
                f"width: 36px; height: 36px; border-radius: 6px; "
                f"{'background: var(--croc-primary); color: white;' if active else 'background: var(--croc-bg); color: var(--croc-text);'} "
                f"{'opacity: 0.4; pointer-events: none;' if disabled else ''} "
                f"border: 1px solid var(--croc-border); text-decoration: none; "
                f"font-weight: {'700' if active else '400'}; "
                f"transition: var(--croc-transition);"
            )
            link = A(str(label), href=f"{base_url}{page}", style=btn_style)
            return link

        if current_page > 1:
            items.append(make_link("←", current_page - 1))

        for i in range(1, total_pages + 1):
            items.append(make_link(i, i, active=(i == current_page)))

        if current_page < total_pages:
            items.append(make_link("→", current_page + 1))

        ul = Element.__new__(Element)
        ul.tag = "div"
        ul.children = items
        ul.id = None
        ul._classes = ["croc-pagination"]
        ul._style = "display: flex; gap: 0.25rem; align-items: center; list-style: none;"
        ul._attrs = {}
        ul._extra_attrs = {}

        super().__init__(ul, attrs={"aria-label": "pagination"}, **kwargs)
