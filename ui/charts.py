"""Plotly chart builders that follow the design system.

Rules applied (dataviz method): ranked horizontal bars in ONE hue for magnitude /
part-to-whole (no donuts); emphasis = accent + recessive gray with visible labels;
recessive grid; hover tooltips on every mark; no dual axes; transparent background
so charts sit on the glass card surface.
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.theme import CHART, FONT_BODY

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}


def _base_layout(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=24, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_BODY, color=CHART["ink_2"], size=12),
        hoverlabel=dict(bgcolor=CHART["surface"], bordercolor=CHART["accent"],
                        font=dict(family=FONT_BODY, color=CHART["ink"], size=12)),
        showlegend=False,
        bargap=0.35,
    )
    fig.update_xaxes(gridcolor=CHART["grid"], zeroline=False, linecolor=CHART["axis"],
                     tickfont=dict(color=CHART["muted"]))
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor=CHART["axis"],
                     tickfont=dict(color=CHART["ink_2"]))
    return fig


def ranked_bars(df: pd.DataFrame, label: str, value: str, unit: str = "") -> None:
    """Ranked horizontal bars, largest on top, single accent hue, value at bar end."""
    if df.empty:
        st.caption("No data available.")
        return
    d = df.sort_values(value, ascending=True)
    fig = go.Figure(go.Bar(
        x=d[value], y=d[label], orientation="h",
        marker=dict(color=CHART["accent"], cornerradius=4, line=dict(width=0)),
        text=d[value], textposition="outside", textfont=dict(color=CHART["ink"]),
        hovertemplate=f"<b>%{{y}}</b><br>%{{x}} {unit}<extra></extra>",
        cliponaxis=False,
    ))
    _base_layout(fig, height=max(180, 46 * len(d) + 30))
    fig.update_xaxes(showgrid=True, showticklabels=False)
    st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")


def career_timeline(roles: list[dict]) -> None:
    """Gantt-style timeline; the current role is emphasised, past roles recessive gray.
    Every bar carries a visible text label (the gray is intentionally low-contrast)."""
    rows = []
    for r in roles:
        rows.append(dict(company=r["company"], role=r["role"], start=pd.Timestamp(r["start"]),
                         end=pd.Timestamp(r["end"]) if r["end"] else pd.Timestamp.today().normalize(),
                         current=r["end"] is None, period=r["period"]))
    df = pd.DataFrame(rows).sort_values("start", ascending=False)
    fig = go.Figure()
    for _, r in df.iterrows():
        dur_ms = (r["end"] - r["start"]).total_seconds() * 1000
        # Label lives on the axis (company + role + period), so it is always visible and
        # never clipped at the plot edge — the low-contrast gray bars rely on it.
        label = (f"<b>{r['company']}</b><br><span style='font-size:11px'>"
                 f"{r['role']} · {r['period']}</span>")
        fig.add_trace(go.Bar(
            x=[dur_ms], base=[r["start"]], y=[label], orientation="h",
            marker=dict(color=CHART["accent"] if r["current"] else CHART["deemphasis"],
                        cornerradius=4, line=dict(width=0)),
            hovertemplate=f"<b>{r['company']}</b><br>{r['role']}<br>{r['period']}<extra></extra>",
        ))
    _base_layout(fig, height=72 * len(df) + 50)
    fig.update_layout(bargap=0.45)
    fig.update_xaxes(type="date", showgrid=True, tickformat="%Y",
                     range=[df["start"].min() - pd.DateOffset(months=3),
                            df["end"].max() + pd.DateOffset(months=3)])
    fig.update_yaxes(autorange="reversed", ticklabelstandoff=10)
    st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
