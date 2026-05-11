"""
component_tab.py — Component Intelligence tab for the UAS THREATMAP dashboard
==============================================================================
PURPOSE: Compliance, sanctions, export-control, and OSINT risk analysis only.

Renders the full "Component Intelligence" tab. Call render_component_tab()
from app.py to embed this view into the main Streamlit tab layout.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

from data.component_data import (
    get_component_intelligence,
    get_region_component_matrix,
    get_red_flag_table,
    SENSITIVITY_COLOR,
    SENSITIVITY_ORDER,
    CATEGORY_ICON,
)

# ── Colour / label helpers ────────────────────────────────────────────────────
RISK_BADGE = {
    10: ("badge-crit",  "CRITICAL"),
    9:  ("badge-crit",  "CRITICAL"),
    8:  ("badge-high",  "HIGH"),
    7:  ("badge-high",  "HIGH"),
    6:  ("badge-mod",   "ELEVATED"),
    5:  ("badge-mod",   "MODERATE"),
    4:  ("badge-low",   "LOW"),
    3:  ("badge-low",   "LOW"),
    2:  ("badge-low",   "LOW"),
    1:  ("badge-low",   "LOW"),
    0:  ("badge-low",   "LOW"),
}

CONF_BADGE = {
    "High":       "badge-hi-conf",
    "Medium":     "badge-med-conf",
    "Low":        "badge-lo-conf",
    "Unverified": "badge-unver",
}

SENS_BADGE = {
    "Common civilian":    "badge-low",
    "Dual-use":           "badge-mod",
    "Sensitive dual-use": "badge-high",
    "Military-adjacent":  "badge-crit",
}

PLOTLY_BASE = dict(
    paper_bgcolor="#0d0f15",
    plot_bgcolor="#0d0f15",
    font_family="IBM Plex Mono",
    margin=dict(t=20, b=10, l=0, r=0),
)

CHART_COLORS = ["#e8503a", "#f07c2a", "#f0c040", "#3ab87a", "#4a90d9", "#9b6dff"]


def _badge(text: str, css_class: str) -> str:
    return f"<span class='badge {css_class}'>{text}</span>"


def _sens_badge(level: str) -> str:
    return _badge(level.upper(), SENS_BADGE.get(level, "badge-unver"))


def _risk_badge(score: int) -> str:
    cls, label = RISK_BADGE.get(min(score, 10), ("badge-low", "LOW"))
    return f"<span class='badge {cls}'>{label} ({score}/10)</span>"


def _conf_badge(c: str) -> str:
    return _badge(c, CONF_BADGE.get(c, "badge-unver"))


def _section(title: str) -> None:
    st.markdown(
        f"<div class='section-title'>{title}</div>",
        unsafe_allow_html=True,
    )


# ── Main render function ──────────────────────────────────────────────────────

def render_component_tab() -> None:
    """Renders the full Component Intelligence tab. Call from app.py tabs[N]."""

    st.markdown("## Component Intelligence")
    st.markdown(
        "<div style='color:#6b7599;font-size:13px;margin-bottom:8px'>"
        "Compliance and export-control risk analysis of dual-use drone components. "
        "For OSINT, sanctions screening, and procurement monitoring purposes only."
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Load data ─────────────────────────────────────────────────────────────
    df = get_component_intelligence()

    # ── Sidebar-style filters rendered inline at top ──────────────────────────
    with st.expander("🔍  Filters", expanded=True):
        fc1, fc2, fc3, fc4, fc5 = st.columns(5)

        all_cats = sorted(df["category"].unique())
        sel_cats = fc1.multiselect(
            "Category", all_cats, default=all_cats, label_visibility="visible"
        )

        all_sens = ["Common civilian", "Dual-use", "Sensitive dual-use", "Military-adjacent"]
        sel_sens = fc2.multiselect(
            "Sensitivity", all_sens, default=all_sens, label_visibility="visible"
        )

        all_regions = sorted({r for row in df["procurement_regions"] for r in row})
        sel_regions = fc3.multiselect(
            "Procurement region", all_regions, default=all_regions, label_visibility="visible"
        )

        risk_min, risk_max = fc4.slider(
            "Procurement risk (0–10)", 0, 10, (0, 10)
        )

        all_conf = ["High", "Medium", "Low", "Unverified"]
        sel_conf = fc5.multiselect(
            "Source confidence", all_conf, default=all_conf, label_visibility="visible"
        )

    # Apply filters
    mask = (
        df["category"].isin(sel_cats)
        & df["sensitivity_level"].isin(sel_sens)
        & df["source_confidence"].isin(sel_conf)
        & df["procurement_risk_score"].between(risk_min, risk_max)
        & df["procurement_regions"].apply(
            lambda regs: any(r in sel_regions for r in regs)
        )
    )
    fdf = df[mask].copy()

    # ── KPI row ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Components tracked",        len(fdf))
    k2.metric("Military-adjacent",         len(fdf[fdf["sensitivity_level"] == "Military-adjacent"]))
    k3.metric("Sensitive dual-use",        len(fdf[fdf["sensitivity_level"] == "Sensitive dual-use"]))
    k4.metric("Avg procurement risk",      f"{fdf['procurement_risk_score'].mean():.1f}/10" if len(fdf) else "—")
    k5.metric("High-risk (≥8)",           len(fdf[fdf["procurement_risk_score"] >= 8]))
    k6.metric("Categories represented",    fdf["category"].nunique())

    st.divider()

    # ════════════════════════════════════════════════════════════════
    # SECTION A — OVERVIEW CHARTS
    # ════════════════════════════════════════════════════════════════
    _section("A · Visualisations")

    row1_l, row1_r = st.columns(2)

    # Chart 1 — Sensitivity distribution
    with row1_l:
        _section("Component risk distribution by sensitivity")
        sens_counts = (
            fdf["sensitivity_level"]
            .value_counts()
            .reindex(list(SENSITIVITY_COLOR.keys()), fill_value=0)
            .reset_index()
        )
        sens_counts.columns = ["Sensitivity", "Count"]
        fig_sens = px.bar(
            sens_counts, x="Sensitivity", y="Count",
            color="Sensitivity", color_discrete_map=SENSITIVITY_COLOR,
            template="plotly_dark",
        )
        fig_sens.update_layout(showlegend=False, **PLOTLY_BASE)
        fig_sens.update_traces(marker_line_width=0)
        st.plotly_chart(fig_sens, use_container_width=True)

    # Chart 2 — Category breakdown (pie)
    with row1_r:
        _section("Component count by category")
        cat_counts = fdf["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.pie(
            cat_counts, names="Category", values="Count",
            color_discrete_sequence=CHART_COLORS,
            template="plotly_dark", hole=0.42,
        )
        fig_cat.update_layout(
            **PLOTLY_BASE,
            legend=dict(font_size=9, orientation="v"),
        )
        fig_cat.update_traces(textfont_size=9)
        st.plotly_chart(fig_cat, use_container_width=True)

    row2_l, row2_r = st.columns(2)

    # Chart 3 — Procurement risk score distribution
    with row2_l:
        _section("Procurement risk score distribution")
        fig_risk = px.histogram(
            fdf, x="procurement_risk_score", nbins=10,
            color_discrete_sequence=["#f07c2a"],
            template="plotly_dark",
            labels={"procurement_risk_score": "Risk Score (0–10)"},
        )
        fig_risk.update_layout(showlegend=False, **PLOTLY_BASE)
        fig_risk.update_traces(marker_line_width=0)
        st.plotly_chart(fig_risk, use_container_width=True)

    # Chart 4 — Sensitive dual-use component count per category (stacked bar)
    with row2_r:
        _section("Sensitive + military-adjacent components by category")
        sens_cat = (
            fdf[fdf["sensitivity_level"].isin(["Sensitive dual-use", "Military-adjacent"])]
            .groupby(["category", "sensitivity_level"])
            .size()
            .reset_index(name="Count")
        )
        fig_sc = px.bar(
            sens_cat, x="Count", y="category", color="sensitivity_level",
            color_discrete_map=SENSITIVITY_COLOR,
            orientation="h", template="plotly_dark",
            labels={"category": "", "sensitivity_level": "Sensitivity"},
        )
        fig_sc.update_layout(**PLOTLY_BASE, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_sc, use_container_width=True)

    # Chart 5 — Component × region matrix (heatmap)
    st.divider()
    _section("Component-by-region procurement matrix")
    matrix = get_region_component_matrix(fdf)
    if not matrix.empty:
        # Filter matrix columns to selected regions
        matrix_cols = [c for c in matrix.columns if c in sel_regions]
        if matrix_cols:
            matrix_filtered = matrix[matrix_cols]
            fig_heat = go.Figure(
                data=go.Heatmap(
                    z=matrix_filtered.values,
                    x=matrix_filtered.columns.tolist(),
                    y=matrix_filtered.index.tolist(),
                    colorscale=[[0, "#0d0f15"], [0.3, "#1e2a3a"], [0.7, "#f07c2a"], [1, "#e8503a"]],
                    hovertemplate="%{y}<br>%{x}: %{z} components<extra></extra>",
                    showscale=True,
                    colorbar=dict(
                       title=dict(
    text="Count",
    font=dict(size=10, color="#6b7599")
),
                        tickfont=dict(size=9, color="#6b7599"),
                        bgcolor="#0d0f15",
                    ),
                )
            )
            fig_heat.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0d0f15",
                plot_bgcolor="#0d0f15",
                font_family="IBM Plex Mono",
                margin=dict(t=20, b=20, l=0, r=0),
                height=340,
                xaxis=dict(tickfont=dict(size=10), title=""),
                yaxis=dict(tickfont=dict(size=10), title="", autorange="reversed"),
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("No data for the selected region filter.")
    else:
        st.info("No component-region data available.")

    # ════════════════════════════════════════════════════════════════
    # SECTION B — COMPONENT CATALOGUE
    # ════════════════════════════════════════════════════════════════
    st.divider()
    _section("B · Component catalogue")

    search_term = st.text_input(
        "Search components",
        placeholder="Component name, use case, export control regime, notes…",
        label_visibility="collapsed",
    )
    if search_term:
        mask_search = fdf.apply(
            lambda r: search_term.lower() in str(r).lower(), axis=1
        )
        fdf = fdf[mask_search]

    st.markdown(
        f"<div style='color:#6b7599;font-size:11px;font-family:IBM Plex Mono,monospace;"
        f"margin-bottom:12px'>{len(fdf)} components match current filters</div>",
        unsafe_allow_html=True,
    )

    # Group by category
    for cat in sorted(fdf["category"].unique()):
        icon = CATEGORY_ICON.get(cat, "◌")
        cat_df = fdf[fdf["category"] == cat].sort_values(
            "procurement_risk_score", ascending=False
        )

        st.markdown(
            f"<div style='background:#0d0f15;border:1px solid #1e2230;border-radius:4px;"
            f"padding:8px 14px;margin-bottom:4px;font-family:IBM Plex Mono,monospace;"
            f"font-size:12px;color:#6b7599;letter-spacing:.08em'>"
            f"{icon} &nbsp; {cat.upper()} &nbsp;·&nbsp; {len(cat_df)} components</div>",
            unsafe_allow_html=True,
        )

        for _, row in cat_df.iterrows():
            label = (
                f"{row['component_name']}  "
                f"{'·' * row['procurement_risk_score']}  "
                f"[{row['sensitivity_level']}]"
            )
            with st.expander(label):
                _render_component_card(row)

        st.markdown("")

    # ════════════════════════════════════════════════════════════════
    # SECTION C — RED FLAG TABLE
    # ════════════════════════════════════════════════════════════════
    st.divider()
    _section("C · Procurement red-flag register")
    st.markdown(
        "<div style='color:#6b7599;font-size:12px;margin-bottom:10px'>"
        "Consolidated view of all documented red flags across filtered components, "
        "ordered by procurement risk score."
        "</div>",
        unsafe_allow_html=True,
    )

    rf_df = get_red_flag_table(fdf)
    if not rf_df.empty:
        rf_df = rf_df.sort_values("Procurement Risk", ascending=False)

        # Colour-code the sensitivity column
        def _style_sens(val):
            c = SENSITIVITY_COLOR.get(val, "#6b7599")
            return f"color: {c}; font-weight: 500"

    styled = rf_df.style.map(_style_sens, subset=["Sensitivity"])
            st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Procurement Risk": st.column_config.ProgressColumn(
                    "Risk (0–10)", min_value=0, max_value=10, format="%d"
                ),
                "Export Control": st.column_config.TextColumn(
                    "Export control", width="medium"
                ),
            },
        )

        # Download
        csv = rf_df.to_csv(index=False)
        st.download_button(
            "Download red-flag register (.csv)",
            csv,
            file_name="component_red_flags.csv",
            mime="text/csv",
        )
    else:
        st.info("No red flag data for the current filter selection.")

    # ════════════════════════════════════════════════════════════════
    # SECTION D — ANALYST VIEW
    # ════════════════════════════════════════════════════════════════
    st.divider()
    _section("D · Analyst view")
    _render_analyst_view(fdf)


# ── Card renderer ─────────────────────────────────────────────────────────────

def _render_component_card(row: pd.Series) -> None:
    """Renders the expanded detail card for a single component."""

    # Header badges
    c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
    c1.markdown(_sens_badge(row["sensitivity_level"]), unsafe_allow_html=True)
    c2.markdown(_risk_badge(row["procurement_risk_score"]), unsafe_allow_html=True)
    c3.markdown(_conf_badge(row["source_confidence"]), unsafe_allow_html=True)
    c4.markdown(
        f"<span style='font-family:IBM Plex Mono,monospace;font-size:10px;color:#3a4060'>"
        f"{row['control_regime']}</span>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    # Two-column detail layout
    left, right = st.columns(2)

    with left:
        st.markdown("**Civilian use case**")
        st.markdown(
            f"<div style='font-size:12px;color:#c8cfe0;line-height:1.6'>{row['civilian_use_case']}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown("**Dual-use relevance**")
        st.markdown(
            f"<div style='font-size:12px;color:#c8cfe0;line-height:1.6'>{row['dual_use_relevance']}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown("**Export-control relevance**")
        st.markdown(
            f"<div style='background:#0d111a;border-left:3px solid #4a90d9;border-radius:2px;"
            f"padding:8px 12px;font-size:12px;color:#c8cfe0;line-height:1.5'>"
            f"{row['export_control_relevance']}</div>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("**Procurement red flags**")
        for flag in row.get("red_flags", []):
            st.markdown(
                f"<div style='background:#1a0f0d;border-left:3px solid #e8503a;border-radius:2px;"
                f"padding:6px 10px;font-size:12px;color:#c8cfe0;margin-bottom:4px;line-height:1.5'>"
                f"⚑ &nbsp;{flag}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("")
        st.markdown("**Known procurement regions**")
        region_chips = " ".join(
            [f"<span class='badge badge-unver'>{r}</span>" for r in row.get("procurement_regions", [])]
        )
        st.markdown(region_chips, unsafe_allow_html=True)

    # Notes + source
    if row.get("notes"):
        st.markdown("")
        st.markdown(
            f"<div style='background:#0d0f15;border:1px solid #1e2230;border-radius:3px;"
            f"padding:8px 12px;font-size:11px;color:#6b7599;line-height:1.5'>"
            f"<b style='color:#3a4060'>Analyst note:</b> {row['notes']}</div>",
            unsafe_allow_html=True,
        )

    if row.get("source_url"):
        st.markdown(
            f"<div style='font-size:10px;color:#3a4060;font-family:IBM Plex Mono,monospace;"
            f"margin-top:6px'>Source: "
            f"<a href='{row['source_url']}' style='color:#4a90d9'>{row['source_url']}</a></div>",
            unsafe_allow_html=True,
        )


# ── Analyst view renderer ─────────────────────────────────────────────────────

def _render_analyst_view(df: pd.DataFrame) -> None:
    """Answers the four key analyst questions from the filtered component dataset."""

    st.markdown(
        "<div style='color:#6b7599;font-size:12px;margin-bottom:14px'>"
        "Structured analysis of the filtered component dataset across four intelligence questions."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Q1: Highest procurement risk ────────────────────────────────────────
    with st.expander("Q1 · Which components create the highest procurement risk?", expanded=True):
        top_risk = (
            df.sort_values("procurement_risk_score", ascending=False)
            .head(10)[["component_name", "category", "sensitivity_level", "procurement_risk_score", "control_regime"]]
            .reset_index(drop=True)
        )
        top_risk.columns = ["Component", "Category", "Sensitivity", "Risk Score", "Control Regime"]

        if not top_risk.empty:
            # Narrative
            top1 = top_risk.iloc[0]
            st.markdown(
                f"<div class='alert-box'>The highest-risk component in the current filter set is "
                f"<b>{top1['Component']}</b> (risk score {top1['Risk Score']}/10), "
                f"classified as <b>{top1['Sensitivity']}</b> under <b>{top1['Control Regime']}</b>. "
                f"{len(df[df['procurement_risk_score'] >= 8])} of {len(df)} filtered components score ≥8/10.</div>",
                unsafe_allow_html=True,
            )

            def _style_risk(val):
                if val >= 9:   return "color: #e8503a; font-weight: 600"
                elif val >= 7: return "color: #f07c2a; font-weight: 500"
                elif val >= 5: return "color: #f0c040"
                return "color: #3ab87a"

            styled_risk = top_risk.style.applymap(_style_risk, subset=["Risk Score"])
            st.dataframe(styled_risk, use_container_width=True, hide_index=True)
        else:
            st.info("No components match the current filter.")

    # ── Q2: Regional concentration of sensitive components ──────────────────
    with st.expander("Q2 · Which regions show concentration of sensitive components?"):
        sens_df = df[df["sensitivity_level"].isin(["Sensitive dual-use", "Military-adjacent"])]
        if not sens_df.empty:
            region_counts: dict[str, int] = Counter()
            for _, row in sens_df.iterrows():
                for r in row["procurement_regions"]:
                    region_counts[r] += 1

            reg_df = (
                pd.DataFrame(region_counts.items(), columns=["Region", "Sensitive Component Count"])
                .sort_values("Sensitive Component Count", ascending=False)
            )

            # Narrative
            top_reg = reg_df.iloc[0]
            st.markdown(
                f"<div class='info-box'><b>{top_reg['Region']}</b> is the most represented procurement "
                f"region for sensitive/military-adjacent components, appearing in "
                f"<b>{top_reg['Sensitive Component Count']}</b> component records. "
                f"{len(reg_df)} distinct regions are represented in sensitive component supply chains.</div>",
                unsafe_allow_html=True,
            )

            fig_reg = px.bar(
                reg_df, x="Sensitive Component Count", y="Region",
                orientation="h", color="Sensitive Component Count",
                color_continuous_scale=[[0, "#1e2a3a"], [0.5, "#f07c2a"], [1, "#e8503a"]],
                template="plotly_dark",
            )
            fig_reg.update_layout(
                showlegend=False, **PLOTLY_BASE,
                height=300,
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.info("No sensitive or military-adjacent components in current filter set.")

    # ── Q3: Civilian items elevated by context ───────────────────────────────
    with st.expander("Q3 · Which components are common civilian items but elevated in context?"):
        civ_elevated = df[
            (df["sensitivity_level"].isin(["Common civilian", "Dual-use"])) &
            (df["procurement_risk_score"] >= 5)
        ].sort_values("procurement_risk_score", ascending=False)

        if not civ_elevated.empty:
            st.markdown(
                f"<div class='info-box'>"
                f"{len(civ_elevated)} component(s) are classified as <b>Common civilian</b> or "
                f"<b>Dual-use</b> but carry a procurement risk score ≥5/10. "
                f"These items become elevated risk indicators when procured in bulk, in combination "
                f"with higher-sensitivity components, or by entities without a documented civilian use case."
                f"</div>",
                unsafe_allow_html=True,
            )

            for _, row in civ_elevated.iterrows():
                col_a, col_b = st.columns([3, 1])
                col_a.markdown(
                    f"<div style='font-size:12px;font-weight:500;color:#c8cfe0'>{row['component_name']}</div>"
                    f"<div style='font-size:11px;color:#6b7599'>{row['category']} · {row['sensitivity_level']}</div>",
                    unsafe_allow_html=True,
                )
                col_b.markdown(
                    _risk_badge(row["procurement_risk_score"]), unsafe_allow_html=True
                )
                if row.get("red_flags"):
                    st.markdown(
                        f"<div style='font-size:11px;color:#6b7599;margin-left:10px;margin-bottom:8px'>"
                        f"Key contextual signal: {row['red_flags'][0]}</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No elevated civilian components in current filter set.")

    # ── Q4: Collection gaps ──────────────────────────────────────────────────
    with st.expander("Q4 · What collection gaps remain?"):
        low_conf = df[df["source_confidence"].isin(["Low", "Unverified"])]
        no_url   = df[df["source_url"].isna() | (df["source_url"] == "")]
        high_risk_low_conf = df[
            (df["procurement_risk_score"] >= 7) &
            (df["source_confidence"].isin(["Low", "Medium", "Unverified"]))
        ]

        st.markdown(
            f"<div style='background:#0d111a;border:1px solid #1e2230;border-radius:4px;"
            f"padding:14px 16px;font-size:13px;line-height:1.8'>"
            f"<b style='color:#4a90d9'>Confidence gaps:</b> "
            f"{len(low_conf)} component records carry Low or Unverified source confidence.<br>"
            f"<b style='color:#4a90d9'>Missing source URLs:</b> "
            f"{len(no_url)} records lack a source URL — citation traceability is incomplete.<br>"
            f"<b style='color:#e8503a'>High-risk / low-confidence overlap:</b> "
            f"{len(high_risk_low_conf)} components score ≥7 procurement risk but have Medium or lower "
            f"source confidence — these should be prioritised for additional corroboration.<br>"
            f"<b style='color:#f0c040'>Manufacturing / Modification category:</b> "
            f"This category has the fewest published open-source references; procurement signals "
            f"are largely inference-based rather than documented.<br>"
            f"<b style='color:#f0c040'>Non-state actor sourcing:</b> "
            f"Commercial FPV components sourced by non-state actors in the Sahel and Sudan "
            f"are almost entirely undocumented at the individual procurement level."
            f"</div>",
            unsafe_allow_html=True,
        )

        if not high_risk_low_conf.empty:
            st.markdown("")
            _section("Priority components for additional sourcing")
            for _, row in high_risk_low_conf.iterrows():
                st.markdown(
                    f"<span class='badge badge-high'>RISK {row['procurement_risk_score']}/10</span>"
                    f"&nbsp;&nbsp;<b>{row['component_name']}</b>"
                    f"&nbsp;·&nbsp;<span style='color:#6b7599;font-size:12px'>"
                    f"Confidence: {row['source_confidence']}</span>",
                    unsafe_allow_html=True,
                )
