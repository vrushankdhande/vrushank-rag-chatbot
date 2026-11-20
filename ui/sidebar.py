"""Branded sidebar with navigation (active highlight) and a profile section."""
from html import escape

import streamlit as st

from profile_info import PROFILE
from ui.components import avatar

PAGES = {  # key -> (icon, label)
    "chat": (":material/forum:", "AI Chat"),
    "dashboard": (":material/space_dashboard:", "Dashboard"),
    "about": (":material/person:", "About Vrushank"),
}


def _go(page: str) -> None:
    st.session_state.page = page  # on_click callback: no extra st.rerun() needed


def render_sidebar() -> str:
    """Render brand + nav + profile. Returns the active page key.
    Page-specific sidebar content can be added after calling this."""
    st.session_state.setdefault("page", "chat")
    with st.sidebar:
        st.markdown(
            '<div class="brand"><div class="logo">VD</div><div>'
            '<div class="name">Vrushank AI</div><div class="tag">RAG assistant · Groq + MongoDB</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="nav-label">Navigate</div>', unsafe_allow_html=True)
        with st.container(key="nav"):
            for key, (icon, label) in PAGES.items():
                st.button(
                    label, icon=icon, key=f"nav_{key}",
                    type="primary" if st.session_state.page == key else "secondary",
                    on_click=_go, args=(key,), width="stretch",
                )
        st.markdown(
            f'<div class="profile">{avatar("vrushank_image.jpg", 40)}<div>'
            f'<div class="who">{escape(PROFILE["name"])}</div>'
            f'<div class="role">{escape(PROFILE["title"])} · {escape(PROFILE["location"])}</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )
    return st.session_state.page
