"""
UI components for croc-ui: Card, Badge, Alert, Modal, Tooltip, Progress, Spinner,
Accordion, Table, List, Tag, Divider, Avatar.
"""
from ..base import Element
from ..components.typography import H3, P
from typing import Any, Dict, List, Optional, Tuple, Union
import builtins
builtins_max = builtins.max


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------
class Card(Element):
    tag = "div"

    def __init__(self, *children, title: Optional[str] = None,
                 subtitle: Optional[str] = None, footer: Optional[Any] = None,
                 shadow: bool = True, hover: bool = False,
                 padding: str = "1.25rem", **kwargs):
        style = kwargs.pop("style", {})
        shadow_val = "var(--croc-shadow)" if shadow else "none"
        card_style = (
            f"background: var(--croc-bg); border: 1px solid var(--croc-border); "
            f"border-radius: var(--croc-border-radius, 8px); box-shadow: {shadow_val}; "
            f"overflow: hidden;"
            + (f" transition: var(--croc-transition); cursor: pointer;" if hover else "")
        )
        if isinstance(style, dict):
            card_style += "; " + "; ".join(f"{k}:{v}" for k, v in style.items())
        elif isinstance(style, str) and style:
            card_style += "; " + style

        inner = []
        if title or subtitle:
            header_children = []
            if title:
                h = Element.__new__(Element)
                h.tag = "h3"
                h.children = [title]
                h.id = None
                h._classes = ["croc-card-title"]
                h._style = "font-size: 1.125rem; font-weight: 700; color: var(--croc-text); margin-bottom: 0.25rem;"
                h._attrs = {}
                h._extra_attrs = {}
                header_children.append(h)
            if subtitle:
                s = Element.__new__(Element)
                s.tag = "p"
                s.children = [subtitle]
                s.id = None
                s._classes = ["croc-card-subtitle"]
                s._style = "font-size: 0.875rem; color: var(--croc-text-muted);"
                s._attrs = {}
                s._extra_attrs = {}
                header_children.append(s)
            hdr = Element.__new__(Element)
            hdr.tag = "div"
            hdr.children = header_children
            hdr.id = None
            hdr._classes = ["croc-card-header"]
            hdr._style = f"padding: {padding}; border-bottom: 1px solid var(--croc-border);"
            hdr._attrs = {}
            hdr._extra_attrs = {}
            inner.append(hdr)

        body = Element.__new__(Element)
        body.tag = "div"
        body.children = list(children)
        body.id = None
        body._classes = ["croc-card-body"]
        body._style = f"padding: {padding};"
        body._attrs = {}
        body._extra_attrs = {}
        inner.append(body)

        if footer:
            ftr = Element.__new__(Element)
            ftr.tag = "div"
            ftr.children = [footer] if not isinstance(footer, list) else footer
            ftr.id = None
            ftr._classes = ["croc-card-footer"]
            ftr._style = f"padding: {padding}; border-top: 1px solid var(--croc-border); background: var(--croc-bg-secondary);"
            ftr._attrs = {}
            ftr._extra_attrs = {}
            inner.append(ftr)

        classes = kwargs.pop("classes", [])
        if isinstance(classes, str):
            classes = classes.split()
        super().__init__(*inner, classes=list(classes) + ["croc-card"], style=card_style, **kwargs)


# ---------------------------------------------------------------------------
# Badge
# ---------------------------------------------------------------------------
class Badge(Element):
    tag = "span"

    COLORS = {
        "primary": ("var(--croc-primary)", "white"),
        "secondary": ("var(--croc-secondary)", "white"),
        "success": ("var(--croc-success)", "white"),
        "danger": ("var(--croc-danger)", "white"),
        "warning": ("var(--croc-warning)", "white"),
        "info": ("var(--croc-info)", "white"),
        "light": ("var(--croc-bg-secondary)", "var(--croc-text)"),
    }

    def __init__(self, text: str, variant: str = "primary", pill: bool = False, **kwargs):
        bg, fg = self.COLORS.get(variant, self.COLORS["primary"])
        radius = "999px" if pill else "4px"
        style = (
            f"display: inline-flex; align-items: center; "
            f"padding: 0.2em 0.6em; font-size: 0.75em; font-weight: 700; "
            f"background: {bg}; color: {fg}; border-radius: {radius}; "
            f"line-height: 1;"
        )
        super().__init__(text, style=style, **kwargs)


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------
class Alert(Element):
    tag = "div"

    STYLES = {
        "info": ("#dbeafe", "#1e40af", "#93c5fd"),
        "success": ("#dcfce7", "#166534", "#86efac"),
        "warning": ("#fef3c7", "#92400e", "#fcd34d"),
        "danger": ("#fee2e2", "#991b1b", "#fca5a5"),
    }

    def __init__(self, message: str, variant: str = "info",
                 title: Optional[str] = None, dismissible: bool = False, **kwargs):
        bg, text_color, border_color = self.STYLES.get(variant, self.STYLES["info"])
        style = (
            f"padding: 1rem 1.25rem; border-radius: 8px; "
            f"background: {bg}; color: {text_color}; "
            f"border-left: 4px solid {border_color}; "
            f"position: relative;"
        )
        children = []
        if title:
            t = Element.__new__(Element)
            t.tag = "strong"
            t.children = [title + " "]
            t.id = None
            t._classes = []
            t._style = None
            t._attrs = {}
            t._extra_attrs = {}
            children.append(t)
        children.append(message)
        if dismissible:
            btn = Element.__new__(Element)
            btn.tag = "button"
            btn.children = ["×"]
            btn.id = None
            btn._classes = []
            btn._style = "position: absolute; top: 0.5rem; right: 0.75rem; background: none; border: none; font-size: 1.25rem; cursor: pointer; color: inherit; line-height: 1;"
            btn._attrs = {"onclick": "this.parentElement.remove()", "type": "button"}
            btn._extra_attrs = {}
            children.append(btn)
        super().__init__(*children, style=style, **kwargs)


# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------
class Modal(Element):
    tag = "div"

    def __init__(self, *body_children, id: str = "croc-modal", title: Optional[str] = None,
                 footer: Optional[Any] = None, **kwargs):
        overlay_style = (
            "display: none; position: fixed; inset: 0; "
            "background: rgba(0,0,0,0.5); z-index: 9999; "
            "align-items: center; justify-content: center; "
            "backdrop-filter: blur(2px);"
        )
        dialog_style = (
            "background: var(--croc-bg); border-radius: 12px; "
            "max-width: 540px; width: 90%; box-shadow: var(--croc-shadow-lg); "
            "overflow: hidden; max-height: 90vh; display: flex; flex-direction: column;"
        )

        modal_children = []

        if title:
            hdr = Element.__new__(Element)
            hdr.tag = "div"
            hdr.children = []
            hdr.id = None
            hdr._classes = ["croc-modal-header"]
            hdr._style = "padding: 1rem 1.25rem; border-bottom: 1px solid var(--croc-border); display: flex; align-items: center; justify-content: space-between;"
            hdr._attrs = {}
            hdr._extra_attrs = {}

            title_el = Element.__new__(Element)
            title_el.tag = "h4"
            title_el.children = [title]
            title_el.id = None
            title_el._classes = []
            title_el._style = "font-weight: 700; font-size: 1.125rem;"
            title_el._attrs = {}
            title_el._extra_attrs = {}

            close_btn = Element.__new__(Element)
            close_btn.tag = "button"
            close_btn.children = ["×"]
            close_btn.id = None
            close_btn._classes = []
            close_btn._style = "background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--croc-text-muted); line-height: 1;"
            close_btn._attrs = {"onclick": f"document.getElementById('{id}').style.display='none'", "type": "button"}
            close_btn._extra_attrs = {}

            hdr.children = [title_el, close_btn]
            modal_children.append(hdr)

        body = Element.__new__(Element)
        body.tag = "div"
        body.children = list(body_children)
        body.id = None
        body._classes = ["croc-modal-body"]
        body._style = "padding: 1.25rem; overflow-y: auto; flex: 1;"
        body._attrs = {}
        body._extra_attrs = {}
        modal_children.append(body)

        if footer:
            ftr = Element.__new__(Element)
            ftr.tag = "div"
            ftr.children = [footer] if not isinstance(footer, list) else footer
            ftr.id = None
            ftr._classes = ["croc-modal-footer"]
            ftr._style = "padding: 1rem 1.25rem; border-top: 1px solid var(--croc-border); display: flex; justify-content: flex-end; gap: 0.5rem;"
            ftr._attrs = {}
            ftr._extra_attrs = {}
            modal_children.append(ftr)

        dialog = Element.__new__(Element)
        dialog.tag = "div"
        dialog.children = modal_children
        dialog.id = None
        dialog._classes = ["croc-modal-dialog"]
        dialog._style = dialog_style
        dialog._attrs = {}
        dialog._extra_attrs = {}

        super().__init__(dialog, id=id, style=overlay_style,
                         attrs={"onclick": f"if(event.target===this)this.style.display='none'"},
                         **{k: v for k, v in kwargs.items()})

    def open_script(self) -> str:
        return f"document.getElementById('{self.id}').style.display='flex';"


# ---------------------------------------------------------------------------
# Tooltip
# ---------------------------------------------------------------------------
class Tooltip(Element):
    tag = "span"

    def __init__(self, *children, tip: str, position: str = "top", **kwargs):
        style = "position: relative; display: inline-block;"
        tip_style = (
            f"position: absolute; background: #1e293b; color: white; "
            f"padding: 0.35rem 0.65rem; border-radius: 6px; font-size: 0.8rem; "
            f"white-space: nowrap; pointer-events: none; opacity: 0; "
            f"transition: opacity 0.2s; z-index: 100; "
        )
        pos_map = {
            "top": "bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%);",
            "bottom": "top: calc(100% + 6px); left: 50%; transform: translateX(-50%);",
            "left": "right: calc(100% + 6px); top: 50%; transform: translateY(-50%);",
            "right": "left: calc(100% + 6px); top: 50%; transform: translateY(-50%);",
        }
        tip_style += pos_map.get(position, pos_map["top"])

        tip_el = Element.__new__(Element)
        tip_el.tag = "span"
        tip_el.children = [tip]
        tip_el.id = None
        tip_el._classes = ["croc-tooltip-tip"]
        tip_el._style = tip_style
        tip_el._attrs = {}
        tip_el._extra_attrs = {}

        hover_style = style + " --croc-tip-opacity: 1;"
        super().__init__(*list(children) + [tip_el], style=style,
                         attrs={"onmouseenter": "this.querySelector('.croc-tooltip-tip').style.opacity='1'",
                                "onmouseleave": "this.querySelector('.croc-tooltip-tip').style.opacity='0'"},
                         **kwargs)


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------
class Progress(Element):
    tag = "div"

    def __init__(self, value: float = 0, max: float = 100, label: Optional[str] = None,
                 variant: str = "primary", show_label: bool = False, **kwargs):
        max_val = max
        pct = min(100, builtins_max(0, (value / max_val) * 100)) if max_val else 0
        color_map = {
            "primary": "var(--croc-primary)",
            "success": "var(--croc-success)",
            "warning": "var(--croc-warning)",
            "danger": "var(--croc-danger)",
        }
        bar_color = color_map.get(variant, color_map["primary"])

        children = []
        if label or show_label:
            lbl_el = Element.__new__(Element)
            lbl_el.tag = "div"
            lbl_el.children = [label or f"{pct:.0f}%"]
            lbl_el.id = None
            lbl_el._classes = []
            lbl_el._style = "font-size: 0.875rem; margin-bottom: 0.25rem; color: var(--croc-text-muted);"
            lbl_el._attrs = {}
            lbl_el._extra_attrs = {}
            children.append(lbl_el)

        bar = Element.__new__(Element)
        bar.tag = "div"
        bar.children = []
        bar.id = None
        bar._classes = ["croc-progress-bar"]
        bar._style = (
            f"width: {pct}%; height: 100%; background: {bar_color}; "
            f"border-radius: 999px; transition: width 0.4s ease;"
        )
        bar._attrs = {}
        bar._extra_attrs = {}

        track = Element.__new__(Element)
        track.tag = "div"
        track.children = [bar]
        track.id = None
        track._classes = ["croc-progress-track"]
        track._style = "height: 8px; background: var(--croc-bg-secondary); border-radius: 999px; overflow: hidden;"
        track._attrs = {}
        track._extra_attrs = {}
        children.append(track)

        super().__init__(*children, **kwargs)


# ---------------------------------------------------------------------------
# Spinner
# ---------------------------------------------------------------------------
class Spinner(Element):
    tag = "div"

    def __init__(self, size: str = "24px", color: str = "var(--croc-primary)",
                 label: Optional[str] = None, **kwargs):
        spin_style = (
            f"width: {size}; height: {size}; "
            f"border: 3px solid var(--croc-border); "
            f"border-top-color: {color}; "
            f"border-radius: 50%; "
            f"animation: croc-spin 0.7s linear infinite;"
        )
        spin_el = Element.__new__(Element)
        spin_el.tag = "div"
        spin_el.children = []
        spin_el.id = None
        spin_el._classes = ["croc-spinner"]
        spin_el._style = spin_style
        spin_el._attrs = {}
        spin_el._extra_attrs = {}

        children = [spin_el]
        if label:
            lbl_el = Element.__new__(Element)
            lbl_el.tag = "span"
            lbl_el.children = [label]
            lbl_el.id = None
            lbl_el._classes = []
            lbl_el._style = "font-size: 0.875rem; color: var(--croc-text-muted);"
            lbl_el._attrs = {}
            lbl_el._extra_attrs = {}
            children.append(lbl_el)

        super().__init__(*children,
                         style="display: inline-flex; align-items: center; gap: 0.5rem;",
                         **kwargs)

    def render(self) -> str:
        keyframes = "<style>@keyframes croc-spin { to { transform: rotate(360deg); } }</style>"
        return keyframes + super().render()


# ---------------------------------------------------------------------------
# Accordion
# ---------------------------------------------------------------------------
class Accordion(Element):
    tag = "div"

    def __init__(self, items: List[Tuple[str, Any]], allow_multiple: bool = False, **kwargs):
        acc_items = []
        for i, (title, content) in enumerate(items):
            item_id = f"croc-acc-{id(self)}-{i}"

            body = Element.__new__(Element)
            body.tag = "div"
            body.children = [content]
            body.id = f"{item_id}-body"
            body._classes = ["croc-acc-body"]
            body._style = "display: none; padding: 0.75rem 1rem; border-top: 1px solid var(--croc-border);"
            body._attrs = {}
            body._extra_attrs = {}

            toggle_js = f"""
var b=document.getElementById('{item_id}-body');
var i=document.getElementById('{item_id}-icon');
var open=b.style.display==='block';
{'document.querySelectorAll(".croc-acc-body").forEach(function(x){{x.style.display="none"}}); document.querySelectorAll(".croc-acc-icon").forEach(function(x){{x.textContent="▶"}});' if not allow_multiple else ''}
b.style.display=open?'none':'block';
i.textContent=open?'▶':'▼';
"""
            icon_el = Element.__new__(Element)
            icon_el.tag = "span"
            icon_el.children = ["▶"]
            icon_el.id = f"{item_id}-icon"
            icon_el._classes = ["croc-acc-icon"]
            icon_el._style = "margin-left: auto; font-size: 0.75rem; transition: var(--croc-transition);"
            icon_el._attrs = {}
            icon_el._extra_attrs = {}

            title_el = Element.__new__(Element)
            title_el.tag = "span"
            title_el.children = [title]
            title_el.id = None
            title_el._classes = []
            title_el._style = None
            title_el._attrs = {}
            title_el._extra_attrs = {}

            hdr = Element.__new__(Element)
            hdr.tag = "button"
            hdr.children = [title_el, icon_el]
            hdr.id = None
            hdr._classes = ["croc-acc-header"]
            hdr._style = "width: 100%; display: flex; align-items: center; padding: 0.75rem 1rem; background: none; border: none; cursor: pointer; font-weight: 600; font-size: 1rem; text-align: left;"
            hdr._attrs = {"onclick": toggle_js, "type": "button"}
            hdr._extra_attrs = {}

            item = Element.__new__(Element)
            item.tag = "div"
            item.children = [hdr, body]
            item.id = None
            item._classes = ["croc-acc-item"]
            item._style = "border: 1px solid var(--croc-border); border-radius: 8px; overflow: hidden; margin-bottom: 0.5rem;"
            item._attrs = {}
            item._extra_attrs = {}
            acc_items.append(item)

        super().__init__(*acc_items, **kwargs)


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------
class Table(Element):
    tag = "div"

    def __init__(self, headers: List[str], rows: List[List[Any]],
                 striped: bool = True, hover: bool = True,
                 bordered: bool = False, **kwargs):
        th_style = "padding: 0.75rem 1rem; text-align: left; font-weight: 700; color: var(--croc-text); border-bottom: 2px solid var(--croc-border); white-space: nowrap;"
        td_style = "padding: 0.75rem 1rem; color: var(--croc-text); border-bottom: 1px solid var(--croc-border);"

        header_cells = []
        for h in headers:
            th = Element.__new__(Element)
            th.tag = "th"
            th.children = [str(h)]
            th.id = None
            th._classes = []
            th._style = th_style
            th._attrs = {}
            th._extra_attrs = {}
            header_cells.append(th)

        tr_head = Element.__new__(Element)
        tr_head.tag = "tr"
        tr_head.children = header_cells
        tr_head.id = None
        tr_head._classes = []
        tr_head._style = None
        tr_head._attrs = {}
        tr_head._extra_attrs = {}

        thead = Element.__new__(Element)
        thead.tag = "thead"
        thead.children = [tr_head]
        thead.id = None
        thead._classes = []
        thead._style = None
        thead._attrs = {}
        thead._extra_attrs = {}

        body_rows = []
        for idx, row_data in enumerate(rows):
            tds = []
            for cell in row_data:
                td = Element.__new__(Element)
                td.tag = "td"
                td.children = [str(cell) if not isinstance(cell, Element) else cell]
                td.id = None
                td._classes = []
                td._style = td_style
                td._attrs = {}
                td._extra_attrs = {}
                tds.append(td)

            bg = "var(--croc-bg-secondary)" if (striped and idx % 2 == 1) else "var(--croc-bg)"
            tr = Element.__new__(Element)
            tr.tag = "tr"
            tr.children = tds
            tr.id = None
            tr._classes = ["croc-table-row"]
            tr._style = f"background: {bg};"
            tr._attrs = {}
            tr._extra_attrs = {}
            body_rows.append(tr)

        tbody = Element.__new__(Element)
        tbody.tag = "tbody"
        tbody.children = body_rows
        tbody.id = None
        tbody._classes = []
        tbody._style = None
        tbody._attrs = {}
        tbody._extra_attrs = {}

        table = Element.__new__(Element)
        table.tag = "table"
        table.children = [thead, tbody]
        table.id = None
        table._classes = ["croc-table"]
        table._style = (
            "width: 100%; border-collapse: collapse; "
            + ("border: 1px solid var(--croc-border);" if bordered else "")
        )
        table._attrs = {}
        table._extra_attrs = {}

        wrapper_style = "overflow-x: auto; border-radius: 8px; " + ("border: 1px solid var(--croc-border);" if not bordered else "")
        super().__init__(table, style=wrapper_style, **kwargs)


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------
class List(Element):
    def __init__(self, items: List[Any], ordered: bool = False, **kwargs):
        self.tag = "ol" if ordered else "ul"
        li_children = []
        for item in items:
            li = Element.__new__(Element)
            li.tag = "li"
            li.children = [item] if not isinstance(item, list) else item
            li.id = None
            li._classes = []
            li._style = "padding: 0.25rem 0;"
            li._attrs = {}
            li._extra_attrs = {}
            li_children.append(li)
        super().__init__(*li_children, **kwargs)


# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------
class Tag(Element):
    tag = "span"

    def __init__(self, text: str, color: str = "var(--croc-primary)",
                 removable: bool = False, **kwargs):
        style = (
            f"display: inline-flex; align-items: center; gap: 0.25rem; "
            f"padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.8rem; "
            f"background: {color}20; color: {color}; border: 1px solid {color}40; "
            f"font-weight: 500;"
        )
        children = [text]
        if removable:
            x = Element.__new__(Element)
            x.tag = "span"
            x.children = ["×"]
            x.id = None
            x._classes = []
            x._style = "cursor: pointer; font-size: 1rem; line-height: 1;"
            x._attrs = {"onclick": "this.parentElement.remove()"}
            x._extra_attrs = {}
            children.append(x)
        super().__init__(*children, style=style, **kwargs)


# ---------------------------------------------------------------------------
# Divider
# ---------------------------------------------------------------------------
class Divider(Element):
    tag = "hr"

    def __init__(self, label: Optional[str] = None, **kwargs):
        if label:
            self.tag = "div"
            style = "display: flex; align-items: center; gap: 1rem; color: var(--croc-text-muted); font-size: 0.875rem; margin: 1rem 0;"
            line_style = "flex: 1; height: 1px; background: var(--croc-border);"

            left = Element.__new__(Element)
            left.tag = "span"
            left.children = []
            left.id = None
            left._classes = []
            left._style = line_style
            left._attrs = {}
            left._extra_attrs = {}

            right = Element.__new__(Element)
            right.tag = "span"
            right.children = []
            right.id = None
            right._classes = []
            right._style = line_style
            right._attrs = {}
            right._extra_attrs = {}

            super().__init__(left, label, right, style=style, **kwargs)
        else:
            super().__init__(style="border: none; border-top: 1px solid var(--croc-border); margin: 1rem 0;", **kwargs)

    def render(self) -> str:
        if self.tag == "hr":
            attrs = self._render_id() + self._render_classes() + self._render_style() + self._render_attrs()
            return f"<hr{attrs} />"
        return super().render()


# ---------------------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------------------
class Avatar(Element):
    tag = "div"

    def __init__(self, src: Optional[str] = None, initials: Optional[str] = None,
                 size: str = "48px", shape: str = "circle",
                 color: str = "var(--croc-primary)", **kwargs):
        radius = "50%" if shape == "circle" else "8px"
        base_style = (
            f"width: {size}; height: {size}; border-radius: {radius}; "
            f"overflow: hidden; display: inline-flex; align-items: center; "
            f"justify-content: center; flex-shrink: 0; font-weight: 700; "
        )
        if src:
            img = Element.__new__(Element)
            img.tag = "img"
            img.children = []
            img.id = None
            img._classes = []
            img._style = "width: 100%; height: 100%; object-fit: cover;"
            img._attrs = {"src": src, "alt": initials or "avatar", "loading": "lazy"}
            img._extra_attrs = {}
            super().__init__(img, style=base_style, **kwargs)
        else:
            text = initials[:2].upper() if initials else "?"
            font_size = f"calc({size} * 0.4)"
            full_style = base_style + f"background: {color}20; color: {color}; font-size: {font_size};"
            super().__init__(text, style=full_style, **kwargs)
