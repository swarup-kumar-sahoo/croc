"""
croc — A Python library for building server-driven single-page applications.

Example:
    import croc

    app = croc.App(title="Hello croc")
    state = croc.State(count=0)

    @app.page("/")
    def home():
        def increment():
            state.count += 1

        return croc.Page([
            croc.Heading("Counter App"),
            croc.Text(f"Count: {state.count}"),
            croc.Button("Click me!", on_click=increment),
        ])

    app.run()
"""

from .app import App
from .state import State
from .router import Router
from .components import (
    # Base
    Component,
    # Layout
    VStack, HStack, Grid, Box, Divider, Spacer, Center, Page,
    # Text
    Text, Heading, Label, Badge, Code, Link,
    # Input
    Button, Input, Textarea, Select, Checkbox, Switch, Slider,
    # Display
    Card, Image, Table, Alert, Spinner, Progress, Avatar, Stat,
)

__version__ = "0.1.0"
__all__ = [
    "App", "State", "Router",
    # Layout
    "Component", "VStack", "HStack", "Grid", "Box", "Divider", "Spacer", "Center", "Page",
    # Text
    "Text", "Heading", "Label", "Badge", "Code", "Link",
    # Input
    "Button", "Input", "Textarea", "Select", "Checkbox", "Switch", "Slider",
    # Display
    "Card", "Image", "Table", "Alert", "Spinner", "Progress", "Avatar", "Stat",
]