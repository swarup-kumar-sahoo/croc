"""
croc-ui Example App
Showcases all components and the App server.

Run:  python examples/example_app.py
Then: open http://localhost:3000
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from croc_ui import (
    App, Page, Theme,
    Container, Row, Column, Section, Header, Footer, Div,
    H1, H2, H3, H4, P, Span, Code, Blockquote, A,
    Button, Input, Form, Textarea, Select, Option, Checkbox, Label,
    Img, Icon,
    Navbar, Breadcrumb, Tabs, Pagination,
    Card, Badge, Alert, Progress, Spinner, Accordion,
    Table, List, Tag, Divider, Avatar, Tooltip, Modal,
    Style,
)

# ─────────────────────────────────────────────
# Shared components
# ─────────────────────────────────────────────
def make_navbar():
    return Navbar(
        brand="🐊 croc-ui",
        brand_href="/",
        links=[
            ("Home", "/"),
            ("Components", "/components"),
            ("Forms", "/forms"),
            ("Theme", "/theme"),
        ],
        sticky=True,
    )

def base_page(title, *content, active_route="/"):
    page = Page(
        title=f"{title} — croc-ui",
        theme=Theme("default"),
        fonts=["Inter"],
        description="croc-ui component showcase",
        icon_library="fontawesome",
        extra_css="""
        .hero { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); color: white; padding: 4rem 0; }
        .croc-nav-links a:hover { background: var(--croc-bg-secondary); }
        .croc-table-row:hover td { background: var(--croc-bg-secondary) !important; }
        section { padding: 3rem 0; }
        section + section { border-top: 1px solid var(--croc-border); }
        h2 { font-size: 1.75rem; font-weight: 800; margin-bottom: 0.5rem; }
        .section-label { font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
                         letter-spacing: 0.1em; color: var(--croc-primary); margin-bottom: 0.5rem; }
        """,
    )
    page.add(make_navbar())
    for c in content:
        page.add(c)
    page.add(make_footer())
    return page


def make_footer():
    return Footer(
        Container(
            Divider(),
            Row(
                Column(
                    P("Built with 🐊 ", Span("croc-ui", style="color: var(--croc-primary); font-weight: 700;"),
                      style="color: var(--croc-text-muted); font-size: 0.9rem;"),
                ),
                Column(
                    P(
                        A("GitHub", href="https://github.com/swarup-kumar-sahoo/croc", style="color: var(--croc-primary);"),
                        " · ",
                        A("Docs", href="#", style="color: var(--croc-primary);"),
                        style="text-align: right; color: var(--croc-text-muted); font-size: 0.9rem;"
                    ),
                ),
            ),
        ),
        style="padding: 1.5rem 0; margin-top: 2rem;",
    )


# ─────────────────────────────────────────────
# Home page
# ─────────────────────────────────────────────
def home_page():
    hero = Div(
        Container(
            Div(
                Badge("v1.0.0", variant="light", pill=True),
                style="margin-bottom: 1rem;",
            ),
            H1("Build websites with Python.", style="font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 900; margin-bottom: 1rem; line-height: 1.1;"),
            P("croc-ui is a Python library for building beautiful, responsive static websites. Write Python, get HTML.", style="font-size: 1.25rem; opacity: 0.9; max-width: 560px; margin-bottom: 2rem;"),
            Row(
                Button("Get Started →", variant="outline", style="border-color: white; color: white;"),
                Button("View on GitHub", variant="ghost", style="color: white;"),
            ),
        ),
        classes="hero",
    )

    features = Container(
        Section(
            P("Why croc-ui?", classes="section-label"),
            H2("Everything you need"),
            P("From layout to forms, navigation to data display.", style="color: var(--croc-text-muted); margin-bottom: 2rem;"),
            Row(
                Card(
                    H3("🧱 Components", style="margin-bottom: 0.5rem;"),
                    P("30+ ready-to-use UI components. Cards, modals, tables, accordions and more.", style="color: var(--croc-text-muted);"),
                    hover=True,
                ),
                Card(
                    H3("🎨 Theming", style="margin-bottom: 0.5rem;"),
                    P("Built-in theme system with presets. Dark mode, ocean, forest — or create your own.", style="color: var(--croc-text-muted);"),
                    hover=True,
                ),
                Card(
                    H3("⚡ Dev Server", style="margin-bottom: 0.5rem;"),
                    P("Run locally in one line. Hot reload-ready routing system with zero dependencies.", style="color: var(--croc-text-muted);"),
                    hover=True,
                ),
                Card(
                    H3("🐍 Pure Python", style="margin-bottom: 0.5rem;"),
                    P("No templates, no JS frameworks. Just Python classes that render clean HTML.", style="color: var(--croc-text-muted);"),
                    hover=True,
                ),
            ),
        ),
        Section(
            P("Quick Start", classes="section-label"),
            H2("Simple as Python"),
            Card(
                Code(
                    """from croc_ui import App, Page, Navbar, H1, P, Button

app = App()

@app.route("/")
def home():
    page = Page(title="My Site")
    page.add(
        Navbar(brand="My Site", links=[("Home", "/")]),
        H1("Hello, World!"),
        P("Built with croc-ui"),
        Button("Click me", variant="primary"),
    )
    return page

app.run(port=3000)""",
                    style="display: block; white-space: pre; font-size: 0.9rem; line-height: 1.6;",
                ),
                style="background: #0f172a; border-color: #1e293b;",
            ),
        ),
    )
    return base_page("Home", hero, features)


# ─────────────────────────────────────────────
# Components page
# ─────────────────────────────────────────────
def components_page():
    breadcrumb = Container(
        Breadcrumb([("Home", "/"), ("Components", None)]),
        style="padding: 1rem 0;",
    )

    content = Container(
        # Badges
        Section(
            P("Display", classes="section-label"),
            H2("Badges & Tags"),
            Divider(label="Badges"),
            Row(
                *[Badge(v, variant=v, pill=True) for v in ["primary", "secondary", "success", "danger", "warning", "info", "light"]],
                style="flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem;",
            ),
            Divider(label="Tags (removable)"),
            Row(
                Tag("Python", color="#3b82f6", removable=True),
                Tag("FastAPI", color="#8b5cf6", removable=True),
                Tag("croc-ui", color="#10b981", removable=True),
                style="flex-wrap: wrap; gap: 0.5rem;",
            ),
        ),

        # Alerts
        Section(
            P("Feedback", classes="section-label"),
            H2("Alerts"),
            Alert("This is an informational message.", variant="info", title="Info:", dismissible=True),
            Div(style="height: 0.75rem;"),
            Alert("Operation completed successfully!", variant="success", title="Success:", dismissible=True),
            Div(style="height: 0.75rem;"),
            Alert("Please review before proceeding.", variant="warning", title="Warning:", dismissible=True),
            Div(style="height: 0.75rem;"),
            Alert("Something went wrong. Please try again.", variant="danger", title="Error:", dismissible=True),
        ),

        # Cards
        Section(
            P("Layout", classes="section-label"),
            H2("Cards"),
            Row(
                Card(
                    P("A basic card with body content.", style="color: var(--croc-text-muted);"),
                    Button("Action", variant="primary", size="sm"),
                    title="Basic Card",
                    subtitle="With subtitle",
                ),
                Card(
                    Avatar(initials="SK", size="48px"),
                    H3("Swarup Kumar", style="margin-top: 0.75rem; margin-bottom: 0.25rem;"),
                    P("Creator of croc-ui", style="color: var(--croc-text-muted); font-size: 0.875rem;"),
                    title=None,
                    footer=Row(
                        Badge("Python", variant="primary", pill=True),
                        Badge("Web Dev", variant="secondary", pill=True),
                    ),
                    style="text-align: center;",
                ),
                Card(
                    Progress(value=75, variant="success", label="Storage Used", show_label=True),
                    Div(style="height: 0.75rem;"),
                    Progress(value=40, variant="warning", label="Memory", show_label=True),
                    Div(style="height: 0.75rem;"),
                    Progress(value=90, variant="danger", label="CPU", show_label=True),
                    title="System Stats",
                ),
            ),
        ),

        # Tabs
        Section(
            P("Navigation", classes="section-label"),
            H2("Tabs"),
            Tabs(
                tabs=[
                    ("Overview", P("This is the overview tab content. croc-ui makes building HTML with Python easy.", style="color: var(--croc-text-muted);")),
                    ("Installation", Code("pip install croc-ui", style="display: block; padding: 1rem; background: var(--croc-bg-secondary); border-radius: 8px;")),
                    ("Usage", P("Import components and build your page!", style="color: var(--croc-text-muted);")),
                ],
                active=0,
            ),
        ),

        # Accordion
        Section(
            P("Disclosure", classes="section-label"),
            H2("Accordion"),
            Accordion(
                items=[
                    ("What is croc-ui?", P("croc-ui is a Python library that lets you build static websites using Python classes.", style="color: var(--croc-text-muted);")),
                    ("Do I need to know HTML/CSS?", P("No! croc-ui abstracts HTML and CSS into Python. You just use Python classes and methods.", style="color: var(--croc-text-muted);")),
                    ("Can I use custom CSS?", P("Yes! You can pass style dicts, CSS strings, or use the Style() builder on any element.", style="color: var(--croc-text-muted);")),
                ],
            ),
        ),

        # Table
        Section(
            P("Data", classes="section-label"),
            H2("Table"),
            Table(
                headers=["Component", "Tag", "Category", "Status"],
                rows=[
                    ["Card", "div", "Layout", Badge("Stable", variant="success", pill=True)],
                    ["Navbar", "nav", "Navigation", Badge("Stable", variant="success", pill=True)],
                    ["Modal", "div", "Overlay", Badge("Stable", variant="success", pill=True)],
                    ["Accordion", "div", "Disclosure", Badge("Stable", variant="success", pill=True)],
                    ["Tabs", "div", "Navigation", Badge("Beta", variant="warning", pill=True)],
                ],
                striped=True,
                hover=True,
            ),
        ),

        # Spinners & Avatars
        Section(
            P("Misc", classes="section-label"),
            H2("Spinners & Avatars"),
            Row(
                Spinner(size="32px"),
                Spinner(size="32px", color="var(--croc-success)", label="Loading..."),
                Spinner(size="32px", color="var(--croc-danger)"),
                style="align-items: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;",
            ),
            Row(
                Avatar(initials="SK", size="56px"),
                Avatar(initials="AB", size="56px", color="var(--croc-success)"),
                Avatar(initials="XY", size="56px", color="var(--croc-danger)", shape="square"),
                style="gap: 1rem; align-items: center;",
            ),
        ),

        # Pagination
        Section(
            P("Navigation", classes="section-label"),
            H2("Pagination"),
            Pagination(total_pages=7, current_page=3),
        ),
    )

    return base_page("Components", breadcrumb, content)


# ─────────────────────────────────────────────
# Forms page
# ─────────────────────────────────────────────
def forms_page():
    breadcrumb = Container(
        Breadcrumb([("Home", "/"), ("Forms", None)]),
        style="padding: 1rem 0;",
    )

    form_section = Container(
        Section(
            P("Input Controls", classes="section-label"),
            H2("Form Elements"),
            Row(
                Card(
                    Form(
                        H3("Contact Us", style="margin-bottom: 1.5rem;"),
                        Div(
                            Label("Full Name", for_="name"),
                            Input(type="text", id="name", name="name", placeholder="John Doe",
                                  style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--croc-border); border-radius: 6px; margin-top: 0.25rem; font-size: 1rem; background: var(--croc-bg); color: var(--croc-text);"),
                            style="margin-bottom: 1rem;",
                        ),
                        Div(
                            Label("Email Address", for_="email"),
                            Input(type="email", id="email", name="email", placeholder="you@example.com",
                                  style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--croc-border); border-radius: 6px; margin-top: 0.25rem; font-size: 1rem; background: var(--croc-bg); color: var(--croc-text);"),
                            style="margin-bottom: 1rem;",
                        ),
                        Div(
                            Label("Subject", for_="subject"),
                            Select(
                                Option("General Inquiry", value="general"),
                                Option("Bug Report", value="bug"),
                                Option("Feature Request", value="feature"),
                                name="subject", id="subject",
                                style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--croc-border); border-radius: 6px; margin-top: 0.25rem; font-size: 1rem; background: var(--croc-bg); color: var(--croc-text);",
                            ),
                            style="margin-bottom: 1rem;",
                        ),
                        Div(
                            Label("Message", for_="msg"),
                            Textarea("", name="msg", id="msg", placeholder="Your message...", rows=4,
                                     style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--croc-border); border-radius: 6px; margin-top: 0.25rem; font-size: 1rem; background: var(--croc-bg); color: var(--croc-text); resize: vertical;"),
                            style="margin-bottom: 1.25rem;",
                        ),
                        Div(
                            Checkbox(name="agree", value="yes", id="agree"),
                            Label(" I agree to the terms", for_="agree", style="margin-left: 0.5rem; cursor: pointer;"),
                            style="display: flex; align-items: center; margin-bottom: 1.25rem;",
                        ),
                        Button("Send Message →", variant="primary", type="submit"),
                        action="#", method="post",
                    ),
                    padding="1.5rem",
                ),
                Card(
                    H3("Button Variants", style="margin-bottom: 1rem;"),
                    *[Div(Button(f"{v.capitalize()} Button", variant=v), style="margin-bottom: 0.5rem;")
                      for v in ["primary", "secondary", "success", "danger", "warning", "outline", "ghost"]],
                    Divider(label="Sizes"),
                    Row(
                        Button("Small", variant="primary", size="sm"),
                        Button("Medium", variant="primary", size="md"),
                        Button("Large", variant="primary", size="lg"),
                        style="gap: 0.5rem; align-items: center;",
                    ),
                    padding="1.5rem",
                ),
            ),
        ),
    )

    return base_page("Forms", breadcrumb, form_section)


# ─────────────────────────────────────────────
# Theme page
# ─────────────────────────────────────────────
def theme_page():
    breadcrumb = Container(
        Breadcrumb([("Home", "/"), ("Theme", None)]),
        style="padding: 1rem 0;",
    )

    content = Container(
        Section(
            P("Design Tokens", classes="section-label"),
            H2("Theme System"),
            P("croc-ui uses CSS variables for consistent theming. Switch presets or override tokens individually.", style="color: var(--croc-text-muted); margin-bottom: 2rem;"),
            Row(
                *[Card(
                    P(name, style=f"font-weight: 700; color: {colors[0]};"),
                    P(f"Primary: {colors[0]}", style="font-size: 0.875rem; color: var(--croc-text-muted);"),
                    style=f"border-top: 4px solid {colors[0]};",
                ) for name, colors in [
                    ("Default", ["#3b82f6"]),
                    ("Dark", ["#60a5fa"]),
                    ("Ocean", ["#0284c7"]),
                    ("Forest", ["#16a34a"]),
                ]],
            ),
            Divider(label="Usage"),
            Card(
                Code(
                    """from croc_ui import Page, Theme

# Use a preset
page = Page(theme=Theme("dark"))

# Or customize
page = Page(theme=Theme(
    preset="default",
    primary="#ff6b35",
    font_family="'Playfair Display', serif",
    border_radius="12px",
))""",
                    style="display: block; white-space: pre; font-size: 0.875rem; line-height: 1.6;",
                ),
                style="background: #0f172a; border-color: #1e293b;",
            ),
        ),
    )

    return base_page("Theme", breadcrumb, content)


# ─────────────────────────────────────────────
# Wire up the app
# ─────────────────────────────────────────────
app = App()

app.add_route("/", home_page)
app.add_route("/components", components_page)
app.add_route("/forms", forms_page)
app.add_route("/theme", theme_page)

if __name__ == "__main__":
    app.run(port=3000)
