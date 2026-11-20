"""Read-only, cached queries over the knowledge base for the dashboard.
Every function degrades gracefully (empty result) if MongoDB is unreachable."""
import re
import time

import pandas as pd
import streamlit as st

from personal_code import GROQ_API_KEY, get_collection

SOURCE_LABELS = {
    "resume_2026": "Resume",
    "github_readme": "Project READMEs",
    "github_repos": "GitHub repo catalog",
    "github_portfolio": "Project portfolio (older)",
    "kaggle": "Kaggle datasets",
}

_REPO_LINE = re.compile(
    r"^- (?P<name>\S+) \((?P<url>https://github\.com/[^)]+)\): (?P<desc>.*?)(?: Language: (?P<lang>[^.]+)\.)?$"
)
_KAGGLE_LINE = re.compile(r"^- (?P<name>.+?): (?P<url>https://www\.kaggle\.com/datasets/\S+)$")


@st.cache_data(ttl=600, show_spinner=False)
def knowledge_breakdown() -> pd.DataFrame:
    """Number of knowledge chunks per source."""
    try:
        rows = list(get_collection().aggregate([{"$group": {"_id": "$source", "n": {"$sum": 1}}}]))
    except Exception:  # noqa: BLE001
        return pd.DataFrame(columns=["source", "chunks"])
    return pd.DataFrame(
        [{"source": SOURCE_LABELS.get(r["_id"], "Other"), "chunks": r["n"]} for r in rows]
    ).groupby("source", as_index=False)["chunks"].sum()


@st.cache_data(ttl=600, show_spinner=False)
def github_repos() -> pd.DataFrame:
    """All public repos (name, url, description, language, recency rank) parsed from the catalog."""
    try:
        docs = list(get_collection().find({"source": "github_repos"}, {"_id": 1, "text": 1}).sort("_id", 1))
    except Exception:  # noqa: BLE001
        return pd.DataFrame(columns=["name", "url", "description", "language", "recency"])
    repos, order = {}, []
    for d in docs:
        text = d["text"]
        if "complete list of all" in text:
            # recency index (may span several chunks, inserted in order): names, newest first,
            # separated by commas or newlines
            body = text.split("\n", 1)[1] if "\n" in text else ""
            order += [n.strip() for n in re.split(r"[,\n]", body) if n.strip()]
            continue
        for line in text.splitlines():
            m = _REPO_LINE.match(line.strip())
            if m:
                repos[m["name"]] = {
                    "name": m["name"], "url": m["url"],
                    "description": "" if m["desc"] == "No description." else m["desc"],
                    "language": (m["lang"] or "Not specified").strip(),
                }
    rank = {n: i for i, n in enumerate(order)}
    df = pd.DataFrame(repos.values())
    if df.empty:
        return df
    df["recency"] = df["name"].map(rank).fillna(len(rank)).astype(int)
    return df.sort_values("recency").reset_index(drop=True)


@st.cache_data(ttl=600, show_spinner=False)
def kaggle_datasets() -> pd.DataFrame:
    """Public Kaggle datasets (name, url, description) from the kaggle chunks."""
    try:
        docs = list(get_collection().find({"source": "kaggle"}, {"_id": 0, "text": 1}))
    except Exception:  # noqa: BLE001
        return pd.DataFrame(columns=["name", "url", "description"])
    found, details = {}, {}
    for d in docs:
        lines = d["text"].splitlines()
        for line in lines:
            m = _KAGGLE_LINE.match(line.strip())
            if m:
                found[m["url"]] = re.sub(r"\s*\([^)]*\)$", "", m["name"])  # drop "(most downloaded)" etc.
        head = re.match(r"^Vrushank Dhande Kaggle dataset: .+? \((https://[^)]+)\)$", lines[0])
        if head and len(lines) > 1:
            desc = lines[1].strip()
            if desc.endswith(":") and len(lines) > 2:  # e.g. "Two files:" -> include the first item
                desc += " " + lines[2].strip().lstrip("- ")
            details[head[1]] = desc if len(desc) <= 320 else desc[:317].rsplit(" ", 1)[0] + "…"
    return pd.DataFrame(
        [{"name": n, "url": u, "description": details.get(u, "")} for u, n in found.items()]
    )


@st.cache_data(ttl=60, show_spinner=False)
def service_status() -> dict:
    """Live health of the backing services (cached for a minute)."""
    status = {"groq": bool(GROQ_API_KEY)}
    try:
        coll = get_collection()
        t0 = time.perf_counter()
        coll.database.client.admin.command("ping")
        status["mongo_ms"] = round((time.perf_counter() - t0) * 1000)
        status["mongo"] = True
        idx = [i for i in coll.list_search_indexes() if i.get("name") == "vector_index"]
        status["index"] = bool(idx and idx[0].get("queryable"))
        status["docs"] = coll.estimated_document_count()
    except Exception:  # noqa: BLE001
        status.update(mongo=False, index=False, docs=0, mongo_ms=None)
    return status
