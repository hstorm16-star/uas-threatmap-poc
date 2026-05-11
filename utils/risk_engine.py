"""
risk_engine.py — Risk scoring for entity records.
===================================================
The score is a weighted sum of 7 sub-dimensions, each 0–10.
Change the WEIGHTS dict to rebalance the model.
THRESHOLDS controls where Low/Moderate/High/Critical break.
"""

WEIGHTS = {
    "conflict_relevance":      0.22,
    "sanctions_exposure":      0.20,
    "dual_use_sensitivity":    0.15,
    "military_use_evidence":   0.20,
    "intermediary_risk":       0.10,
    "transshipment_risk":      0.08,
    "source_confidence_score": 0.05,   # higher confidence → more reliable score
}

THRESHOLDS = {
    "Critical": 75,
    "High":     55,
    "Moderate": 35,
    "Low":      0,
}


def score_entity(row) -> int:
    """Return 0–100 composite risk score for a single entity row."""
    raw = sum(
        row.get(field, 0) * weight
        for field, weight in WEIGHTS.items()
    )
    # Each sub-field is 0–10; max raw = 1.0 * 10 = 10
    return min(100, int(round(raw * 10)))


def RISK_LEVELS(score: int) -> str:
    """Map a numeric score to a categorical risk level."""
    if score >= THRESHOLDS["Critical"]:
        return "Critical"
    elif score >= THRESHOLDS["High"]:
        return "High"
    elif score >= THRESHOLDS["Moderate"]:
        return "Moderate"
    else:
        return "Low"
