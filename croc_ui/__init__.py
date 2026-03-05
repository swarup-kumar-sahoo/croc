"""
croc-ui: A Python library for building beautiful static websites using Python.
Repository: https://github.com/swarup-kumar-sahoo/croc
"""

from .app import App
from .page import Page
from .components.layout import (
    Container, Row, Column, Section, Header, Footer, Nav, Main, Aside, Div
)
from .components.typography import (
    H1, H2, H3, H4, H5, H6, P, Span, Text, Code, Pre, Blockquote, Label, A, Br, Hr
)
from .components.forms import (
    Form, Input, Button, Textarea, Select, Option, Checkbox, Radio, FileInput, Range
)
from .components.media import Img, Video, Audio, Icon, SVG
from .components.navigation import Navbar, Sidebar, Breadcrumb, Tabs, Pagination
from .components.ui import (
    Card, Badge, Alert, Modal, Tooltip, Progress, Spinner,
    Accordion, Table, List, Tag, Divider, Avatar
)
from .styles.style import Style
from .styles.theme import Theme

__version__ = "1.0.0"
__author__ = "Swarup Kumar Sahoo"
__repo__ = "https://github.com/swarup-kumar-sahoo/croc"

__all__ = [
    # App & Page
    "App", "Page",
    # Layout
    "Container", "Row", "Column", "Section", "Header", "Footer",
    "Nav", "Main", "Aside", "Div",
    # Typography
    "H1", "H2", "H3", "H4", "H5", "H6", "P", "Span", "Text",
    "Code", "Pre", "Blockquote", "Label", "A", "Br", "Hr",
    # Forms
    "Form", "Input", "Button", "Textarea", "Select", "Option",
    "Checkbox", "Radio", "FileInput", "Range",
    # Media
    "Img", "Video", "Audio", "Icon", "SVG",
    # Navigation
    "Navbar", "Sidebar", "Breadcrumb", "Tabs", "Pagination",
    # UI Components
    "Card", "Badge", "Alert", "Modal", "Tooltip", "Progress",
    "Spinner", "Accordion", "Table", "List", "Tag", "Divider", "Avatar",
    # Styles
    "Style", "Theme",
]
