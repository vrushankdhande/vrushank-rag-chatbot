"""About page — profile, experience, skills, education, links."""
from html import escape

import streamlit as st

from profile_info import EDUCATION, PROFILE, ROLES, SKILLS, SPOKEN_LANGUAGES
from ui.cards import list_card
from ui.components import avatar, chips, section_title, status_pill


def render() -> None:
    st.markdown(
        f'<div class="hero">{avatar("vrushank_image.jpg", 96)}<div>'
        f'<div class="eyebrow">✦ About</div>'
        f'<div class="page-title"><span class="grad-text">{escape(PROFILE["name"])}</span></div>'
        f'<div class="page-sub">{escape(PROFILE["title"])} · {escape(PROFILE["location"])}<br>'
        f'{escape(PROFILE["summary"])}</div>'
        f'{status_pill("Currently at ERGOBITE Tech Solutions", "good")}</div></div>',
        unsafe_allow_html=True,
    )

    links = st.columns(len(PROFILE["links"]))
    for col, (name, url) in zip(links, PROFILE["links"].items()):
        col.link_button(name, url, icon=":material/open_in_new:", width="stretch")

    left, right = st.columns([1.5, 1])
    with left:
        section_title("Experience", "💼")
        for i, r in enumerate(ROLES):
            current = " · current" if r["end"] is None else ""
            with st.expander(f"{r['role']} — {r['company']}  ·  {r['period']}{current}", expanded=i == 0):
                st.caption(r["location"])
                st.markdown("\n".join(f"- {h}" for h in r["highlights"]))

    with right:
        section_title("Skills", "🛠️")
        with st.container(key="card_skills"):
            for group, items in SKILLS.items():
                st.markdown(f"**{group}**")
                chips(items)
                st.write("")
        section_title("Education", "🎓")
        list_card(EDUCATION)
        section_title("Languages", "🌐")
        chips(SPOKEN_LANGUAGES)
