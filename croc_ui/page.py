"""
Page class for croc-ui — represents a full HTML page.
"""
from typing import Any, List, Optional, Union
from .base import Element
from .styles.theme import Theme


class Page:
    """
    A full HTML page with head configuration and body content.

    Usage:
        page = Page(
            title="My Site",
            theme=Theme("dark"),
        )
        page.add(Navbar(...), Container(...))
        html = page.render()
    """

    def __init__(
        self,
        title: str = "croc-ui App",
        theme: Optional[Theme] = None,
        favicon: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        fonts: Optional[List[str]] = None,
        extra_css: Optional[str] = None,
        extra_js: Optional[str] = None,
        scripts: Optional[List[str]] = None,
        stylesheets: Optional[List[str]] = None,
        lang: str = "en",
        charset: str = "UTF-8",
        viewport: str = "width=device-width, initial-scale=1.0",
        body_style: Optional[str] = None,
        icon_library: Optional[str] = None,  # "fontawesome", "bootstrap-icons", "material"
    ):
        self.title = title
        self.theme = theme or Theme()
        self.favicon = favicon
        self.description = description
        self.author = author
        self.fonts = fonts or []
        self.extra_css = extra_css or ""
        self.extra_js = extra_js or ""
        self.scripts = scripts or []
        self.stylesheets = stylesheets or []
        self.lang = lang
        self.charset = charset
        self.viewport = viewport
        self.body_style = body_style or ""
        self.icon_library = icon_library
        self._children: List[Any] = []

    def add(self, *children: Any) -> "Page":
        """Add elements to the page body."""
        self._children.extend(children)
        return self

    def __iadd__(self, child: Any) -> "Page":
        self._children.append(child)
        return self

    def _render_head(self) -> str:
        head_parts = [f'<meta charset="{self.charset}">']
        head_parts.append(f'<meta name="viewport" content="{self.viewport}">')
        head_parts.append(f'<title>{self.title}</title>')

        if self.description:
            head_parts.append(f'<meta name="description" content="{self.description}">')
        if self.author:
            head_parts.append(f'<meta name="author" content="{self.author}">')

        if self.favicon:
            head_parts.append(f'<link rel="icon" href="{self.favicon}">')

        # Google Fonts
        for font_url in self.fonts:
            if font_url.startswith("http"):
                head_parts.append(f'<link rel="stylesheet" href="{font_url}">')
            else:
                name = font_url.replace(" ", "+")
                head_parts.append(
                    f'<link rel="preconnect" href="https://fonts.googleapis.com">'
                    f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                    f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={name}:wght@300;400;500;600;700&display=swap">'
                )

        # Icon libraries
        if self.icon_library == "fontawesome":
            head_parts.append('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">')
        elif self.icon_library == "bootstrap-icons":
            head_parts.append('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">')
        elif self.icon_library == "material":
            head_parts.append('<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">')

        # External stylesheets
        for sheet in self.stylesheets:
            head_parts.append(f'<link rel="stylesheet" href="{sheet}">')

        # Theme CSS
        theme_css = self.theme.to_base_css()
        head_parts.append(f'<style>{theme_css}</style>')

        if self.extra_css:
            head_parts.append(f'<style>{self.extra_css}</style>')

        return "\n    ".join(head_parts)

    def _render_body(self) -> str:
        body_style = self.body_style
        parts = []
        for child in self._children:
            if isinstance(child, Element):
                parts.append(child.render())
            elif isinstance(child, str):
                parts.append(child)
            else:
                parts.append(str(child))

        for script_url in self.scripts:
            parts.append(f'<script src="{script_url}"></script>')

        if self.extra_js:
            parts.append(f'<script>{self.extra_js}</script>')

        body_attr = f' style="{body_style}"' if body_style else ""
        return f'<body{body_attr}>\n' + "\n".join(parts) + "\n</body>"

    def render(self) -> str:
        head = self._render_head()
        body = self._render_body()
        return f"""<!DOCTYPE html>
<html lang="{self.lang}">
<head>
    {head}
</head>
{body}
</html>"""

    def save(self, path: str) -> str:
        """Save the rendered HTML to a file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())
        return path

    def __str__(self) -> str:
        return self.render()
