# 🐊 croc-ui

> A Python library for building beautiful static websites using Python — no HTML/CSS required.

[![Python](https://img.shields.io/badge/Python-3.8+-3b82f6?style=flat-square&logo=python)](https://python.org)
[![GitHub](https://img.shields.io/badge/GitHub-swarup--kumar--sahoo/croc-181717?style=flat-square&logo=github)](https://github.com/swarup-kumar-sahoo/croc)

**croc-ui** lets you build complete, styled static websites entirely in Python. Write Python classes, get beautiful HTML. Run locally with a built-in dev server.

---

## ✨ Features

- **30+ UI Components** — Cards, Navbars, Modals, Tabs, Tables, Accordions, Badges, Alerts, Forms, and more
- **Fluent Style Builder** — Chain CSS properties with `Style().color("red").font_size("16px")`
- **Theme System** — Built-in presets (`default`, `dark`, `ocean`, `forest`) or build your own
- **Zero Dependencies** — Uses only Python's standard library
- **Dev Server** — One-line local server with route registration, static file serving, and browser auto-open
- **Page Builder** — Full HTML page with `<head>`, Google Fonts, icon libraries, and meta tags

---

## 🚀 Installation

```bash
pip install croc-ui
```

Or from source:

```bash
git clone https://github.com/swarup-kumar-sahoo/croc
cd croc
pip install -e .
```

---

## ⚡ Quick Start

```python
from croc_ui import App, Page, Navbar, Container, H1, P, Button, Card, Theme

app = App()

@app.route("/")
def home():
    page = Page(
        title="My Website",
        theme=Theme("default"),
        fonts=["Inter"],
    )
    page.add(
        Navbar(brand="My Site", links=[("Home", "/"), ("About", "/about")], sticky=True),
        Container(
            H1("Welcome to My Site"),
            P("Built entirely in Python with croc-ui.", style="color: var(--croc-text-muted);"),
            Button("Get Started →", variant="primary"),
        ),
    )
    return page

@app.route("/about")
def about():
    page = Page(title="About")
    page.add(
        Container(
            H1("About"),
            Card(
                P("This site was built with croc-ui — Python-powered web UI."),
                title="About croc-ui",
            )
        )
    )
    return page

app.run(port=3000)
```

Run it:
```bash
python app.py
```

Opens at **http://localhost:3000** 🎉

---

## 📦 Component Reference

### Layout
| Component | Description |
|-----------|-------------|
| `Container` | Centered max-width wrapper |
| `Row` | Flexbox row |
| `Column` | Flex column with optional span |
| `Section` | `<section>` block |
| `Header` / `Footer` | Semantic header/footer |
| `Div` | Generic `<div>` |

### Typography
| Component | Description |
|-----------|-------------|
| `H1`–`H6` | Headings |
| `P` | Paragraph |
| `Span` / `Text` | Inline text |
| `Code` / `Pre` | Code blocks |
| `Blockquote` | Quoted text |
| `Label` | Form label with `for_` attribute |

### Forms
| Component | Description |
|-----------|-------------|
| `Form` | `<form>` with action/method |
| `Input` | Text, email, password, number, etc. |
| `Button` | 8 variants, 3 sizes |
| `Textarea` | Multi-line text input |
| `Select` + `Option` | Dropdown |
| `Checkbox` / `Radio` | Boolean inputs |
| `FileInput` | File upload |
| `Range` | Slider |

### Navigation
| Component | Description |
|-----------|-------------|
| `Navbar` | Responsive top nav with brand + links |
| `Sidebar` | Vertical nav panel |
| `Breadcrumb` | Path breadcrumbs |
| `Tabs` | Tabbed content panels |
| `Pagination` | Page navigation |

### UI Components
| Component | Description |
|-----------|-------------|
| `Card` | Content card with header/footer |
| `Badge` | Inline status badge |
| `Alert` | Dismissible alert message |
| `Modal` | Overlay dialog |
| `Tooltip` | Hover tooltip |
| `Progress` | Progress bar |
| `Spinner` | Loading spinner |
| `Accordion` | Collapsible sections |
| `Table` | Striped/hover data table |
| `List` | Ordered/unordered list |
| `Tag` | Removable filter tag |
| `Divider` | Horizontal rule with optional label |
| `Avatar` | Image or initials avatar |

### Media
| Component | Description |
|-----------|-------------|
| `Img` | Image with lazy loading |
| `Video` / `Audio` | Media elements |
| `Icon` | Font Awesome / Bootstrap / Material icon |
| `SVG` / `Path` | SVG elements |

---

## 🎨 Styling

### Inline styles (dict or string)

```python
H1("Hello", style={"color": "red", "font_size": "2rem"})
H1("Hello", style="color: red; font-size: 2rem")
```

### Fluent Style builder

```python
from croc_ui import Style

s = Style().color("red").font_size("2rem").padding("1rem").background_color("#f0f0f0")
H1("Hello", style=s)
```

### CSS classes

```python
Div("content", classes="my-class another-class")
Div("content", classes=["my-class", "another-class"])
```

### Extra CSS on the Page

```python
page = Page(extra_css="""
  .hero { background: linear-gradient(135deg, #3b82f6, #8b5cf6); }
  .hero h1 { color: white; }
""")
```

---

## 🎭 Themes

```python
from croc_ui import Theme

# Built-in presets: "default", "dark", "ocean", "forest"
theme = Theme("dark")

# Override individual tokens
theme = Theme(
    preset="default",
    primary="#ff6b35",
    font_family="'Playfair Display', serif",
    border_radius="12px",
    shadow="0 4px 20px rgba(0,0,0,0.15)",
)

page = Page(theme=theme)
```

---

## 🌐 App & Routing

```python
from croc_ui import App, Page

app = App(static_dir="./static")  # optional static file directory

# Decorator style
@app.route("/")
def home():
    return Page(title="Home")

# Programmatic
app.add_route("/about", about_page_fn)
app.add_page("/contact", contact_page_instance)

# Run
app.run(
    host="127.0.0.1",  # default
    port=3000,          # default
    open_browser=True,  # auto-open browser
)
```

---

## 📄 Saving Static HTML

```python
page = Page(title="My Page")
page.add(H1("Hello!"))
page.save("index.html")      # saves rendered HTML to file
print(page.render())         # get HTML string
```

---

## 📁 Project Structure

```
croc-ui/
├── croc_ui/
│   ├── __init__.py         # Public API exports
│   ├── app.py              # Dev server (App class)
│   ├── page.py             # Page builder
│   ├── base.py             # Element base classes
│   ├── components/
│   │   ├── layout.py       # Container, Row, Column, etc.
│   │   ├── typography.py   # H1-H6, P, Code, etc.
│   │   ├── forms.py        # Input, Button, Select, etc.
│   │   ├── media.py        # Img, Video, Icon, SVG
│   │   ├── navigation.py   # Navbar, Tabs, Pagination
│   │   └── ui.py           # Card, Alert, Modal, Table, etc.
│   └── styles/
│       ├── style.py        # Fluent Style builder
│       └── theme.py        # Theme system
└── examples/
    └── example_app.py      # Full showcase app
```

---

## 🤝 Contributing

Issues and PRs welcome at [https://github.com/swarup-kumar-sahoo/croc](https://github.com/swarup-kumar-sahoo/croc)

---

## 📝 License

MIT License — © Swarup Kumar Sahoo
