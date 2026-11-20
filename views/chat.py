"""AI Chat page — the original RAG chatbot behaviour, restyled."""
from html import escape

import streamlit as st

from profile_info import PROFILE
from ui.components import avatar, status_pill

SUGGESTIONS = [
    "Who is Vrushank Dhande?",
    "Which Company he worked?",
    "What work he did at Saregama India Limited?",
    "How many years of experience he has?",
    "List Github projects",
    "Explain vectorless-rag",
]


def init_state() -> None:
    defaults = {
        "conversations": [],
        "selected_chat": None,
        "asked_questions": set(),
        "show_suggestions_heading": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def ask(question: str, llm_response) -> None:
    """Run the RAG pipeline (with conversation memory) and store the turn."""
    st.session_state.asked_questions.add(question)
    st.session_state.show_suggestions_heading = False
    st.session_state.selected_chat = None

    with st.spinner("Searching the knowledge base and thinking…"):
        response = llm_response(question, history=st.session_state.conversations)

    st.session_state.conversations.append({"user": question, "assistant": response})
    st.rerun()


def _select_chat(i) -> None:
    st.session_state.selected_chat = i


def _clear_chat() -> None:
    st.session_state.conversations = []
    st.session_state.asked_questions = set()
    st.session_state.selected_chat = None
    st.session_state.show_suggestions_heading = True


def render_sidebar_history() -> None:
    with st.sidebar:
        st.markdown('<div class="nav-label">Chat history</div>', unsafe_allow_html=True)
        with st.container(key="history"):
            if not st.session_state.conversations:
                st.caption("Your questions will appear here.")
            for i, chat in enumerate(st.session_state.conversations):
                st.button(chat["user"][:50], key=f"history_{i}", icon=":material/chat_bubble:",
                          type="tertiary", on_click=_select_chat, args=(i,))
            if st.session_state.selected_chat is not None:
                st.button("⬅️ Show full chat", on_click=_select_chat, args=(None,), width="stretch")
        if st.session_state.conversations:
            st.button("🧹 Clear Chat", on_click=_clear_chat, width="stretch")


def _hero() -> None:
    st.markdown(
        f'<div class="hero">{avatar("vrushank_image.jpg", 76)}<div>'
        f'<div class="eyebrow">✦ AI assistant · retrieval-augmented</div>'
        f'<div class="page-title">Ask me anything about <span class="grad-text">{escape(PROFILE["name"])}</span></div>'
        f'<div class="page-sub">Experience, projects, GitHub repos and Kaggle work, answered from a '
        f'MongoDB vector knowledge base with Groq LLM reasoning.</div>'
        f'{status_pill("Knowledge base online", "good")}</div></div>',
        unsafe_allow_html=True,
    )


def render(llm_response) -> None:
    init_state()
    render_sidebar_history()

    if not st.session_state.conversations:
        _hero()
    else:
        st.markdown(
            f'<div class="eyebrow">✦ AI Chat</div>'
            f'<div class="page-title" style="font-size:1.6rem">Conversation with '
            f'<span class="grad-text">Vrushank AI</span></div>',
            unsafe_allow_html=True,
        )

    # ---- messages ----
    selected = st.session_state.selected_chat
    if selected is not None and selected < len(st.session_state.conversations):
        visible = [st.session_state.conversations[selected]]
    else:
        visible = st.session_state.conversations

    for chat in visible:
        with st.chat_message("user", avatar="🧑"):
            st.markdown(chat["user"])
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(chat["assistant"])

    # ---- suggestions ----
    remaining = [q for q in SUGGESTIONS if q not in st.session_state.asked_questions]
    if remaining:
        if st.session_state.show_suggestions_heading:
            st.markdown('<div class="section-title">💡 Suggested questions</div>', unsafe_allow_html=True)
        with st.container(key="suggestions"):
            cols = st.columns(3)
            for i, question in enumerate(remaining):
                # key from the question's fixed position, so it stays stable as the list shrinks
                if cols[i % 3].button(question, key=f"suggest_{SUGGESTIONS.index(question)}",
                                      icon=":material/auto_awesome:", width="stretch"):
                    ask(question, llm_response)

    # ---- question handed over from another page (dashboard quick actions) ----
    pending = st.session_state.pop("pending_question", None)
    if pending:
        ask(pending, llm_response)

    # ---- input ----
    prompt = st.chat_input("Ask about experience, projects, skills, Kaggle…")
    if prompt:
        ask(prompt, llm_response)
