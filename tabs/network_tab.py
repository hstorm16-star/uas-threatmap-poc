"""
network_tab.py — Supply Chain Network & Enrichment Indicators Tab
=================================================================
Renders tabs[5] — Network & Enrichment in UAS THREATMAP v3.

Covers:
  - Supply chain relationship network visualization
  - Telecom / connectivity enrichment indicators
  - Maritime / AIS enrichment indicators
  - Sanctions adaptation cycle mapping
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ── Layout helpers ────────────────────────────────────────────────────────────

def _section(title: str) -> None:
    st.markdown(
        f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;"
        f"letter-spacing:.1em;color:#3a4060;text-transform:uppercase;"
        f"margin-bottom:6px'>{title}</div>",
        unsafe_allow_html=True,
    )

def _info(msg: str) -> None:
    st.markdown(
        f"<div style='background:#0d111a;border:1px solid #4a90d933;border-left:3px solid #4a90d9;"
        f"border-radius:3px;padding:8px 12px;font-size:12px;color:#c8cfe0;margin:6px 0'>{msg}</div>",
        unsafe_allow_html=True,
    )

def _warn(msg: str) -> None:
    st.markdown(
        f"<div style='background:#1a0f0d;border:1px solid #e8503a33;border-left:3px solid #e8503a;"
        f"border-radius:3px;padding:8px 12px;font-size:12px;color:#c8cfe0;margin:6px 0'>{msg}</div>",
        unsafe_allow_html=True,
    )

PLOTLY_BASE = dict(
    paper_bgcolor="#0d0f15",
    plot_bgcolor="#0d0f15",
    font_family="IBM Plex Mono",
    margin=dict(t=20, b=10, l=0, r=0),
)


# ── Network data ──────────────────────────────────────────────────────────────

def _get_network_data():
    """
    Returns (nodes, edges) representing the documented supply chain relationship network.
    Data type: OSINT + ASSESSED composite.
    """
    nodes = [
        # Western OEMs
        {"id": "W1", "label": "Western OEM\n(US/EU/JP/CH)", "group": "oem",       "x": 0.1, "y": 0.5,  "size": 18, "confidence": "High"},
        {"id": "W2", "label": "Chinese OEM\n(Shenzhen/Zhuhai)", "group": "oem",   "x": 0.1, "y": 0.2,  "size": 22, "confidence": "High"},
        # Distribution layer
        {"id": "D1", "label": "Auth. distributor\n(EU/US)",    "group": "dist",    "x": 0.28, "y": 0.5, "size": 14, "confidence": "High"},
        {"id": "D2", "label": "Marketplace\n(Alibaba/AliEx)", "group": "dist",     "x": 0.28, "y": 0.2, "size": 18, "confidence": "High"},
        {"id": "D3", "label": "Grey-market\nbroker (HK)",     "group": "dist",     "x": 0.28, "y": 0.75,"size": 16, "confidence": "High"},
        # Intermediary layer
        {"id": "I1", "label": "HK shell cos.\n(addresses)",   "group": "shell",    "x": 0.46, "y": 0.65,"size": 20, "confidence": "High"},
        {"id": "I2", "label": "UAE trading\nco.",             "group": "shell",    "x": 0.46, "y": 0.4, "size": 18, "confidence": "High"},
        {"id": "I3", "label": "Turkey straw\nbuyer",          "group": "shell",    "x": 0.46, "y": 0.2, "size": 14, "confidence": "High"},
        {"id": "I4", "label": "India\nintermediary",          "group": "shell",    "x": 0.46, "y": 0.85,"size": 10, "confidence": "Low"},
        # Hub layer
        {"id": "H1", "label": "Kazakhstan\nre-export",        "group": "hub",      "x": 0.62, "y": 0.3, "size": 16, "confidence": "High"},
        {"id": "H2", "label": "Malaysia\ntransship",          "group": "hub",      "x": 0.62, "y": 0.15,"size": 14, "confidence": "High"},
        {"id": "H3", "label": "Oman / Qatar\n(emerging)",    "group": "hub",      "x": 0.62, "y": 0.55,"size": 10, "confidence": "Low"},
        {"id": "H4", "label": "Kyrgyzstan\n(emerging)",      "group": "hub",      "x": 0.62, "y": 0.70,"size": 10, "confidence": "Low"},
        # End nodes
        {"id": "E1", "label": "Russia\n(Yelabuga/FPV)",      "group": "end",      "x": 0.82, "y": 0.25,"size": 24, "confidence": "High"},
        {"id": "E2", "label": "Iran IRGC\n(HESA/KIPAS)",     "group": "end",      "x": 0.82, "y": 0.55,"size": 22, "confidence": "High"},
        {"id": "E3", "label": "Non-state\nactors (Sahel)",   "group": "end",      "x": 0.82, "y": 0.80,"size": 14, "confidence": "High"},
        # Tech transfer
        {"id": "T1", "label": "Technology\ntransfer JV",     "group": "tech",     "x": 0.64, "y": 0.45,"size": 12, "confidence": "Medium"},
    ]

    edges = [
        # OEM → distribution
        ("W1", "D1", "direct sale",          "High",   "#6b7599", 1.0),
        ("W2", "D2", "marketplace listing",  "High",   "#6b7599", 1.2),
        ("W1", "D3", "grey-market resale",   "Medium", "#6b7599", 0.7),
        ("W2", "D3", "grey-market resale",   "High",   "#6b7599", 0.9),
        # Distribution → intermediary
        ("D1", "I1", "re-export routing",    "High",   "#f07c2a", 1.5),
        ("D1", "I2", "re-export routing",    "High",   "#f07c2a", 1.3),
        ("D2", "I1", "marketplace order",    "High",   "#f07c2a", 1.8),
        ("D2", "I3", "marketplace order",    "High",   "#f07c2a", 1.0),
        ("D3", "I1", "broker chain",         "High",   "#e8503a", 1.6),
        ("D3", "I2", "broker chain",         "High",   "#e8503a", 1.4),
        ("D3", "I4", "broker chain",         "Low",    "#f0c040", 0.6),
        # Intermediary → hub
        ("I1", "H1", "Central Asia route",   "High",   "#f07c2a", 1.5),
        ("I1", "H4", "emerging route",       "Low",    "#f0c040", 0.5),
        ("I2", "H3", "Gulf re-export",       "Low",    "#f0c040", 0.6),
        ("I2", "E2", "direct to Iran",       "High",   "#e8503a", 1.2),
        ("I3", "H1", "Turkey-Kaz route",     "High",   "#f07c2a", 1.0),
        ("I4", "E2", "India-Iran chain",     "Low",    "#f0c040", 0.5),
        ("D2", "H2", "Malaysia transship",   "High",   "#f07c2a", 1.4),
        # Hub → end
        ("H1", "E1", "road entry to Russia", "High",   "#e8503a", 1.8),
        ("H2", "E1", "via Russia proxy",     "Medium", "#f07c2a", 0.8),
        ("H3", "E2", "Gulf to Iran",         "Low",    "#f0c040", 0.5),
        ("H4", "E1", "Kyrgyz-Russia",        "Low",    "#f0c040", 0.5),
        # Tech transfer path
        ("W2", "T1", "technology transfer",  "Medium", "#9b6dff", 0.8),
        ("T1", "E1", "local production",     "Medium", "#9b6dff", 0.8),
        ("T1", "E2", "local production",     "High",   "#9b6dff", 1.0),
        # Open market → non-state actors
        ("D2", "E3", "open commercial",      "High",   "#4a90d9", 1.2),
    ]
    return nodes, edges


GROUP_COLOR = {
    "oem":   "#6b7599",
    "dist":  "#4a90d9",
    "shell": "#f07c2a",
    "hub":   "#f0c040",
    "end":   "#e8503a",
    "tech":  "#9b6dff",
}
GROUP_LABEL = {
    "oem":   "OEM / manufacturer",
    "dist":  "Distributor / marketplace",
    "shell": "Intermediary / shell co.",
    "hub":   "Transshipment hub",
    "end":   "End-use / production",
    "tech":  "Technology transfer",
}


# ── Main render ───────────────────────────────────────────────────────────────

def render_network_tab() -> None:
    st.markdown("## Network & Enrichment Indicators")
    st.markdown(
        "<div style='color:#6b7599;font-size:13px;margin-bottom:8px'>"
        "Supply chain relationship network, telecom/connectivity enrichment indicators, "
        "and maritime/AIS enrichment patterns. For compliance and OSINT analysis."
        "</div>",
        unsafe_allow_html=True,
    )
    _warn(
        "Network visualization is based on documented and assessed patterns, not individual attribution. "
        "Edge weights reflect documented prevalence of routing patterns, not confirmed transaction counts. "
        "Low-confidence nodes and edges are explicitly labeled."
    )
    st.divider()

    sub = st.tabs(["Supply chain network", "Telecom / connectivity", "Maritime / AIS", "Sanctions adaptation cycle"])

    # ── SUB-TAB 1: SUPPLY CHAIN NETWORK ─────────────────────────────────────
    with sub[0]:
        _section("Supplier → intermediary → hub → end-use network (documented and assessed)")

        nodes, edges = _get_network_data()
        node_df = pd.DataFrame(nodes)

        # Build Plotly network figure using scatter + shapes
        fig = go.Figure()

        # Draw edges first
        for src_id, dst_id, label, conf, color, width in edges:
            src = next(n for n in nodes if n["id"] == src_id)
            dst = next(n for n in nodes if n["id"] == dst_id)
            opacity = {"High": 0.7, "Medium": 0.45, "Low": 0.25}.get(conf, 0.4)
            dash = "dot" if conf == "Low" else ("dash" if conf == "Medium" else "solid")
            fig.add_trace(go.Scatter(
                x=[src["x"], dst["x"], None],
                y=[src["y"], dst["y"], None],
                mode="lines",
                line=dict(color=color, width=width, dash=dash),
                opacity=opacity,
                hoverinfo="skip",
                showlegend=False,
            ))

        # Draw nodes
        for grp, grp_label in GROUP_LABEL.items():
            grp_nodes = [n for n in nodes if n["group"] == grp]
            if not grp_nodes:
                continue
            fig.add_trace(go.Scatter(
                x=[n["x"] for n in grp_nodes],
                y=[n["y"] for n in grp_nodes],
                mode="markers+text",
                marker=dict(
                    size=[n["size"] for n in grp_nodes],
                    color=GROUP_COLOR[grp],
                    opacity=0.85,
                    line=dict(color=GROUP_COLOR[grp], width=1.5),
                ),
                text=[n["label"] for n in grp_nodes],
                textposition="top center",
                textfont=dict(size=9, color="#c8cfe0"),
                hovertext=[
                    f"<b>{n['label']}</b><br>Group: {grp_label}<br>Confidence: {n['confidence']}"
                    for n in grp_nodes
                ],
                hoverinfo="text",
                name=grp_label,
                showlegend=True,
            ))

        fig.update_layout(
            **PLOTLY_BASE,
            height=480,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.02, 1.02]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
            legend=dict(font_size=10, bgcolor="#0d0f15", bordercolor="#1e2230", borderwidth=1,
                        itemsizing="constant"),
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)

        _section("Edge confidence legend")
        st.markdown(
            "<div style='font-size:11px;color:#6b7599;font-family:IBM Plex Mono,monospace'>"
            "Solid line = High confidence (corroborated) &nbsp;|&nbsp; "
            "Dashed = Medium confidence (assessed) &nbsp;|&nbsp; "
            "Dotted = Low confidence (emerging indicator)"
            "</div>",
            unsafe_allow_html=True,
        )

        st.divider()
        _section("Documented intermediary chains — summary")

        chains = [
            ("Shenzhen OEM → HK shell → UAE trading co. → Iran IRGC", "High", "Corroborated — OFAC Nov 2025; OCCRP Mar 2026"),
            ("EU distributor → HK shell → Kazakhstan → Russia Yelabuga", "High", "Corroborated — OCCRP Mar 2026; Defcon Level May 2026"),
            ("Alibaba marketplace → HK freight-forwarder → Russia", "High", "Corroborated — ISIS Nov 2023; Ukraine DIU"),
            ("Chinese OEM → Malaysia re-export → US market (tariff evasion)", "High", "Verified — Congressional letter Mar 2024"),
            ("Chinese OEM → Technology transfer JV → Local Russia/Iran production", "Medium", "Assessed — Bloomberg Jul 2025; CSIS Feb 2026"),
            ("Alibaba marketplace → Open commercial → Sahel non-state actors", "High", "Corroborated — Africa Center Feb 2026"),
            ("UAE trading co. → Oman/Qatar re-export → Iran (emerging)", "Low", "Emerging indicator — FinCEN Jun 2025"),
            ("HK shell → Kyrgyzstan → Russia (post-Kazakhstan pressure)", "Low", "Assessed — Defcon Level May 2026"),
            ("India intermediary → UAE → Iran procurement chain", "Low", "Emerging — OFAC Nov 2025 single action"),
        ]
        for chain, conf, src in chains:
            cls = {"High": "badge-hi-conf", "Medium": "badge-med-conf", "Low": "badge-lo-conf"}.get(conf, "badge-unver")
            st.markdown(
                f"<div style='display:flex;gap:10px;align-items:flex-start;margin-bottom:6px'>"
                f"<span class='badge {cls}' style='flex-shrink:0'>{conf}</span>"
                f"<div><div style='font-size:12px;color:#c8cfe0'>{chain}</div>"
                f"<div style='font-size:10px;color:#3a4060;font-family:IBM Plex Mono,monospace'>{src}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── SUB-TAB 2: TELECOM / CONNECTIVITY ───────────────────────────────────
    with sub[1]:
        st.markdown("### Telecom and Connectivity Enrichment Indicators")
        _warn(
            "IMPORTANT: Telecom and connectivity indicators are contextual enrichment signals only. "
            "They are not standalone attribution mechanisms. All indicators below should be treated "
            "as corroborating signals requiring combination with other intelligence."
        )
        st.markdown("")

        telecom_indicators = [
            {
                "indicator": "Starlink IP ranges in procurement communications",
                "confidence": "Low — contextual only",
                "description": (
                    "Starlink terminal use has been documented in Russian-controlled territories. "
                    "Starlink IP ranges appearing in drone marketplace order activity from "
                    "unexpected geolocations may warrant additional scrutiny. "
                    "<b>Critical caveat:</b> Starlink IP attribution is inherently unreliable "
                    "for precise geolocation due to satellite routing. Do not use as standalone attribution."
                ),
                "collection_note": "Requires marketplace platform cooperation or network traffic data.",
                "level": "low",
            },
            {
                "indicator": "Dormitory / NAT-shared IP procurement environments",
                "confidence": "Low — analyst inference",
                "description": (
                    "Yelabuga and Alabuga SEZ facilities house workers in dormitory environments. "
                    "Multiple procurement orders from the same NAT-translated IP block within "
                    "a short timeframe may indicate organized procurement from a shared network. "
                    "This pattern is consistent with, but not specific to, production facility environments."
                ),
                "collection_note": "Requires marketplace order metadata. Not currently collectible via open-source.",
                "level": "low",
            },
            {
                "indicator": "Regional IP clustering in procurement order data",
                "confidence": "Medium — where data is available",
                "description": (
                    "Clustering of drone component orders from IP ranges geolocating to "
                    "Kazakhstan, UAE, Turkey, or HK may be a contextual signal. "
                    "When combined with entity-level red flags (new company, freight forwarder address), "
                    "IP clustering strengthens the overall indicator picture. "
                    "Open-source availability of this data depends on platform cooperation."
                ),
                "collection_note": "Partially collectible via open-source trade data where IP metadata is available.",
                "level": "moderate",
            },
            {
                "indicator": "VoIP / encrypted communication platform use by procurement actors",
                "confidence": "Low — technical inference",
                "description": (
                    "Telegram and WeChat procurement communities for FPV components are referenced "
                    "in open-source reporting. These platforms' use by procurement actors is an "
                    "observed behavioral pattern but not a technically detectable indicator via "
                    "standard OSINT without platform access."
                ),
                "collection_note": "Requires specialized monitoring capability beyond this dashboard.",
                "level": "low",
            },
            {
                "indicator": "Satellite maritime terminal registrations (Starlink Maritime, Inmarsat)",
                "confidence": "Medium — maritime context",
                "description": (
                    "Shadow fleet vessels using Starlink Maritime terminals have been documented. "
                    "Terminal registration jurisdiction mismatches (e.g., Russian-controlled vessel "
                    "with Starlink terminal registered to UAE entity) may be detectable via "
                    "SpaceX/Starlink account data where accessible to investigators."
                ),
                "collection_note": "Relevant for maritime OSINT specialist tools (Windward, Pole Star).",
                "level": "moderate",
            },
        ]

        for ind in telecom_indicators:
            color = {"critical": "#e8503a", "high": "#f07c2a", "moderate": "#f0c040", "low": "#3ab87a"}.get(ind["level"], "#6b7599")
            with st.expander(f"◉  {ind['indicator']}"):
                st.markdown(
                    f"<span class='badge badge-{'hi' if 'Medium' in ind['confidence'] else 'lo'}-conf'>"
                    f"Confidence: {ind['confidence']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown("")
                st.markdown(f"**Description:** {ind['description']}", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='background:#0d0f15;border-left:3px solid {color};border-radius:2px;"
                    f"padding:6px 10px;font-size:11px;color:#6b7599;margin-top:8px'>"
                    f"Collection note: {ind['collection_note']}</div>",
                    unsafe_allow_html=True,
                )

    # ── SUB-TAB 3: MARITIME / AIS ────────────────────────────────────────────
    with sub[2]:
        st.markdown("### Maritime and AIS Enrichment Indicators")
        _info(
            "Maritime indicators are relevant to the oil revenue funding mechanism for UAV procurement, "
            "not to direct drone component shipping (which is primarily air and road freight). "
            "AIS anomaly detection is a viable screening tool but requires corroboration."
        )
        st.markdown("")

        maritime_indicators = [
            {
                "indicator": "AIS position gap > 12 hours in restricted transit zone",
                "confidence": "High — established methodology",
                "description": "Vessels disabling AIS transponders while transiting restricted zones (Bosphorus, Kerch Strait, Gulf of Oman) is a documented evasion behavior. Gaps >12 hours in high-traffic restricted zones are a significant red flag.",
                "tools": "Windward, MarineTraffic, Pole Star, Lloyd's List Intelligence",
                "level": "high",
            },
            {
                "indicator": "Ship-to-ship transfer in international waters",
                "confidence": "High — established methodology",
                "description": "Cargo transfers at sea, outside port surveillance, documented for Russian oil shadow fleet. STS transfers in Gulf of Oman, Laccadive Sea, and Red Sea approaches are primary monitoring zones.",
                "tools": "Windward, UNOSAT, C4ADS maritime tracking",
                "level": "high",
            },
            {
                "indicator": "Port clustering at UAE (Fujairah, Khor Fakkan, Khorfakkan)",
                "confidence": "High — documented",
                "description": "UAE port clustering for vessels in Russian oil trade is well-documented. Fujairah and Khor Fakkan are primary documented staging points. Multiple calls at these ports by vessel associated with sanctioned beneficial owner are a screening flag.",
                "tools": "MarineTraffic port call history; Kharon vessel screening",
                "level": "high",
            },
            {
                "indicator": "Flag state hopping / rapid reflagging",
                "confidence": "High — established methodology",
                "description": "Shadow fleet vessels reflagging rapidly through Gabon, Palau, St Kitts, Cameroon to obscure ownership and avoid enhanced scrutiny associated with prior flag state. Multiple reflaggings within 12 months are a significant red flag.",
                "tools": "Lloyd's List Intelligence; IHS Markit Sea-web; Kharon",
                "level": "high",
            },
            {
                "indicator": "Beneficial ownership chain leading to sanctioned entity",
                "confidence": "High — primary indicator",
                "description": "Ultimate beneficial ownership of vessel in sanctioned entity through layers of intermediate holdcos is the primary legal basis for maritime sanctions screening. Ownership chain analysis through multiple jurisdictions required.",
                "tools": "Sayari; Kharon; OpenCorporates; Kharon maritime",
                "level": "critical",
            },
            {
                "indicator": "Starlink Maritime terminal in unexpected jurisdiction",
                "confidence": "Low — emerging methodology",
                "description": "Shadow fleet vessels using Starlink Maritime have been documented. Terminal registration jurisdiction mismatch (vessel flagged to Gabon, terminal registered to UAE entity linked to sanctioned network) may be detectable. Low standalone confidence; corroborating indicator.",
                "tools": "Specialized OSINT; requires terminal registration data",
                "level": "low",
            },
        ]

        for ind in maritime_indicators:
            color = {"critical": "#e8503a", "high": "#f07c2a", "moderate": "#f0c040", "low": "#3ab87a"}.get(ind["level"], "#6b7599")
            with st.expander(f"⚓  {ind['indicator']}"):
                cls = "badge-crit" if ind["level"] == "critical" else ("badge-high" if ind["level"] == "high" else "badge-lo-conf")
                st.markdown(f"<span class='badge {cls}'>{ind['confidence']}</span>", unsafe_allow_html=True)
                st.markdown("")
                st.markdown(f"**Description:** {ind['description']}")
                st.markdown(
                    f"<div style='background:#0d0f15;border-left:3px solid {color};border-radius:2px;"
                    f"padding:6px 10px;font-size:11px;color:#6b7599;margin-top:8px'>"
                    f"Tools/sources: {ind['tools']}</div>",
                    unsafe_allow_html=True,
                )

        # Simple AIS methodology visual
        st.divider()
        _section("AIS screening methodology — decision flow (analyst reference)")
        st.markdown(
            "<div style='background:#0d0f15;border:1px solid #1e2230;border-radius:4px;padding:14px 16px;"
            "font-family:IBM Plex Mono,monospace;font-size:11px;color:#6b7599;line-height:2'>"
            "1. Identify vessel of interest (cargo manifest, port call, trade data) <br>"
            "2. Query AIS history → flag gaps >12hr in restricted zones <br>"
            "3. Query port call history → flag UAE/Indian Ocean staging clusters <br>"
            "4. Query beneficial ownership chain → flag sanctioned entity links <br>"
            "5. Query flag state history → flag rapid reflagging pattern <br>"
            "6. Query P&amp;I club / insurer → flag non-standard or absent cover <br>"
            "7. Aggregate indicator score → escalate where 3+ flags present <br>"
            "8. Corroborate with trade data, OFAC/BIS screening → decision"
            "</div>",
            unsafe_allow_html=True,
        )

    # ── SUB-TAB 4: SANCTIONS ADAPTATION CYCLE ───────────────────────────────
    with sub[3]:
        st.markdown("### Sanctions Adaptation Cycle")
        _info(
            "The following describes the observed pattern of sanctions action and network adaptation. "
            "This is an analytical framework based on documented patterns, not a prediction of future behavior."
        )
        st.markdown("")

        phases = [
            ("Phase 1", "Initial restriction", "#4a90d9",
             "Western export controls or sanctions designate specific entities, addresses, or components. "
             "Immediate effect: named entities lose access to controlled goods and financial systems."),
            ("Phase 2", "Rapid entity replacement", "#f0c040",
             "Within 2–6 weeks: new entities registered at adjacent addresses or in secondary jurisdictions. "
             "Shared directors, beneficial owners, and commodity flows continue under new corporate identity. "
             "BIS June 2024 address-level Entity List addition was a direct response to this pattern."),
            ("Phase 3", "Hub migration", "#f07c2a",
             "As primary transshipment hubs face enhanced scrutiny (Kazakhstan, Turkey, UAE), "
             "flows migrate to secondary hubs (Kyrgyzstan, Oman, Qatar, Vietnam). "
             "This migration takes 1–6 months and involves establishing new corporate infrastructure."),
            ("Phase 4", "Payment channel adaptation", "#9b6dff",
             "Increased US Treasury pressure on financial channels drives adaptation: "
             "gold barter (documented), CIPS transactions, cryptocurrency, and informal value transfer "
             "progressively replace USD-SWIFT-based payments. Each adaptation makes monitoring harder."),
            ("Phase 5", "Structural shift to in-country production", "#e8503a",
             "Ultimate adaptation: technology transfer and in-country JV production eliminates "
             "cross-border shipping risk entirely. Documented for Iran-Russia (Yelabuga). "
             "This represents the most durable evasion mechanism and the hardest to interdict. "
             "Once established, domestic production capacity persists even if component supply is cut."),
            ("Phase 6", "Second-order effects", "#6b7599",
             "Increased domestic production leads to: (a) reduced dependency on Western components; "
             "(b) development of indigenous alternatives; (c) potential export of capability to "
             "third parties. This cycle, if completed, represents a fundamental long-term shift "
             "that export controls alone cannot reverse."),
        ]

        for phase, title, color, body in phases:
            st.markdown(
                f"<div style='display:flex;gap:14px;align-items:flex-start;margin-bottom:12px'>"
                f"<div style='background:{color}22;border:1px solid {color}55;border-radius:3px;"
                f"padding:4px 10px;font-family:IBM Plex Mono,monospace;font-size:10px;"
                f"color:{color};white-space:nowrap;flex-shrink:0'>{phase}</div>"
                f"<div><div style='font-weight:500;color:#c8cfe0;font-size:13px;margin-bottom:3px'>{title}</div>"
                f"<div style='font-size:12px;color:#6b7599;line-height:1.6'>{body}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        _section("Key implication for compliance analysts")
        st.markdown(
            "<div style='background:#0d111a;border:1px solid #4a90d933;border-left:3px solid #4a90d9;"
            "border-radius:3px;padding:12px 16px;font-size:13px;color:#c8cfe0;line-height:1.7'>"
            "Effective procurement risk monitoring requires continuous updating of entity lists, "
            "hub profiles, and routing patterns. A static screening list becomes outdated within "
            "weeks of a designation action as networks adapt. "
            "<b>Recommended practice:</b> treat entity screening as a living process with "
            "quarterly refresh cycles, not a one-time check."
            "</div>",
            unsafe_allow_html=True,
        )
