"""
sample_data.py — All dummy intelligence data lives here.
=========================================================
HOW TO REPLACE WITH YOUR OWN DATA
-----------------------------------
Each function returns a pandas DataFrame. You can swap any
function body with:  return pd.read_csv("path/to/your.csv")

Required columns are documented above each function.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ── Entities ──────────────────────────────────────────────────────────────────
# Required columns:
#   name, category, region, lat, lon, summary, source, source_confidence,
#   source_type, ttps (list), date_identified,
#   Risk scoring inputs (0–10 each):
#     conflict_relevance, sanctions_exposure, dual_use_sensitivity,
#     military_use_evidence, intermediary_risk, transshipment_risk, source_confidence_score

def get_entities() -> pd.DataFrame:
    data = [
        {
            "name": "Shenzhen / Zhuhai OEM cluster",
            "category": "Procurement network",
            "region": "China",
            "lat": 22.5, "lon": 114.1,
            "summary": "Primary source of FPV motors, ESCs, flight controllers, GPS modules. DJI, BetaFPV, iFlight, Autel. Components sold openly on Alibaba/AliExpress with no end-use verification. China dominates permanent magnet production for motors, mature semiconductors, and sensors.",
            "source": "RUSI 2025; Atlantic Council 2024",
            "source_confidence": "High",
            "source_type": "Academic/research",
            "ttps": ["Marketplace sourcing", "Dual-use concealment", "Electronics distributor sourcing"],
            "date_identified": datetime(2023, 1, 10),
            "conflict_relevance": 9, "sanctions_exposure": 7, "dual_use_sensitivity": 9,
            "military_use_evidence": 8, "intermediary_risk": 5, "transshipment_risk": 6,
            "source_confidence_score": 9,
        },
        {
            "name": "Hong Kong shell company cluster",
            "category": "Procurement network",
            "region": "Hong Kong",
            "lat": 22.3, "lon": 114.2,
            "summary": "178+ companies used in 672 sanctioned shipments Jan 2024–Mar 2025 (OCCRP). BIS added entire addresses to Entity List June 2024 after identifying pattern of shell companies at common addresses. Generic trading company names, no digital footprint.",
            "source": "OCCRP 2026; CNAS 2025; BIS Entity List",
            "source_confidence": "High",
            "source_type": "Government",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Logistics/transshipment routing"],
            "date_identified": datetime(2022, 10, 5),
            "conflict_relevance": 9, "sanctions_exposure": 10, "dual_use_sensitivity": 8,
            "military_use_evidence": 9, "intermediary_risk": 10, "transshipment_risk": 9,
            "source_confidence_score": 10,
        },
        {
            "name": "UAE financial intermediary network",
            "category": "Transshipment hub",
            "region": "UAE",
            "lat": 24.5, "lon": 54.4,
            "summary": "Primary Gulf transshipment and financial intermediation node. Front companies process payments for sanctioned goods. Nov 2025 OFAC action named UAE entities in Iran UAV network. FinCEN 2025 advisory explicitly flags UAE transactions.",
            "source": "FinCEN Advisory 2025; OFAC Nov 2025",
            "source_confidence": "High",
            "source_type": "Government",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Sanctioned entity proximity"],
            "date_identified": datetime(2022, 9, 1),
            "conflict_relevance": 9, "sanctions_exposure": 10, "dual_use_sensitivity": 7,
            "military_use_evidence": 8, "intermediary_risk": 10, "transshipment_risk": 10,
            "source_confidence_score": 10,
        },
        {
            "name": "Turkey banking and transit corridor",
            "category": "Transshipment hub",
            "region": "Turkey",
            "lat": 39.9, "lon": 32.9,
            "summary": "Turkish bank accounts used to obscure revenue origin in Russian procurement (Kharon 2026). Turkey has not joined Western sanctions on Russia or Iran, creating legal financial pathway exploitable for illicit transactions. Turkish straw-buyer companies documented.",
            "source": "Kharon 2026; IFI 2025",
            "source_confidence": "High",
            "source_type": "OSINT community",
            "ttps": ["Shell/front company procurement", "Re-export routing", "Logistics/transshipment routing"],
            "date_identified": datetime(2022, 8, 20),
            "conflict_relevance": 8, "sanctions_exposure": 7, "dual_use_sensitivity": 6,
            "military_use_evidence": 7, "intermediary_risk": 8, "transshipment_risk": 9,
            "source_confidence_score": 8,
        },
        {
            "name": "Central Asia re-export corridor",
            "category": "Transshipment hub",
            "region": "Central Asia",
            "lat": 48.0, "lon": 66.9,
            "summary": "Kazakhstan, Armenia, Georgia, Uzbekistan. Dramatic post-2022 import spikes of EU/US electronics correlated with onward re-export to Russia. Not subject to Western sanctions regimes. Defcon Level sanctions tracker flags as key evasion corridor.",
            "source": "Defcon Level 2025; IFI 2025",
            "source_confidence": "Medium",
            "source_type": "Academic/research",
            "ttps": ["Re-export routing", "Logistics/transshipment routing", "Dual-use concealment"],
            "date_identified": datetime(2022, 11, 15),
            "conflict_relevance": 8, "sanctions_exposure": 8, "dual_use_sensitivity": 7,
            "military_use_evidence": 7, "intermediary_risk": 7, "transshipment_risk": 9,
            "source_confidence_score": 7,
        },
        {
            "name": "Iran IRGC / HESA Isfahan",
            "category": "Production node",
            "region": "Iran",
            "lat": 32.4, "lon": 51.7,
            "summary": "HESA Isfahan: est. 150–250 Shahed units/month. KIPAS network designated Nov 2025. Iran–Russia barter payments in gold confirmed via IRGC email breach. Imports ~$10M drone-relevant components per 2-month window. BeiDou access granted 2021.",
            "source": "OFAC Nov 2025; Iran International 2024",
            "source_confidence": "High",
            "source_type": "Government",
            "ttps": ["Commercial drone modification", "Sanctioned entity proximity", "Electronics distributor sourcing"],
            "date_identified": datetime(2022, 9, 15),
            "conflict_relevance": 10, "sanctions_exposure": 10, "dual_use_sensitivity": 9,
            "military_use_evidence": 10, "intermediary_risk": 9, "transshipment_risk": 8,
            "source_confidence_score": 10,
        },
        {
            "name": "Yelabuga SEZ, Tatarstan",
            "category": "Production node",
            "region": "Russia",
            "lat": 55.8, "lon": 52.1,
            "summary": "Russian Geran-2 production facility established under 2023 Iran-Russia agreement. Reported 6,000 airframe/year design capacity. Launched 1,000+ drones/week by Mar 2025. Assemblies almost entirely from Western components. LATAM-sourced labour documented.",
            "source": "CSIS 2026; OCCRP 2026; User research 2025",
            "source_confidence": "High",
            "source_type": "Media",
            "ttps": ["Commercial drone modification", "Sanctioned entity proximity"],
            "date_identified": datetime(2023, 3, 1),
            "conflict_relevance": 10, "sanctions_exposure": 10, "dual_use_sensitivity": 9,
            "military_use_evidence": 10, "intermediary_risk": 8, "transshipment_risk": 7,
            "source_confidence_score": 9,
        },
        {
            "name": "LATAM labour pipeline to Russia",
            "category": "Labour pipeline",
            "region": "Latin America",
            "lat": -14.2, "lon": -51.9,
            "summary": "Individuals sourced from Latin America recruited to travel to production facilities in Russia (Yelabuga SEZ and related sites) for drone assembly work. Exploits legal travel corridors. Avoids sanctions on Russian nationals performing military-industrial work.",
            "source": "User research 2025",
            "source_confidence": "Medium",
            "source_type": "OSINT community",
            "ttps": ["Shell/front company procurement", "Logistics/transshipment routing"],
            "date_identified": datetime(2024, 6, 1),
            "conflict_relevance": 8, "sanctions_exposure": 6, "dual_use_sensitivity": 5,
            "military_use_evidence": 7, "intermediary_risk": 7, "transshipment_risk": 5,
            "source_confidence_score": 5,
        },
        {
            "name": "Sudan RSF drone acquisition",
            "category": "Conflict zone",
            "region": "Africa",
            "lat": 15.6, "lon": 32.5,
            "summary": "Rapid Support Forces acquired Chinese CH-4 drones, Serbian Yugoimport mortar drones (via UAE), Russian FPV quadcopters, Chinese Sunflower suicide drones. Drone used in assassination attempt on Gen. Burhan July 2024.",
            "source": "Africa Center for Strategic Studies 2026",
            "source_confidence": "High",
            "source_type": "Academic/research",
            "ttps": ["Commercial drone modification", "Re-export routing"],
            "date_identified": datetime(2023, 5, 1),
            "conflict_relevance": 10, "sanctions_exposure": 6, "dual_use_sensitivity": 7,
            "military_use_evidence": 10, "intermediary_risk": 6, "transshipment_risk": 7,
            "source_confidence_score": 8,
        },
        {
            "name": "Sahel non-state FPV use",
            "category": "Conflict zone",
            "region": "Africa",
            "lat": 13.5, "lon": -2.1,
            "summary": "JNIM and ISGS using commercial FPVs to drop IEDs in Burkina Faso, Mali. Feb 2025 JNIM attack at Djibo used FPVs with IEDs made from plastic bottles. Components via open commercial channels — no realistic export control interdict.",
            "source": "Africa Center for Strategic Studies 2026",
            "source_confidence": "High",
            "source_type": "Academic/research",
            "ttps": ["Commercial drone modification", "Marketplace sourcing"],
            "date_identified": datetime(2023, 8, 10),
            "conflict_relevance": 9, "sanctions_exposure": 3, "dual_use_sensitivity": 8,
            "military_use_evidence": 9, "intermediary_risk": 3, "transshipment_risk": 3,
            "source_confidence_score": 8,
        },
        {
            "name": "Malaysia transshipment — tariff evasion",
            "category": "Transshipment hub",
            "region": "Southeast Asia",
            "lat": 4.2, "lon": 108.0,
            "summary": "Chinese drone tariff evasion via transshipment. Exported ~0 drones to US pre-2022; 242,000 units 2022; 565,000 first 11 months 2023 (Congressional letter Mar 2024). Probable overlap with export control evasion.",
            "source": "Atlantic Council 2024; US Congress 2024",
            "source_confidence": "High",
            "source_type": "Government",
            "ttps": ["Re-export routing", "Dual-use concealment", "Logistics/transshipment routing"],
            "date_identified": datetime(2023, 6, 1),
            "conflict_relevance": 5, "sanctions_exposure": 7, "dual_use_sensitivity": 7,
            "military_use_evidence": 4, "intermediary_risk": 8, "transshipment_risk": 9,
            "source_confidence_score": 9,
        },
        {
            "name": "Ukrainian conflict theater",
            "category": "Conflict zone",
            "region": "Ukraine",
            "lat": 48.4, "lon": 31.2,
            "summary": "Primary Geran-2 strike theater. Russia launched 38,000+ Shaheds in 2025; 1,000+/week by Mar 2025. Ukraine forensic analysis: 57 Western components per Shahed-136. 92-94% interception rate by layered air defense.",
            "source": "CSIS 2026; Ukraine DIU; OCCRP 2026",
            "source_confidence": "High",
            "source_type": "Government",
            "ttps": ["Commercial drone modification"],
            "date_identified": datetime(2022, 9, 13),
            "conflict_relevance": 10, "sanctions_exposure": 8, "dual_use_sensitivity": 8,
            "military_use_evidence": 10, "intermediary_risk": 5, "transshipment_risk": 5,
            "source_confidence_score": 10,
        },
    ]
    df = pd.DataFrame(data)
    df["date_identified"] = pd.to_datetime(df["date_identified"])
    return df


# ── Incidents ─────────────────────────────────────────────────────────────────
# Required columns:
#   date, location, region, lat, lon, incident_type, description, source, confidence

def get_incidents() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    base = datetime(2022, 9, 1)

    regions = {
        "Ukraine":   (49.0, 31.0, 4.0),
        "Africa":    (13.5, 20.0, 10.0),
        "Middle East":(28.0, 45.0, 6.0),
        "Russia":    (55.0, 50.0, 5.0),
        "Southeast Asia":(10.0, 108.0, 5.0),
    }
    types = ["Strike / loitering munition", "Reconnaissance / ISR",
             "Component seizure", "Interdiction / interception",
             "Procurement flagged"]

    rows = []
    n = 320
    # Weight incidents heavily toward Ukraine and Africa
    region_weights = [0.45, 0.25, 0.10, 0.12, 0.08]
    reg_names = list(regions.keys())
    chosen_regs = rng.choice(reg_names, size=n, p=region_weights)

    for i in range(n):
        reg = chosen_regs[i]
        lat_c, lon_c, spread = regions[reg]
        # Gradually increasing volume over time (weighted toward recent)
        days_since = int(rng.exponential(scale=400))
        days_since = min(days_since, 960)
        date = base + timedelta(days=days_since)
        rows.append({
            "date": date,
            "location": f"{reg} — incident {i+1}",
            "region": reg,
            "lat": lat_c + rng.normal(0, spread),
            "lon": lon_c + rng.normal(0, spread),
            "incident_type": rng.choice(types, p=[0.4,0.25,0.15,0.12,0.08]),
            "description": f"Sample incident record — replace with OSINT data.",
            "source": rng.choice(["Ukraine DIU","Africa Center","OCCRP","Media report","CAR"]),
            "confidence": rng.choice(["High","Medium","Low"]),
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


# ── Components ────────────────────────────────────────────────────────────────
# Required columns:
#   component_category, component_name, classification, common_suppliers, notes

def get_components() -> pd.DataFrame:
    data = [
        # Motors
        {"component_category":"Motors","component_name":"Brushless outrunner motors (2204–2806)","classification":"Dual-use","common_suppliers":"T-Motor, Emax, BrotherHobby (CN)","notes":"Used in both racing FPV and weaponised drones"},
        {"component_category":"Motors","component_name":"Permanent magnet motors (high-torque MALE UAV)","classification":"Sensitive dual-use","common_suppliers":"Chinese state manufacturers","notes":"China controls ~90% of rare earth magnet supply"},
        {"component_category":"Motors","component_name":"Standard DC hobby motors","classification":"Common civilian","common_suppliers":"Global","notes":"Low threat relevance"},
        # ESCs
        {"component_category":"ESCs","component_name":"BLHeli-S / KISS ESC (30A+)","classification":"Dual-use","common_suppliers":"Hobbywing, Flycolor (CN)","notes":"Found in weaponised FPV drones Ukraine theater"},
        {"component_category":"ESCs","component_name":"High-voltage ESC (>6S)","classification":"Sensitive dual-use","common_suppliers":"Hobbywing, APD (CN/US)","notes":"Required for larger military-grade systems"},
        # Flight controllers
        {"component_category":"Flight controllers","component_name":"F4 / F7 autopilot (Betaflight)","classification":"Dual-use","common_suppliers":"Matek, SpeedyBee, Holybro (CN)","notes":"Commercially ubiquitous; found in Shahed components"},
        {"component_category":"Flight controllers","component_name":"Pixhawk / ArduPilot stack","classification":"Sensitive dual-use","common_suppliers":"Holybro, CubePilot (US/CN)","notes":"Full autopilot; mission-planning capable"},
        {"component_category":"Flight controllers","component_name":"Custom IRGC autopilot modules","classification":"Military-adjacent","common_suppliers":"Iranian domestic (KIPAS network)","notes":"OFAC designated Nov 2025"},
        # GPS
        {"component_category":"GPS modules","component_name":"u-blox M8 / M9 series","classification":"Sensitive dual-use","common_suppliers":"u-blox AG (Switzerland)","notes":"Found in Shahed-136 wreckage; subject of sanctions"},
        {"component_category":"GPS modules","component_name":"BeiDou receiver modules","classification":"Sensitive dual-use","common_suppliers":"Chinese state / commercial","notes":"Iran granted BeiDou access 2021; used in Shahed nav upgrade"},
        {"component_category":"GPS modules","component_name":"Standard civilian GPS chips","classification":"Common civilian","common_suppliers":"MediaTek, Quectel (CN)","notes":"Lower precision; widely available"},
        # Telemetry
        {"component_category":"Telemetry systems","component_name":"SiK radio telemetry (433/915MHz)","classification":"Dual-use","common_suppliers":"RFDesign (AU), clones (CN)","notes":"Standard ArduPilot telemetry"},
        {"component_category":"Telemetry systems","component_name":"DJI OcuSync / O3 video link","classification":"Sensitive dual-use","common_suppliers":"DJI (CN)","notes":"Provides encrypted HD video; found in military configs"},
        # Batteries
        {"component_category":"Batteries","component_name":"LiPo 4S–6S (hobby grade)","classification":"Dual-use","common_suppliers":"Tattu, CNHL (CN)","notes":"Primary FPV power source"},
        {"component_category":"Batteries","component_name":"Li-ion 18650 / 21700 packs","classification":"Dual-use","common_suppliers":"Samsung SDI, CATL, Molicel","notes":"Used in longer-range systems; dual-use with EVs"},
        # Thermal optics
        {"component_category":"Thermal optics","component_name":"FLIR Boson / Lepton modules","classification":"Military-adjacent","common_suppliers":"Teledyne FLIR (US)","notes":"Export controlled; found in Russian UAV configs"},
        {"component_category":"Thermal optics","component_name":"Chinese thermal cores (Hikmicro, InfiRay)","classification":"Sensitive dual-use","common_suppliers":"Hikvision / Hikmicro (CN)","notes":"Lower-cost alternative emerging in conflict zones"},
        # Frames
        {"component_category":"Carbon frames","component_name":"3–7 inch FPV frames (CF)","classification":"Common civilian","common_suppliers":"Global (CN dominant)","notes":"Commodity item; freely available"},
        {"component_category":"Carbon frames","component_name":"Custom MALE airframes","classification":"Military-adjacent","common_suppliers":"Specialised mfr","notes":"Usually bespoke production"},
        # Anti-jam
        {"component_category":"Anti-jamming modules","component_name":"GPS anti-jam / anti-spoof modules","classification":"Military-adjacent","common_suppliers":"Controlled; US/EU export restriction","notes":"High-priority interdiction target"},
        {"component_category":"Anti-jamming modules","component_name":"Gyro-based INS backup","classification":"Sensitive dual-use","common_suppliers":"Chinese front cos. (OFAC Feb 2025)","notes":"Sanctioned in Feb 2025 OFAC action"},
    ]
    return pd.DataFrame(data)


# ── TTPs ──────────────────────────────────────────────────────────────────────
def get_ttp_entries() -> pd.DataFrame:
    data = [
        {
            "ttp_name": "Commercial drone modification",
            "category": "Weaponisation",
            "risk_level": "Critical",
            "description": "Off-the-shelf civilian drones modified with payload release mechanisms, FPV cameras, or explosive payloads. Requires minimal technical expertise. Documented extensively in Ukraine, Sahel, Sudan.",
            "indicators": [
                "Purchase of hobby drone accessories alongside payload-mount hardware",
                "3D printing of payload release brackets",
                "Bulk purchase of identical consumer FPV units",
            ],
            "example": "JNIM FPV-IED attack, Djibo, Burkina Faso, February 2025",
            "source": "Africa Center 2026; Ukraine DIU",
        },
        {
            "ttp_name": "Shell/front company procurement",
            "category": "Procurement evasion",
            "risk_level": "Critical",
            "description": "Purpose-built or repurposed legal entities used to purchase controlled components, obscure beneficial ownership, and generate false end-user certificates. Companies often have no operational history or digital footprint.",
            "indicators": [
                "Company registered <90 days before large order",
                "No website, LinkedIn presence, or trade reviews",
                "Registered address shared with other flagged entities (BIS address-level Entity List)",
                "Generic name ('Global Tech Trading Solutions LLC')",
            ],
            "example": "178 HK companies, 672 sanctioned shipments, Jan 2024–Mar 2025 (OCCRP)",
            "source": "OCCRP 2026; BIS Entity List June 2024",
        },
        {
            "ttp_name": "Marketplace sourcing",
            "category": "Procurement evasion",
            "risk_level": "High",
            "description": "Using open e-commerce platforms (Alibaba, AliExpress, eBay, specialist hobby sites) to purchase dual-use components without triggering distributor-level export controls. No formal KYC required.",
            "indicators": [
                "Bulk orders to freight forwarding addresses",
                "Multiple small orders below reporting thresholds (structuring)",
                "Shipping to residential or non-commercial addresses",
            ],
            "example": "Shahed-136 components sourced from public marketplaces per ISIS 2023 analysis",
            "source": "ISIS 2023; Ukraine DIU 2023",
        },
        {
            "ttp_name": "Re-export routing",
            "category": "Logistics evasion",
            "risk_level": "Critical",
            "description": "Goods exported legally to a non-sanctioned country, then re-exported with amended or falsified documentation to a sanctioned destination. Country of origin may be changed at transit point.",
            "indicators": [
                "Multiple transshipment legs with no commercial rationale",
                "Consignee is a freight forwarder rather than identified end-user",
                "Country of origin changed at UAE, Turkey, or Malaysia transit",
                "HS code altered between legs",
            ],
            "example": "Malaysia re-export of Chinese drones to avoid 25% US tariffs — 565,000 units 2023",
            "source": "Atlantic Council 2024; Congressional letter March 2024",
        },
        {
            "ttp_name": "Dual-use concealment",
            "category": "Documentation fraud",
            "risk_level": "High",
            "description": "Military-application components documented as civilian goods. False end-user certificates describe agricultural, surveying, or delivery drone applications to avoid enhanced scrutiny.",
            "indicators": [
                "Quantity inconsistent with stated civilian application (e.g. 5,000 GPS modules for 'agriculture')",
                "Operating spec (temperature range, shock resistance) inconsistent with civilian claim",
                "Component combination constituting a UAV subsystem (FC + ESC + motors + GPS)",
            ],
            "example": "u-blox cited 'civilian product dismantling' as route into Russian drones (u-blox statement 2024)",
            "source": "OCCRP 2026; u-blox 2024",
        },
        {
            "ttp_name": "Sanctioned entity proximity",
            "category": "Network risk",
            "risk_level": "Critical",
            "description": "Entities not themselves designated but sharing ownership, address, directors, or trade relationships with OFAC/BIS/EU-listed entities. EU/UK regulations extend liability below the 50% ownership threshold.",
            "indicators": [
                "Director also listed in OFAC action",
                "Same registered address as designated entity",
                "Transactions with entities listed in recent OFAC press releases",
                "Ownership chain reaches designated party below 50% threshold",
            ],
            "example": "KIPAS subsidiaries PARPO and ARIAPA designated Nov 2025 for proximity to IRGC-QF",
            "source": "OFAC Nov 2025; Kharon 2026",
        },
        {
            "ttp_name": "Electronics distributor sourcing",
            "category": "Procurement evasion",
            "risk_level": "High",
            "description": "Purchasing restricted components from authorised electronics distributors in countries without re-export controls, exploiting the gap between authorised sales and illegal end-use.",
            "indicators": [
                "Distributor sales to known transshipment-hub addresses",
                "Components ordered in excess of buyer's stated product line needs",
                "Buyer lacks verifiable operational presence",
            ],
            "example": "200,000+ illicit microelectronics shipments to Russia from US-brand distributors 2022–2024 (NYT investigation)",
            "source": "NYT 2024; IFI 2025",
        },
        {
            "ttp_name": "Logistics/transshipment routing",
            "category": "Logistics evasion",
            "risk_level": "High",
            "description": "Use of multi-leg logistics through non-sanctioned jurisdictions to obscure origin and final destination. Central Asia, UAE, and Turkey are the most documented corridors for Russia-bound goods.",
            "indicators": [
                "Kazakhstan/Armenia/Georgia volume spikes post-2022",
                "Freight forwarder as listed consignee",
                "CIPS payment system used for settlement",
                "Invoice currency changed between legs",
            ],
            "example": "Central Asia electronics imports surged post-Feb 2022 with documented onward re-export to Russia",
            "source": "Defcon Level 2025; IFI 2025",
        },
    ]
    return pd.DataFrame(data)


# ── Sources ───────────────────────────────────────────────────────────────────
def get_sources() -> pd.DataFrame:
    data = [
        {"source_name":"OCCRP","source_type":"OSINT community","confidence":"High","url":"https://occrp.org"},
        {"source_name":"OFAC SDN List","source_type":"Government","confidence":"High","url":"https://home.treasury.gov"},
        {"source_name":"BIS Entity List","source_type":"Government","confidence":"High","url":"https://bis.doc.gov"},
        {"source_name":"FinCEN Advisory 2025","source_type":"Government","confidence":"High","url":"https://fincen.gov"},
        {"source_name":"Atlantic Council","source_type":"Academic/research","confidence":"High","url":"https://atlanticcouncil.org"},
        {"source_name":"CSIS","source_type":"Academic/research","confidence":"High","url":"https://csis.org"},
        {"source_name":"RUSI","source_type":"Academic/research","confidence":"High","url":"https://rusi.org"},
        {"source_name":"Africa Center for Strategic Studies","source_type":"Academic/research","confidence":"High","url":"https://africacenter.org"},
        {"source_name":"Conflict Armament Research","source_type":"Academic/research","confidence":"High","url":"https://conflictarm.com"},
        {"source_name":"Kharon","source_type":"OSINT community","confidence":"High","url":"https://kharon.com"},
        {"source_name":"Ukraine DIU (War Sanctions Portal)","source_type":"Government","confidence":"High","url":"https://war.ukraine.ua"},
        {"source_name":"IFI 2025","source_type":"Academic/research","confidence":"High","url":"https://finintegrity.org"},
        {"source_name":"User research 2025","source_type":"OSINT community","confidence":"Medium","url":""},
    ]
    return pd.DataFrame(data)
