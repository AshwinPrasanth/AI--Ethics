# risk_model.py

"""
Simplified risk scoring abstraction for a sepsis CDSS.

This does NOT represent the real Epic Sepsis Model.
It approximates a sub-symbolic weighted aggregation
to enable ethical validation testing.
"""


def compute_risk_score(patient):
    """
    Simulated sub-symbolic risk scoring function.
    Uses weighted aggregation to approximate learned model behavior.
    """

    # Basic input validation
    required_keys = [
        "temperature",
        "heart_rate",
        "lactate",
        "wbc",
        "systolic_bp"
    ]

    for key in required_keys:
        if key not in patient or patient[key] is None:
            raise ValueError(f"Missing required feature: {key}")

    # Weighted aggregation (approximation of learned model)
    score = (
        0.8 * patient["temperature"] +
        0.6 * patient["heart_rate"] +
        1.2 * patient["lactate"] +
        0.5 * patient["wbc"] -
        0.7 * patient["systolic_bp"]
    )

    # Scale to interpretable range
    return max(score / 10, 0)


def generate_explanation(patient):
    """
    Simulated feature contribution explanation.
    Approximates post-hoc interpretability.
    """

    return {
        "temperature_contribution": 0.8 * patient["temperature"] / 10,
        "heart_rate_contribution": 0.6 * patient["heart_rate"] / 10,
        "lactate_contribution": 1.2 * patient["lactate"] / 10,
        "wbc_contribution": 0.5 * patient["wbc"] / 10,
        "bp_contribution": -0.7 * patient["systolic_bp"] / 10
    }


def trigger_alert(risk_score, threshold=5):
    """
    Alert fires when risk exceeds threshold.
    Default threshold aligns with validation study abstraction.
    """
    return risk_score >= threshold


def evaluate_threshold(patient, threshold):
    """
    Evaluate alert behavior under different threshold configurations.
    Used to simulate utilitarian trade-off analysis.
    """
    score = compute_risk_score(patient)
    return score >= threshold
