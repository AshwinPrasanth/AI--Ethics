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


def trigger_alert(risk_score, threshold=5):
    return risk_score >= threshold
