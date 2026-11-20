"""Global CSS: one design system applied to every Streamlit widget."""
import streamlit as st

from ui.theme import COLORS as C
from ui.theme import FONT_BODY, FONT_DISPLAY, GOOGLE_FONTS, GRADIENT


def _css() -> str:
    return f"""
<style>
@import url('{GOOGLE_FONTS}');

:root {{
  --bg: {C['bg']}; --surface: {C['surface']};
  --glass: {C['glass']}; --glass-strong: {C['glass_strong']};
  --border: {C['border']}; --border-glow: {C['border_glow']};
  --text: {C['text']}; --text-2: {C['text_2']}; --muted: {C['muted']};
  --blue: {C['blue']}; --purple: {C['purple']}; --cyan: {C['cyan']};
  --good: {C['good']}; --warning: {C['warning']}; --critical: {C['critical']};
  --gradient: {GRADIENT};
  --radius: 16px; --radius-sm: 12px;
  --shadow: 0 10px 40px rgba(2, 6, 23, 0.55);
  --glow: 0 0 0 1px var(--border-glow), 0 0 24px rgba(79, 140, 255, 0.25);
  --ease: cubic-bezier(.2, .8, .2, 1);
}}

/* ---------- base ---------- */
/* Background lives on body (gradient fallback) + the animated canvas (z-index -1);
   the app containers are transparent so both show through. */
html {{ background: var(--bg); }}
body {{
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(79,140,255,.16), transparent 60%),
    radial-gradient(900px 500px at 110% 10%, rgba(139,92,246,.14), transparent 60%),
    radial-gradient(800px 600px at 50% 120%, rgba(34,211,238,.10), transparent 60%),
    var(--bg) !important;
  background-attachment: fixed !important;
}}
.stApp {{
  background: transparent !important;
  color: var(--text);
  font-family: {FONT_BODY};
}}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background: transparent !important; }}
[data-testid="stHeader"] {{ background: rgba(5,8,22,.55) !important; backdrop-filter: blur(14px); }}
[data-testid="stAppDeployButton"] {{ display: none; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 2.2rem; padding-bottom: 7rem; max-width: 1180px; }}
h1, h2, h3, h4 {{ font-family: {FONT_DISPLAY}; color: var(--text); letter-spacing: -0.01em; }}
p, li, label, span, div {{ font-family: {FONT_BODY}; }}
a {{ color: var(--cyan) !important; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
[data-testid="stCaptionContainer"] {{ color: var(--muted) !important; }}
::selection {{ background: rgba(79,140,255,.35); }}
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-thumb {{ background: rgba(148,163,255,.18); border-radius: 10px; }}
::-webkit-scrollbar-track {{ background: transparent; }}

/* entrance animation for content blocks */
[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"] {{
  animation: fadeUp .45s var(--ease) both;
}}
@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, rgba(5,8,22,.92), rgba(10,16,34,.92)) !important;
  backdrop-filter: blur(18px);
  border-right: 1px solid var(--border);
}}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{ padding-top: .5rem; }}
.st-key-nav [data-testid="stButton"] button {{
  width: 100%; justify-content: flex-start; text-align: left;
  border-radius: var(--radius-sm); padding: .62rem .9rem; margin: 2px 0;
  background: transparent; border: 1px solid transparent; color: var(--text-2);
  transition: all .25s var(--ease);
}}
.st-key-nav [data-testid="stButton"] button > div,
.st-key-history [data-testid="stButton"] button > div,
.st-key-suggestions [data-testid="stButton"] button > div {{ justify-content: flex-start; width: 100%; }}
.st-key-nav [data-testid="stButton"] button:hover {{
  background: rgba(79,140,255,.08); border-color: var(--border); color: var(--text);
  transform: translateX(3px);
}}
.st-key-nav [data-testid="stBaseButton-primary"] {{
  background: linear-gradient(90deg, rgba(79,140,255,.22), rgba(139,92,246,.14)) !important;
  border: 1px solid var(--border-glow) !important; color: var(--text) !important;
  box-shadow: inset 3px 0 0 var(--cyan), 0 0 18px rgba(79,140,255,.18);
}}
.st-key-history [data-testid="stButton"] button {{
  width: 100%; justify-content: flex-start; text-align: left; font-size: .85rem;
  padding: .45rem .75rem; color: var(--text-2);
}}

/* ---------- buttons ---------- */
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button, [data-testid="stLinkButton"] a {{
  font-family: {FONT_BODY}; font-weight: 500; border-radius: var(--radius-sm);
  transition: transform .2s var(--ease), box-shadow .25s var(--ease), border-color .25s, background .25s;
}}
[data-testid="stBaseButton-secondary"], [data-testid="stLinkButton"] a {{
  background: var(--glass) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; backdrop-filter: blur(10px);
}}
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stLinkButton"] a:hover {{
  border-color: var(--border-glow) !important; box-shadow: var(--glow); transform: translateY(-2px);
  text-decoration: none;
}}
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {{
  background: var(--gradient) !important; color: #fff !important; border: 0 !important;
  box-shadow: 0 6px 24px rgba(79,140,255,.35);
}}
[data-testid="stBaseButton-primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 10px 32px rgba(139,92,246,.45); }}
[data-testid="stBaseButton-tertiary"] {{ color: var(--text-2) !important; }}
[data-testid="stBaseButton-tertiary"]:hover {{ color: var(--cyan) !important; }}
button:focus-visible, a:focus-visible {{ outline: 2px solid var(--cyan) !important; outline-offset: 2px; }}

/* suggestion chips */
.st-key-suggestions [data-testid="stButton"] button {{
  width: 100%; min-height: 3.1rem; border-radius: 14px; font-size: .9rem; text-align: left;
  justify-content: flex-start; color: var(--text-2) !important;
}}
.st-key-suggestions [data-testid="stButton"] button:hover {{ color: var(--text) !important; }}

/* ---------- inputs ---------- */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-baseweb="select"] > div, [data-testid="stFileUploaderDropzone"] {{
  background: var(--glass-strong) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important;
  transition: border-color .2s, box-shadow .2s;
}}
[data-testid="stTextInput"] [data-baseweb="input"], [data-testid="stTextArea"] [data-baseweb="textarea"] {{
  background: transparent !important; border: 0 !important;
}}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus,
[data-baseweb="select"] > div:focus-within {{
  border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(79,140,255,.22) !important;
}}
[data-baseweb="tag"] {{ background: rgba(79,140,255,.18) !important; border: 1px solid var(--border-glow); border-radius: 8px !important; }}
[data-baseweb="tag"] span {{ color: var(--text) !important; }}
[data-baseweb="popover"] ul, [data-baseweb="menu"] {{ background: var(--surface) !important; border: 1px solid var(--border); }}
[data-testid="stFileUploaderDropzone"] {{ border-style: dashed !important; }}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: var(--blue) !important; box-shadow: var(--glow); }}
[data-testid="stWidgetLabel"] p {{ color: var(--text-2) !important; font-weight: 500; font-size: .85rem; }}

/* chat input */
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {{ background: transparent !important; }}
[data-testid="stBottom"] {{ background: linear-gradient(180deg, transparent, rgba(5,8,22,.9) 45%) !important; }}
[data-testid="stChatInput"] {{
  background: var(--glass-strong) !important; border: 1px solid var(--border-glow) !important;
  border-radius: 18px !important; backdrop-filter: blur(16px);
  box-shadow: 0 0 0 1px rgba(79,140,255,.12), 0 8px 40px rgba(79,140,255,.18);
}}
[data-testid="stChatInput"]:focus-within {{ box-shadow: 0 0 0 3px rgba(79,140,255,.25), 0 8px 48px rgba(139,92,246,.25); }}
[data-testid="stChatInputTextArea"] {{ color: var(--text) !important; background: transparent !important; }}
[data-testid="stChatInput"] button {{ background: var(--gradient) !important; border-radius: 12px !important; }}

/* ---------- chat messages ---------- */
div[data-testid="stChatMessage"] {{
  background: var(--glass) !important; border: 1px solid var(--border);
  border-radius: 18px; padding: 1rem 1.1rem !important; margin-bottom: .9rem;
  max-width: 82%; margin-right: auto; backdrop-filter: blur(12px); box-shadow: var(--shadow);
  animation: fadeUp .35s var(--ease) both;
}}
div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {{
  background: linear-gradient(135deg, rgba(79,140,255,.9), rgba(139,92,246,.85)) !important;
  border: 0; margin-left: auto; margin-right: 0; max-width: 70%;
}}
div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) * {{ color: #fff !important; }}
div[data-testid="stChatMessage"] table {{ font-size: .85rem; }}

/* ---------- tabs ---------- */
[data-testid="stTabs"] [role="tablist"] {{
  gap: .35rem; border-bottom: 1px solid var(--border); padding-bottom: 2px;
}}
[data-testid="stTab"] {{
  background: transparent; border-radius: 10px 10px 0 0; padding: .55rem 1rem !important;
  color: var(--text-2); transition: color .2s, background .2s;
}}
[data-testid="stTab"]:hover {{ color: var(--text); background: rgba(79,140,255,.06); }}
[data-testid="stTab"][aria-selected="true"] {{ color: var(--text); }}
[data-baseweb="tab-highlight"] {{ background: var(--gradient) !important; height: 3px !important; border-radius: 3px; }}
[data-baseweb="tab-border"] {{ display: none; }}

/* ---------- expander / form / containers ---------- */
[data-testid="stExpander"] details, [data-testid="stForm"] {{
  background: var(--glass) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; backdrop-filter: blur(12px);
  transition: border-color .25s, box-shadow .25s;
}}
[data-testid="stExpander"] details:hover {{ border-color: var(--border-glow) !important; }}
[data-testid="stExpander"] summary {{ color: var(--text) !important; font-weight: 600; }}
.st-key-card, [class*="st-key-card_"] {{
  background: var(--glass); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1.1rem 1.2rem 1rem; backdrop-filter: blur(12px); box-shadow: var(--shadow);
  transition: border-color .25s, box-shadow .25s;
}}
.st-key-card:hover, [class*="st-key-card_"]:hover {{ border-color: var(--border-glow); }}

/* ---------- metrics ---------- */
[data-testid="stMetric"] {{
  background: var(--glass); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1rem 1.1rem; backdrop-filter: blur(12px); position: relative; overflow: hidden;
  transition: transform .25s var(--ease), border-color .25s, box-shadow .25s;
}}
[data-testid="stMetric"]::before {{
  content: ""; position: absolute; inset: 0 0 auto 0; height: 2px; background: var(--gradient);
}}
[data-testid="stMetric"]:hover {{ transform: translateY(-3px); border-color: var(--border-glow); box-shadow: var(--glow); }}
[data-testid="stMetricLabel"] p {{ color: var(--text-2) !important; font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; }}
[data-testid="stMetricValue"] {{ font-family: {FONT_DISPLAY}; color: var(--text) !important; font-weight: 600; }}
[data-testid="stMetricDelta"] {{ color: var(--cyan) !important; }}

/* ---------- progress / dataframe / alerts / plotly ---------- */
[data-testid="stProgress"] > div > div > div {{ background: rgba(148,163,255,.12) !important; border-radius: 99px; }}
[data-testid="stProgress"] > div > div > div > div {{ background: var(--gradient) !important; border-radius: 99px; }}
[data-testid="stDataFrame"] {{ border: 1px solid var(--border); border-radius: var(--radius-sm); overflow: hidden; }}
[data-testid="stAlertContainer"] {{ background: var(--glass) !important; border: 1px solid var(--border); border-radius: var(--radius-sm); }}
[data-testid="stPlotlyChart"] {{ border-radius: var(--radius-sm); }}
[data-testid="stSpinner"] {{ color: var(--text-2); }}

/* ---------- custom components (ui/components.py, ui/cards.py) ---------- */
.eyebrow {{ display: inline-flex; align-items: center; gap: .45rem; font-size: .75rem; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase; color: var(--cyan); }}
.page-title {{ font-family: {FONT_DISPLAY}; font-size: clamp(1.8rem, 3.2vw, 2.6rem); font-weight: 700;
  line-height: 1.15; margin: .35rem 0 .4rem; color: var(--text); }}
.grad-text {{ background: var(--gradient); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.page-sub {{ color: var(--text-2); font-size: 1.02rem; max-width: 760px; margin-bottom: 1.2rem; }}
.section-title {{ font-family: {FONT_DISPLAY}; font-size: 1.05rem; font-weight: 600; color: var(--text);
  margin: 1.4rem 0 .7rem; display: flex; align-items: center; gap: .5rem; }}
.section-title::after {{ content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, var(--border), transparent); }}
.pill {{ display: inline-flex; align-items: center; gap: .4rem; padding: .28rem .7rem; border-radius: 99px;
  font-size: .78rem; font-weight: 500; background: var(--glass); border: 1px solid var(--border); color: var(--text-2); }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}
.dot.good {{ background: var(--good); box-shadow: 0 0 10px var(--good); animation: pulse 2s infinite; }}
.dot.warning {{ background: var(--warning); box-shadow: 0 0 10px var(--warning); }}
.dot.critical {{ background: var(--critical); box-shadow: 0 0 10px var(--critical); }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .45; }} }}
.chips {{ display: flex; flex-wrap: wrap; gap: .45rem; }}
.chip {{ padding: .3rem .7rem; border-radius: 99px; font-size: .8rem; color: var(--text-2);
  background: rgba(79,140,255,.08); border: 1px solid var(--border); transition: all .2s; }}
.chip:hover {{ color: var(--text); border-color: var(--border-glow); }}
.glass {{ background: var(--glass); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1.1rem 1.2rem; backdrop-filter: blur(12px); box-shadow: var(--shadow);
  transition: transform .25s var(--ease), border-color .25s, box-shadow .25s; height: 100%; }}
.glass:hover {{ transform: translateY(-3px); border-color: var(--border-glow); box-shadow: var(--glow); }}
.glass h4 {{ margin: 0 0 .35rem; font-size: 1rem; }}
.glass p {{ margin: 0; color: var(--text-2); font-size: .88rem; line-height: 1.5; }}
.glass .meta {{ color: var(--muted); font-size: .78rem; margin-top: .6rem; }}
.status-card {{ display: flex; align-items: center; gap: .8rem; }}
.status-card .label {{ color: var(--text); font-weight: 600; font-size: .92rem; }}
.status-card .detail {{ color: var(--muted); font-size: .8rem; }}
.brand {{ display: flex; align-items: center; gap: .7rem; padding: .2rem .2rem 1rem; }}
.brand .logo {{ width: 38px; height: 38px; border-radius: 12px; background: var(--gradient);
  display: grid; place-items: center; font-family: {FONT_DISPLAY}; font-weight: 700; color: #fff;
  box-shadow: 0 0 22px rgba(79,140,255,.45); }}
.brand .name {{ font-family: {FONT_DISPLAY}; font-weight: 600; color: var(--text); line-height: 1.1; }}
.brand .tag {{ font-size: .72rem; color: var(--muted); }}
.nav-label {{ font-size: .7rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
  margin: .9rem 0 .35rem .3rem; }}
.profile {{ display: flex; align-items: center; gap: .75rem; padding: .8rem; border-radius: var(--radius-sm);
  background: var(--glass); border: 1px solid var(--border); margin-top: .6rem; }}
.avatar {{ border-radius: 50%; object-fit: cover; border: 2px solid transparent;
  background: var(--gradient) border-box; }}
.avatar-ring {{ padding: 3px; border-radius: 50%; background: var(--gradient); display: inline-flex;
  box-shadow: 0 0 28px rgba(79,140,255,.45); }}
.profile .who {{ font-weight: 600; color: var(--text); font-size: .9rem; }}
.profile .role {{ font-size: .75rem; color: var(--muted); }}
.hero {{ display: flex; align-items: center; gap: 1.3rem; margin-bottom: .6rem; }}
.list-row {{ display: flex; justify-content: space-between; gap: 1rem; padding: .55rem 0;
  border-bottom: 1px solid var(--border); font-size: .88rem; }}
.list-row:last-child {{ border-bottom: 0; }}
.list-row .k {{ color: var(--text); }}
.list-row .v {{ color: var(--muted); white-space: nowrap; }}

/* ---------- responsive & motion preferences ---------- */
@media (max-width: 768px) {{
  [data-testid="stMainBlockContainer"] {{ padding-left: 1rem; padding-right: 1rem; }}
  div[data-testid="stChatMessage"], div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {{ max-width: 100%; }}
  .hero {{ flex-direction: column; align-items: flex-start; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation: none !important; transition: none !important; }}
}}
</style>
"""


def inject_global_css() -> None:
    """Apply the design system. Call once per run, before rendering content."""
    st.markdown(_css(), unsafe_allow_html=True)
