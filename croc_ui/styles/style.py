"""
Style utilities for croc-ui.
"""
from typing import Dict, Optional, Union


class Style:
    """
    Fluent CSS style builder.

    Usage:
        style = Style().color("red").font_size("16px").padding("10px")
        element = Div(style=style)
    """

    def __init__(self, **initial_styles):
        self._styles: Dict[str, str] = {}
        for k, v in initial_styles.items():
            self._styles[k.replace("_", "-")] = str(v)

    def _set(self, prop: str, value: str) -> "Style":
        self._styles[prop] = value
        return self

    # --- Typography ---
    def color(self, v): return self._set("color", v)
    def font_size(self, v): return self._set("font-size", v)
    def font_family(self, v): return self._set("font-family", v)
    def font_weight(self, v): return self._set("font-weight", v)
    def font_style(self, v): return self._set("font-style", v)
    def line_height(self, v): return self._set("line-height", v)
    def letter_spacing(self, v): return self._set("letter-spacing", v)
    def text_align(self, v): return self._set("text-align", v)
    def text_decoration(self, v): return self._set("text-decoration", v)
    def text_transform(self, v): return self._set("text-transform", v)
    def white_space(self, v): return self._set("white-space", v)

    # --- Box Model ---
    def margin(self, v): return self._set("margin", v)
    def margin_top(self, v): return self._set("margin-top", v)
    def margin_right(self, v): return self._set("margin-right", v)
    def margin_bottom(self, v): return self._set("margin-bottom", v)
    def margin_left(self, v): return self._set("margin-left", v)
    def padding(self, v): return self._set("padding", v)
    def padding_top(self, v): return self._set("padding-top", v)
    def padding_right(self, v): return self._set("padding-right", v)
    def padding_bottom(self, v): return self._set("padding-bottom", v)
    def padding_left(self, v): return self._set("padding-left", v)
    def width(self, v): return self._set("width", v)
    def height(self, v): return self._set("height", v)
    def min_width(self, v): return self._set("min-width", v)
    def min_height(self, v): return self._set("min-height", v)
    def max_width(self, v): return self._set("max-width", v)
    def max_height(self, v): return self._set("max-height", v)

    # --- Background ---
    def background(self, v): return self._set("background", v)
    def background_color(self, v): return self._set("background-color", v)
    def background_image(self, v): return self._set("background-image", v)
    def background_size(self, v): return self._set("background-size", v)
    def background_position(self, v): return self._set("background-position", v)
    def background_repeat(self, v): return self._set("background-repeat", v)

    # --- Border ---
    def border(self, v): return self._set("border", v)
    def border_top(self, v): return self._set("border-top", v)
    def border_right(self, v): return self._set("border-right", v)
    def border_bottom(self, v): return self._set("border-bottom", v)
    def border_left(self, v): return self._set("border-left", v)
    def border_radius(self, v): return self._set("border-radius", v)
    def border_color(self, v): return self._set("border-color", v)
    def border_width(self, v): return self._set("border-width", v)
    def border_style(self, v): return self._set("border-style", v)
    def outline(self, v): return self._set("outline", v)

    # --- Flexbox ---
    def display(self, v): return self._set("display", v)
    def flex(self, v): return self._set("flex", v)
    def flex_direction(self, v): return self._set("flex-direction", v)
    def flex_wrap(self, v): return self._set("flex-wrap", v)
    def flex_grow(self, v): return self._set("flex-grow", v)
    def flex_shrink(self, v): return self._set("flex-shrink", v)
    def flex_basis(self, v): return self._set("flex-basis", v)
    def justify_content(self, v): return self._set("justify-content", v)
    def align_items(self, v): return self._set("align-items", v)
    def align_self(self, v): return self._set("align-self", v)
    def align_content(self, v): return self._set("align-content", v)
    def gap(self, v): return self._set("gap", v)
    def row_gap(self, v): return self._set("row-gap", v)
    def column_gap(self, v): return self._set("column-gap", v)

    # --- Grid ---
    def grid_template_columns(self, v): return self._set("grid-template-columns", v)
    def grid_template_rows(self, v): return self._set("grid-template-rows", v)
    def grid_column(self, v): return self._set("grid-column", v)
    def grid_row(self, v): return self._set("grid-row", v)
    def grid_area(self, v): return self._set("grid-area", v)

    # --- Position ---
    def position(self, v): return self._set("position", v)
    def top(self, v): return self._set("top", v)
    def right(self, v): return self._set("right", v)
    def bottom(self, v): return self._set("bottom", v)
    def left(self, v): return self._set("left", v)
    def z_index(self, v): return self._set("z-index", v)

    # --- Effects ---
    def opacity(self, v): return self._set("opacity", v)
    def box_shadow(self, v): return self._set("box-shadow", v)
    def text_shadow(self, v): return self._set("text-shadow", v)
    def transform(self, v): return self._set("transform", v)
    def transition(self, v): return self._set("transition", v)
    def animation(self, v): return self._set("animation", v)
    def filter(self, v): return self._set("filter", v)
    def backdrop_filter(self, v): return self._set("backdrop-filter", v)
    def overflow(self, v): return self._set("overflow", v)
    def overflow_x(self, v): return self._set("overflow-x", v)
    def overflow_y(self, v): return self._set("overflow-y", v)
    def cursor(self, v): return self._set("cursor", v)
    def pointer_events(self, v): return self._set("pointer-events", v)
    def user_select(self, v): return self._set("user-select", v)
    def visibility(self, v): return self._set("visibility", v)

    # --- Misc ---
    def object_fit(self, v): return self._set("object-fit", v)
    def object_position(self, v): return self._set("object-position", v)
    def resize(self, v): return self._set("resize", v)
    def list_style(self, v): return self._set("list-style", v)
    def vertical_align(self, v): return self._set("vertical-align", v)
    def float(self, v): return self._set("float", v)
    def clear(self, v): return self._set("clear", v)

    def custom(self, prop: str, value: str) -> "Style":
        """Set any arbitrary CSS property."""
        return self._set(prop, value)

    def merge(self, other: "Style") -> "Style":
        """Merge another Style object into this one."""
        self._styles.update(other._styles)
        return self

    def to_dict(self) -> Dict[str, str]:
        return dict(self._styles)

    def to_css_string(self) -> str:
        return "; ".join(f"{k}: {v}" for k, v in self._styles.items())

    def __str__(self):
        return self.to_css_string()
