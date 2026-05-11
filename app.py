"""
Drone Procurement & Conflict-Use Intelligence Dashboard
=======================================================
Run with:  streamlit run app.py

DATA REPLACEMENT GUIDE
----------------------
All sample data lives in data/sample_data.py
To use your own CSVs, replace any of the load_*() functions
in data/loaders.py with pd.read_csv("your_file.csv").
Column names are documented at the top of each loader.
"""

import streamlit as st

st.set_page_config(
    page_title="UAS THREATMAP",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
code, .stCode { font-family: 'IBM Plex Mono', monospace !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0f15;
    border-right: 1px solid #1e2230;
}
section[data-testid="stSidebar"] * { color: #c8cfe0 !important; }

/* Main background */
.stApp { background: #08090d; color: #c8cfe0; }

/* Metric cards */
div[data-testid="metric-container"] {
    background: #0d0f15;
    border: 1px solid #1e2230;
    border-radius: 4px;
    padding: 12px 16px;
}
div[data-testid="metric-container"] label { color: #6b7599 !important; font-size: 11px !important; letter-spacing: .08em; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #c8cfe0 !important; font-family: 'IBM Plex Mono', monospace !important; }

/* Tabs */
button[data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; letter-spacing: .06em; color: #6b7599 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #e8503a !important; border-bottom-color: #e8503a !important; }

/* Dataframe */
.stDataFrame { border: 1px solid #1e2230 !important; border-radius: 4px !important; }

/* Selectbox / multiselect */
div[data-baseweb="select"] { background: #0d0f15 !important; border-color: #1e2230 !important; }

/* Risk badge helpers (used in st.markdown) */
.badge { display:inline-block; font-family:'IBM Plex Mono',monospace; font-size:10px;
         padding:2px 7px; border-radius:3px; font-weight:600; letter-spacing:.05em; }
.badge-crit  { background:rgba(232,80,58,.2);  color:#e8503a; border:1px solid rgba(232,80,58,.4); }
.badge-high  { background:rgba(240,124,42,.2); color:#f07c2a; border:1px solid rgba(240,124,42,.4); }
.badge-mod   { background:rgba(240,192,64,.15);color:#f0c040; border:1px solid rgba(240,192,64,.3); }
.badge-low   { background:rgba(58,184,122,.15);color:#3ab87a; border:1px solid rgba(58,184,122,.3); }
.badge-hi-conf { background:rgba(58,184,122,.15);color:#3ab87a; border:1px solid rgba(58,184,122,.3); }
.badge-med-conf{ background:rgba(240,192,64,.15);color:#f0c040; border:1px solid rgba(240,192,64,.3); }
.badge-lo-conf { background:rgba(240,124,42,.2); color:#f07c2a; border:1px solid rgba(240,124,42,.4); }
.badge-unver   { background:rgba(107,117,153,.15);color:#6b7599; border:1px solid rgba(107,117,153,.3);}

h1,h2,h3 { font-family:'IBM Plex Mono',monospace !important; color:#c8cfe0 !important; }
.section-title { font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.1em;
                 color:#3a4060; text-transform:uppercase; margin-bottom:6px; }
.alert-box { background:#1a0f0d; border:1px solid #e8503a33; border-left:3px solid #e8503a;
             border-radius:3px; padding:10px 14px; margin:8px 0; font-size:13px; }
.info-box  { background:#0d111a; border:1px solid #4a90d933; border-left:3px solid #4a90d9;
             border-radius:3px; padding:10px 14px; margin:8px 0; font-size:13px; }
</style>
""", unsafe_allow_html=True)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from data.sample_data import (
    get_entities, get_incidents, get_components,
    get_ttp_entries, get_sources
)
from utils.risk_engine import score_entity, RISK_LEVELS
from utils.analyst_brief import generate_brief
from tabs.component_tab import render_component_tab
from tabs.network_tab import render_network_tab
from tabs.gaps_tab import render_gaps_tab

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    entities   = get_entities()
    incidents  = get_incidents()
    components = get_components()
    ttps       = get_ttp_entries()
    sources    = get_sources()
    # Apply risk scoring
    entities["risk_score"]  = entities.apply(score_entity, axis=1)
    entities["risk_level"]  = entities["risk_score"].apply(lambda s: RISK_LEVELS(s))
    return entities, incidents, components, ttps, sources

entities, incidents, components, ttps, sources = load_all()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ◈ UAS THREATMAP")
    st.markdown("<div style='color:#3a4060;font-size:10px;font-family:IBM Plex Mono,monospace;letter-spacing:.08em'>DRONE PROCUREMENT INTELLIGENCE</div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div class='section-title'>Risk filter</div>", unsafe_allow_html=True)
    risk_filter = st.multiselect(
        "Risk level", ["Critical", "High", "Moderate", "Low"],
        default=["Critical", "High", "Moderate", "Low"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='section-title'>Region filter</div>", unsafe_allow_html=True)
    all_regions = sorted(entities["region"].dropna().unique().tolist())
    region_filter = st.multiselect("Region", all_regions, default=all_regions, label_visibility="collapsed")

    st.markdown("<div class='section-title'>Confidence filter</div>", unsafe_allow_html=True)
    conf_filter = st.multiselect(
        "Confidence", ["High", "Medium", "Low", "Unverified"],
        default=["High", "Medium", "Low", "Unverified"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='section-title'>Data type filter</div>", unsafe_allow_html=True)
    data_type_filter = st.multiselect(
        "Data type", ["OSINT", "ASSESSED", "INFERRED", "SYNTHETIC"],
        default=["OSINT", "ASSESSED", "INFERRED"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='section-title'>Date range</div>", unsafe_allow_html=True)
    min_date = incidents["date"].min()
    max_date = incidents["date"].max()
    date_range = st.date_input("Date range", value=(min_date, max_date), label_visibility="collapsed")

    st.divider()
    st.markdown("<div style='color:#3a4060;font-size:10px;font-family:IBM Plex Mono,monospace'>v2.0 · OSINT BASIS · UNCLASSIFIED<br>Updated May 2026</div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown(
        "<div style='background:#1a0f0d;border:1px solid #e8503a33;border-left:2px solid #e8503a;"
        "border-radius:2px;padding:6px 8px;font-size:9px;color:#6b7599;font-family:IBM Plex Mono,monospace;line-height:1.5'>"
        "Contains OSINT-sourced, assessed, and synthetic/demo data. "
        "Not a substitute for primary source verification."
        "</div>",
        unsafe_allow_html=True,
    )

# Apply filters
filtered_entities = entities[
    (entities["risk_level"].isin(risk_filter)) &
    (entities["region"].isin(region_filter)) &
    (entities["source_confidence"].isin(conf_filter)) &
    (entities["data_type"].isin(data_type_filter))
]

if len(date_range) == 2:
    d0, d1 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered_incidents = incidents[(incidents["date"] >= d0) & (incidents["date"] <= d1)]
else:
    filtered_incidents = incidents

# ── Disclaimer banner ────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:#0d0f15;border:1px solid #2a2f42;border-radius:3px;"
    "padding:7px 14px;margin-bottom:10px;font-size:10px;color:#3a4060;"
    "font-family:IBM Plex Mono,monospace;letter-spacing:.04em'>"
    "⚠ Dashboard contains a mixture of open-source reporting, analytical assessment, and synthetic/demo data "
    "for intelligence workflow prototyping. For compliance, sanctions, export-control, and OSINT analysis only. "
    "Not a substitute for primary source verification."
    "</div>",
    unsafe_allow_html=True,
)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["Overview", "Risk Map", "Entities", "Components", "Network", "TTPs", "Trends", "Analyst Brief", "Research Gaps"])

# ════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## Threat Overview")

    # KPI row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total entities",    len(filtered_entities))
    c2.metric("Critical",          len(filtered_entities[filtered_entities["risk_level"]=="Critical"]))
    c3.metric("Incidents (period)",len(filtered_incidents))
    c4.metric("Regions active",    filtered_incidents["region"].nunique() if "region" in filtered_incidents.columns else "—")
    c5.metric("Components tracked",len(components))
    c6.metric("TTPs documented",   len(ttps))

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<div class='section-title'>Risk level distribution — entities</div>", unsafe_allow_html=True)
        risk_counts = filtered_entities["risk_level"].value_counts().reindex(
            ["Critical","High","Moderate","Low"], fill_value=0
        ).reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        color_map = {"Critical":"#e8503a","High":"#f07c2a","Moderate":"#f0c040","Low":"#3ab87a"}
        fig_risk = px.bar(risk_counts, x="Risk Level", y="Count",
                          color="Risk Level", color_discrete_map=color_map,
                          template="plotly_dark")
        fig_risk.update_layout(showlegend=False, paper_bgcolor="#0d0f15",
                               plot_bgcolor="#0d0f15", margin=dict(t=10,b=10,l=0,r=0),
                               font_family="IBM Plex Mono")
        fig_risk.update_traces(marker_line_width=0)
        st.plotly_chart(fig_risk, use_container_width=True)

    with col_right:
        st.markdown("<div class='section-title'>Category breakdown</div>", unsafe_allow_html=True)
        cat_counts = filtered_entities["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.pie(cat_counts, names="Category", values="Count",
                         color_discrete_sequence=["#e8503a","#f07c2a","#f0c040","#4a90d9","#9b6dff","#3ab87a"],
                         template="plotly_dark", hole=.45)
        fig_cat.update_layout(paper_bgcolor="#0d0f15", margin=dict(t=10,b=10,l=0,r=0),
                              font_family="IBM Plex Mono", legend=dict(font_size=10))
        fig_cat.update_traces(textfont_size=10)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()
    st.markdown("<div class='section-title'>Recent high-risk entities</div>", unsafe_allow_html=True)
    top_risk = filtered_entities[filtered_entities["risk_level"].isin(["Critical","High"])].head(5)
    for _, row in top_risk.iterrows():
        lvl = row["risk_level"]
        badge_cls = "badge-crit" if lvl=="Critical" else "badge-high"
        st.markdown(
            f"<span class='badge {badge_cls}'>{lvl.upper()}</span>&nbsp;&nbsp;"
            f"<b>{row['name']}</b> — {row['region']} &nbsp;·&nbsp; "
            f"<span style='color:#6b7599;font-size:12px'>{row['category']}</span>",
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════
# TAB 2 — RISK MAP
# ════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## Risk Map")

    map_layer = st.radio("Map layer", ["All entities", "Conflict incidents", "Procurement hubs"],
                         horizontal=True)

    RISK_COLOR = {"Critical":"#e8503a","High":"#f07c2a","Moderate":"#f0c040","Low":"#3ab87a"}

    if map_layer == "All entities":
        map_df = filtered_entities.dropna(subset=["lat","lon"])
        fig_map = px.scatter_geo(
            map_df, lat="lat", lon="lon",
            color="risk_level", color_discrete_map=RISK_COLOR,
            hover_name="name",
            hover_data={"lat":False,"lon":False,"category":True,"region":True,"risk_score":True},
            size="risk_score", size_max=20,
            projection="natural earth", template="plotly_dark",
        )

    elif map_layer == "Conflict incidents":
        inc_map = filtered_incidents.dropna(subset=["lat","lon"])
        fig_map = px.density_mapbox(
            inc_map, lat="lat", lon="lon", radius=18,
            hover_name="location", hover_data={"incident_type":True,"date":True},
            mapbox_style="carto-darkmatter", zoom=1, center={"lat":30,"lon":30},
            color_continuous_scale="OrRd", template="plotly_dark",
        )
        fig_map.update_layout(mapbox_style="carto-darkmatter")

    else:  # Procurement hubs
        hubs = filtered_entities[filtered_entities["category"].isin(
            ["Procurement network","Transshipment hub"])].dropna(subset=["lat","lon"])
        fig_map = px.scatter_geo(
            hubs, lat="lat", lon="lon", color="category",
            color_discrete_map={"Procurement network":"#e8503a","Transshipment hub":"#f07c2a"},
            hover_name="name", size="risk_score", size_max=22,
            projection="natural earth", template="plotly_dark",
        )

    fig_map.update_layout(
        paper_bgcolor="#08090d", geo=dict(bgcolor="#08090d",
        landcolor="#111520", oceancolor="#0a0c11",
        showframe=False, coastlinecolor="#1e2230"),
        margin=dict(t=0,b=0,l=0,r=0), height=480,
        font_family="IBM Plex Mono",
        legend=dict(bgcolor="#0d0f15", bordercolor="#1e2230", borderwidth=1)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("<div class='section-title'>Heightened activity alerts</div>", unsafe_allow_html=True)
    # Simple rolling comparison: last 30 days vs prior 30
    now = filtered_incidents["date"].max()
    recent = filtered_incidents[filtered_incidents["date"] >= now - pd.Timedelta(days=30)]
    prior  = filtered_incidents[(filtered_incidents["date"] < now - pd.Timedelta(days=30)) &
                                (filtered_incidents["date"] >= now - pd.Timedelta(days=60))]
    if len(prior) > 0 and len(recent) > len(prior) * 1.25:
        pct = int((len(recent)/len(prior)-1)*100)
        st.markdown(f"<div class='alert-box'>⚠ Incident volume up <b>+{pct}%</b> in the last 30 days vs prior period ({len(recent)} vs {len(prior)} events). Possible heightened operational tempo.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='info-box'>ℹ Activity within normal range — {len(recent)} incidents last 30 days vs {len(prior)} prior 30 days.</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — ENTITIES
# ════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## Entity Registry")

    col_search, col_ttp = st.columns([2,2])
    with col_search:
        search = st.text_input("Search entities", placeholder="Name, region, notes…")
    with col_ttp:
        all_ttps = sorted(set(t for row in filtered_entities["ttps"].dropna() for t in row))
        ttp_sel = st.multiselect("Filter by TTP", all_ttps)

    disp = filtered_entities.copy()
    if search:
        mask = disp.apply(lambda r: search.lower() in str(r).lower(), axis=1)
        disp = disp[mask]
    if ttp_sel:
        disp = disp[disp["ttps"].apply(lambda x: bool(x and any(t in x for t in ttp_sel)))]

    # Risk badge column
    def risk_badge(lvl):
        cls = {"Critical":"badge-crit","High":"badge-high","Moderate":"badge-mod","Low":"badge-low"}.get(lvl,"")
        return f"<span class='badge {cls}'>{lvl.upper()}</span>"

    def conf_badge(c):
        cls = {"High":"badge-hi-conf","Medium":"badge-med-conf","Low":"badge-lo-conf","Unverified":"badge-unver"}.get(c,"")
        return f"<span class='badge {cls}'>{c}</span>"

    DATA_TYPE_COLOR = {
        "OSINT":      "#3ab87a", "ASSESSED": "#f0c040",
        "SYNTHETIC":  "#6b7599", "INFERRED": "#9b6dff",
    }

    for _, row in disp.iterrows():
        dt = row.get("data_type", "OSINT")
        dt_color = DATA_TYPE_COLOR.get(dt, "#6b7599")
        with st.expander(f"{row['name']}  ·  {row['region']}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.markdown(risk_badge(row["risk_level"]), unsafe_allow_html=True)
            c2.markdown(f"<span style='color:#6b7599;font-size:12px'>Score: <b style='color:#c8cfe0'>{row['risk_score']}/100</b></span>", unsafe_allow_html=True)
            c3.markdown(conf_badge(row["source_confidence"]), unsafe_allow_html=True)
            c4.markdown(f"<span style='color:#6b7599;font-size:12px'>{row['category']}</span>", unsafe_allow_html=True)
            c5.markdown(
                f"<span style='font-family:IBM Plex Mono,monospace;font-size:9px;"
                f"color:{dt_color};border:1px solid {dt_color}44;padding:2px 6px;"
                f"border-radius:2px'>[{dt}]</span>",
                unsafe_allow_html=True
            )
            st.markdown(f"**Summary:** {row.get('summary','—')}")
            if row.get("uncertainty_note"):
                st.markdown(
                    f"<div style='background:#0d0f15;border-left:3px solid #9b6dff;border-radius:2px;"
                    f"padding:6px 10px;font-size:11px;color:#6b7599;margin:6px 0'>"
                    f"Uncertainty note: {row['uncertainty_note']}</div>",
                    unsafe_allow_html=True,
                )
            if row.get("ttps"):
                ttp_html = " ".join([f"<span class='badge badge-unver'>{t}</span>" for t in row["ttps"]])
                st.markdown(f"**TTPs:** {ttp_html}", unsafe_allow_html=True)
            if row.get("source"):
                st.markdown(f"<span style='color:#3a4060;font-size:11px'>Source: {row['source']}</span>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — COMPONENTS (full intelligence layer)
# ════════════════════════════════════════════════════════════════
with tabs[3]:
    render_component_tab()

# ════════════════════════════════════════════════════════════════
# TAB 5 — NETWORK
# ════════════════════════════════════════════════════════════════
with tabs[4]:
    render_network_tab()

# ════════════════════════════════════════════════════════════════
# TAB 6 — TTPs
# ════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## Tactics, Techniques & Procedures")

    ttp_risk = st.multiselect("Filter by risk level", ["Critical","High","Moderate","Low"],
                              default=["Critical","High","Moderate","Low"])
    ttp_disp = ttps[ttps["risk_level"].isin(ttp_risk)]

    for _, row in ttp_disp.iterrows():
        lvl = row["risk_level"]
        badge_cls = {"Critical":"badge-crit","High":"badge-high","Moderate":"badge-mod","Low":"badge-low"}.get(lvl,"")
        with st.expander(f"{row['ttp_name']}"):
            st.markdown(
                f"<span class='badge {badge_cls}'>{lvl.upper()}</span>&nbsp;"
                f"<span style='color:#6b7599;font-size:11px'>{row['category']}</span>",
                unsafe_allow_html=True
            )
            st.markdown(f"**Description:** {row['description']}")
            if row.get("indicators"):
                st.markdown("**Indicators:**")
                for ind in row["indicators"]:
                    st.markdown(f"- {ind}")
            if row.get("example"):
                st.markdown(f"**Documented example:** *{row['example']}*")
            if row.get("source"):
                st.markdown(f"<span style='color:#3a4060;font-size:11px'>Source: {row['source']}</span>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div class='section-title'>TTP frequency across entities</div>", unsafe_allow_html=True)
    ttp_flat = [t for row in entities["ttps"].dropna() for t in row]
    from collections import Counter
    ttp_freq = pd.DataFrame(Counter(ttp_flat).most_common(12), columns=["TTP","Count"])
    fig_ttp = px.bar(ttp_freq, x="Count", y="TTP", orientation="h",
                     color="Count", color_continuous_scale="OrRd", template="plotly_dark")
    fig_ttp.update_layout(showlegend=False, paper_bgcolor="#0d0f15", plot_bgcolor="#0d0f15",
                          margin=dict(t=10,b=10,l=0,r=0), font_family="IBM Plex Mono",
                          yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_ttp, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 7 — TRENDS
# ════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("## Time-Series Trends")

    granularity = st.radio("Granularity", ["Weekly","Monthly"], horizontal=True)
    freq = "W" if granularity=="Weekly" else "ME"

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("<div class='section-title'>Incident volume over time</div>", unsafe_allow_html=True)
        inc_ts = (filtered_incidents.set_index("date")
                  .resample(freq)["incident_type"].count()
                  .reset_index()
                  .rename(columns={"incident_type":"Count","date":"Date"}))
        # Heightened activity flag
        if len(inc_ts) > 1:
            inc_ts["rolling_avg"] = inc_ts["Count"].rolling(4, min_periods=1).mean()
            inc_ts["alert"] = inc_ts["Count"] > inc_ts["rolling_avg"] * 1.5

        fig_inc = go.Figure()
        fig_inc.add_trace(go.Scatter(x=inc_ts["Date"], y=inc_ts["Count"],
                                     mode="lines+markers", line=dict(color="#4a90d9",width=2),
                                     name="Incidents"))
        if "alert" in inc_ts.columns:
            alert_pts = inc_ts[inc_ts["alert"]]
            fig_inc.add_trace(go.Scatter(x=alert_pts["Date"], y=alert_pts["Count"],
                                         mode="markers", marker=dict(color="#e8503a",size=10,symbol="star"),
                                         name="Heightened activity"))
        fig_inc.update_layout(template="plotly_dark", paper_bgcolor="#0d0f15",
                              plot_bgcolor="#0d0f15", margin=dict(t=10,b=10,l=0,r=0),
                              font_family="IBM Plex Mono", legend=dict(font_size=10))
        st.plotly_chart(fig_inc, use_container_width=True)

    with col_r:
        st.markdown("<div class='section-title'>Incident type breakdown</div>", unsafe_allow_html=True)
        type_ts = (filtered_incidents.set_index("date")
                   .groupby([pd.Grouper(freq=freq),"incident_type"])
                   .size().reset_index(name="Count"))
        fig_type = px.area(type_ts, x="date", y="Count", color="incident_type",
                           color_discrete_sequence=["#e8503a","#f07c2a","#4a90d9","#9b6dff","#3ab87a"],
                           template="plotly_dark")
        fig_type.update_layout(paper_bgcolor="#0d0f15", plot_bgcolor="#0d0f15",
                               margin=dict(t=10,b=10,l=0,r=0), font_family="IBM Plex Mono",
                               legend=dict(font_size=10))
        st.plotly_chart(fig_type, use_container_width=True)

    st.divider()

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        st.markdown("<div class='section-title'>New entities identified per month</div>", unsafe_allow_html=True)
        if "date_identified" in entities.columns:
            ent_ts = (entities.set_index("date_identified")
                      .resample("ME")["name"].count()
                      .reset_index().rename(columns={"name":"Count","date_identified":"Date"}))
            fig_ent = px.bar(ent_ts, x="Date", y="Count", template="plotly_dark",
                             color_discrete_sequence=["#9b6dff"])
            fig_ent.update_layout(paper_bgcolor="#0d0f15", plot_bgcolor="#0d0f15",
                                  margin=dict(t=10,b=10,l=0,r=0), font_family="IBM Plex Mono")
            st.plotly_chart(fig_ent, use_container_width=True)

    with col_r2:
        st.markdown("<div class='section-title'>Activity by region</div>", unsafe_allow_html=True)
        if "region" in filtered_incidents.columns:
            reg_ts = (filtered_incidents.groupby(
                        [pd.Grouper(key="date",freq=freq),"region"])
                      .size().reset_index(name="Count"))
            fig_reg = px.line(reg_ts, x="date", y="Count", color="region",
                              color_discrete_sequence=["#e8503a","#f07c2a","#f0c040","#4a90d9","#3ab87a","#9b6dff"],
                              template="plotly_dark")
            fig_reg.update_layout(paper_bgcolor="#0d0f15", plot_bgcolor="#0d0f15",
                                  margin=dict(t=10,b=10,l=0,r=0), font_family="IBM Plex Mono",
                                  legend=dict(font_size=10))
            st.plotly_chart(fig_reg, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 8 — ANALYST BRIEF
# ════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("## Analyst Brief Generator")
    st.markdown("<div style='color:#6b7599;font-size:13px'>Select records to synthesise an analyst-style intelligence summary.</div>", unsafe_allow_html=True)
    st.divider()

    col_sel, col_brief = st.columns([2, 3])

    with col_sel:
        st.markdown("<div class='section-title'>Select entities</div>", unsafe_allow_html=True)
        entity_options = filtered_entities["name"].tolist()
        selected_names = st.multiselect("Entities", entity_options, max_selections=8, label_visibility="collapsed")

        st.markdown("<div class='section-title'>Select TTPs</div>", unsafe_allow_html=True)
        ttp_options = ttps["ttp_name"].tolist()
        selected_ttps = st.multiselect("TTPs", ttp_options, label_visibility="collapsed")

        st.markdown("<div class='section-title'>Focus region</div>", unsafe_allow_html=True)
        focus_region = st.selectbox("Region", ["All"] + all_regions, label_visibility="collapsed")

        st.markdown("<div class='section-title'>Collection gaps (analyst note)</div>", unsafe_allow_html=True)
        analyst_gaps = st.text_area("Gaps", height=80,
                                    placeholder="Note any known gaps in the data…",
                                    label_visibility="collapsed")

        generate = st.button("Generate Brief", type="primary", use_container_width=True)

    with col_brief:
        if generate and selected_names:
            selected_ents = filtered_entities[filtered_entities["name"].isin(selected_names)]
            selected_ttp_rows = ttps[ttps["ttp_name"].isin(selected_ttps)]
            brief = generate_brief(selected_ents, selected_ttp_rows, focus_region, analyst_gaps)
            st.markdown(brief, unsafe_allow_html=True)

            plain = brief.replace("<b>","**").replace("</b>","**").replace("<br>","\n")
            import re
            plain = re.sub(r'<[^>]+>','',plain)
            st.download_button("Download Brief (.txt)", plain, file_name="analyst_brief.txt", mime="text/plain")

        elif generate:
            st.warning("Select at least one entity to generate a brief.")
        else:
            st.markdown("<div class='empty-panel' style='color:#3a4060;font-family:IBM Plex Mono,monospace;font-size:12px;text-align:center;padding:60px 20px'>Select entities on the left<br>and click Generate Brief</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 9 — RESEARCH GAPS
# ════════════════════════════════════════════════════════════════
with tabs[8]:
    render_gaps_tab()
