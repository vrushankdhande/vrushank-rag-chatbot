"""Small reusable building blocks: page headers, section titles, status pills, chips."""
import base64
from html import escape
from pathlib import Path

import streamlit as st


def page_header(eyebrow: str, title: str, highlight: str = "", subtitle: str = "") -> None:
    """Big gradient page header. `highlight` is appended to the title in gradient text."""
    hl = f' <span class="grad-text">{escape(highlight)}</span>' if highlight else ""
    sub = f'<div class="page-sub">{escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f'<div class="eyebrow">✦ {escape(eyebrow)}</div>'
        f'<div class="page-title">{escape(title)}{hl}</div>{sub}',
        unsafe_allow_html=True,
    )


def section_title(text: str, icon: str = "") -> None:
    st.markdown(f'<div class="section-title">{icon} {escape(text)}</div>', unsafe_allow_html=True)


def status_pill(label: str, state: str = "good") -> str:
    """HTML for a status pill. state: good | warning | critical (dot + text, never colour alone)."""
    return f'<span class="pill"><span class="dot {state}"></span>{escape(label)}</span>'


def chips(items: list[str]) -> None:
    st.markdown(
        '<div class="chips">' + "".join(f'<span class="chip">{escape(i)}</span>' for i in items) + "</div>",
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def image_data_uri(path: str) -> str:
    """Inline an image as a data URI (cached) so it can be used inside custom HTML."""
    p = Path(path)
    if not p.exists():
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def avatar(path: str, size: int = 56) -> str:
    uri = image_data_uri(path)
    if not uri:
        return ""
    return (
        f'<span class="avatar-ring"><img class="avatar" src="{uri}" '
        f'width="{size}" height="{size}" alt="Vrushank Dhande"></span>'
    )
