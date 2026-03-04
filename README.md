<div align="center">

```
 ██████╗██████╗  ██████╗  ██████╗
██╔════╝██╔══██╗██╔═══██╗██╔════╝
██║     ██████╔╝██║   ██║██║     
██║     ██╔══██╗██║   ██║██║     
╚██████╗██║  ██║╚██████╔╝╚██████╗
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝
```

### 🐊 Build web UIs in pure Python. No JavaScript. No HTML. No templates.

[![PyPI version](https://img.shields.io/pypi/v/croc-ui?color=22c55e&labelColor=0f172a&style=for-the-badge)](https://pypi.org/project/croc-ui)
[![Python](https://img.shields.io/pypi/pyversions/croc-ui?color=3b82f6&labelColor=0f172a&style=for-the-badge)](https://pypi.org/project/croc-ui)
[![License](https://img.shields.io/pypi/l/croc-ui?color=f59e0b&labelColor=0f172a&style=for-the-badge)](https://github.com/swarup-kumar-sahoo/croc/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/swarup-kumar-sahoo/croc?color=ec4899&labelColor=0f172a&style=for-the-badge)](https://github.com/swarup-kumar-sahoo/croc)

<br/>

**croc** is a Python-first framework for building server-driven single-page apps.  
Write components in Python → croc handles the rest.

[Getting Started](#-quick-start) · [Components](#-components) · [Examples](#-examples) · [Roadmap](#-roadmap)

---

</div>

## ✨ Why croc?

| | croc | Streamlit | Dash | Raw HTML/JS |
|---|---|---|---|---|
| Pure Python UI | ✅ | ✅ | ⚠️ | ❌ |
| SPA routing | ✅ | ❌ | ✅ | ✅ |
| Real-time WebSocket | ✅ | ✅ | ⚠️ | ✅ |
| Component model | ✅ | ❌ | ✅ | ✅ |
| Zero JS required | ✅ | ✅ | ❌ | ❌ |
| Tailwind styling | ✅ | ❌ | ❌ | ✅ |

---

## 📦 Installation

```bash
pip install croc-ui
```

---

## ⚡ Quick Start

```python
import croc

app = croc.App(title="My App")
state = croc.State(count=0)

@app.page("/")
def home():
    def increment():
        state.count += 1

    return croc.Page([
        croc.Heading("🐊 Hello, croc!"),
        croc.Text(f"You clicked {state.count} times"),
        croc.Button("Click me!", on_click=increment),
    ])

app.run()  # → http://localhost:8000
```

That's it. **No HTML. No JS. No config.**

---

## 🔧 How It Works

```
┌──────────────────────────────────────────┐
│  Your Python App                         │
│                                          │
│   state = State(count=0)                 │
│   state.count += 1  ──► triggers render  │
│                              │           │
│         Component Tree (JSON)│           │
│              FastAPI + WebSocket         │
└──────────────────────────────┼───────────┘
                               │
┌──────────────────────────────▼───────────┐
│  Browser  (croc-client.js)               │
│                                          │
│   JSON tree ──► DOM (Tailwind CSS)       │
│   click / input ──► WebSocket ──► Python │
└──────────────────────────────────────────┘
```

1. 🐍 You write Python components and state
2. 🔄 croc serializes the component tree to JSON over WebSocket
3. 🌐 The browser renders it as a real DOM with Tailwind CSS
4. ⚡ Events (clicks, inputs) are sent back to Python instantly
5. 🔁 State change → automatic re-render, no manual DOM work

---

## 🧩 Components

### 📐 Layout
```python
croc.Page([...])          # Top-level page wrapper
croc.VStack([...])        # Vertical flex column
croc.HStack([...])        # Horizontal flex row
croc.Grid([...], cols=3)  # CSS Grid
croc.Box([...])           # Generic container
croc.Center([...])        # Centers children
croc.Divider()            # Horizontal rule
croc.Spacer()             # Flexible gap
```

### ✍️ Text
```python
croc.Heading("Title", level=1)
croc.Text("Hello!", size="lg", weight="bold")
croc.Badge("new", variant="success")
croc.Code("import croc", block=True)
croc.Link("Docs", href="/docs")
croc.Label("Name")
```

### 🎛️ Input
```python
croc.Button("Submit", on_click=handler, variant="primary")
croc.Input(label="Name", on_change=handler)
croc.Textarea(label="Message", rows=4)
croc.Select(options=[("a","Option A")], on_change=handler)
croc.Checkbox(label="Agree", on_change=handler)
croc.Switch(label="Dark mode", on_change=handler)
croc.Slider(min=0, max=100, on_change=handler)
```

### 📊 Display
```python
croc.Card(title="Stats", children=[...])
croc.Alert("Success!", variant="success")
croc.Table(columns=["Name","Age"], rows=[...])
croc.Progress(value=75, max=100)
croc.Spinner(size="md")
croc.Avatar(name="Alice Smith")
croc.Stat(label="Revenue", value="$12k", delta="+8%")
croc.Image(src="/logo.png", alt="Logo")
```

---

## 🗂️ Routing

```python
@app.page("/")
def home():
    return croc.Page([croc.Heading("Home")])

@app.page("/dashboard")
def dashboard():
    return croc.Page([croc.Heading("Dashboard")])

@app.not_found
def not_found():
    return croc.Page([croc.Heading("404 — Not Found")])
```

Client-side navigation — **no page reload:**
```python
croc.Link("Dashboard", href="/dashboard")
```

---

## 🧠 State Management

```python
# Create reactive state
state = croc.State(
    name="Alice",
    count=0,
    dark=False,
)

# Read
print(state.count)     # 0

# Write — triggers re-render automatically
state.count += 1

# Batch update
state.update(name="Bob", count=10)
```

---

## 🎨 Examples

### Counter App
```python
import croc

app = croc.App(title="Counter")
state = croc.State(count=0)

@app.page("/")
def home():
    return croc.Page([
        croc.Card(title="Counter", children=[
            croc.Center([croc.Heading(str(state.count), level=1)]),
            croc.HStack([
                croc.Button("−", on_click=lambda: state.update(count=state.count - 1), variant="secondary"),
                croc.Button("+", on_click=lambda: state.update(count=state.count + 1)),
            ]),
        ]),
    ])

app.run()
```

### Dashboard
```python
import croc

app = croc.App(title="Dashboard")

@app.page("/")
def dashboard():
    return croc.Page([
        croc.Heading("📊 Dashboard"),
        croc.Grid(cols=3, children=[
            croc.Stat(label="Users",   value="12,430", delta="+12%"),
            croc.Stat(label="Revenue", value="$84k",   delta="+8%"),
            croc.Stat(label="Uptime",  value="99.9%",  delta="+0.1%"),
        ]),
        croc.Card(title="Recent Users", children=[
            croc.Table(
                columns=["Name", "Role", "Status"],
                rows=[
                    ["Alice",   "Engineer", "Active"],
                    ["Bob",     "Designer", "Active"],
                    ["Charlie", "Manager",  "Away"],
                ],
            ),
        ]),
    ])

app.run()
```

---

## 📁 Project Structure

```
my-app/
├── app.py          ← your croc app
├── pages/
│   ├── home.py
│   └── dashboard.py
└── requirements.txt
```

---

## 🤝 Contributing

PRs and issues welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/swarup-kumar-sahoo/croc
cd croc
pip install -e ".[dev]"
python examples/demo.py
```

---

## 📄 License

MIT © [Swarup Kumar Sahoo](https://github.com/swarup-kumar-sahoo)

---

<div align="center">

**Made with 🐊 and Python**

If croc helped you, give it a ⭐ on [GitHub](https://github.com/swarup-kumar-sahoo/croc)!

</div>