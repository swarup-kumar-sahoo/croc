"""
Theme system for croc-ui.
"""
from typing import Dict, Optional


class Theme:
    """
    Design token system for consistent styling across your app.

    Usage:
        theme = Theme(
            primary="#3b82f6",
            font_family="'Inter', sans-serif"
        )
        page = Page(theme=theme)
    """

    PRESETS = {
        "default": {
            "primary": "#3b82f6",
            "secondary": "#8b5cf6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "info": "#06b6d4",
            "light": "#f8fafc",
            "dark": "#0f172a",
            "text": "#1e293b",
            "text_muted": "#64748b",
            "bg": "#ffffff",
            "bg_secondary": "#f1f5f9",
            "border": "#e2e8f0",
            "font_family": "'Inter', system-ui, sans-serif",
            "font_size_base": "16px",
            "border_radius": "8px",
            "shadow": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
            "shadow_lg": "0 10px 15px -3px rgba(0,0,0,0.1)",
            "transition": "all 0.2s ease",
        },
        "dark": {
            "primary": "#60a5fa",
            "secondary": "#a78bfa",
            "success": "#34d399",
            "warning": "#fbbf24",
            "danger": "#f87171",
            "info": "#22d3ee",
            "light": "#1e293b",
            "dark": "#f8fafc",
            "text": "#f1f5f9",
            "text_muted": "#94a3b8",
            "bg": "#0f172a",
            "bg_secondary": "#1e293b",
            "border": "#334155",
            "font_family": "'Inter', system-ui, sans-serif",
            "font_size_base": "16px",
            "border_radius": "8px",
            "shadow": "0 1px 3px rgba(0,0,0,0.3)",
            "shadow_lg": "0 10px 15px -3px rgba(0,0,0,0.4)",
            "transition": "all 0.2s ease",
        },
        "ocean": {
            "primary": "#0284c7",
            "secondary": "#0891b2",
            "success": "#059669",
            "warning": "#d97706",
            "danger": "#dc2626",
            "info": "#0369a1",
            "light": "#f0f9ff",
            "dark": "#082f49",
            "text": "#0c4a6e",
            "text_muted": "#0369a1",
            "bg": "#f0f9ff",
            "bg_secondary": "#e0f2fe",
            "border": "#bae6fd",
            "font_family": "'Merriweather', Georgia, serif",
            "font_size_base": "16px",
            "border_radius": "4px",
            "shadow": "0 2px 8px rgba(2, 132, 199, 0.15)",
            "shadow_lg": "0 8px 24px rgba(2, 132, 199, 0.2)",
            "transition": "all 0.3s ease",
        },
        "forest": {
            "primary": "#16a34a",
            "secondary": "#65a30d",
            "success": "#15803d",
            "warning": "#ca8a04",
            "danger": "#b91c1c",
            "info": "#0284c7",
            "light": "#f0fdf4",
            "dark": "#052e16",
            "text": "#14532d",
            "text_muted": "#166534",
            "bg": "#f0fdf4",
            "bg_secondary": "#dcfce7",
            "border": "#bbf7d0",
            "font_family": "'Lora', Georgia, serif",
            "font_size_base": "16px",
            "border_radius": "6px",
            "shadow": "0 2px 8px rgba(22, 163, 74, 0.15)",
            "shadow_lg": "0 8px 24px rgba(22, 163, 74, 0.2)",
            "transition": "all 0.25s ease",
        },
    }

    def __init__(self, preset: str = "default", **overrides):
        base = self.PRESETS.get(preset, self.PRESETS["default"]).copy()
        base.update(overrides)
        self._tokens: Dict[str, str] = base

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._tokens.get(key, default)

    def set(self, key: str, value: str) -> "Theme":
        self._tokens[key] = value
        return self

    def to_css_variables(self) -> str:
        vars_css = "\n".join(
            f"  --croc-{k.replace('_', '-')}: {v};"
            for k, v in self._tokens.items()
        )
        return f":root {{\n{vars_css}\n}}"

    def to_base_css(self) -> str:
        return f"""
{self.to_css_variables()}

*, *::before, *::after {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: var(--croc-font-family);
  font-size: var(--croc-font-size-base);
  color: var(--croc-text);
  background-color: var(--croc-bg);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

a {{
  color: var(--croc-primary);
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

img {{
  max-width: 100%;
  height: auto;
}}

code {{
  font-family: 'Fira Code', 'Cascadia Code', monospace;
  background: var(--croc-bg-secondary);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.875em;
}}

pre code {{
  background: transparent;
  padding: 0;
}}

/* Croc UI Utility Classes */
.croc-container {{
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}}

.croc-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}}

.croc-col {{
  flex: 1;
  min-width: 0;
}}

.croc-flex {{ display: flex; }}
.croc-flex-col {{ flex-direction: column; }}
.croc-items-center {{ align-items: center; }}
.croc-justify-center {{ justify-content: center; }}
.croc-justify-between {{ justify-content: space-between; }}
.croc-text-center {{ text-align: center; }}
.croc-text-right {{ text-align: right; }}
.croc-w-full {{ width: 100%; }}
.croc-h-full {{ height: 100%; }}
.croc-hidden {{ display: none; }}

/* Responsive */
@media (max-width: 768px) {{
  .croc-row {{
    flex-direction: column;
  }}
  .croc-hide-mobile {{
    display: none;
  }}
}}
"""
