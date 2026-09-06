"""
SHADE Visual Design System.

Centralised dark / light theme layer using CSS custom properties injected
via st.markdown.  Cards and layout inherit the palette automatically
through the CSS cascade — no per-card styling needed.

Public API
----------
apply_theme()   Call once in app.py after init_state().
                Renders the sidebar theme toggle and injects the <style>.
get_palette()   Returns the active palette dict so matplotlib charts
                (or inline SVG) can coordinate colours with the UI theme.
"""

import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════
#  Palettes
# ═══════════════════════════════════════════════════════════════════════════

DARK_PALETTE: dict = {
    # Core
    "bg":             "#0B1117",
    "surface":        "#111923",
    "elevated":       "#17222D",
    "border":         "#263442",
    "primary":        "#20B8A6",
    "primary_hover":  "#1DA394",
    "text":           "#F3F7F8",
    "text_secondary": "#9BAAB5",
    # Semantic
    "success": "#36C98F",
    "warning": "#F3B562",
    "danger":  "#EF6262",
    "info":    "#55A9FF",
    # Derived surfaces
    "code_bg":    "#0D1520",
    "sidebar_bg": "#0E151D",
    "input_bg":   "#17222D",
    # Effects
    "shadow":       "rgba(0,0,0,0.35)",
    "shadow_lg":    "rgba(0,0,0,0.50)",
    "glass_bg":     "rgba(17,25,35,0.60)",
    "glass_border": "rgba(38,52,66,0.50)",
    "bg_gradient":  "linear-gradient(170deg,#0B1117 0%,#0D1620 40%,#0F1925 100%)",
    "primary_glow": "rgba(32,184,166,0.25)",
}

LIGHT_PALETTE: dict = {
    # Core
    "bg":             "#F5F8FA",
    "surface":        "#FFFFFF",
    "elevated":       "#FFFFFF",
    "border":         "#DCE5EA",
    "primary":        "#087F78",
    "primary_hover":  "#066B65",
    "text":           "#17242D",
    "text_secondary": "#52636F",
    # Semantic
    "success": "#36C98F",
    "warning": "#F3B562",
    "danger":  "#EF6262",
    "info":    "#55A9FF",
    # Derived surfaces
    "code_bg":    "#EDF2F6",
    "sidebar_bg": "#EBF0F4",
    "input_bg":   "#F0F4F7",
    # Effects
    "shadow":       "rgba(0,0,0,0.06)",
    "shadow_lg":    "rgba(0,0,0,0.12)",
    "glass_bg":     "rgba(255,255,255,0.70)",
    "glass_border": "rgba(220,229,234,0.60)",
    "bg_gradient":  "linear-gradient(170deg,#F5F8FA 0%,#EFF4F8 40%,#F2F6FA 100%)",
    "primary_glow": "rgba(8,127,120,0.15)",
}


# ═══════════════════════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════════════════════

def get_palette() -> dict:
    """Return the active palette dict for the current theme."""
    return (
        DARK_PALETTE
        if st.session_state.get("shade_dark_mode", True)
        else LIGHT_PALETTE
    )


def apply_theme() -> None:
    """Inject theme CSS and render the sidebar toggle.  Call once in app.py."""
    # Initialise on first run only; subsequent runs are managed by the toggle
    # widget through its key binding.
    if "shade_dark_mode" not in st.session_state:
        st.session_state.shade_dark_mode = True

    # ── Sidebar toggle ────────────────────────────────────────────────
    with st.sidebar:
        st.toggle(
            "🌙 Dark mode",
            key="shade_dark_mode",
            help="Switch between dark and light appearance",
        )

    # ── Inject CSS ────────────────────────────────────────────────────
    p = get_palette()
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:'
        'wght@400;500;600;700;800&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(f"<style>{_build_css(p)}</style>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  CSS generator (private)
# ═══════════════════════════════════════════════════════════════════════════

def _build_css(p: dict) -> str:  # noqa: C901 — long but purely declarative
    return f"""
/* ═══════════════════════════════════════════════════════════════════ */
/*  SHADE Design System — auto-generated from ui/theme.py            */
/* ═══════════════════════════════════════════════════════════════════ */

/* ── CSS Custom Properties ─────────────────────────────────────── */

:root {{
    --shade-bg:              {p["bg"]};
    --shade-surface:         {p["surface"]};
    --shade-elevated:        {p["elevated"]};
    --shade-border:          {p["border"]};
    --shade-primary:         {p["primary"]};
    --shade-primary-hover:   {p["primary_hover"]};
    --shade-text:            {p["text"]};
    --shade-text-secondary:  {p["text_secondary"]};
    --shade-success:         {p["success"]};
    --shade-warning:         {p["warning"]};
    --shade-danger:          {p["danger"]};
    --shade-info:            {p["info"]};
    --shade-code-bg:         {p["code_bg"]};
    --shade-sidebar-bg:      {p["sidebar_bg"]};
    --shade-input-bg:        {p["input_bg"]};
    --shade-radius:          12px;
    --shade-radius-sm:       8px;
    --shade-font:            'Inter', -apple-system, BlinkMacSystemFont,
                             'Segoe UI', Roboto, sans-serif;
}}

/* ── App Shell ─────────────────────────────────────────────────── */

.stApp {{
    background: {p["bg_gradient"]} !important;
    color: var(--shade-text) !important;
    font-family: var(--shade-font) !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
}}

[data-testid="stBottom"] {{
    background: transparent !important;
}}

/* ── Sidebar ───────────────────────────────────────────────────── */

[data-testid="stSidebar"] {{
    background-color: var(--shade-sidebar-bg) !important;
    border-right: 1px solid var(--shade-border) !important;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {{
    color: var(--shade-text) !important;
}}

[data-testid="stSidebar"] h2 {{
    color: var(--shade-primary) !important;
    font-family: var(--shade-font) !important;
    font-weight: 700 !important;
}}

[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {{
    color: var(--shade-text) !important;
    font-family: var(--shade-font) !important;
}}

/* ── Typography ────────────────────────────────────────────────── */

.stApp h1 {{
    font-family: var(--shade-font) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: var(--shade-text) !important;
}}

.stApp h2, .stApp h3 {{
    font-family: var(--shade-font) !important;
    font-weight: 700 !important;
    color: var(--shade-text) !important;
}}

.stApp h4 {{
    font-family: var(--shade-font) !important;
    font-weight: 600 !important;
    color: var(--shade-text) !important;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span {{
    color: var(--shade-text-secondary) !important;
}}

/* ── Surfaces / Cards (glassmorphism) ──────────────────────────── */

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {p["glass_bg"]} !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid {p["glass_border"]} !important;
    border-radius: var(--shade-radius) !important;
    box-shadow: 0 1px 4px {p["shadow"]} !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: {p["primary"]}40 !important;
    box-shadow: 0 4px 16px {p["shadow_lg"]} !important;
}}

/* ── Buttons ───────────────────────────────────────────────────── */

.stButton > button {{
    background-color: var(--shade-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--shade-radius-sm) !important;
    font-family: var(--shade-font) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}}

.stButton > button:hover {{
    background-color: var(--shade-primary-hover) !important;
    box-shadow: 0 4px 14px {p["primary_glow"]} !important;
    transform: translateY(-1px);
}}

.stButton > button:active {{
    transform: translateY(0) !important;
}}

.stButton > button:disabled {{
    background-color: var(--shade-border) !important;
    color: var(--shade-text-secondary) !important;
    opacity: 0.6 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}}

/* ── Metrics ───────────────────────────────────────────────────── */

[data-testid="stMetricValue"] {{
    color: var(--shade-primary) !important;
    font-family: var(--shade-font) !important;
    font-weight: 700 !important;
}}

[data-testid="stMetricLabel"] p {{
    color: var(--shade-text-secondary) !important;
}}

/* ── Code Blocks ───────────────────────────────────────────────── */

[data-testid="stCode"] {{
    background-color: var(--shade-code-bg) !important;
    border: 1px solid var(--shade-border) !important;
    border-radius: var(--shade-radius-sm) !important;
}}

[data-testid="stCode"] code {{
    color: var(--shade-text) !important;
}}

/* ── Inputs ────────────────────────────────────────────────────── */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {{
    background-color: var(--shade-input-bg) !important;
    color: var(--shade-text) !important;
    border: 1px solid var(--shade-border) !important;
    border-radius: var(--shade-radius-sm) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {{
    border-color: var(--shade-primary) !important;
    box-shadow: 0 0 0 3px {p["primary_glow"]} !important;
}}

.stSlider [data-testid="stThumbValue"] {{
    color: var(--shade-text) !important;
}}

/* ── Alerts ────────────────────────────────────────────────────── */

[data-testid="stAlert"] {{
    border-radius: var(--shade-radius-sm) !important;
}}

/* ── Expanders ─────────────────────────────────────────────────── */

[data-testid="stExpander"] {{
    background-color: var(--shade-surface) !important;
    border: 1px solid var(--shade-border) !important;
    border-radius: var(--shade-radius) !important;
}}

[data-testid="stExpander"] [data-testid="stExpanderToggleDetails"] {{
    color: var(--shade-text) !important;
}}

/* ── Dividers ──────────────────────────────────────────────────── */

hr {{
    border-color: var(--shade-border) !important;
    opacity: 0.6;
}}

/* ── Scrollbar ─────────────────────────────────────────────────── */

::-webkit-scrollbar {{
    width: 7px;
    height: 7px;
}}

::-webkit-scrollbar-track {{
    background: var(--shade-bg);
}}

::-webkit-scrollbar-thumb {{
    background: var(--shade-border);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--shade-text-secondary);
}}

/* ── Charts ────────────────────────────────────────────────────── */

[data-testid="stVegaLiteChart"] {{
    background-color: var(--shade-surface);
    border-radius: var(--shade-radius-sm);
    padding: 6px;
}}

[data-testid="stGraphVizChart"] {{
    background-color: var(--shade-surface);
    border-radius: var(--shade-radius-sm);
    padding: 8px;
}}

/* ── Images ────────────────────────────────────────────────────── */

[data-testid="stImage"] {{
    border-radius: var(--shade-radius-sm);
    overflow: hidden;
}}

/* ── Toggle widget text ────────────────────────────────────────── */

[data-testid="stToggle"] label span {{
    color: var(--shade-text) !important;
}}

/* ── Hide default Streamlit footer ─────────────────────────────── */

footer {{
    visibility: hidden !important;
}}
"""
