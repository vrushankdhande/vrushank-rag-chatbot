"""Card components: glass info cards, status cards, list cards."""
from html import escape

import streamlit as st


def info_card(title: str, body: str, meta: str = "", link: str = "") -> None:
    """Glass card with title, body text, optional meta line and link (all escaped)."""
    t = escape(title)
    if link:
        t = f'<a href="{escape(link, quote=True)}" target="_blank" rel="noopener">{t} ↗</a>'
    m = f'<div class="meta">{escape(meta)}</div>' if meta else ""
    st.markdown(f'<div class="glass"><h4>{t}</h4><p>{escape(body)}</p>{m}</div>', unsafe_allow_html=True)


def status_card(label: str, detail: str, state: str) -> None:
    """Service status: coloured dot + label + text state, so meaning never relies on colour."""
    word = {"good": "Operational", "warning": "Degraded", "critical": "Down"}[state]
    st.markdown(
        f'<div class="glass status-card"><span class="dot {state}"></span>'
        f'<div><div class="label">{escape(label)} · {word}</div>'
        f'<div class="detail">{escape(detail)}</div></div></div>',
        unsafe_allow_html=True,
    )


def list_card(rows: list[tuple[str, str]], empty: str = "Nothing yet.") -> None:
    """A glass card of key/value rows (e.g. recent activity)."""
    if not rows:
        body = f'<p>{escape(empty)}</p>'
    else:
        body = "".join(
            f'<div class="list-row"><span class="k">{escape(k)}</span><span class="v">{escape(v)}</span></div>'
            for k, v in rows
        )
    st.markdown(f'<div class="glass">{body}</div>', unsafe_allow_html=True)
