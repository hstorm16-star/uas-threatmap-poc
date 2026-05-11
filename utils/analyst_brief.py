"""
analyst_brief.py — Generates structured analyst summaries from selected records.
"""

import pandas as pd
from datetime import datetime


def generate_brief(
    entities: pd.DataFrame,
    ttps: pd.DataFrame,
    focus_region: str,
    analyst_gaps: str,
) -> str:
    """
    Returns an HTML-formatted analyst brief string for Streamlit st.markdown().
    """
    now = datetime.now().strftime("%d %b %Y")

    # ── Derive key fields ────────────────────────────────────────────────────
    crit = entities[entities["risk_level"] == "Critical"]
    high = entities[entities["risk_level"] == "High"]

    all_ttps = sorted(set(
        t for row in entities["ttps"].dropna() for t in row
    ))
    if not ttps.empty:
        ttp_names = ttps["ttp_name"].tolist()
        all_ttps = sorted(set(all_ttps) | set(ttp_names))

    regions = entities["region"].dropna().unique().tolist()
    region_str = focus_region if focus_region != "All" else ", ".join(regions)

    sources_all = []
    for s in entities["source"].dropna():
        for part in s.split(";"):
            sources_all.append(part.strip())
    unique_sources = sorted(set(sources_all))

    conf_counts = entities["source_confidence"].value_counts().to_dict()
    dominant_conf = max(conf_counts, key=conf_counts.get) if conf_counts else "Unknown"

    risk_counts = entities["risk_level"].value_counts().to_dict()

    # ── Heightened activity logic ─────────────────────────────────────────────
    activity_note = ""
    if len(crit) > 0:
        activity_note = f"<span style='color:#e8503a'>⚠ {len(crit)} CRITICAL-rated entit{'y' if len(crit)==1 else 'ies'} included.</span>"

    # ── Recommended next steps ────────────────────────────────────────────────
    next_steps = []
    if "Shell/front company procurement" in all_ttps:
        next_steps.append("Cross-reference named entities against BIS Entity List address-level additions (June 2024 onwards).")
    if "Re-export routing" in all_ttps or "Logistics/transshipment routing" in all_ttps:
        next_steps.append("Review trade data for volume anomalies at documented transshipment hubs (UAE, Turkey, Malaysia, Central Asia).")
    if "Sanctioned entity proximity" in all_ttps:
        next_steps.append("Conduct ownership chain analysis to <50% threshold per EU/UK sanctions guidance.")
    if "Marketplace sourcing" in all_ttps:
        next_steps.append("Monitor Alibaba/AliExpress for bulk orders of component combinations consistent with UAV subsystems.")
    if not next_steps:
        next_steps.append("Conduct enhanced due diligence on all identified entities.")
        next_steps.append("File SARs where financial institution exposure exists.")

    gaps_html = analyst_gaps.strip() if analyst_gaps.strip() else "No analyst gaps recorded. Consider documenting data limitations."

    # ── Compose brief ─────────────────────────────────────────────────────────
    entity_rows = ""
    for _, row in entities.iterrows():
        lvl = row["risk_level"]
        cls = {"Critical":"badge-crit","High":"badge-high","Moderate":"badge-mod","Low":"badge-low"}.get(lvl,"")
        entity_rows += (
            f"<tr style='border-bottom:1px solid #1e2230'>"
            f"<td style='padding:6px 8px'>{row['name']}</td>"
            f"<td style='padding:6px 8px'><span class='badge {cls}'>{lvl.upper()}</span></td>"
            f"<td style='padding:6px 8px;color:#6b7599'>{row.get('category','—')}</td>"
            f"<td style='padding:6px 8px;color:#6b7599'>{row.get('region','—')}</td>"
            f"<td style='padding:6px 8px;font-size:11px;color:#6b7599'>{row.get('source_confidence','—')}</td>"
            f"</tr>"
        )

    ttp_items = "".join([f"<li style='margin-bottom:4px'>{t}</li>" for t in all_ttps]) or "<li>None recorded</li>"
    step_items = "".join([f"<li style='margin-bottom:4px'>{s}</li>" for s in next_steps])
    source_chips = "".join([f"<span class='badge badge-unver' style='margin:2px'>{s}</span>" for s in unique_sources])

    brief = f"""
<div style='background:#0d0f15;border:1px solid #1e2230;border-radius:4px;padding:20px 24px;font-family:"IBM Plex Sans",sans-serif'>

<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px'>
  <div>
    <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;letter-spacing:.1em;text-transform:uppercase'>Intelligence assessment · open source basis · unclassified</div>
    <div style='font-size:18px;font-weight:500;color:#c8cfe0;margin-top:4px'>UAS Procurement & Conflict-Use Threat Brief</div>
  </div>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-align:right'>
    Generated: {now}<br>
    Region: {region_str}<br>
    Entities: {len(entities)}
  </div>
</div>

<hr style='border:none;border-top:1px solid #1e2230;margin:12px 0'>

<div style='margin-bottom:16px'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>Key Risk Assessment</div>
  <div style='font-size:13px;line-height:1.7;color:#c8cfe0'>
    {activity_note}<br>
    Risk distribution across selected entities:
    <b style='color:#e8503a'>Critical: {risk_counts.get("Critical",0)}</b> &nbsp;
    <b style='color:#f07c2a'>High: {risk_counts.get("High",0)}</b> &nbsp;
    <b style='color:#f0c040'>Moderate: {risk_counts.get("Moderate",0)}</b> &nbsp;
    <b style='color:#3ab87a'>Low: {risk_counts.get("Low",0)}</b>
    <br>Dominant source confidence: <b>{dominant_conf}</b>.
  </div>
</div>

<div style='margin-bottom:16px'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>Entity Summary</div>
  <table style='width:100%;border-collapse:collapse;font-size:12px'>
    <thead>
      <tr style='border-bottom:1px solid #2a2f42'>
        <th style='text-align:left;padding:6px 8px;color:#6b7599;font-weight:400'>Entity</th>
        <th style='text-align:left;padding:6px 8px;color:#6b7599;font-weight:400'>Risk</th>
        <th style='text-align:left;padding:6px 8px;color:#6b7599;font-weight:400'>Category</th>
        <th style='text-align:left;padding:6px 8px;color:#6b7599;font-weight:400'>Region</th>
        <th style='text-align:left;padding:6px 8px;color:#6b7599;font-weight:400'>Confidence</th>
      </tr>
    </thead>
    <tbody>{entity_rows}</tbody>
  </table>
</div>

<div style='margin-bottom:16px'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>TTPs Observed</div>
  <ul style='font-size:13px;color:#c8cfe0;padding-left:20px;margin:0'>{ttp_items}</ul>
</div>

<div style='margin-bottom:16px'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>Source Basis</div>
  <div>{source_chips}</div>
</div>

<div style='margin-bottom:16px;background:#1a0f0d;border:1px solid #e8503a33;border-left:3px solid #e8503a;border-radius:3px;padding:10px 14px'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#e8503a;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>Collection Gaps</div>
  <div style='font-size:13px;color:#c8cfe0'>{gaps_html}</div>
</div>

<div style='margin-bottom:0'>
  <div style='font-family:"IBM Plex Mono",monospace;font-size:10px;color:#3a4060;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>Recommended Next Steps</div>
  <ol style='font-size:13px;color:#c8cfe0;padding-left:20px;margin:0'>{step_items}</ol>
</div>

</div>
"""
    return brief
