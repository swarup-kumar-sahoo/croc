"""
Form components for croc-ui.
"""
from ..base import Element, VoidElement
from typing import Any, Dict, List, Optional, Tuple, Union


class Form(Element):
    tag = "form"

    def __init__(self, *children, action: str = "", method: str = "post",
                 enctype: Optional[str] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["action"] = action
        attrs["method"] = method
        if enctype:
            attrs["enctype"] = enctype
        super().__init__(*children, attrs=attrs, **kwargs)


class Input(VoidElement):
    tag = "input"

    def __init__(self, type: str = "text", name: Optional[str] = None,
                 value: Optional[str] = None, placeholder: Optional[str] = None,
                 required: bool = False, disabled: bool = False,
                 readonly: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = type
        if name:
            attrs["name"] = name
        if value is not None:
            attrs["value"] = value
        if placeholder:
            attrs["placeholder"] = placeholder
        if required:
            attrs["required"] = True
        if disabled:
            attrs["disabled"] = True
        if readonly:
            attrs["readonly"] = True
        super().__init__(attrs=attrs, **kwargs)


class Button(Element):
    tag = "button"

    VARIANTS = {
        "primary": "background: var(--croc-primary); color: white; border: none;",
        "secondary": "background: var(--croc-secondary); color: white; border: none;",
        "success": "background: var(--croc-success); color: white; border: none;",
        "danger": "background: var(--croc-danger); color: white; border: none;",
        "warning": "background: var(--croc-warning); color: white; border: none;",
        "outline": "background: transparent; color: var(--croc-primary); border: 2px solid var(--croc-primary);",
        "ghost": "background: transparent; color: var(--croc-text); border: none;",
        "link": "background: transparent; color: var(--croc-primary); border: none; text-decoration: underline;",
    }

    def __init__(self, *children, type: str = "button", variant: str = "primary",
                 disabled: bool = False, size: str = "md", **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = type
        if disabled:
            attrs["disabled"] = True

        size_padding = {"sm": "0.25rem 0.75rem", "md": "0.5rem 1.25rem", "lg": "0.75rem 1.75rem"}
        size_font = {"sm": "0.875rem", "md": "1rem", "lg": "1.125rem"}

        variant_style = self.VARIANTS.get(variant, self.VARIANTS["primary"])
        base_style = (
            f"padding: {size_padding.get(size, '0.5rem 1.25rem')}; "
            f"font-size: {size_font.get(size, '1rem')}; "
            f"border-radius: var(--croc-border-radius, 8px); "
            f"cursor: pointer; "
            f"font-weight: 600; "
            f"transition: var(--croc-transition, all 0.2s ease); "
            f"display: inline-flex; align-items: center; gap: 0.5rem; "
            f"{variant_style}"
        )

        existing_style = kwargs.pop("style", "")
        if existing_style:
            final_style = base_style + "; " + str(existing_style)
        else:
            final_style = base_style

        super().__init__(*children, attrs=attrs, style=final_style, **kwargs)


class Textarea(Element):
    tag = "textarea"

    def __init__(self, content: str = "", name: Optional[str] = None,
                 placeholder: Optional[str] = None, rows: int = 4,
                 cols: Optional[int] = None, required: bool = False,
                 disabled: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if name:
            attrs["name"] = name
        if placeholder:
            attrs["placeholder"] = placeholder
        attrs["rows"] = rows
        if cols:
            attrs["cols"] = cols
        if required:
            attrs["required"] = True
        if disabled:
            attrs["disabled"] = True
        super().__init__(content, attrs=attrs, **kwargs)


class Select(Element):
    tag = "select"

    def __init__(self, *options, name: Optional[str] = None, required: bool = False,
                 disabled: bool = False, multiple: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if name:
            attrs["name"] = name
        if required:
            attrs["required"] = True
        if disabled:
            attrs["disabled"] = True
        if multiple:
            attrs["multiple"] = True
        super().__init__(*options, attrs=attrs, **kwargs)


class Option(Element):
    tag = "option"

    def __init__(self, label: str, value: Optional[str] = None, selected: bool = False,
                 disabled: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if value is not None:
            attrs["value"] = value
        if selected:
            attrs["selected"] = True
        if disabled:
            attrs["disabled"] = True
        super().__init__(label, attrs=attrs, **kwargs)


class Checkbox(VoidElement):
    tag = "input"

    def __init__(self, name: Optional[str] = None, value: Optional[str] = None,
                 checked: bool = False, disabled: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "checkbox"
        if name:
            attrs["name"] = name
        if value:
            attrs["value"] = value
        if checked:
            attrs["checked"] = True
        if disabled:
            attrs["disabled"] = True
        super().__init__(attrs=attrs, **kwargs)


class Radio(VoidElement):
    tag = "input"

    def __init__(self, name: Optional[str] = None, value: Optional[str] = None,
                 checked: bool = False, disabled: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "radio"
        if name:
            attrs["name"] = name
        if value:
            attrs["value"] = value
        if checked:
            attrs["checked"] = True
        if disabled:
            attrs["disabled"] = True
        super().__init__(attrs=attrs, **kwargs)


class FileInput(VoidElement):
    tag = "input"

    def __init__(self, name: Optional[str] = None, accept: Optional[str] = None,
                 multiple: bool = False, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "file"
        if name:
            attrs["name"] = name
        if accept:
            attrs["accept"] = accept
        if multiple:
            attrs["multiple"] = True
        super().__init__(attrs=attrs, **kwargs)


class Range(VoidElement):
    tag = "input"

    def __init__(self, name: Optional[str] = None, min: Union[int, float] = 0,
                 max: Union[int, float] = 100, step: Union[int, float] = 1,
                 value: Optional[Union[int, float]] = None, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs["type"] = "range"
        attrs["min"] = min
        attrs["max"] = max
        attrs["step"] = step
        if name:
            attrs["name"] = name
        if value is not None:
            attrs["value"] = value
        super().__init__(attrs=attrs, **kwargs)


class Fieldset(Element):
    tag = "fieldset"


class Legend(Element):
    tag = "legend"
