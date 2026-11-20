"""Design tokens: the single source of truth for colours, fonts and chart styling."""

COLORS = {
    # surfaces
    "bg": "#050816",            # page (deep navy-black)
    "bg_2": "#0a1022",
    "surface": "#0f1629",       # card / chart surface
    "glass": "rgba(15, 22, 41, 0.62)",
    "glass_strong": "rgba(15, 22, 41, 0.82)",
    "border": "rgba(148, 163, 255, 0.14)",
    "border_glow": "rgba(79, 140, 255, 0.45)",
    # ink
    "text": "#e8ecf8",
    "text_2": "#a9b3cf",
    "muted": "#6f7a99",
    # accents
    "blue": "#4f8cff",
    "purple": "#8b5cf6",
    "cyan": "#22d3ee",
    # status (always paired with an icon + label, never colour alone)
    "good": "#22c55e",
    "warning": "#fab219",
    "critical": "#ef4444",
}

GRADIENT = f"linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['purple']} 55%, {COLORS['cyan']} 100%)"

FONT_BODY = "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif"
FONT_DISPLAY = "'Poppins', 'Inter', system-ui, sans-serif"
GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
    "&family=Poppins:wght@500;600;700&display=swap"
)

# Chart tokens (validated with the dataviz palette validator against CHART["surface"]):
# a single accent hue for magnitude, and a recessive gray for de-emphasised marks
# (gray is sub-3:1 by design, so marks using it always carry visible text labels).
CHART = {
    "surface": COLORS["surface"],
    "accent": "#3987e5",
    "deemphasis": "#3b4457",
    "grid": "rgba(148, 163, 255, 0.08)",
    "axis": "#2a3350",
    "ink": COLORS["text"],
    "ink_2": COLORS["text_2"],
    "muted": COLORS["muted"],
}
