"""
croc demo app — showcases all v0.1 components and features.
Run with: python examples/demo.py
"""
import croc

app = croc.App(title="🐊 croc demo", theme="light")

# ── Shared state ─────────────────────────────────────────────────────────────
state = croc.State(
    count=0,
    name="World",
    dark=False,
    checked=False,
    slider_val=40,
    selected="b",
    text_input="",
)


# ── Pages ─────────────────────────────────────────────────────────────────────

@app.page("/")
def home():
    def increment():
        state.count += 1

    def decrement():
        state.count -= 1

    def reset():
        state.count = 0

    return croc.Page(title="croc demo", children=[
        croc.HStack([
            croc.Heading("🐊 croc", level=1),
            croc.Badge("v0.1.0", variant="info"),
        ]),
        croc.Text("A Python library for building server-driven single-page apps.", size="lg"),
        croc.Divider(),

        # Navigation
        croc.HStack([
            croc.Link("Home", href="/"),
            croc.Link("Components", href="/components"),
            croc.Link("About", href="/about"),
        ]),
        croc.Divider(),

        # Counter card
        croc.Card(title="Counter", subtitle="Click the buttons to update state", children=[
            croc.Center([
                croc.Heading(str(state.count), level=1),
            ]),
            croc.HStack([
                croc.Button("−", on_click=decrement, variant="secondary"),
                croc.Button("Reset", on_click=reset, variant="ghost"),
                croc.Button("+", on_click=increment, variant="primary"),
            ]),
        ]),

        # Stats row
        croc.Grid(cols=3, children=[
            croc.Stat(label="Total Clicks", value=str(state.count), delta="+1"),
            croc.Stat(label="Uptime", value="99.9%", delta="+0.1%"),
            croc.Stat(label="Components", value="24", delta="+24"),
        ]),
    ])


@app.page("/components")
def components():
    def on_name_change(value=""):
        state.text_input = value

    def on_select_change(value=""):
        state.selected = value

    def on_slider_change(value=50):
        state.slider_val = value

    def on_check_change(checked=False):
        state.checked = checked

    def on_switch_change(checked=False):
        state.dark = checked

    return croc.Page(title="Components — croc demo", children=[
        croc.HStack([
            croc.Link("← Back", href="/"),
            croc.Heading("Component Gallery", level=2),
        ]),
        croc.Divider(),

        # Badges
        croc.Card(title="Badges", children=[
            croc.HStack([
                croc.Badge("default"),
                croc.Badge("success", variant="success"),
                croc.Badge("warning", variant="warning"),
                croc.Badge("error", variant="error"),
                croc.Badge("info", variant="info"),
            ]),
        ]),

        # Buttons
        croc.Card(title="Buttons", children=[
            croc.HStack([
                croc.Button("Primary"),
                croc.Button("Secondary", variant="secondary"),
                croc.Button("Danger", variant="danger"),
                croc.Button("Ghost", variant="ghost"),
                croc.Button("Outline", variant="outline"),
                croc.Button("Disabled", disabled=True),
            ]),
        ]),

        # Alerts
        croc.Card(title="Alerts", children=[
            croc.VStack([
                croc.Alert("This is an info alert.", variant="info", title="Info"),
                croc.Alert("Action completed!", variant="success", title="Success"),
                croc.Alert("Proceed with caution.", variant="warning", title="Warning"),
                croc.Alert("Something went wrong.", variant="error", title="Error"),
            ]),
        ]),

        # Inputs
        croc.Card(title="Inputs", children=[
            croc.VStack([
                croc.Input(label="Your name", placeholder="Type something...",
                           value=state.text_input, on_change=on_name_change),
                croc.Text(f"You typed: {state.text_input or '—'}"),
                croc.Textarea(label="Message", placeholder="Write a message...", rows=3),
                croc.Select(
                    label="Pick an option",
                    options=[("a", "Option A"), ("b", "Option B"), ("c", "Option C")],
                    value=state.selected,
                    on_change=on_select_change,
                ),
                croc.Text(f"Selected: {state.selected}"),
                croc.Checkbox(label="Enable feature", checked=state.checked,
                              on_change=on_check_change),
                croc.Switch(label="Dark mode", checked=state.dark,
                            on_change=on_switch_change),
                croc.Slider(label="Volume", min=0, max=100, value=state.slider_val,
                            on_change=on_slider_change),
                croc.Text(f"Slider value: {state.slider_val}"),
            ]),
        ]),

        # Progress
        croc.Card(title="Progress", children=[
            croc.VStack([
                croc.Progress(value=state.slider_val, max=100, label="Loading..."),
                croc.Progress(value=72, max=100, label="Uploading"),
            ]),
        ]),

        # Avatars
        croc.Card(title="Avatars", children=[
            croc.HStack([
                croc.Avatar(name="Alice Smith", size="sm"),
                croc.Avatar(name="Bob Jones", size="md"),
                croc.Avatar(name="Charlie Brown", size="lg"),
            ]),
        ]),

        # Code
        croc.Card(title="Code", children=[
            croc.VStack([
                croc.Code("import croc"),
                croc.Code("app = croc.App()\n\n@app.page('/')\ndef home():\n    return croc.Heading('Hello!')\n\napp.run()", block=True),
            ]),
        ]),

        # Table
        croc.Card(title="Table", children=[
            croc.Table(
                columns=["Name", "Role", "Status"],
                rows=[
                    ["Alice", "Engineer", "Active"],
                    ["Bob", "Designer", "Active"],
                    ["Charlie", "Manager", "Away"],
                    ["Diana", "Engineer", "Inactive"],
                ],
            ),
        ]),

        # Spinner
        croc.Card(title="Spinners", children=[
            croc.HStack([
                croc.Spinner(size="sm"),
                croc.Spinner(size="md"),
                croc.Spinner(size="lg"),
            ]),
        ]),
    ])


@app.page("/about")
def about():
    return croc.Page(title="About — croc", children=[
        croc.Link("← Back", href="/"),
        croc.Heading("About croc", level=2),
        croc.Text("croc is a Python library for building server-driven SPAs using FastAPI and WebSockets.", size="lg"),
        croc.Divider(),
        croc.Card(title="How it works", children=[
            croc.VStack([
                croc.Text("1. You write Python components and pages."),
                croc.Text("2. croc renders them on the server as a component tree."),
                croc.Text("3. The browser renders the UI from that tree via WebSocket."),
                croc.Text("4. Events (clicks, inputs) are sent back to Python handlers."),
                croc.Text("5. State changes trigger a re-render — no manual DOM work needed."),
            ]),
        ]),
    ])


@app.not_found
def not_found():
    return croc.Page(title="404", children=[
        croc.Center([
            croc.VStack([
                croc.Heading("404", level=1),
                croc.Text("Page not found."),
                croc.Link("Go Home", href="/"),
            ]),
        ]),
    ])


if __name__ == "__main__":
    app.run(port=8000)
