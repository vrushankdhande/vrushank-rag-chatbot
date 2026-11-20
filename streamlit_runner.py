import streamlit as st

# ---------------- PAGE CONFIG ----------------
# Must be the first Streamlit call, so it runs before personal_code is imported
# (that module may call st.error/st.stop if secrets are missing).
st.set_page_config(
    page_title="Vrushank AI · RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",  # expanded on desktop, collapsed on phones
)

from personal_code import llm_response  # noqa: E402
from ui.animations import render_background  # noqa: E402
from ui.sidebar import render_sidebar  # noqa: E402
from ui.styles import inject_global_css  # noqa: E402
from views import about, chat, dashboard  # noqa: E402

# ---------------- DESIGN SYSTEM ----------------
inject_global_css()
render_background()

# ---------------- NAVIGATION ----------------
page = render_sidebar()

if page == "dashboard":
    dashboard.render()
elif page == "about":
    about.render()
else:
    chat.render(llm_response)
