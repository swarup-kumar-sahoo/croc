<div align="center">

```
 ██████╗██████╗  ██████╗  ██████╗
██╔════╝██╔══██╗██╔═══██╗██╔════╝
██║     ██████╔╝██║   ██║██║     
██║     ██╔══██╗██║   ██║██║     
╚██████╗██║  ██║╚██████╔╝╚██████╗
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝
```

### Build beautiful websites with pure Python. No HTML. No CSS. No hassle.

[![PyPI version](https://img.shields.io/pypi/v/croc-ui?style=flat-square&color=00b4d8&label=PyPI)](https://pypi.org/project/croc-ui/)
[![Python](https://img.shields.io/badge/Python-3.8+-3b82f6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-swarup--kumar--sahoo/croc-181717?style=flat-square&logo=github)](https://github.com/swarup-kumar-sahoo/croc)
[![Downloads](https://img.shields.io/pypi/dm/croc-ui?style=flat-square&color=8b5cf6&label=Downloads)](https://pypi.org/project/croc-ui/)

</div>

---

## What is croc-ui?

**croc-ui** is a Python library that lets you design and ship complete, styled websites using only Python — no templates, no HTML files, no CSS knowledge required. Write Python classes, get production-ready HTML.

```python
from croc_ui import App, Page, Theme, Navbar, H1, P, Button

app = App()

@app.route("/")
def home():
    page = Page(title="My Site", theme=Theme("default"))
    page.add(
        Navbar(brand="My Site", links=[("Home", "/"), ("About", "/about")]),
        H1("Hello, World!"),
        P("Built entirely in Python."),
        Button("Get Started →", variant="primary"),
    )
    return page

app.run(port=3000)  # → opens http://localhost:3000
```

---

## Installation

```bash
pip install croc-ui
```

Or install from source:

```bash
git clone https://github.com/swarup-kumar-sahoo/croc
cd croc
pip install -e .
```

---

## Features

| | Feature | Description |
|---|---|---|
| 🧱 | **30+ Components** | Cards, Navbars, Modals, Tabs, Tables, Accordions, Alerts & more |
| 🎨 | **Theme System** | Presets: `default` `dark` `ocean` `forest` — or build your own |
| ✍️ | **Style Builder** | Fluent API: `Style().color("red").padding("1rem").font_size("16px")` |
| ⚡ | **Dev Server** | Built-in localhost server with routing & browser auto-open |
| 📄 | **Page Builder** | Full `<head>` config — Google Fonts, meta tags, icon libraries |
| 🔗 | **Zero Dependencies** | Pure Python standard library only |

---

## Quick Start

```python
from croc_ui import (
    App, Page, Theme,
    Navbar, Container, Row,
    H1, H2, P, Button,
    Card, Badge, Alert, Table,
)

app = App()

@app.route("/")
def home():
    page = Page(
        title="Dashboard",
        theme=Theme("dark"),
        fonts=["Inter"],
    )
    page.add(
        Navbar(brand="🐊 My App", links=[("Home", "/"), ("Docs", "/docs")], sticky=True),
        Container(
            H1("Welcome back 👋"),
            Alert("Server is running smoothly.", variant="success"),
            Row(
                Card(H2("42"),   P("Active Users"),  style="text-align:center;"),
                Card(H2("98%"),  P("Uptime"),         style="text-align:center;"),
                Card(H2("1.2s"), P("Avg Response"),   style="text-align:center;"),
            ),
            Table(
                headers=["Name", "Status", "Date"],
                rows=[
                    ["Deploy #41", Badge("Live", variant="success", pill=True), "Mar 5, 2026"],
                    ["Deploy #40", Badge("Done", variant="info",    pill=True), "Mar 4, 2026"],
                ],
            ),
        ),
    )
    return page

app.run(port=3000)
```

---

## Component Reference

<details>
<summary><strong>🧱 Layout</strong></summary>

| Component | Tag | Description |
|-----------|-----|-------------|
| `Container` | `div` | Centered max-width wrapper (1200px) |
| `Row` | `div` | Flexbox row with gap |
| `Column` | `div` | Flex column, optional span |
| `Section` | `section` | Semantic section block |
| `Header` | `header` | Page header |
| `Footer` | `footer` | Page footer |
| `Div` | `div` | Generic block element |

</details>

<details>
<summary><strong>✍️ Typography</strong></summary>

| Component | Tag | Description |
|-----------|-----|-------------|
| `H1` – `H6` | `h1`–`h6` | Headings |
| `P` | `p` | Paragraph |
| `Span` / `Text` | `span` | Inline text |
| `A` | `a` | Anchor / link |
| `Code` / `Pre` | `code`/`pre` | Code blocks |
| `Blockquote` | `blockquote` | Quoted text |
| `Label` | `label` | Form label |

</details>

<details>
<summary><strong>📝 Forms</strong></summary>

| Component | Description |
|-----------|-------------|
| `Form` | `<form>` with action & method |
| `Input` | text, email, password, number… |
| `Button` | 8 variants × 3 sizes |
| `Textarea` | Multi-line input |
| `Select` + `Option` | Dropdown |
| `Checkbox` / `Radio` | Boolean inputs |
| `FileInput` | File upload |
| `Range` | Slider |

</details>

<details>
<summary><strong>🧭 Navigation</strong></summary>

| Component | Description |
|-----------|-------------|
| `Navbar` | Responsive top nav with brand + links |
| `Sidebar` | Vertical nav panel |
| `Breadcrumb` | Path breadcrumbs |
| `Tabs` | Tabbed content panels |
| `Pagination` | Page number navigation |

</details>

<details>
<summary><strong>🎛️ UI Components</strong></summary>

| Component | Description |
|-----------|-------------|
| `Card` | Content card with optional header/footer |
| `Badge` | Inline status label |
| `Alert` | Dismissible message banner |
| `Modal` | Overlay dialog |
| `Tooltip` | Hover tooltip |
| `Progress` | Animated progress bar |
| `Spinner` | Loading indicator |
| `Accordion` | Collapsible sections |
| `Table` | Striped, hoverable data table |
| `List` | Ordered / unordered list |
| `Tag` | Removable filter chip |
| `Divider` | Horizontal rule with optional label |
| `Avatar` | Image or initials avatar |

</details>

<details>
<summary><strong>🖼️ Media</strong></summary>

| Component | Description |
|-----------|-------------|
| `Img` | Image with lazy loading |
| `Video` / `Audio` | Media elements |
| `Icon` | Font Awesome / Bootstrap Icons / Material |
| `SVG` / `Path` | Raw SVG elements |

</details>

---

## Styling

**Inline — dict or string:**
```python
H1("Hello", style={"color": "red", "font_size": "2rem"})
H1("Hello", style="color: red; font-size: 2rem")
```

**Fluent Style builder:**
```python
from croc_ui import Style

s = Style().color("red").font_size("2rem").padding("1rem").background("#f0f4ff")
H1("Hello", style=s)
```

**CSS classes:**
```python
Div("content", classes="hero bold")
Div("content", classes=["hero", "bold"])
```

**Page-level CSS:**
```python
page = Page(extra_css="""
    .hero { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; }
""")
```

---

## Themes

```python
from croc_ui import Theme

# Built-in presets
page = Page(theme=Theme("dark"))     # dark
page = Page(theme=Theme("ocean"))    # ocean blue
page = Page(theme=Theme("forest"))   # forest green

# Custom tokens
page = Page(theme=Theme(
    preset="default",
    primary="#ff6b35",
    font_family="'Playfair Display', serif",
    border_radius="12px",
))
```

---

## App & Routing

```python
from croc_ui import App

app = App(static_dir="./static")   # serve static files from ./static

@app.route("/")
def home(): ...

app.add_route("/about", about_fn)
app.add_page("/contact", contact_page)

app.run(
    host="127.0.0.1",
    port=3000,
    open_browser=True,
)
```

---

## Save Static HTML

```python
page = Page(title="My Page")
page.add(H1("Hello!"))

page.save("index.html")   # write to file
print(page.render())      # get HTML string
```

---

## Project Structure

```
croc/
├── croc_ui/
│   ├── __init__.py            # Public API
│   ├── app.py                 # Dev server
│   ├── page.py                # Page builder
│   ├── base.py                # Base element classes
│   ├── components/
│   │   ├── layout.py          # Container, Row, Column…
│   │   ├── typography.py      # H1–H6, P, Code, A…
│   │   ├── forms.py           # Input, Button, Select…
│   │   ├── media.py           # Img, Video, Icon, SVG
│   │   ├── navigation.py      # Navbar, Tabs, Pagination
│   │   └── ui.py              # Card, Alert, Modal, Table…
│   └── styles/
│       ├── style.py           # Fluent Style builder
│       └── theme.py           # Theme system & presets
└── examples/
    └── example_app.py         # Full showcase (run this!)
```

---

## Contributing

Issues and pull requests are welcome!
👉 [github.com/swarup-kumar-sahoo/croc](https://github.com/swarup-kumar-sahoo/croc)

---

<div align="center">

Made with 🐊 by [Swarup Kumar Sahoo](https://github.com/swarup-kumar-sahoo) · MIT License

</div>