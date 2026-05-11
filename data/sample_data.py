"""
sample_data.py — Core intelligence datasets for UAS THREATMAP v3
=================================================================
Updated through May 2026.

DATA CLASSIFICATION NOTICE
This module contains a mixture of:
  [OSINT]     Open-source-reported and corroborated information
  [ASSESSED]  Analyst assessment based on pattern analysis
  [SYNTHETIC] Synthetic/demo data for visualization purposes
  [INFERRED]  Analytical inference from indirect indicators

For compliance, sanctions, export-control, OSINT, and intelligence-analysis
purposes only.

HOW TO REPLACE WITH YOUR OWN DATA
Each get_*() function returns pd.DataFrame.
Swap body with: return pd.read_csv("path/to/your.csv")
Required columns documented above each function.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ─────────────────────────────────────────────────────────────────────────────
# ENTITIES
# ─────────────────────────────────────────────────────────────────────────────

def get_entities() -> pd.DataFrame:
    data = [
        {
            "name": "Shenzhen / Pearl River Delta OEM cluster",
            "category": "Procurement network",
            "region": "China",
            "lat": 22.5, "lon": 114.1,
            "summary": "Observed pattern: primary manufacturing hub for FPV motors, ESCs, flight controllers, GPS modules, composite frames. DJI, BetaFPV, iFlight, Autel, T-Motor documented. China's 2023-24 export controls on drone-related items represent a formal restriction layer; open-source reporting indicates ongoing grey-market flows. Permanent magnet supply dependency creates geopolitically significant chokepoint leveraged selectively.",
            "source": "RUSI Nov 2025; Atlantic Council Mar 2026; US-China ESRC Nov 2025",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Marketplace sourcing", "Dual-use concealment", "Electronics distributor sourcing"],
            "date_identified": datetime(2022, 9, 1),
            "conflict_relevance": 10, "sanctions_exposure": 8, "dual_use_sensitivity": 10,
            "military_use_evidence": 9, "intermediary_risk": 6, "transshipment_risk": 7,
            "source_confidence_score": 10,
            "uncertainty_note": "Verified reporting; individual company culpability varies significantly.",
        },
        {
            "name": "Hong Kong shell company address clusters",
            "category": "Procurement network",
            "region": "Hong Kong",
            "lat": 22.32, "lon": 114.17,
            "summary": "Corroborated reporting: 178+ entities in 672 sanctioned shipments Jan 2024-Mar 2025 (OCCRP). BIS June 2024 novel response: added entire addresses to Entity List. Post-designation behavior: rapid re-registration at adjacent addresses or migration to Shenzhen/Guangzhou. Generic names, absent digital footprints, co-located directorships are recurring indicators.",
            "source": "OCCRP Mar 2026; CNAS Mar 2025; BIS Entity List Jun 2024",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Intermediary replacement"],
            "date_identified": datetime(2022, 10, 5),
            "conflict_relevance": 9, "sanctions_exposure": 10, "dual_use_sensitivity": 8,
            "military_use_evidence": 9, "intermediary_risk": 10, "transshipment_risk": 9,
            "source_confidence_score": 10,
            "uncertainty_note": "Well-corroborated pattern. Individual entity culpability requires case-by-case analysis.",
        },
        {
            "name": "Alibaba / AliExpress procurement corridor",
            "category": "Procurement network",
            "region": "China",
            "lat": 30.3, "lon": 120.2,
            "summary": "Observed pattern: open e-commerce marketplace procurement represents highest-volume, lowest-visibility channel for dual-use FPV components. No end-use verification at point of sale. Structuring behavior — multiple orders below $800 de minimis threshold — documented. Post-2024: increasing use of WeChat and Telegram procurement communities by conflict-zone actors.",
            "source": "ISIS Nov 2023; Ukraine DIU 2024; OCCRP methodology",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Marketplace sourcing", "Structuring", "Dual-use concealment"],
            "date_identified": datetime(2022, 11, 1),
            "conflict_relevance": 9, "sanctions_exposure": 7, "dual_use_sensitivity": 9,
            "military_use_evidence": 8, "intermediary_risk": 6, "transshipment_risk": 5,
            "source_confidence_score": 9,
            "uncertainty_note": "Pattern well-established; individual transaction attribution inherently limited.",
        },
        {
            "name": "Autel Robotics / Aero-HIT reported JV",
            "category": "Procurement network",
            "region": "China",
            "lat": 29.8, "lon": 121.5,
            "summary": "Emerging indicator (moderate confidence): Bloomberg July 2025 reported potential JV between Autel Robotics and sanctioned Russian drone company Aero-HIT to localize Autel production in Russia. If confirmed, represents technology-transfer pathway eliminating cross-border interdiction risk. Consistent with broader Chinese strategy of in-country production to minimize sanctions exposure.",
            "source": "Bloomberg Jul 2025; US-China ESRC Nov 2025",
            "source_confidence": "Medium", "source_type": "Media", "data_type": "ASSESSED",
            "ttps": ["Technology transfer JV", "Sanctioned entity proximity", "Intermediary replacement"],
            "date_identified": datetime(2025, 7, 1),
            "conflict_relevance": 8, "sanctions_exposure": 9, "dual_use_sensitivity": 8,
            "military_use_evidence": 7, "intermediary_risk": 9, "transshipment_risk": 4,
            "source_confidence_score": 6,
            "uncertainty_note": "Emerging indicator — reported but not independently corroborated as of assessment date.",
        },
        {
            "name": "UAE financial intermediary and re-export network",
            "category": "Transshipment hub",
            "region": "UAE",
            "lat": 24.5, "lon": 54.4,
            "summary": "Corroborated reporting: UAE is primary Gulf financial intermediation and re-export hub for Russian and Iranian procurement. OFAC Nov 2025 named UAE entities in Iran UAV network. FinCEN Jun 2025 advisory explicitly flags UAE-linked transactions. Post-2024: some actors observed migrating to Oman and Qatar as secondary hubs following enhanced UAE banking scrutiny.",
            "source": "FinCEN Jun 2025; OFAC Nov 2025; IFI Oct 2025",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Document fraud", "Intermediary replacement"],
            "date_identified": datetime(2022, 9, 1),
            "conflict_relevance": 9, "sanctions_exposure": 10, "dual_use_sensitivity": 8,
            "military_use_evidence": 8, "intermediary_risk": 10, "transshipment_risk": 10,
            "source_confidence_score": 10,
            "uncertainty_note": "Well-corroborated. Oman/Qatar secondary hub migration is an emerging indicator.",
        },
        {
            "name": "Turkey banking and transit corridor",
            "category": "Transshipment hub",
            "region": "Turkey",
            "lat": 39.9, "lon": 32.9,
            "summary": "Corroborated reporting: Turkish banking and transit geography exploited for dual-use goods routing to Russia. Straw-buyer companies and Turkish bank accounts documented (Kharon 2026). April 2025: Russian national sentenced to nearly 6 years for export violations using Turkish accounts. Post-2024: reported migration toward smaller regional banks and non-bank channels following US Treasury secondary sanctions pressure.",
            "source": "Kharon Feb 2026; IFI Oct 2025; DOJ Apr 2025",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Banking channel exploitation"],
            "date_identified": datetime(2022, 8, 20),
            "conflict_relevance": 8, "sanctions_exposure": 8, "dual_use_sensitivity": 7,
            "military_use_evidence": 7, "intermediary_risk": 8, "transshipment_risk": 9,
            "source_confidence_score": 9,
            "uncertainty_note": "Well-corroborated. Adaptation to smaller banks is assessed with emerging corroboration.",
        },
        {
            "name": "Kazakhstan re-export corridor",
            "category": "Transshipment hub",
            "region": "Central Asia",
            "lat": 51.2, "lon": 71.4,
            "summary": "Corroborated reporting: Kazakhstan recorded dramatic post-2022 import spikes in electronics consistent with Russian re-export. Not subject to Western sanctions. Recurring corridor: EU/US components exported to Kazakhstani trading companies, forwarded by road to Russia. Post-2024: US secondary sanctions pressure has partially constrained corridor; actors reportedly migrating to Kyrgyzstan and Uzbekistan.",
            "source": "Defcon Level May 2026; IFI Oct 2025; CNAS Mar 2025",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Re-export routing", "Logistics/transshipment routing", "Dual-use concealment"],
            "date_identified": datetime(2022, 11, 1),
            "conflict_relevance": 8, "sanctions_exposure": 8, "dual_use_sensitivity": 8,
            "military_use_evidence": 7, "intermediary_risk": 7, "transshipment_risk": 9,
            "source_confidence_score": 8,
            "uncertainty_note": "Corroborated. Kyrgyzstan/Uzbekistan migration is an assessed trend requiring monitoring.",
        },
        {
            "name": "Armenia and Georgia transit nodes",
            "category": "Transshipment hub",
            "region": "Central Asia",
            "lat": 40.2, "lon": 44.5,
            "summary": "Observed pattern: Armenia and Georgia serve as secondary re-export nodes for Russia-bound dual-use goods. Georgian banking under increased scrutiny following US advisories. Armenian entities documented in some procurement chains. Kyrgyzstan emerging as alternative. Pattern: goods imported under civilian declarations, transited by road/air, re-entered Russia via border crossings.",
            "source": "Defcon Level 2025; Reuters investigative 2024",
            "source_confidence": "Medium", "source_type": "Media", "data_type": "ASSESSED",
            "ttps": ["Re-export routing", "Logistics/transshipment routing", "Intermediary replacement"],
            "date_identified": datetime(2023, 3, 1),
            "conflict_relevance": 7, "sanctions_exposure": 7, "dual_use_sensitivity": 6,
            "military_use_evidence": 6, "intermediary_risk": 7, "transshipment_risk": 8,
            "source_confidence_score": 6,
            "uncertainty_note": "Moderate confidence. Entity-level corroboration incomplete in open-source record.",
        },
        {
            "name": "Iran IRGC / HESA Isfahan production complex",
            "category": "Production node",
            "region": "Iran",
            "lat": 32.4, "lon": 51.7,
            "summary": "Verified reporting: HESA Isfahan assessed at 150-250 Shahed-series units/month. KIPAS network (UAV component mfr) designated OFAC November 2025 alongside PARPO and ARIAPA subsidiaries. Ma Jie (China-based) sanctioned for coordinating Iranian defense officials with Chinese suppliers. Post-June 2025 12-Day War: Iran urgently reconstituting degraded capacity. February 2025: Chinese front companies sanctioned for supplying gyro navigation devices to enhance Iranian UAV guidance.",
            "source": "OFAC Nov 2025; OFAC Feb 2025; Atlantic Council Mar 2026",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Sanctioned entity proximity", "Electronics distributor sourcing", "Barter payment"],
            "date_identified": datetime(2022, 9, 15),
            "conflict_relevance": 10, "sanctions_exposure": 10, "dual_use_sensitivity": 9,
            "military_use_evidence": 10, "intermediary_risk": 9, "transshipment_risk": 8,
            "source_confidence_score": 10,
            "uncertainty_note": "Verified from government sanctions actions and corroborated OSINT.",
        },
        {
            "name": "Sahara Thunder — Iran-Russia UAV brokerage",
            "category": "Procurement network",
            "region": "Iran",
            "lat": 33.7, "lon": 51.4,
            "summary": "Verified reporting: front company designated OFAC April 2024 (with UK, Canada). Assessed as supporting IRGC and facilitating Shahed sales to Russia. IRGC server breach revealed drone-for-gold barter arrangements. Illustrative of layered front company structure separating Iranian state actors from visible commercial transactions.",
            "source": "OFAC Apr 2024; Iran International Jun 2024",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Shell/front company procurement", "Sanctioned entity proximity", "Barter payment"],
            "date_identified": datetime(2024, 4, 1),
            "conflict_relevance": 10, "sanctions_exposure": 10, "dual_use_sensitivity": 7,
            "military_use_evidence": 10, "intermediary_risk": 10, "transshipment_risk": 6,
            "source_confidence_score": 10,
            "uncertainty_note": "Verified — designated entity with corroborated breach reporting.",
        },
        {
            "name": "Yelabuga (Alabuga) SEZ — Geran-2 production",
            "category": "Production node",
            "region": "Russia",
            "lat": 55.8, "lon": 52.1,
            "summary": "Corroborated reporting: Yelabuga SEZ established as Russia's primary Geran-2 production facility under 2023 Iran-Russia technology transfer. Reported 6,000 airframe/year capacity. Russia launched 38,000+ Shaheds in 2025, 1,000+/week by March 2025 (CSIS). Satellite imagery confirms facility expansion 2023-24. Assemblies assessed as almost entirely Western-origin components via intermediary chains.",
            "source": "CSIS Feb 2026; OCCRP Mar 2026; Quwa May 2026",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Commercial drone modification", "Sanctioned entity proximity", "Technology transfer JV"],
            "date_identified": datetime(2023, 3, 1),
            "conflict_relevance": 10, "sanctions_exposure": 10, "dual_use_sensitivity": 9,
            "military_use_evidence": 10, "intermediary_risk": 8, "transshipment_risk": 7,
            "source_confidence_score": 9,
            "uncertainty_note": "Corroborated by multiple independent OSINT channels and satellite imagery.",
        },
        {
            "name": "LATAM foreign labor recruitment pathway",
            "category": "Labour pipeline",
            "region": "Latin America",
            "lat": -8.0, "lon": -55.0,
            "summary": "Reported recruitment pathway (low confidence): open-source reporting indicates individuals sourced from Latin American countries recruited to travel to Russian production facilities including Yelabuga for drone assembly roles. Exploits legal travel corridors. Circumvents sanctions targeting Russian nationals in military-industrial work. Analyst note: coercive recruitment elements are not confirmed in available open-source record; framing as voluntary industrial labor recruitment is more consistent with available indicators.",
            "source": "User research 2025; open-source labor migration reporting",
            "source_confidence": "Low", "source_type": "OSINT community", "data_type": "ASSESSED",
            "ttps": ["Foreign labor sourcing", "Logistics/transshipment routing"],
            "date_identified": datetime(2024, 6, 1),
            "conflict_relevance": 7, "sanctions_exposure": 6, "dual_use_sensitivity": 4,
            "military_use_evidence": 6, "intermediary_risk": 6, "transshipment_risk": 4,
            "source_confidence_score": 4,
            "uncertainty_note": "Low confidence — not corroborated by multiple independent sources. Coercive framing not supported by available open-source record. Treat as emerging indicator.",
        },
        {
            "name": "Alabuga SEZ — domestic FPV assembly",
            "category": "Production node",
            "region": "Russia",
            "lat": 55.75, "lon": 52.4,
            "summary": "Observed pattern: Alabuga SEZ (co-located with Yelabuga) assessed as hosting FPV drone assembly alongside Geran-2 production. Domestic Russian FPV capacity has grown significantly post-2023, reducing reliance on imported complete units while retaining dependence on imported components. Recruitment advertising for electronics assembly roles documented in Russian-language sources.",
            "source": "Militarnyi Feb 2024; open-source Russian recruitment postings",
            "source_confidence": "Medium", "source_type": "Media", "data_type": "ASSESSED",
            "ttps": ["Commercial drone modification", "Marketplace sourcing"],
            "date_identified": datetime(2023, 9, 1),
            "conflict_relevance": 9, "sanctions_exposure": 10, "dual_use_sensitivity": 8,
            "military_use_evidence": 9, "intermediary_risk": 6, "transshipment_risk": 5,
            "source_confidence_score": 6,
            "uncertainty_note": "Moderate confidence. Domestic FPV production growth is an assessed trend.",
        },
        {
            "name": "Ukraine conflict theater — primary UAV use zone",
            "category": "Conflict zone",
            "region": "Ukraine",
            "lat": 48.4, "lon": 31.2,
            "summary": "Verified reporting: primary operational theater for Geran-2/Shahed loitering munitions and FPV drones. Russia launched 38,000+ Shaheds in 2025; Ukraine documented 57 Western-origin components per Shahed-136. Ukraine became world's largest domestic FPV producer by output (2M+ units 2024). Conflict-zone wreckage analysis provides ground-truth component sourcing data for compliance analysis.",
            "source": "CSIS Feb 2026; Ukraine DIU; OCCRP Mar 2026",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Commercial drone modification"],
            "date_identified": datetime(2022, 9, 13),
            "conflict_relevance": 10, "sanctions_exposure": 8, "dual_use_sensitivity": 8,
            "military_use_evidence": 10, "intermediary_risk": 4, "transshipment_risk": 4,
            "source_confidence_score": 10,
            "uncertainty_note": "Verified — multiple independent corroborating sources.",
        },
        {
            "name": "Sudan RSF — multi-source drone acquisition",
            "category": "Conflict zone",
            "region": "Africa",
            "lat": 15.6, "lon": 32.5,
            "summary": "Corroborated reporting: RSF documented operating Chinese CH-4 drones, Serbian Yugoimport mortar UAVs (reportedly via UAE), Russian FPV quadcopters, and Chinese Sunflower suicide drones. Drone assassination attempt on General Burhan July 2024. This theater demonstrates non-state actor access to multiple simultaneous drone ecosystems from diverse sourcing chains.",
            "source": "Africa Center Feb 2026; Jane's 2025",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Commercial drone modification", "Re-export routing"],
            "date_identified": datetime(2023, 5, 1),
            "conflict_relevance": 10, "sanctions_exposure": 6, "dual_use_sensitivity": 7,
            "military_use_evidence": 10, "intermediary_risk": 6, "transshipment_risk": 7,
            "source_confidence_score": 8,
            "uncertainty_note": "Corroborated on platform types; specific RSF supply chain routing is partially assessed.",
        },
        {
            "name": "Sahel — non-state FPV IED deployment",
            "category": "Conflict zone",
            "region": "Africa",
            "lat": 13.5, "lon": -2.1,
            "summary": "Corroborated reporting: JNIM and ISGS using commercial FPV drones to drop IEDs in Burkina Faso, Mali, Niger. February 2025: JNIM FPV-IED attack at Djibo. Components sourced via open commercial channels — no realistic export-control interdiction path. Represents qualitatively different procurement challenge: no sanctions exposure, commodity technology, purely open-market acquisition.",
            "source": "Africa Center Feb 2026; ACLED 2025",
            "source_confidence": "High", "source_type": "Academic/research", "data_type": "OSINT",
            "ttps": ["Commercial drone modification", "Marketplace sourcing"],
            "date_identified": datetime(2023, 8, 10),
            "conflict_relevance": 9, "sanctions_exposure": 2, "dual_use_sensitivity": 8,
            "military_use_evidence": 9, "intermediary_risk": 2, "transshipment_risk": 2,
            "source_confidence_score": 9,
            "uncertainty_note": "Corroborated on use patterns; sourcing chain for specific actors undocumented.",
        },
        {
            "name": "Malaysia tariff-evasion transshipment",
            "category": "Transshipment hub",
            "region": "Southeast Asia",
            "lat": 4.2, "lon": 108.0,
            "summary": "Verified reporting: Chinese drone tariff evasion via Malaysian transshipment (Congressional letter Mar 2024). Malaysia: ~0 drone exports to US pre-2022; 242,000 units 2022; 565,000 in 11 months 2023. Pattern: Chinese OEMs routing through Malaysian entities to avoid 25% tariffs. Post-2024: some actors reportedly shifting to Vietnam and Thailand.",
            "source": "Atlantic Council Jun 2024; US Congressional Letter Mar 2024",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["Re-export routing", "Dual-use concealment", "Logistics/transshipment routing"],
            "date_identified": datetime(2023, 6, 1),
            "conflict_relevance": 5, "sanctions_exposure": 7, "dual_use_sensitivity": 7,
            "military_use_evidence": 4, "intermediary_risk": 8, "transshipment_risk": 9,
            "source_confidence_score": 9,
            "uncertainty_note": "Verified on tariff evasion. Export-control overlap is assessed.",
        },
        {
            "name": "India — emerging intermediary jurisdiction",
            "category": "Transshipment hub",
            "region": "Southeast Asia",
            "lat": 20.6, "lon": 78.9,
            "summary": "Emerging indicator (low-moderate confidence): India documented as intermediary in some Iranian procurement chains per OFAC November 2025 action. India's large electronics sector and non-sanction-aligned posture create structural facilitation capacity. Analyst note: India's complex posture — some tolerance of grey-zone trade alongside formal export control commitments — requires careful framing. Pattern requires further corroboration.",
            "source": "OFAC Nov 2025; analyst assessment",
            "source_confidence": "Low", "source_type": "Government", "data_type": "ASSESSED",
            "ttps": ["Re-export routing", "Electronics distributor sourcing"],
            "date_identified": datetime(2024, 11, 1),
            "conflict_relevance": 6, "sanctions_exposure": 7, "dual_use_sensitivity": 7,
            "military_use_evidence": 5, "intermediary_risk": 7, "transshipment_risk": 6,
            "source_confidence_score": 4,
            "uncertainty_note": "Low confidence. Emerging pattern requiring additional corroboration.",
        },
        {
            "name": "Shadow fleet maritime logistics network",
            "category": "Logistics node",
            "region": "Maritime",
            "lat": 40.0, "lon": 48.0,
            "summary": "Corroborated reporting: Russia operates shadow tanker fleet circumventing oil sanctions, generating revenue funding UAV procurement. UK NCA/OFSI issued Red Alert July 2025. AIS spoofing documented as standard evasion practice. Port clustering in UAE, Turkish straits, Indian Ocean documented. Connectivity indicator: some vessels using Starlink maritime terminals — potential OSINT enrichment data point.",
            "source": "UK NCA Jul 2025; CNAS Mar 2025; Windward maritime OSINT",
            "source_confidence": "High", "source_type": "Government", "data_type": "OSINT",
            "ttps": ["AIS spoofing", "Maritime evasion", "Logistics/transshipment routing"],
            "date_identified": datetime(2022, 12, 1),
            "conflict_relevance": 8, "sanctions_exposure": 9, "dual_use_sensitivity": 5,
            "military_use_evidence": 7, "intermediary_risk": 8, "transshipment_risk": 10,
            "source_confidence_score": 9,
            "uncertainty_note": "Corroborated on maritime evasion patterns. Individual vessel attribution requires primary source.",
        },
        {
            "name": "Starlink connectivity indicators",
            "category": "Connectivity indicator",
            "region": "Russia",
            "lat": 55.7, "lon": 37.6,
            "summary": "Contextual enrichment indicator (analyst inference, low standalone confidence): Starlink terminal use documented in Russian-occupied Ukrainian territories and reported in production-adjacent environments. As a contextual enrichment indicator, Starlink IP ranges in procurement-related communications from unexpected geographic locations may warrant additional scrutiny. Important caveat: Starlink IP attribution is inherently unreliable for precise geolocation. Corroborating indicator only — not standalone attribution.",
            "source": "Open-source technical community; analyst inference",
            "source_confidence": "Low", "source_type": "OSINT community", "data_type": "INFERRED",
            "ttps": ["Telecom enrichment indicator"],
            "date_identified": datetime(2023, 6, 1),
            "conflict_relevance": 5, "sanctions_exposure": 4, "dual_use_sensitivity": 3,
            "military_use_evidence": 4, "intermediary_risk": 3, "transshipment_risk": 3,
            "source_confidence_score": 3,
            "uncertainty_note": "Low confidence as standalone indicator. Valid only as contextual enrichment when combined with other signals.",
        },
    ]
    df = pd.DataFrame(data)
    df["date_identified"] = pd.to_datetime(df["date_identified"])
    return df


# ─────────────────────────────────────────────────────────────────────────────
# INCIDENTS (SYNTHETIC trendline data)
# ─────────────────────────────────────────────────────────────────────────────

def get_incidents() -> pd.DataFrame:
    """
    SYNTHETIC/demo incident data generated to illustrate realistic 2022-2026 trendlines.
    Volume distribution, incident types, and regional splits reflect documented real-world
    patterns. Individual incidents are not individually source-backed.
    Replace with sourced records for operational use.
    """
    rng = np.random.default_rng(42)
    base = pd.Timestamp("2022-09-01")
    end  = pd.Timestamp("2026-05-01")
    total_days = (end - base).days  # ~1338

    regions = {
        "Ukraine":       (49.0,  31.0, 4.5, 0.43),
        "Africa":        (13.5,  20.0, 10., 0.22),
        "Middle East":   (28.0,  45.0, 6.0, 0.10),
        "Russia":        (55.0,  50.0, 5.0, 0.11),
        "Southeast Asia":(10.0, 108.0, 5.0, 0.06),
        "Central Asia":  (43.0,  63.0, 6.0, 0.08),
    }
    type_pool = [
        ("Strike / loitering munition",      0.37),
        ("Reconnaissance / ISR",             0.23),
        ("Component seizure / interdiction", 0.17),
        ("Procurement flagged",              0.13),
        ("Wreckage / forensic analysis",     0.10),
    ]
    types, tprob = zip(*type_pool)
    sources_pool = ["Ukraine DIU","Africa Center","OCCRP","CAR","Media","CSIS","Kharon","ACLED"]

    rows, n = [], 580
    reg_names = list(regions.keys())
    reg_probs = [regions[r][3] for r in reg_names]
    chosen = rng.choice(reg_names, size=n, p=reg_probs)

    for i in range(n):
        reg = chosen[i]
        lat_c, lon_c, spread, _ = regions[reg]
        day = min(int(rng.exponential(scale=480)), total_days - 1)
        rows.append({
            "date":          base + pd.Timedelta(days=day),
            "location":      f"{reg} sector",
            "region":        reg,
            "lat":           round(float(lat_c + rng.normal(0, spread)), 3),
            "lon":           round(float(lon_c + rng.normal(0, spread)), 3),
            "incident_type": rng.choice(types, p=tprob),
            "description":   "[SYNTHETIC] Representative incident for visualization.",
            "source":        rng.choice(sources_pool),
            "confidence":    rng.choice(["High","Medium","Low"], p=[0.38,0.42,0.20]),
            "data_type":     "SYNTHETIC",
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# COMPONENTS (summary for Overview tab; full detail in component_data.py)
# ─────────────────────────────────────────────────────────────────────────────

def get_components() -> pd.DataFrame:
    data = [
        {"component_name": "Brushless outrunner motors",    "component_category": "Propulsion",         "classification": "Dual-use",          "notes": "T-Motor, Emax; documented in conflict-zone FPV drones"},
        {"component_name": "ESC BLHeli-S/32 (30A+)",        "component_category": "Propulsion",         "classification": "Dual-use",          "notes": "Hobbywing, Flycolor; found in Ukraine wreckage"},
        {"component_name": "u-blox M8/M9/F9 GPS",           "component_category": "Navigation/Control", "classification": "Sensitive dual-use", "notes": "Found in Shahed-136; u-blox enhanced controls post-2022"},
        {"component_name": "BeiDou receivers",               "component_category": "Navigation/Control", "classification": "Sensitive dual-use", "notes": "Iran BeiDou access granted 2021; Shahed nav upgrade"},
        {"component_name": "F4/F7 flight controllers",      "component_category": "Navigation/Control", "classification": "Dual-use",          "notes": "Matek, SpeedyBee; documented in conflict drones"},
        {"component_name": "Pixhawk/ArduPilot autopilot",   "component_category": "Navigation/Control", "classification": "Sensitive dual-use", "notes": "Full autonomous capability; ECCN 7A994"},
        {"component_name": "IMU (MEMS tactical grade)",     "component_category": "Navigation/Control", "classification": "Sensitive dual-use", "notes": "ECCN 7A003 for high-performance specs"},
        {"component_name": "Gyro INS backup modules",       "component_category": "Counter-Jamming",    "classification": "Military-adjacent",  "notes": "OFAC Feb 2025: Chinese suppliers designated for Iran UAV"},
        {"component_name": "Anti-jamming GNSS (AJ-GPS)",    "component_category": "Counter-Jamming",    "classification": "Military-adjacent",  "notes": "ECCN 7A994/ITAR; highest interdiction priority"},
        {"component_name": "FLIR Boson thermal module",     "component_category": "Sensors",            "classification": "Military-adjacent",  "notes": "ECCN 6A003; Teledyne FLIR enhanced controls"},
        {"component_name": "InfiRay/Hikmicro thermal",      "component_category": "Sensors",            "classification": "Sensitive dual-use", "notes": "Chinese substitute post-FLIR restriction; Hikvision Entity List"},
        {"component_name": "3-axis gimbal stabiliser",      "component_category": "Sensors",            "classification": "Dual-use",          "notes": "ISR payload indicator when combined with thermal camera"},
        {"component_name": "DJI O3/O4 Air Unit",            "component_category": "Communications",     "classification": "Sensitive dual-use", "notes": "DoD §1260H; BIS ICTS review ANPRM Jan 2025"},
        {"component_name": "ELRS/TBS Crossfire RC link",    "component_category": "Communications",     "classification": "Sensitive dual-use", "notes": "10-40km range; BVLOS-capable; documented in strike FPV"},
        {"component_name": "Military encrypted datalink",   "component_category": "Communications",     "classification": "Military-adjacent",  "notes": "ITAR USML Cat. XI; licence required all destinations"},
        {"component_name": "LiPo 4S-6S battery packs",     "component_category": "Power",              "classification": "Dual-use",          "notes": "Tattu, CNHL; conflict-zone documented"},
        {"component_name": "Li-ion 18650/21700 cells",     "component_category": "Power",              "classification": "Dual-use",          "notes": "EV/UAV supply chain overlap makes interdiction difficult"},
        {"component_name": "Carbon fiber FPV frames",       "component_category": "Airframe",           "classification": "Dual-use",          "notes": "Commodity; bulk quantity + combination is the signal"},
        {"component_name": "MALE composite fuselage",       "component_category": "Airframe",           "classification": "Sensitive dual-use", "notes": "MTCR Cat. I if range/payload thresholds met"},
        {"component_name": "Texas Instruments / ADI chips", "component_category": "Electronics",        "classification": "Sensitive dual-use", "notes": "Found in Shahed-136 wreckage; key interdiction target"},
        {"component_name": "SiK telemetry 433/915MHz",     "component_category": "Communications",     "classification": "Dual-use",          "notes": "Standard ArduPilot link; Chinese clones widespread"},
        {"component_name": "PCB / custom electronics",     "component_category": "Electronics",        "classification": "Dual-use",          "notes": "Custom PCB ordering via JLCPCB, PCBWay is an indicator"},
    ]
    return pd.DataFrame(data)


# ─────────────────────────────────────────────────────────────────────────────
# TTPs
# ─────────────────────────────────────────────────────────────────────────────

def get_ttp_entries() -> pd.DataFrame:
    data = [
        {
            "ttp_name": "Shell/front company procurement",
            "category": "Procurement evasion", "risk_level": "Critical",
            "description": "Recurring pattern: purpose-built legal entities to purchase controlled components, obscure beneficial ownership, generate false EUCs. Post-2024 adaptation: faster entity cycling, migration to jurisdictions with weaker beneficial ownership registries.",
            "indicators": ["Entity <90 days old before large order","No digital presence discoverable","Address on BIS Entity List","Generic company name","Director in prior OFAC/BIS action"],
            "example": "178 HK companies, 672 sanctioned shipments Jan 2024-Mar 2025 (OCCRP)",
            "source": "OCCRP Mar 2026; BIS Entity List Jun 2024",
        },
        {
            "ttp_name": "Intermediary replacement / phoenix cycling",
            "category": "Procurement evasion", "risk_level": "Critical",
            "description": "Observed pattern: following designation, networks rapidly establish replacement entities at adjacent addresses with overlapping directorships or in secondary jurisdictions. Observed cycling time: 2-6 weeks post-designation.",
            "indicators": ["New entity at/near recently designated address","Shared director with designated entity","Same commodity flows via new identity","Migration pattern: HK→Shenzhen→Kyrgyzstan"],
            "example": "Post-designation HK entity migration documented in multiple OCCRP investigations",
            "source": "OCCRP Mar 2026; CNAS Mar 2025; Kharon Feb 2026",
        },
        {
            "ttp_name": "Marketplace sourcing and structuring",
            "category": "Procurement evasion", "risk_level": "High",
            "description": "Open e-commerce platforms used to purchase dual-use components without distributor-level controls. Structuring: multiple orders below $800 de minimis. Post-2024: Telegram/WeChat procurement communities increasingly used by conflict-zone actors.",
            "indicators": ["Bulk orders to freight-forwarding addresses","Multiple orders below $800 from same buyer","Shipping to residential addresses","Account <30 days old for bulk order"],
            "example": "Shahed component sourcing via public marketplaces (ISIS Nov 2023)",
            "source": "ISIS Nov 2023; Ukraine DIU 2024",
        },
        {
            "ttp_name": "Re-export routing via transshipment hub",
            "category": "Logistics evasion", "risk_level": "Critical",
            "description": "Recurring corridor: goods legally exported to non-sanctioned jurisdiction, re-exported with amended documentation to sanctioned destination. Primary hubs: UAE, Turkey, HK, Kazakhstan, Malaysia. Post-2024 adaptation: Oman, Qatar, Kyrgyzstan, Vietnam as secondary hubs.",
            "indicators": ["Multi-leg shipment with no commercial rationale","Consignee is freight forwarder","Country of origin changed at transit","HS code altered between legs","Volume spike at transit inconsistent with local demand"],
            "example": "Malaysia: 565,000 Chinese drone re-exports to US 2023 (Congressional letter)",
            "source": "Atlantic Council Jun 2024; IFI Oct 2025; Defcon Level May 2026",
        },
        {
            "ttp_name": "Dual-use concealment / false EUC",
            "category": "Documentation fraud", "risk_level": "High",
            "description": "Military-application components documented as civilian goods. Common misclassification: HS code manipulation, civilian-application EUC for specs inconsistent with claimed use.",
            "indicators": ["Quantity inconsistent with stated civilian scale","Specs (temp, shock) inconsistent with civilian claim","Component combination forming UAV subsystem","EUC from entity with no documented sector operation"],
            "example": "u-blox components in Shahed via 'civilian product' channel (2024)",
            "source": "OCCRP Mar 2026; u-blox 2024",
        },
        {
            "ttp_name": "Technology transfer / in-country JV production",
            "category": "Production evasion", "risk_level": "Critical",
            "description": "Observed and assessed: rather than shipping components, actors establish JVs or technology-transfer agreements to produce locally in sanctioned jurisdictions. Eliminates cross-border interdiction risk. Documented for Iran-Russia (Yelabuga). Emerging for China-Russia. Most difficult interdiction challenge in current regime.",
            "indicators": ["JV/licensing between sanctioned entity and foreign OEM","Production equipment procurement by sanctioned entity","Foreign technical personnel travel to sanctioned country","Rapid domestic production growth inconsistent with prior capability"],
            "example": "Iran-Russia Yelabuga facility; reported Autel/Aero-HIT JV Jul 2025",
            "source": "CSIS Feb 2026; Bloomberg Jul 2025; US-China ESRC Nov 2025",
        },
        {
            "ttp_name": "Barter / non-USD payment channels",
            "category": "Financial evasion", "risk_level": "High",
            "description": "Documented: Russia-Iran arms transactions via gold barter (confirmed per IRGC server breach). CIPS as alternative to SWIFT for RMB transactions. Significance: transactions outside SWIFT/USD are substantially harder for US financial intelligence to monitor.",
            "indicators": ["Commodity shipments accompanying arms deliveries","CIPS-settled transactions for dual-use goods","Invoice currency changed between legs","Cryptocurrency used for component payments"],
            "example": "Russia-Iran gold-for-drones barter confirmed via IRGC email breach (2024)",
            "source": "IFI Oct 2025; US-China ESRC Nov 2025; Iran International",
        },
        {
            "ttp_name": "AIS spoofing and maritime evasion",
            "category": "Logistics evasion", "risk_level": "High",
            "description": "Corroborated: shadow fleet vessels falsely broadcast AIS positions in permitted waters while transiting restricted zones. Port clustering at UAE, Turkish straits, Indian Ocean documented. Starlink terminal connectivity noted as potential OSINT enrichment indicator.",
            "indicators": ["AIS position gap >12hr in restricted zone","Position inconsistent with last known port","Vessel ownership chain reaches sanctioned beneficial owner","Starlink terminal in unusual jurisdiction for vessel flag"],
            "example": "UK NCA shadow fleet Red Alert Jul 2025; Windward AIS spoofing datasets",
            "source": "UK NCA Jul 2025; OFSI Jul 2025",
        },
        {
            "ttp_name": "Electronics distributor gap exploitation",
            "category": "Procurement evasion", "risk_level": "High",
            "description": "Recurring: authorized distributors sell to legitimate-appearing buyers in non-sanctioned jurisdictions; goods diverted downstream. 200,000+ illicit microelectronics shipments to Russia via this pathway 2022-2024 (NYT). Most components are EAR99 and require no licence.",
            "indicators": ["Distributor sales to transshipment-hub addresses","Buyer volume exceeds plausible operational requirement","Buyer lacks verifiable operational presence","Repeat orders at intervals suggesting re-export not internal use"],
            "example": "$4B+ controlled chips to Russia via distributor chains 2022-24 (NYT 2024)",
            "source": "NYT 2024; IFI Oct 2025; Kharon Feb 2026",
        },
        {
            "ttp_name": "Foreign labor / industrial workforce sourcing",
            "category": "Production evasion", "risk_level": "Moderate",
            "description": "Reported recruitment pathway (low-moderate confidence): foreign nationals recruited to Russian production facilities for assembly roles. Exploits legal travel corridors; circumvents sanctions on Russian military-industrial workers. Analyst note: coercive elements not confirmed in open-source record; framing as voluntary industrial recruitment is more consistent with available indicators.",
            "indicators": ["Recruitment advertising in foreign-language platforms for assembly roles in Russia","Visa applications from unexpected source countries to Russia","Social media posts from recruits at identifiable facilities","Remittance flows from Russia to source countries"],
            "example": "Reported LATAM recruitment for Yelabuga/Alabuga (user research 2025, low confidence)",
            "source": "User research 2025; open-source labor migration indicators",
        },
    ]
    return pd.DataFrame(data)


# ─────────────────────────────────────────────────────────────────────────────
# SOURCES
# ─────────────────────────────────────────────────────────────────────────────

def get_sources() -> pd.DataFrame:
    data = [
        {"source_name": "OFAC SDN / Consolidated List",      "source_type": "Government",        "confidence": "High",   "url": "https://home.treasury.gov"},
        {"source_name": "BIS Entity List",                   "source_type": "Government",        "confidence": "High",   "url": "https://bis.doc.gov"},
        {"source_name": "FinCEN Advisory Jun 2025",          "source_type": "Government",        "confidence": "High",   "url": "https://fincen.gov"},
        {"source_name": "OCCRP Mar 2026",                    "source_type": "OSINT community",   "confidence": "High",   "url": "https://occrp.org"},
        {"source_name": "CSIS Feb 2026",                     "source_type": "Academic/research", "confidence": "High",   "url": "https://csis.org"},
        {"source_name": "RUSI Nov 2025",                     "source_type": "Academic/research", "confidence": "High",   "url": "https://rusi.org"},
        {"source_name": "Atlantic Council Mar 2026",         "source_type": "Academic/research", "confidence": "High",   "url": "https://atlanticcouncil.org"},
        {"source_name": "US-China ESRC Nov 2025",            "source_type": "Government",        "confidence": "High",   "url": "https://uscc.gov"},
        {"source_name": "Africa Center Feb 2026",            "source_type": "Academic/research", "confidence": "High",   "url": "https://africacenter.org"},
        {"source_name": "Conflict Armament Research",        "source_type": "Academic/research", "confidence": "High",   "url": "https://conflictarm.com"},
        {"source_name": "Kharon Feb 2026",                   "source_type": "OSINT community",   "confidence": "High",   "url": "https://kharon.com"},
        {"source_name": "Ukraine DIU / War Sanctions Portal","source_type": "Government",        "confidence": "High",   "url": "https://war.ukraine.ua"},
        {"source_name": "IFI Oct 2025",                      "source_type": "Academic/research", "confidence": "High",   "url": "https://finintegrity.org"},
        {"source_name": "CNAS Mar 2025",                     "source_type": "Academic/research", "confidence": "High",   "url": "https://cnas.org"},
        {"source_name": "Defcon Level May 2026",             "source_type": "OSINT community",   "confidence": "High",   "url": "https://defconlevel.com"},
        {"source_name": "UK NCA / OFSI Jul 2025",            "source_type": "Government",        "confidence": "High",   "url": "https://nationalcrimeagency.gov.uk"},
        {"source_name": "Quwa May 2026",                     "source_type": "Academic/research", "confidence": "Medium", "url": "https://quwa.org"},
        {"source_name": "ISIS Nov 2023",                     "source_type": "Academic/research", "confidence": "High",   "url": "https://isis-online.org"},
        {"source_name": "Bloomberg Jul 2025",                "source_type": "Media",             "confidence": "Medium", "url": "https://bloomberg.com"},
        {"source_name": "User research 2025",                "source_type": "OSINT community",   "confidence": "Low",    "url": ""},
        {"source_name": "SYNTHETIC / demo data",             "source_type": "Synthetic",         "confidence": "N/A",    "url": ""},
    ]
    return pd.DataFrame(data)
