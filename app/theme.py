COLORS = {
    "bg_deep": "#FAF7F4",
    "bg_surface": "#F2EDE8",
    "bg_elevated": "#EAE2DA",
    "border_subtle": "#D4C4B8",
    "border_emphasis": "#B5A294",
    "text_primary": "#1A1311",
    "text_secondary": "#4A3C34",
    "text_muted": "#8A7B71",
    "accent_rose": "#B83860",
    "accent_amber": "#9A6018",
    "accent_amethyst": "#6B4E9B",
    "signal_stable": "#2E7A1A",
    "signal_watch": "#9A6018",
    "signal_acute": "#8B1A1A",
    "signal_lost": "#5A1010",
}

def news2_color(news2: int) -> str:
    if news2 <= 2:
        return COLORS["signal_stable"]
    elif news2 <= 4:
        return COLORS["signal_watch"]
    else:
        return COLORS["signal_acute"]

def kintsugi_css() -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Newsreader:ital,wght@0,400;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Newsreader', serif;
    background-color: {COLORS['bg_deep']};
    color: {COLORS['text_primary']};
}}

h1, h2, h3 {{
    font-family: 'Fraunces', serif;
    color: {COLORS['text_primary']};
}}

.stButton > button {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border_emphasis']};
    font-family: 'Fraunces', serif;
    transition: border-color 0.15s ease;
}}

.stButton > button:hover {{
    border-color: {COLORS['accent_rose']};
    color: {COLORS['accent_rose']};
}}

.news2-number {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 47px;
    font-weight: 500;
    line-height: 1;
}}

.vitals-strip {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: {COLORS['text_secondary']};
}}

.ambient-text {{
    font-family: 'Newsreader', serif;
    font-style: italic;
    font-size: 16px;
    color: {COLORS['text_primary']};
    padding: 12px;
    border-left: 3px solid {COLORS['accent_rose']};
    background-color: {COLORS['bg_elevated']};
    margin: 8px 0;
}}

.chart-entry {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {COLORS['text_secondary']};
}}

.patient-card {{
    background-color: {COLORS['bg_surface']};
    border: 1px solid {COLORS['border_subtle']};
    border-radius: 4px;
    padding: 16px;
    margin-bottom: 8px;
}}

.patient-card-focal {{
    border: 1px solid {COLORS['border_emphasis']};
}}

.signal-lost-highlight {{
    background-color: {COLORS['signal_lost']};
    color: {COLORS['text_primary']};
    padding: 2px 6px;
    border-radius: 2px;
}}

.handoff-panel {{
    background-color: {COLORS['bg_elevated']};
    border: 1px solid {COLORS['border_subtle']};
    border-radius: 4px;
    padding: 20px;
    height: 100%;
}}

.caption-thesis {{
    font-family: 'Fraunces', serif;
    font-size: 24px;
    text-align: center;
    color: {COLORS['accent_rose']};
    margin-top: 24px;
}}

.tool-call-row {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    padding: 4px 0;
    border-bottom: 1px solid {COLORS['border_subtle']};
}}

footer {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {COLORS['text_muted']};
}}
</style>
"""
