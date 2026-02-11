# model.py

def compute_risk_score(patient):
    """
    Simulated sub-symbolic risk scoring function.
    Not rule-based. Weighted aggregation approximates learned model behavior.
    """
    score = 0

    score += 0.8 * patient["temperature"]
    score += 0.6 * patient["heart_rate"]
    score += 1.2 * patient["lactate"]
    score += 0.5 * patient["wbc"]
    score -= 0.7 * patient["systolic_bp"]

    return max(score / 10, 0)

def generate_explanation(patient):
    explanation = {
        "temperature": patient["temperature"] * 0.05,
        "heart_rate": patient["heart_rate"] * 0.02,
        "lactate": patient["lactate"] * 1.5,
        "wbc": patient["wbc"] * 0.1,
        "systolic_bp": (120 - patient["systolic_bp"]) * 0.03
    }
    return explanation

def trigger_alert(risk_score, threshold=5):
    return risk_score >= threshold
