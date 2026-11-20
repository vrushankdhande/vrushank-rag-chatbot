"""Dashboard — live overview of the knowledge base, GitHub and Kaggle work."""
import streamlit as st

import insights
from profile_info import PROFILE, ROLES
from ui.cards import info_card, list_card, status_card
from ui.charts import career_timeline, ranked_bars
from ui.components import page_header, section_title

QUICK_ACTIONS = [
    (":material/work:", "Current role", "Which company is he currently working at and what does he do there?"),
    (":material/hub:", "AxiomLoop", "What is AxiomLoop and how does it work?"),
    (":material/dataset:", "Kaggle work", "What does he have on Kaggle?"),
    (":material/code:", "Latest projects", "What are his latest projects?"),
]


def _ask_in_chat(question: str) -> None:
    st.session_state.pending_question = question
    st.session_state.page = "chat"


def render() -> None:
    page_header("Dashboard", "Knowledge base", "at a glance",
                "Live view of everything the assistant knows: resume, GitHub projects and Kaggle datasets.")

    status = insights.service_status()
    kb = insights.knowledge_breakdown()
    repos = insights.github_repos()
    kaggle = insights.kaggle_datasets()

    # ---- KPIs ----
    c = st.columns(5)
    c[0].metric("Experience", f"{PROFILE['experience']} yrs")
    c[1].metric("Companies", len(ROLES))
    c[2].metric("GitHub repos", len(repos) if not repos.empty else "—")
    c[3].metric("Kaggle datasets", len(kaggle) if not kaggle.empty else "—")
    c[4].metric("KB chunks", int(kb["chunks"].sum()) if not kb.empty else "—",
                help="Text chunks in the MongoDB vector knowledge base")

    # ---- status ----
    section_title("System status", "🛰️")
    s = st.columns(3)
    with s[0]:
        status_card("MongoDB Atlas",
                    f"{status['docs']} documents · {status['mongo_ms']} ms ping" if status["mongo"] else "Unreachable",
                    "good" if status["mongo"] else "critical")
    with s[1]:
        status_card("Vector search index", "vector_index · 384-dim cosine" if status["index"] else "Not queryable",
                    "good" if status["index"] else ("warning" if status["mongo"] else "critical"))
    with s[2]:
        status_card("Groq LLM", "openai/gpt-oss-120b · key configured" if status["groq"] else "API key missing",
                    "good" if status["groq"] else "critical")

    # ---- quick actions ----
    section_title("Quick actions", "⚡")
    q = st.columns(len(QUICK_ACTIONS))
    for col, (icon, label, question) in zip(q, QUICK_ACTIONS):
        col.button(label, icon=icon, key=f"qa_{label}", on_click=_ask_in_chat, args=(question,),
                   width="stretch", help=question)

    st.write("")
    tab_overview, tab_github, tab_kaggle = st.tabs(
        [":material/insights: Overview", ":material/code: GitHub", ":material/dataset: Kaggle"]
    )

    with tab_overview:
        left, right = st.columns([1.05, 1])
        with left:
            with st.container(key="card_career"):
                section_title("Career timeline", "🧭")
                career_timeline(ROLES)
        with right:
            with st.container(key="card_kb"):
                section_title("What the assistant knows", "🧠")
                ranked_bars(kb, "source", "chunks", unit="chunks")
                with st.expander("View as table"):
                    st.dataframe(kb.sort_values("chunks", ascending=False), hide_index=True, width="stretch")

        a, b = st.columns(2)
        with a:
            section_title("Recently updated on GitHub", "🕒")
            recent = repos.head(5) if not repos.empty else repos
            list_card([(r["name"], r["language"]) for _, r in recent.iterrows()], "No repositories found.")
        with b:
            section_title("Your questions this session", "💬")
            convs = st.session_state.get("conversations", [])
            list_card([(cv["user"][:60], f"#{i + 1}") for i, cv in enumerate(convs[-5:])][::-1],
                      "No questions yet — try a quick action above.")

    with tab_github:
        if repos.empty:
            st.info("GitHub data is unavailable right now.")
        else:
            f1, f2 = st.columns([2, 1])
            query = f1.text_input("Search repositories", placeholder="e.g. agent, RAG, CNN…")
            langs = sorted(repos["language"].unique())
            chosen = f2.multiselect("Language", langs, placeholder="All languages")
            view = repos
            if query:
                mask = view["name"].str.contains(query, case=False) | view["description"].str.contains(query, case=False)
                view = view[mask]
            if chosen:
                view = view[view["language"].isin(chosen)]
            left, right = st.columns([1.6, 1])
            with left:
                st.dataframe(
                    view[["name", "url", "language", "description"]],
                    hide_index=True, width="stretch", height=420,
                    column_config={
                        "name": st.column_config.TextColumn("Repository", width="medium"),
                        "url": st.column_config.LinkColumn("Link", display_text="Open ↗", width="small"),
                        "language": st.column_config.TextColumn("Language", width="small"),
                        "description": st.column_config.TextColumn("Description", width="large"),
                    },
                )
                st.caption(f"Showing {len(view)} of {len(repos)} repositories · newest first")
            with right:
                with st.container(key="card_lang"):
                    section_title("Repositories by language", "📊")
                    by_lang = view.groupby("language", as_index=False).size().rename(columns={"size": "repos"})
                    ranked_bars(by_lang, "language", "repos", unit="repos")

    with tab_kaggle:
        if kaggle.empty:
            st.info("Kaggle data is unavailable right now.")
        else:
            st.caption("Public datasets scraped and published by Vrushank — India's live-events and music landscape.")
            cols = st.columns(2)
            for i, (_, d) in enumerate(kaggle.iterrows()):
                with cols[i % 2]:
                    info_card(d["name"], d["description"] or "Kaggle dataset.", "kaggle.com", d["url"])
                    st.write("")
