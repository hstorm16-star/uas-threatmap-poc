"""
gaps_tab.py — Research Gaps, Collection Priorities, and Expansion Opportunities
================================================================================
For UAS THREATMAP v3. Renders tabs[8] — Research Gaps.
"""

import streamlit as st


def _section(title: str) -> None:
    st.markdown(
        f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;"
        f"letter-spacing:.1em;color:#3a4060;text-transform:uppercase;"
        f"margin-bottom:6px'>{title}</div>",
        unsafe_allow_html=True,
    )


def _gap_card(title: str, body: str, level: str = "high") -> None:
    color = {"critical": "#e8503a", "high": "#f07c2a", "moderate": "#f0c040", "low": "#3ab87a"}.get(level, "#6b7599")
    st.markdown(
        f"<div style='background:#0d0f15;border:1px solid #1e2230;border-left:3px solid {color};"
        f"border-radius:3px;padding:10px 14px;margin-bottom:8px'>"
        f"<div style='font-weight:500;font-size:13px;color:#c8cfe0;margin-bottom:4px'>{title}</div>"
        f"<div style='font-size:12px;color:#6b7599;line-height:1.6'>{body}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_gaps_tab() -> None:
    st.markdown("## Research Gaps & Collection Priorities")
    st.markdown(
        "<div style='color:#6b7599;font-size:13px;margin-bottom:8px'>"
        "Structured analysis of underdeveloped areas, weakly supported assumptions, "
        "and future collection priorities derived from the current evidence base. "
        "Updated through May 2026."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='background:#1a0f0d;border:1px solid #e8503a33;border-left:3px solid #e8503a;"
        "border-radius:3px;padding:8px 12px;font-size:11px;color:#6b7599;font-family:IBM Plex Mono,monospace;margin-bottom:16px'>"
        "ANALYST NOTE: Gap identification is itself an analytical product. Absence of evidence "
        "is not evidence of absence. Gaps may reflect collection limitations rather than "
        "absence of activity."
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── SECTION 1: WEAKLY SUPPORTED ASSUMPTIONS ───────────────────────────────
    with st.expander("1 · Weakly supported assumptions in current evidence base", expanded=True):
        _section("Assumptions requiring additional corroboration")

        _gap_card(
            "LATAM labor recruitment — coercive vs voluntary framing",
            "Open-source reporting on Latin American labor recruitment to Russian drone "
            "production facilities is based on limited, uncorroborated sources. The "
            "available record is consistent with voluntary industrial labor recruitment "
            "in special economic zones, not confirmed coercive or deceptive practices. "
            "Coercive framing should not be asserted without stronger sourcing. "
            "<br><b>Collection need:</b> additional corroboration from labor rights "
            "organizations, journalistic investigation, or diplomatic reporting.",
            "high",
        )
        _gap_card(
            "Autel/Aero-HIT JV — reported but not independently corroborated",
            "The Bloomberg July 2025 report of a potential Autel Robotics / Aero-HIT "
            "joint venture is a single-source emerging indicator. The JV structure, "
            "operational status, and production volume are not confirmed. Analyst "
            "confidence should remain moderate until independently corroborated. "
            "<br><b>Collection need:</b> corporate registry filings, satellite imagery "
            "of potential production sites, trade data flows.",
            "high",
        )
        _gap_card(
            "Starlink as production-environment indicator",
            "Starlink IP ranges as an indicator of Yelabuga/Alabuga proximity is "
            "analyst inference with low standalone value. Starlink IP attribution is "
            "inherently unreliable for geolocation. This indicator should only be "
            "used as a corroborating signal in combination with other indicators. "
            "<br><b>Collection need:</b> technical community corroboration; case studies "
            "of Starlink-in-procurement-context detections.",
            "moderate",
        )
        _gap_card(
            "India as systematic intermediary — one designated action is not a pattern",
            "India-based entities appeared in one OFAC action (Nov 2025). This is "
            "insufficient to characterize India as a systematic intermediary jurisdiction "
            "comparable to UAE or Turkey. Risk of over-inference from a single data point. "
            "<br><b>Collection need:</b> trade data analysis, additional enforcement actions, "
            "investigative reporting on India-linked procurement chains.",
            "moderate",
        )

    # ── SECTION 2: UNDERDEVELOPED REGIONS ─────────────────────────────────────
    with st.expander("2 · Underdeveloped geographic regions"):
        _section("Regions with insufficient open-source coverage")

        _gap_card(
            "Kyrgyzstan and Uzbekistan — emerging secondary hubs",
            "Multiple sources reference Kazakhstan-to-Kyrgyzstan migration as sanctions "
            "pressure intensified post-2024. However, Kyrgyzstan and Uzbekistan are almost "
            "entirely absent from specific entity-level documentation in the open-source record. "
            "<br><b>Collection priority:</b> corporate registry monitoring, trade data "
            "import/export volume analysis, financial flows from EU/US to these jurisdictions.",
            "critical",
        )
        _gap_card(
            "Oman and Qatar as secondary UAE successors",
            "FinCEN and OFAC reporting references UAE pressure driving some network actors "
            "toward Oman and Qatar. These jurisdictions have almost no open-source entity-level "
            "documentation despite their structural suitability as transshipment nodes. "
            "<br><b>Collection priority:</b> commercial registry monitoring, shipping route analysis, "
            "financial compliance reporting from Gulf-region banks.",
            "high",
        )
        _gap_card(
            "Vietnam and Thailand — Malaysian tariff evasion successors",
            "Post-2024 reporting references Vietnam and Thailand as emerging alternatives "
            "to Malaysia for tariff evasion routing of Chinese drones. No entity-level "
            "documentation available in open-source record. "
            "<br><b>Collection priority:</b> US customs trade data, Vietnamese/Thai "
            "corporate registry monitoring, electronics import volume analysis.",
            "high",
        )
        _gap_card(
            "African conflict-zone procurement sourcing chains",
            "The Sahel and Sudan theaters are well-documented at the use level but almost "
            "entirely undocumented at the procurement and supply chain level. How are JNIM, "
            "ISGS, and RSF actually acquiring their drone hardware? Regional electronics "
            "markets, diaspora procurement, direct online ordering? None of these pathways "
            "are documented in the open-source record. "
            "<br><b>Collection priority:</b> investigative journalism, regional partner reporting, "
            "Conflict Armament Research field work.",
            "critical",
        )
        _gap_card(
            "North Korea drone production and sourcing",
            "North Korea has developed and deployed indigenous drones and received "
            "Russian technology transfers, but specific component sourcing chains "
            "remain almost entirely opaque in open-source reporting. "
            "<br><b>Collection priority:</b> UN Panel of Experts reporting, satellite imagery, "
            "defector reporting, OFAC designation patterns.",
            "high",
        )

    # ── SECTION 3: MISSING COMPONENT CATEGORIES ───────────────────────────────
    with st.expander("3 · Missing or underdeveloped component intelligence"):
        _section("Component categories requiring expanded coverage")

        _gap_card(
            "Semiconductor / microelectronics sourcing specificity",
            "The dashboard identifies Texas Instruments and Analog Devices as documented "
            "in Shahed wreckage, but the specific procurement pathways for these chips — "
            "which distributors, which intermediaries, which HS codes — are not documented "
            "at the level needed for distributor-level compliance screening. "
            "<br><b>Collection priority:</b> trade data analysis, BIS enforcement actions, "
            "distributor-level due diligence case studies.",
            "critical",
        )
        _gap_card(
            "PCB and custom electronics manufacturing",
            "Custom PCB ordering through platforms like JLCPCB and PCBWay represents a "
            "significant procurement pathway for purpose-built drone electronics. "
            "This channel is almost entirely undocumented in the open-source record "
            "from a compliance perspective. "
            "<br><b>Collection priority:</b> platform-level monitoring methodology development, "
            "OSINT community tradecraft.",
            "high",
        )
        _gap_card(
            "Propellant and energetics for loitering munitions",
            "The dashboard covers airframe and electronics components but does not address "
            "the energetics and propellant supply chain for loitering munitions. This is "
            "a documented procurement challenge for Iran and Russia (Atlantic Council Mar 2026). "
            "<br><b>Collection priority:</b> separate energetics-focused analytical product; "
            "out of scope for this dashboard but flagged as a gap.",
            "moderate",
        )
        _gap_card(
            "RF spectrum analysis tools and counter-drone systems",
            "Procurement of RF jamming, drone detection, and counter-UAS systems "
            "represents both a defensive procurement indicator and, in some contexts, "
            "a signal of anticipated offensive drone use. Not currently captured. "
            "<br><b>Collection priority:</b> component intelligence expansion for counter-UAS layer.",
            "moderate",
        )

    # ── SECTION 4: MISSING LOGISTICS BEHAVIORS ────────────────────────────────
    with st.expander("4 · Missing logistics and routing behaviors"):
        _section("Logistics patterns requiring documentation")

        _gap_card(
            "Air freight routing specificity",
            "Maritime routing is better-documented than air freight in the current evidence "
            "base. Air freight from Chinese OEMs to HK/UAE to sanctioned destinations is "
            "strongly implied but not documented at carrier or routing specificity. "
            "<br><b>Collection priority:</b> air freight trade data, carrier-level screening.",
            "high",
        )
        _gap_card(
            "Road freight across Central Asian borders",
            "Russia-bound goods entering via Kazakhstan, Armenia, and Georgia are "
            "documented at the volume level but not at the specific border crossing, "
            "carrier, or routing level. This specificity is needed for carrier-level "
            "due diligence. "
            "<br><b>Collection priority:</b> ground-level OSINT, border crossing data, "
            "trucking company screening.",
            "high",
        )
        _gap_card(
            "Informal payment and hawala networks",
            "Gold barter is documented for Iran-Russia transactions but informal payment "
            "networks (hawala, cryptocurrency, informal value transfer) for component "
            "procurement are poorly documented. These channels are inherently difficult "
            "to monitor through financial intelligence. "
            "<br><b>Collection priority:</b> FinCEN advisory monitoring, FATF reporting.",
            "moderate",
        )

    # ── SECTION 5: MISSING MARKETPLACE ECOSYSTEMS ─────────────────────────────
    with st.expander("5 · Missing marketplace and digital procurement ecosystems"):
        _section("Digital procurement channels requiring monitoring methodology")

        _gap_card(
            "Telegram and WeChat procurement communities",
            "Post-2024 reporting references Telegram and WeChat group-based procurement "
            "of FPV components by conflict-zone actors. No methodology for systematic "
            "monitoring of these closed communities exists in the public OSINT record. "
            "<br><b>Collection priority:</b> OSINT community tradecraft development; "
            "relevant to specialized OSINT tools rather than this dashboard.",
            "high",
        )
        _gap_card(
            "Russian-language specialty electronics platforms",
            "Russian domestic electronics platforms (Avito, DNS, Chipdip, RadioKot) "
            "may represent secondary procurement channels for components not available "
            "via mainstream Chinese e-commerce. Not documented in current evidence base. "
            "<br><b>Collection priority:</b> Russian-language OSINT capability.",
            "moderate",
        )
        _gap_card(
            "Dark web and encrypted marketplace component sales",
            "While mainstream e-commerce is the primary channel, there are isolated "
            "references to encrypted marketplace activity for sensitive dual-use "
            "components (anti-jamming, military-grade thermal). Not documented at "
            "sufficient fidelity for this dashboard. "
            "<br><b>Collection priority:</b> specialized dark web monitoring capability.",
            "low",
        )

    # ── SECTION 6: MISSING PAYMENT / FINANCIAL INDICATORS ────────────────────
    with st.expander("6 · Missing payment and financial routing indicators"):
        _section("Financial intelligence gaps")

        _gap_card(
            "CIPS transaction monitoring methodology",
            "CIPS (Chinese Cross-Border Interbank Payments System) is identified as a "
            "sanctions-evasion-relevant alternative to SWIFT, but no methodology for "
            "monitoring CIPS flows for dual-use procurement indicators exists in the "
            "public compliance record. "
            "<br><b>Collection priority:</b> FinCEN guidance on CIPS monitoring; "
            "correspondent banking due diligence development.",
            "critical",
        )
        _gap_card(
            "Cryptocurrency use in component procurement",
            "Cryptocurrency is referenced in some TTP documentation but not documented "
            "with specific chain analysis data. Stablecoin (USDT/Tron) use for "
            "sanctioned procurement is an emerging pattern in adjacent domains. "
            "<br><b>Collection priority:</b> blockchain analytics community; "
            "OFAC virtual currency guidance monitoring.",
            "high",
        )
        _gap_card(
            "Trade financing and letter of credit manipulation",
            "False documentation is documented for end-user certificates but trade "
            "financing instruments (letters of credit, documentary collection) as "
            "a procurement evasion mechanism are not specifically documented for "
            "the drone supply chain. "
            "<br><b>Collection priority:</b> trade finance compliance community reporting.",
            "moderate",
        )

    # ── SECTION 7: MISSING TELECOM / CONNECTIVITY INDICATORS ─────────────────
    with st.expander("7 · Missing telecom and connectivity indicators"):
        _section("Digital connectivity intelligence gaps")

        _gap_card(
            "Dormitory / shared-IP procurement environments",
            "Yelabuga/Alabuga production facilities house workers in dormitory "
            "environments. Large numbers of procurement-related internet sessions "
            "from shared or NAT-translated IP ranges may be a detectable pattern "
            "in marketplace data. Methodology not developed. "
            "<br><b>Collection priority:</b> technical OSINT community; "
            "requires marketplace platform cooperation.",
            "moderate",
        )
        _gap_card(
            "VPN and proxy use masking geographic origin",
            "Sophisticated procurement actors likely use VPNs and proxies to mask "
            "geographic origin of marketplace orders. No methodology for detecting "
            "VPN-masked procurement in compliance context is documented. "
            "<br><b>Collection priority:</b> technical fraud detection community.",
            "moderate",
        )
        _gap_card(
            "Mobile device and SIM card indicators",
            "SIM card registration patterns, IMEI tracking, and mobile payment "
            "indicators may provide enrichment data for procurement investigation. "
            "Not currently documented for drone supply chain context. "
            "<br><b>Collection priority:</b> telecom intelligence community.",
            "low",
        )

    # ── SECTION 8: MISSING SANCTIONS TYPOLOGIES ───────────────────────────────
    with st.expander("8 · Missing sanctions evasion typologies"):
        _section("Evasion mechanisms not yet documented in this product")

        _gap_card(
            "Investment vehicle sanctions evasion",
            "Acquisition of stakes in non-sanctioned entities by designated persons "
            "as a mechanism to maintain economic activity is documented in general "
            "sanctions literature but not specifically for drone supply chain actors. "
            "<br><b>Collection priority:</b> corporate ownership analysis expansion.",
            "high",
        )
        _gap_card(
            "Academic and research institution procurement pathways",
            "Russian and Iranian universities and research institutions have been "
            "documented in adjacent WMD procurement literature as intermediary "
            "entities. Application to drone component procurement is not documented. "
            "<br><b>Collection priority:</b> BIS deemed export controls; academic "
            "institution screening methodology.",
            "moderate",
        )
        _gap_card(
            "Humanitarian aid and NGO channel exploitation",
            "Humanitarian corridor exploitation is documented in historical sanctions "
            "evasion literature. Application to drone supply chain context is not "
            "documented in open-source record. "
            "<br><b>Collection priority:</b> low priority; flag for monitoring.",
            "low",
        )

    # ── SECTION 9: FUTURE COLLECTION PRIORITIES ───────────────────────────────
    st.divider()
    st.markdown("### Future Collection Priorities — Ranked")
    st.markdown(
        "<div style='color:#6b7599;font-size:12px;margin-bottom:12px'>"
        "Based on gap analysis above, ranked by combination of analytical impact and collection feasibility."
        "</div>",
        unsafe_allow_html=True,
    )

    priorities = [
        ("1", "CRITICAL", "Kyrgyzstan/Uzbekistan/Oman/Qatar secondary hub entity mapping",
         "Corporate registry monitoring + trade data volume analysis. High feasibility via open OSINT."),
        ("2", "CRITICAL", "African non-state actor drone sourcing chain documentation",
         "Investigative journalism partnership; CAR field work. Lower feasibility but high analytical value."),
        ("3", "CRITICAL", "CIPS monitoring methodology for dual-use goods",
         "Requires FinCEN/financial industry collaboration. High complexity; critical gap."),
        ("4", "HIGH",     "Semiconductor/chip distributor-level screening methodology",
         "Trade data + BIS enforcement pattern analysis. Moderate feasibility."),
        ("5", "HIGH",     "Autel/Aero-HIT JV corroboration",
         "Corporate registry, satellite imagery, trade data. Moderate feasibility."),
        ("6", "HIGH",     "PCB custom manufacturing platform monitoring",
         "OSINT methodology development. Requires platform monitoring tradecraft."),
        ("7", "HIGH",     "Cryptocurrency use in component procurement — chain analysis",
         "Blockchain analytics tools. Emerging area with growing tooling."),
        ("8", "HIGH",     "LATAM labor recruitment — additional corroboration",
         "Labor rights organization reporting; investigative journalism. Time-sensitive."),
        ("9", "MODERATE", "Vietnam/Thailand tariff evasion successor documentation",
         "US customs trade data. High feasibility via open data sources."),
        ("10","MODERATE", "Telegram/WeChat procurement community monitoring methodology",
         "Specialized OSINT community tradecraft. Lower feasibility currently."),
    ]

    for rank, level, title, approach in priorities:
        cls = {"CRITICAL": "badge-crit", "HIGH": "badge-high", "MODERATE": "badge-mod"}.get(level, "badge-low")
        st.markdown(
            f"<div style='display:flex;gap:12px;align-items:flex-start;margin-bottom:8px'>"
            f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#3a4060;"
            f"min-width:24px;padding-top:2px'>#{rank}</div>"
            f"<div style='flex:1'>"
            f"<span class='badge {cls}'>{level}</span>&nbsp;&nbsp;"
            f"<b style='color:#c8cfe0;font-size:13px'>{title}</b>"
            f"<div style='font-size:12px;color:#6b7599;margin-top:3px'>{approach}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    # ── SECTION 10: DASHBOARD EXPANSION AREAS ─────────────────────────────────
    st.divider()
    st.markdown("### Potential Dashboard Expansion Areas")

    exp_cols = st.columns(2)
    with exp_cols[0]:
        _section("Near-term additions (high feasibility)")
        for item in [
            "Energetics/propellant supply chain layer (separate from electronics)",
            "Counter-UAS procurement monitoring tab",
            "Corporate ownership graph for designated entities",
            "Automated BIS/OFAC list change monitoring alerts",
            "Export licence application pattern analysis",
            "Carrier and freight forwarder risk scoring",
        ]:
            st.markdown(f"<div style='font-size:12px;color:#c8cfe0;padding:3px 0'>◌ &nbsp;{item}</div>", unsafe_allow_html=True)

    with exp_cols[1]:
        _section("Longer-term additions (lower feasibility)")
        for item in [
            "CIPS transaction pattern monitoring integration",
            "Satellite imagery change detection for production sites",
            "Natural language processing of Russian/Chinese procurement forums",
            "Blockchain analytics integration for cryptocurrency signals",
            "Biometric/travel pattern analysis for recruitment indicators",
            "Machine learning entity resolution across jurisdictions",
        ]:
            st.markdown(f"<div style='font-size:12px;color:#6b7599;padding:3px 0'>◌ &nbsp;{item}</div>", unsafe_allow_html=True)
