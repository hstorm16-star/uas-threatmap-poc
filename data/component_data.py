"""
component_data.py — Granular drone component intelligence data
==============================================================
PURPOSE: Compliance, sanctions, export-control, and OSINT risk analysis only.
         No assembly instructions, build guidance, or operational content.

HOW TO REPLACE WITH YOUR OWN DATA
-----------------------------------
Replace get_component_intelligence() with:

    def get_component_intelligence():
        df = pd.read_csv("data/your_components.csv")
        # procurement_regions column: pipe-separated string → list
        df["procurement_regions"] = df["procurement_regions"].fillna("").apply(
            lambda x: [r.strip() for r in x.split("|") if r.strip()]
        )
        # red_flags column: pipe-separated string → list
        df["red_flags"] = df["red_flags"].fillna("").apply(
            lambda x: [r.strip() for r in x.split("|") if r.strip()]
        )
        return df

Required CSV columns:
  component_name, category, civilian_use_case, dual_use_relevance,
  sensitivity_level, procurement_risk_score (0-10), procurement_regions (pipe-sep),
  red_flags (pipe-sep), export_control_relevance, source_confidence,
  notes, source_url, control_regime
"""

import pandas as pd

# ── Sensitivity ordering (for sorting/filtering) ─────────────────────────────
SENSITIVITY_ORDER = {
    "Common civilian":    1,
    "Dual-use":           2,
    "Sensitive dual-use": 3,
    "Military-adjacent":  4,
}

SENSITIVITY_COLOR = {
    "Common civilian":    "#3ab87a",
    "Dual-use":           "#f0c040",
    "Sensitive dual-use": "#f07c2a",
    "Military-adjacent":  "#e8503a",
}

CATEGORY_ICON = {
    "Airframe / Structure":             "◻",
    "Propulsion":                       "◎",
    "Power Systems":                    "⬡",
    "Navigation / Control":             "◈",
    "Communications / Telemetry":       "◉",
    "Sensors / Payload-Adjacent":       "◆",
    "Counter-Jamming / Resilience":     "◇",
    "Manufacturing / Modification":     "◧",
}


def get_component_intelligence() -> pd.DataFrame:
    """
    Returns DataFrame of drone component intelligence records.
    All sensitivity and risk assessments are for compliance/OSINT purposes only.
    """
    records = [

        # ══════════════════════════════════════════════════════════════
        # 1. AIRFRAME / STRUCTURE
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "Carbon fiber FPV frames (3–7 inch)",
            "category": "Airframe / Structure",
            "civilian_use_case": "Racing drones, aerial photography, hobbyist builds",
            "dual_use_relevance": "Lightweight structural basis for weaponised FPV platforms. Low individual cost enables bulk procurement without triggering financial controls.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["China", "Hong Kong", "Southeast Asia"],
            "red_flags": [
                "Bulk orders of identical frame SKUs with no stated commercial application",
                "Purchase combined with FPV camera, motor, and ESC kits (subsystem combination)",
                "Shipping to freight-forwarding addresses rather than named businesses",
            ],
            "export_control_relevance": "Generally EAR99 / no ECCN; not subject to MTCR unless integrated into controlled UAS platform",
            "source_confidence": "High",
            "notes": "Commodity item; procurement risk is contextual — quantity and combination with other components is the key signal.",
            "source_url": "https://conflictarm.com",
            "control_regime": "EAR99",
        },
        {
            "component_name": "Fixed-wing composite fuselages (MALE-class)",
            "category": "Airframe / Structure",
            "civilian_use_case": "Aerial survey, agricultural monitoring, long-range ISR for civilian operators",
            "dual_use_relevance": "Structurally identical to military ISR/strike platforms. MALE-class airframes (>150 kg MTOW) trigger MTCR Category I thresholds.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "Turkey", "Iran", "Ukraine (pre-2022)"],
            "red_flags": [
                "Procurement of airframes with payload bay volumes inconsistent with stated civilian mission",
                "Buyers with no documented aviation operation or certification",
                "End-user certificate describes 'agricultural use' for platform with >300 km range",
            ],
            "export_control_relevance": "MTCR Category I if range ≥300 km and payload ≥500 kg. ECCN 9A012 may apply. Licence required for most destinations.",
            "source_confidence": "High",
            "notes": "MTCR Category I threshold is the key compliance tripwire. Range + payload combination determines control status.",
            "source_url": "https://mtcr.info",
            "control_regime": "MTCR Cat. I / ECCN 9A012",
        },
        {
            "component_name": "Propeller assemblies (folding, 5–15 inch)",
            "category": "Airframe / Structure",
            "civilian_use_case": "Photography drones, agricultural spray UAVs, delivery platforms",
            "dual_use_relevance": "Matched to motor/ESC combinations to infer intended platform class. Folding props indicate fixed-wing or VTOL; rigid high-pitch props indicate FPV/strike orientation.",
            "sensitivity_level": "Common civilian",
            "procurement_risk_score": 3,
            "procurement_regions": ["China", "Global"],
            "red_flags": [
                "High-pitch, reinforced propellers ordered in bulk with no hobbyist or commercial operator context",
                "Props sized for >10 kg payload platform ordered alongside unassociated electronics",
            ],
            "export_control_relevance": "Generally uncontrolled as standalone item; controlled when part of complete UAS export",
            "source_confidence": "High",
            "notes": "Standalone risk low. Context of co-procurement is the analytical lever.",
            "source_url": "",
            "control_regime": "EAR99 (standalone)",
        },
        {
            "component_name": "Composite materials (pre-preg carbon, Kevlar weave)",
            "category": "Airframe / Structure",
            "civilian_use_case": "Aerospace, automotive, sports equipment, wind turbine blades",
            "dual_use_relevance": "High-strength composites used in airframe fabrication for both civilian and military UAV programs. Pre-preg materials in particular require specialised curing equipment, suggesting organised production rather than hobbyist use.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["China", "South Korea", "Japan", "USA", "Germany"],
            "red_flags": [
                "Large volume orders routed through trading companies with no aerospace client list",
                "Procurement of composite alongside autoclave or curing equipment by non-aerospace entity",
                "Destination country with documented UAV production program and no legitimate aerospace industry",
            ],
            "export_control_relevance": "ECCN 1C010 applies to certain fibrous/filamentary materials. EAR licence may be required for controlled destinations.",
            "source_confidence": "High",
            "notes": "Bulk procurement of aerospace-grade composite by entities with no documented aerospace application is a meaningful red flag.",
            "source_url": "https://bis.doc.gov",
            "control_regime": "ECCN 1C010 (certain grades)",
        },
        {
            "component_name": "Mounting brackets and payload rails",
            "category": "Airframe / Structure",
            "civilian_use_case": "Camera mounting, sensor attachment, cargo hooks for delivery UAVs",
            "dual_use_relevance": "Payload release mechanisms and munitions rail attachments are structurally similar to civilian gimbal mounts. Modifications to accommodate drop mechanisms are a documented weaponisation pathway.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 4,
            "procurement_regions": ["China", "Ukraine (domestic manufacture)", "Global"],
            "red_flags": [
                "CNC-machined brackets ordered alongside drop-mechanism actuators",
                "Custom rail dimensions inconsistent with any commercially available camera/sensor",
                "3D-printed mount files described in procurement communications",
            ],
            "export_control_relevance": "Uncontrolled as standalone; controlled in context of complete weaponised UAS",
            "source_confidence": "Medium",
            "notes": "The Ukraine conflict has generated significant open-source documentation of payload bracket modification patterns.",
            "source_url": "https://war.ukraine.ua",
            "control_regime": "Context-dependent",
        },

        # ══════════════════════════════════════════════════════════════
        # 2. PROPULSION
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "Brushless outrunner motors (2204–2806 class)",
            "category": "Propulsion",
            "civilian_use_case": "FPV racing, aerial photography, hobbyist multi-rotor",
            "dual_use_relevance": "Direct propulsion component in weaponised FPV drones documented in Ukraine and Sahel conflicts. Low unit cost (~$10–40) enables bulk procurement under financial reporting thresholds.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Hong Kong", "Southeast Asia"],
            "red_flags": [
                "Orders of 500+ identical motor units with no documented commercial production line",
                "Procurement by entity with no hobbyist, photography, or agricultural operation",
                "Motor KV rating and diameter consistent with known weaponised FPV configurations",
                "Combined purchase with identically-spec'd ESCs and frames (subsystem kit signal)",
            ],
            "export_control_relevance": "Generally EAR99. MTCR may apply if integrated into platform meeting Category I/II thresholds.",
            "source_confidence": "High",
            "notes": "China dominates production. T-Motor, Emax, BrotherHobby are major suppliers documented in conflict-zone wreckage analysis.",
            "source_url": "https://rusi.org/explore-our-research/publications/research-papers/decoupling-supply-chains-china",
            "control_regime": "EAR99 (typically)",
        },
        {
            "component_name": "High-torque permanent magnet motors (MALE UAV class)",
            "category": "Propulsion",
            "civilian_use_case": "Large agricultural UAVs, industrial inspection platforms, cargo UAVs",
            "dual_use_relevance": "Required for >25 kg MTOW platforms. China controls ~90% of rare earth permanent magnet supply chain, creating both a procurement chokepoint and a surveillance opportunity.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "Germany", "Japan"],
            "red_flags": [
                "Motors sized for >25 kg platform procured by entity without demonstrated large-UAV operation",
                "Procurement via trading company rather than direct from named OEM",
                "End-user certificate does not match stated power requirements of declared application",
            ],
            "export_control_relevance": "ECCN 9A619 may apply for certain high-performance motors. China's 2023–2024 export controls restrict germanium and rare earth derivatives.",
            "source_confidence": "High",
            "notes": "Rare earth supply dependency creates a monitoring opportunity — large motor procurement requires supply chain access that is geographically concentrated.",
            "source_url": "https://static.rusi.org/rp-drone-supply-chains-china-nov-2025.pdf",
            "control_regime": "ECCN 9A619 (performance-dependent)",
        },
        {
            "component_name": "Electronic Speed Controllers — ESCs (BLHeli-S/32, 30A+)",
            "category": "Propulsion",
            "civilian_use_case": "FPV racing, multi-rotor photography, hobbyist builds",
            "dual_use_relevance": "Critical motor control component found in weaponised FPV wreckage. Hobbywing, Flycolor, and generic BLHeli-series ESCs documented in Ukraine conflict drones.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Hong Kong"],
            "red_flags": [
                "Bulk ESC purchase matching motor quantity (indicates complete propulsion kits, not spares)",
                "Current rating (amps) inconsistent with claimed civilian drone class",
                "Procurement routed via multiple intermediaries for a commodity component",
            ],
            "export_control_relevance": "Generally EAR99. No standalone control; context of complete UAS is the trigger.",
            "source_confidence": "High",
            "notes": "BLHeli firmware is open-source, enabling configuration for non-standard uses. High-amperage ESCs (60A+) indicate larger-platform propulsion.",
            "source_url": "https://conflictarm.com",
            "control_regime": "EAR99",
        },
        {
            "component_name": "Propellers — high-pitch FPV and MALE-class",
            "category": "Propulsion",
            "civilian_use_case": "Racing, photography, survey UAVs",
            "dual_use_relevance": "High-pitch carbon-fibre props optimised for speed and efficiency. Pitch/diameter combination signals intended platform class. Documented in conflict-zone drones.",
            "sensitivity_level": "Common civilian",
            "procurement_risk_score": 3,
            "procurement_regions": ["China", "Global"],
            "red_flags": [
                "Props sized for unmanned platforms >15 kg MTOW ordered without corresponding airframe documentation",
            ],
            "export_control_relevance": "Uncontrolled standalone",
            "source_confidence": "High",
            "notes": "Analytical value is in propeller size/pitch as a proxy for platform class inference.",
            "source_url": "",
            "control_regime": "EAR99",
        },

        # ══════════════════════════════════════════════════════════════
        # 3. POWER SYSTEMS
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "LiPo battery packs (4S–6S, 1300–6000 mAh)",
            "category": "Power Systems",
            "civilian_use_case": "FPV racing, aerial photography, hobbyist multi-rotor",
            "dual_use_relevance": "Primary energy source for small UAS/FPV platforms. High energy density enables significant flight endurance. Tattu, CNHL, and generic Chinese brands documented in conflict-zone platforms.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["China", "Hong Kong", "Southeast Asia"],
            "red_flags": [
                "Bulk purchase of identical cell-count packs with no hobbyist or commercial operator profile",
                "High-C-rating packs (>100C) inconsistent with photography or agricultural use",
                "Batteries shipped with no UN38.3 certification documentation",
            ],
            "export_control_relevance": "Generally uncontrolled; shipping regulations (IATA DGR) apply for air transport. High-capacity packs may require additional documentation.",
            "source_confidence": "High",
            "notes": "Lithium battery logistics are increasingly scrutinised post-Samsung Galaxy incident. Bulk orders via freight forwarders without proper DGR compliance are themselves a red flag.",
            "source_url": "",
            "control_regime": "IATA DGR (transport); EAR99 (export)",
        },
        {
            "component_name": "Li-ion 18650 / 21700 cell packs (high-capacity)",
            "category": "Power Systems",
            "civilian_use_case": "Electric vehicles, power tools, consumer electronics, e-bikes",
            "dual_use_relevance": "Used in longer-endurance UAV platforms where LiPo is impractical. Samsung SDI, CATL, Molicel cells documented in larger fixed-wing UAV platforms. Shares supply chain with EV sector — volume procurement is difficult to distinguish.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["China", "South Korea", "Japan"],
            "red_flags": [
                "Procurement of custom battery management systems alongside large cell quantities",
                "Cell specifications (high-discharge 10A+ continuous) inconsistent with stated EV/e-bike application",
                "Cells destined for entity with no documented consumer electronics or EV production",
            ],
            "export_control_relevance": "Generally EAR99. CATL and Hikvision-adjacent supply chains may attract additional scrutiny under ICTS review.",
            "source_confidence": "Medium",
            "notes": "The EV/UAV battery supply chain overlap makes this a particularly difficult interdiction target. Contextual signals are essential.",
            "source_url": "",
            "control_regime": "EAR99 (generally)",
        },
        {
            "component_name": "Battery Management Systems (BMS)",
            "category": "Power Systems",
            "civilian_use_case": "EV battery packs, industrial energy storage, aviation ground support",
            "dual_use_relevance": "Custom BMS design for multi-cell UAV packs indicates organised rather than hobbyist procurement. BMS design complexity scales with platform size and endurance requirements.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Taiwan", "South Korea"],
            "red_flags": [
                "Custom BMS procured alongside high cell-count packs by entity with no documented industrial application",
                "BMS voltage/current specifications inconsistent with declared end-use",
            ],
            "export_control_relevance": "Generally EAR99; specific configurations with encryption (for data logging) may attract ECCN 5A002 attention",
            "source_confidence": "Medium",
            "notes": "BMS procurement at scale implies production-line rather than individual-unit UAV assembly.",
            "source_url": "",
            "control_regime": "EAR99 (typically)",
        },
        {
            "component_name": "High-capacity charger systems (multi-port, 1000W+)",
            "category": "Power Systems",
            "civilian_use_case": "Racing team fleet operations, commercial UAV fleet management",
            "dual_use_relevance": "Multi-port, high-power chargers indicate fleet-scale operations rather than individual use. Documented in organised procurement for mass FPV drone production.",
            "sensitivity_level": "Common civilian",
            "procurement_risk_score": 4,
            "procurement_regions": ["China", "Global"],
            "red_flags": [
                "Orders of 50+ charger units with no documented commercial fleet operation",
                "Chargers configured for field-deployable power sources (12V DC input) rather than mains",
            ],
            "export_control_relevance": "Uncontrolled",
            "source_confidence": "Medium",
            "notes": "Fleet-scale charger procurement is a secondary indicator — valuable in combination with other signals.",
            "source_url": "",
            "control_regime": "Uncontrolled",
        },

        # ══════════════════════════════════════════════════════════════
        # 4. NAVIGATION / CONTROL
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "F4/F7 FPV flight controllers (Betaflight-compatible)",
            "category": "Navigation / Control",
            "civilian_use_case": "FPV racing, freestyle flying, aerial filming",
            "dual_use_relevance": "Primary flight control hardware for weaponised FPV platforms. Matek, SpeedyBee, and Holybro controllers documented in Ukraine conflict drones. Betaflight firmware is open-source and reconfigurable.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 7,
            "procurement_regions": ["China", "Hong Kong"],
            "red_flags": [
                "Bulk purchase of identical FC models without matching racing or photography business context",
                "FC configured with GPS hold and waypoint capability (indicates autonomous, not manual, operation)",
                "Procurement of FCs with disabled geofencing (custom firmware builds)",
            ],
            "export_control_relevance": "Generally EAR99. If integrated into autonomous system meeting MTCR thresholds, ECCN 7A994 or 9A012 may apply.",
            "source_confidence": "High",
            "notes": "The open-source nature of Betaflight firmware means hardware control is the primary lever — software cannot be interdicted.",
            "source_url": "https://conflictarm.com",
            "control_regime": "EAR99 (typically); ECCN 7A994 (autopilot context)",
        },
        {
            "component_name": "Pixhawk / ArduPilot autopilot stack",
            "category": "Navigation / Control",
            "civilian_use_case": "Professional survey UAVs, cargo drones, agricultural platforms, research",
            "dual_use_relevance": "Full autonomous flight capability including mission planning, waypoint navigation, and payload management. Used in both commercial and military ISR platforms globally.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "USA", "Global"],
            "red_flags": [
                "Procurement by entity with no documented autonomous UAV operation or research mandate",
                "Configuration files or parameter sets indicating armed payload control",
                "Bulk procurement without corresponding platform (airframe, motor) procurement from same entity",
            ],
            "export_control_relevance": "ECCN 7A994 applies to autopilot systems. Licence required for controlled destinations under EAR. MTCR Category II if integrated into controlled platform.",
            "source_confidence": "High",
            "notes": "CubePilot and Holybro are primary manufacturers. Open Hardware design means clones proliferate in uncontrolled supply chains.",
            "source_url": "https://ardupilot.org",
            "control_regime": "ECCN 7A994 / MTCR Cat. II",
        },
        {
            "component_name": "u-blox GPS/GNSS modules (M8, M9, F9 series)",
            "category": "Navigation / Control",
            "civilian_use_case": "Consumer GPS devices, automotive navigation, precision agriculture, surveying",
            "dual_use_relevance": "Found in Shahed-136 wreckage per multiple forensic analyses. u-blox (Switzerland) is the leading manufacturer. Precision GNSS enables accurate terminal guidance. M9/F9 series supports RTK — centimetre-level accuracy.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 9,
            "procurement_regions": ["China", "Hong Kong", "UAE", "Turkey"],
            "red_flags": [
                "Purchase through intermediary rather than direct from authorised u-blox distributor",
                "F9-series RTK modules ordered by entity without documented precision agriculture or surveying operation",
                "Volume orders routed via HK/UAE trading companies with no electronics retail history",
                "Buyer presents end-use as 'automotive' but procures evaluation kit quantities (not automotive production scale)",
            ],
            "export_control_relevance": "u-blox modules are subject to Swiss export controls and re-export restrictions. Specific modules may require licence for controlled destinations. U-blox implemented enhanced end-use monitoring post-Ukraine conflict.",
            "source_confidence": "High",
            "notes": "u-blox publicly acknowledged its modules were found in Iranian drones in Ukraine and implemented enhanced controls. Key interdiction target. M9 and above require documented end-use.",
            "source_url": "https://www.u-blox.com/en/about-us/compliance",
            "control_regime": "Swiss export control / EAR (re-export from US)",
        },
        {
            "component_name": "BeiDou GNSS receiver modules",
            "category": "Navigation / Control",
            "civilian_use_case": "Chinese domestic navigation, agriculture, transport, commercial IoT",
            "dual_use_relevance": "Iran granted BeiDou access by China in 2021. Provides positioning independent of GPS/GLONASS, evading jamming systems tuned to those frequencies. Increasingly found in Iranian-origin UAV platforms.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China"],
            "red_flags": [
                "BeiDou modules procured by entity in non-BeiDou-coverage region without stated logistics/transport application",
                "Combined procurement of BeiDou module with anti-jamming filter (counter-EW intent signal)",
            ],
            "export_control_relevance": "Subject to Chinese export controls. China has placed export restrictions on certain GNSS-related technologies (2023–2024 controls).",
            "source_confidence": "High",
            "notes": "BeiDou access is a state-level bilateral agreement, not a commercial procurement issue — but receiver modules flow through commercial channels.",
            "source_url": "https://www.atlanticcouncil.org/dispatches/from-drones-to-rocket-fuel-china-and-russia-are-helping-iran-through-supply-chains/",
            "control_regime": "Chinese export control",
        },
        {
            "component_name": "Inertial Measurement Units (IMUs)",
            "category": "Navigation / Control",
            "civilian_use_case": "Consumer electronics, gaming controllers, automotive, robotics, drones",
            "dual_use_relevance": "High-grade IMUs enable accurate navigation without GPS — critical for GPS-denied environments or against electronic warfare. MEMS IMUs are commodity; tactical-grade IMUs are controlled.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 7,
            "procurement_regions": ["USA", "Germany", "China", "Japan"],
            "red_flags": [
                "Tactical-grade IMU (bias stability <1 deg/hr) procured by non-aerospace entity",
                "IMU specifications exceed requirements of stated civilian UAV application by significant margin",
                "Procurement of IMU from defence-focused supplier by trading company",
            ],
            "export_control_relevance": "ECCN 7A994 (standard IMUs); ECCN 7A003 or 7A103 for high-performance inertial navigation systems. Licence required for controlled destinations.",
            "source_confidence": "High",
            "notes": "Performance specification is the key differentiator. Consumer-grade IMUs (InvenSense, Bosch) are uncontrolled; navigation-grade IMUs trigger EAR controls.",
            "source_url": "https://bis.doc.gov",
            "control_regime": "ECCN 7A003 / 7A103 (performance-dependent)",
        },
        {
            "component_name": "Servo controllers and actuator modules",
            "category": "Navigation / Control",
            "civilian_use_case": "RC aircraft, robotics, fixed-wing UAV control surfaces",
            "dual_use_relevance": "Control surface actuation for fixed-wing and VTOL platforms. High-precision servo controllers enable accurate guidance for larger platforms. Documented in Shahed components (servo drives cited in ISIS 2023 analysis).",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Japan", "Germany"],
            "red_flags": [
                "Servo specifications (torque, speed) inconsistent with stated hobby aircraft application",
                "Precision servo controllers (digital, feedback-controlled) ordered alongside autopilot hardware",
            ],
            "export_control_relevance": "Generally EAR99; ECCN may apply for high-performance actuators meeting 7A994 thresholds",
            "source_confidence": "High",
            "notes": "ISIS (Institute for Science and International Security) documented servo drives in Shahed-136 components, sourced from European manufacturers via intermediaries.",
            "source_url": "https://isis-online.org",
            "control_regime": "EAR99 (typically)",
        },

        # ══════════════════════════════════════════════════════════════
        # 5. COMMUNICATIONS / TELEMETRY
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "Long-range RC transmitters / receivers (ELRS, TBS Crossfire)",
            "category": "Communications / Telemetry",
            "civilian_use_case": "FPV racing, freestyle, long-range aerial photography",
            "dual_use_relevance": "ExpressLRS (open-source) and TBS Crossfire provide control range of 10–40+ km — far exceeding visual line of sight. Enables beyond-visual-line-of-sight (BVLOS) operation without secondary datalink. Documented in long-range FPV strike drones.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 7,
            "procurement_regions": ["China", "Germany (TBS)", "Global"],
            "red_flags": [
                "ELRS or Crossfire hardware ordered in bulk alongside full FPV kits",
                "Configuration for maximum power output (regulatory violation in many jurisdictions — itself a red flag)",
                "Combined with directional antenna for extended range (FPV attack profile)",
            ],
            "export_control_relevance": "Generally EAR99. Frequency-specific regulations apply in destination country (radio spectrum). ITAR may apply to certain encrypted military-variant datalinks.",
            "source_confidence": "High",
            "notes": "ELRS is open-source firmware running on commodity hardware, making it extremely difficult to control at the software level. Hardware procurement monitoring is the primary lever.",
            "source_url": "https://www.expresslrs.org",
            "control_regime": "EAR99; local radio spectrum regulation",
        },
        {
            "component_name": "Telemetry modules (SiK radio, 433/868/915 MHz)",
            "category": "Communications / Telemetry",
            "civilian_use_case": "UAV ground station connectivity, ArduPilot telemetry, MAVLink data link",
            "dual_use_relevance": "Standard ArduPilot/PX4 telemetry link — provides real-time flight data between platform and ground station. Enables mission monitoring and in-flight parameter adjustment. Documented in professional and conflict-use autonomous UAVs.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["Australia (RFDesign)", "China (clones)", "Global"],
            "red_flags": [
                "SiK radio modules procured alongside Pixhawk/ArduPilot autopilots by entity without UAV operation mandate",
                "Custom frequency configurations outside standard hobbyist or commercial bands",
            ],
            "export_control_relevance": "EAR99 for standard units. ITAR may apply to encrypted military-specification variants.",
            "source_confidence": "High",
            "notes": "SiK firmware is open-source. Clones from Chinese manufacturers are widely available at low cost.",
            "source_url": "",
            "control_regime": "EAR99",
        },
        {
            "component_name": "DJI OcuSync / O3 / O4 video datalink",
            "category": "Communications / Telemetry",
            "civilian_use_case": "DJI consumer and professional drone video transmission",
            "dual_use_relevance": "Encrypted HD video transmission with kilometre-range capability. Widely integrated into military-modified DJI platforms. DJI is on DoD Section 1260H list. O3/O4 Air Unit modules enable DJI transmission in non-DJI airframes.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "Hong Kong", "Global via DJI distributors"],
            "red_flags": [
                "DJI Air Unit / O3 modules procured separately from DJI airframes (indicates third-party integration)",
                "Procurement by entity subject to DoD contractor restrictions (NDAA 2020 Section 848)",
                "Volume orders via non-authorised distributors",
            ],
            "export_control_relevance": "DJI on DoD Section 1260H list (PRC military company). Federal agency procurement prohibited under NDAA. ICTS review ongoing (BIS ANPRM Jan 2025).",
            "source_confidence": "High",
            "notes": "BIS issued UAS-focused ICTS ANPRM in January 2025 targeting Chinese UAS datalinks. DJI is primary target. Federal and defence contractor restrictions already in effect.",
            "source_url": "https://www.sidley.com/en/insights/newsupdates/2025/01/us-department-of-commerce-seeks-to-protect-drones-supply-chain-from-foreign-adversaries",
            "control_regime": "NDAA §848; ICTS review (BIS); DoD §1260H",
        },
        {
            "component_name": "RF datalinks and military-grade encrypted links",
            "category": "Communications / Telemetry",
            "civilian_use_case": "Professional survey UAVs, defence contractor platforms, government ISR",
            "dual_use_relevance": "Encrypted FHSS/DSSS datalinks provide LPI/LPD (low probability of intercept/detection) communications. Key capability for military-class autonomous platforms.",
            "sensitivity_level": "Military-adjacent",
            "procurement_risk_score": 9,
            "procurement_regions": ["USA", "Israel", "UK", "China (emerging)"],
            "red_flags": [
                "Military-specification encrypted datalinks procured by non-defence-contractor entity",
                "FHSS link with AES encryption procured by trading company for 're-export'",
                "Procurement via intermediary in jurisdiction without defence industrial base",
            ],
            "export_control_relevance": "ITAR (USML Category XI) for US-origin military datalinks. EAR ECCN 5E002 for encryption software. Licence required for all non-US destinations.",
            "source_confidence": "High",
            "notes": "Legitimate procurement of encrypted military-grade datalinks requires end-user verification. Any unverified procurement is a significant red flag.",
            "source_url": "https://www.pmddtc.state.gov",
            "control_regime": "ITAR / USML Cat. XI; ECCN 5E002",
        },

        # ══════════════════════════════════════════════════════════════
        # 6. SENSORS / PAYLOAD-ADJACENT
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "Electro-optical cameras (Sony, IMX sensors, gimbal-mounted)",
            "category": "Sensors / Payload-Adjacent",
            "civilian_use_case": "Aerial photography, filmmaking, real estate, inspection",
            "dual_use_relevance": "High-resolution EO cameras provide ISR capability. Gimbal-stabilised HD cameras are standard on both civilian inspection drones and conflict-zone ISR platforms. Sony IMX sensor chips are documented in military-modified commercial drones.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["China", "Japan", "Global"],
            "red_flags": [
                "High-resolution cameras (>50MP) procured alongside range-finding or target-designation accessories",
                "EO payload specifications exceed any stated civilian inspection use case",
                "Procurement of camera without corresponding UAV platform from same entity",
            ],
            "export_control_relevance": "Generally EAR99 for consumer cameras. ECCN 7A994 may apply to military-specification EO systems.",
            "source_confidence": "High",
            "notes": "The EO sensor market is extremely difficult to control due to civilian volume. Context of co-procurement with other components is the analytical lever.",
            "source_url": "",
            "control_regime": "EAR99 (generally)",
        },
        {
            "component_name": "Thermal imaging modules (FLIR Boson, Lepton, InfiRay)",
            "category": "Sensors / Payload-Adjacent",
            "civilian_use_case": "Industrial inspection, firefighting, search and rescue, building inspection",
            "dual_use_relevance": "Thermal modules provide night ISR capability critical to military UAV operations. FLIR Boson found in Russian-modified commercial UAVs. Chinese alternatives (Hikmicro/InfiRay) increasingly documented as Western thermal exports are restricted.",
            "sensitivity_level": "Military-adjacent",
            "procurement_risk_score": 9,
            "procurement_regions": ["USA (FLIR/Teledyne)", "China (Hikmicro, InfiRay)", "France (Lynred)"],
            "red_flags": [
                "FLIR Boson/Lepton modules procured via trading company or broker rather than authorised Teledyne FLIR distributor",
                "Thermal cores procured in quantities exceeding stated inspection fleet size",
                "Thermal module purchased alongside gimbal stabiliser and video transmitter (ISR payload kit)",
                "Procurement by entity in jurisdiction with no documented inspection or emergency services fleet",
            ],
            "export_control_relevance": "FLIR Boson: ECCN 6A003 or ECCN 6E002. Thermal imaging systems are subject to EAR licence requirement for many destinations. ITAR applies to US military-specification thermal systems.",
            "source_confidence": "High",
            "notes": "Teledyne FLIR implemented strict end-use monitoring post-Ukraine conflict. Chinese alternatives (Hikmicro parent Hikvision is on Entity List) are increasingly used as substitutes.",
            "source_url": "https://www.flir.com/discover/cores-components/export-compliance/",
            "control_regime": "ECCN 6A003 / 6E002; ITAR (military-spec)",
        },
        {
            "component_name": "Gimbal stabilisation systems (2/3-axis)",
            "category": "Sensors / Payload-Adjacent",
            "civilian_use_case": "Photography, filmmaking, inspection — image stabilisation",
            "dual_use_relevance": "Stabilised payload mount is required for effective airborne ISR. Gimbal + thermal camera + datalink constitutes a complete ISR payload. Documented in Ukrainian military UAV configurations.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Hong Kong"],
            "red_flags": [
                "3-axis gimbal procured alongside thermal module and video transmitter (complete ISR kit)",
                "Gimbal payload capacity exceeding stated camera weight by significant margin (indicates heavier military payload)",
            ],
            "export_control_relevance": "Generally EAR99 standalone; controlled when integrated into complete ISR system meeting ECCN thresholds",
            "source_confidence": "High",
            "notes": "Combination procurement (gimbal + thermal + transmitter) is a reliable ISR payload signal.",
            "source_url": "",
            "control_regime": "EAR99 (standalone)",
        },
        {
            "component_name": "Laser rangefinders and LiDAR modules",
            "category": "Sensors / Payload-Adjacent",
            "civilian_use_case": "Surveying, 3D mapping, autonomous vehicle sensing, altitude hold",
            "dual_use_relevance": "Laser rangefinders enable accurate target ranging for strike applications. LiDAR provides terrain-following capability for low-altitude penetration flight. Documented in advanced conflict-use UAV configurations.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "USA", "Germany", "Switzerland"],
            "red_flags": [
                "Eye-unsafe laser rangefinder (>Class 3B) procured for 'surveying' application by entity without surveying licence",
                "LiDAR module with terrain-following specification procured by entity without autonomous vehicle or survey mandate",
                "Rangefinder procured alongside EO camera and autopilot (complete guidance suite)",
            ],
            "export_control_relevance": "ECCN 6A005 (laser rangefinders); may require licence for controlled destinations. Eye-safe variants have different control status.",
            "source_confidence": "Medium",
            "notes": "The distinction between eye-safe (surveying) and non-eye-safe (military) laser rangefinders is the key compliance differentiator.",
            "source_url": "https://bis.doc.gov",
            "control_regime": "ECCN 6A005",
        },

        # ══════════════════════════════════════════════════════════════
        # 7. COUNTER-JAMMING / RESILIENCE
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "Anti-jamming GNSS modules (AJ-GPS)",
            "category": "Counter-Jamming / Resilience",
            "civilian_use_case": "Aviation, precision agriculture in high-interference environments, maritime navigation",
            "dual_use_relevance": "Anti-jamming GNSS provides navigation resilience against electronic warfare — a key military capability. Gyro-based INS backup modules procured by Chinese front companies were sanctioned by OFAC in February 2025.",
            "sensitivity_level": "Military-adjacent",
            "procurement_risk_score": 10,
            "procurement_regions": ["USA", "UK", "Israel", "China (emerging)"],
            "red_flags": [
                "Anti-jam GNSS module procured by any non-aviation, non-military entity without documented EW-environment justification",
                "Procurement via intermediary rather than authorised defence-sector distributor",
                "Combined with INS backup (implies full GPS-denied navigation suite)",
                "Any procurement by entity in Iran, Russia, or North Korea supply chains",
            ],
            "export_control_relevance": "ECCN 7A994 (standard AJ-GPS); higher-grade systems ITAR/USML. OFAC designated Chinese suppliers of gyro navigation devices to Iran (February 2025).",
            "source_confidence": "High",
            "notes": "OFAC February 2025 action specifically targeted gyro navigation device suppliers to Iran's UAV program. Highest-priority interdiction target in this category.",
            "source_url": "https://home.treasury.gov/news/press-releases/sb0313",
            "control_regime": "ECCN 7A994 / ITAR (grade-dependent); OFAC Feb 2025",
        },
        {
            "component_name": "Frequency-hopping spread spectrum (FHSS) radios",
            "category": "Counter-Jamming / Resilience",
            "civilian_use_case": "Industrial IoT, SCADA systems, professional RC aircraft (FCC Part 15)",
            "dual_use_relevance": "FHSS provides jamming-resistant communications. Military-grade FHSS with AES-256 encryption is an ITAR-controlled item. Commercial FHSS (ELRS, FrSky) is a simplified version lacking the waveform sophistication of military systems but providing basic jamming resistance.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["USA", "China", "Israel", "Germany"],
            "red_flags": [
                "Industrial FHSS radio procured in bulk with no documented SCADA or industrial operation",
                "FHSS hardware combined with directional high-gain antenna (indicates extended-range BVLOS intent)",
                "Military-specification FHSS acquired without ITAR licence",
            ],
            "export_control_relevance": "Commercial FHSS: EAR ECCN 5A992 or EAR99. Military-grade FHSS: ITAR USML Category XI. Encryption technology: ECCN 5E002.",
            "source_confidence": "High",
            "notes": "The line between commercial and military FHSS is specification-dependent. Bandwidth, waveform agility, and encryption depth are the key differentiators.",
            "source_url": "https://www.pmddtc.state.gov",
            "control_regime": "ECCN 5A992 / ITAR USML Cat. XI (grade-dependent)",
        },
        {
            "component_name": "Redundant / multi-constellation GNSS receivers",
            "category": "Counter-Jamming / Resilience",
            "civilian_use_case": "Professional surveying, precision agriculture, maritime, aviation",
            "dual_use_relevance": "Multi-constellation receivers (GPS + GLONASS + BeiDou + Galileo) provide resilience against single-constellation jamming. RTK variants (u-blox F9) provide centimetre-level accuracy for precision applications.",
            "sensitivity_level": "Sensitive dual-use",
            "procurement_risk_score": 8,
            "procurement_regions": ["China", "Switzerland (u-blox)", "USA (Trimble)", "Japan (Furuno)"],
            "red_flags": [
                "RTK-capable multi-constellation receiver procured by entity without documented precision agriculture or survey operation",
                "Multiple units procured (indicating fleet, not individual platform)",
                "Procurement routed via UAE or HK intermediary (consistent with Iran/Russia supply chain pattern)",
            ],
            "export_control_relevance": "u-blox F9 and similar RTK modules subject to enhanced end-use monitoring post-Ukraine conflict. Swiss export control and EAR re-export rules apply.",
            "source_confidence": "High",
            "notes": "RTK accuracy (~1cm) is the key indicator of precision-guidance rather than general navigation intent.",
            "source_url": "https://www.u-blox.com/en/about-us/compliance",
            "control_regime": "Swiss export control / EAR (re-export)",
        },

        # ══════════════════════════════════════════════════════════════
        # 8. MANUFACTURING / MODIFICATION INDICATORS
        # ══════════════════════════════════════════════════════════════
        {
            "component_name": "3D-printed structural components (FDM/SLA)",
            "category": "Manufacturing / Modification",
            "civilian_use_case": "Rapid prototyping, hobbyist drone builds, component replacement",
            "dual_use_relevance": "3D printing enables rapid manufacture of payload mounts, modified frames, and custom housings without supply chain visibility. Documented in Ukrainian domestic drone production and non-state actor weaponisation.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 5,
            "procurement_regions": ["Global — domestic manufacture"],
            "red_flags": [
                "Bulk procurement of engineering-grade filament (PETG, Nylon, CF-reinforced) at production scale",
                "Industrial FDM printers (Markforged, Stratasys) procured by entity without documented manufacturing business",
                "3D-printed component designs circulating in procurement communications (design file as indicator)",
            ],
            "export_control_relevance": "Equipment and materials generally EAR99. Design files (technical data) may be controlled under ITAR/EAR if they constitute controlled technical data.",
            "source_confidence": "High",
            "notes": "3D printing is fundamentally difficult to control due to distributed manufacture. The analytical signal is scale and context — production-volume printing by non-manufacturing entities.",
            "source_url": "",
            "control_regime": "EAR99 (equipment); ITAR/EAR (technical data, context-dependent)",
        },
        {
            "component_name": "CNC-machined aluminium and titanium components",
            "category": "Manufacturing / Modification",
            "civilian_use_case": "Precision engineering, aerospace components, motorsport, medical devices",
            "dual_use_relevance": "CNC machining enables production of precision structural components, motor mounts, and airframe parts at production scale. Indicates organised manufacturing rather than hobbyist assembly.",
            "sensitivity_level": "Dual-use",
            "procurement_risk_score": 6,
            "procurement_regions": ["China", "Taiwan", "Ukraine (pre-conflict domestic)"],
            "red_flags": [
                "CNC service procured for aerospace-tolerance components by entity without aerospace mandate",
                "Titanium or high-grade aluminium components with dimensions inconsistent with stated product",
                "CNC services combined with composite material procurement (airframe production indicator)",
            ],
            "export_control_relevance": "CNC equipment: ECCN 2B001 for high-precision machines. Certain materials (high-strength alloys) may have additional controls.",
            "source_confidence": "Medium",
            "notes": "Combination of CNC machining capacity + composite materials + electronics procurement is a strong indicator of organised UAV production.",
            "source_url": "https://bis.doc.gov",
            "control_regime": "ECCN 2B001 (equipment); material-dependent",
        },
        {
            "component_name": "Wiring harnesses and connector kits (XT60, JST, MIL-SPEC)",
            "category": "Manufacturing / Modification",
            "civilian_use_case": "Electronics assembly, RC vehicles, industrial equipment, aerospace ground support",
            "dual_use_relevance": "Production-scale wiring harness procurement indicates organised assembly rather than individual unit builds. MIL-SPEC connectors indicate military-standard construction. Documented in production-line Geran-2 assembly facilities.",
            "sensitivity_level": "Common civilian",
            "procurement_risk_score": 4,
            "procurement_regions": ["China", "USA (Amphenol, Molex)", "Germany (Souriau)"],
            "red_flags": [
                "MIL-SPEC connectors (MIL-DTL-38999, MIL-DTL-5015) ordered by non-defence entity",
                "Harness kits ordered at production volume (1,000+ units) by entity without documented electronics manufacturing",
                "Connector specifications matching known UAV production configurations",
            ],
            "export_control_relevance": "Generally EAR99. MIL-SPEC connectors from US manufacturers may require licence for certain destinations.",
            "source_confidence": "Medium",
            "notes": "Volume is the signal here. Individual harness kits are completely mundane; production-scale quantities in combination with other procurement signals are meaningful.",
            "source_url": "",
            "control_regime": "EAR99 (generally)",
        },
        {
            "component_name": "Conformal coating and potting compounds",
            "category": "Manufacturing / Modification",
            "civilian_use_case": "Electronics protection in marine, automotive, and industrial environments",
            "dual_use_relevance": "Applied to electronics boards to provide environmental protection and tamper resistance. Production-scale use indicates hardening of electronics for field deployment conditions (temperature, moisture, vibration).",
            "sensitivity_level": "Common civilian",
            "procurement_risk_score": 3,
            "procurement_regions": ["USA", "Germany", "China", "UK"],
            "red_flags": [
                "Conformal coating equipment procured alongside volume electronics assembly materials",
                "Military-grade potting compound (high temperature, vibration-rated) for stated consumer electronics application",
            ],
            "export_control_relevance": "Generally uncontrolled",
            "source_confidence": "Low",
            "notes": "Low individual signal value; meaningful only as part of a broader production-indicator pattern.",
            "source_url": "",
            "control_regime": "Uncontrolled",
        },
    ]

    df = pd.DataFrame(records)

    # Add computed fields
    df["sensitivity_order"] = df["sensitivity_level"].map(SENSITIVITY_ORDER).fillna(0).astype(int)
    df["sensitivity_color"] = df["sensitivity_level"].map(SENSITIVITY_COLOR)
    df["category_icon"] = df["category"].map(CATEGORY_ICON).fillna("◌")

    # Region list for region-component matrix
    all_regions = set()
    for regions in df["procurement_regions"]:
        all_regions.update(regions)

    return df


def get_region_component_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a pivot table of component categories × procurement regions.
    Cell value = count of components in that category sourced from that region.
    """
    rows = []
    for _, row in df.iterrows():
        for reg in row["procurement_regions"]:
            rows.append({
                "category": row["category"],
                "region": reg,
                "sensitivity_order": row["sensitivity_order"],
            })
    if not rows:
        return pd.DataFrame()

    flat = pd.DataFrame(rows)
    pivot = flat.groupby(["category", "region"]).size().reset_index(name="count")
    matrix = pivot.pivot(index="category", columns="region", values="count").fillna(0).astype(int)
    return matrix


def get_red_flag_table(df: pd.DataFrame) -> pd.DataFrame:
    """Returns flat table of all red flags with component context."""
    rows = []
    for _, row in df.iterrows():
        for flag in row.get("red_flags", []):
            rows.append({
                "Component": row["component_name"],
                "Category": row["category"],
                "Sensitivity": row["sensitivity_level"],
                "Procurement Risk": row["procurement_risk_score"],
                "Red Flag": flag,
                "Export Control": row["export_control_relevance"],
            })
    return pd.DataFrame(rows) if rows else pd.DataFrame()
