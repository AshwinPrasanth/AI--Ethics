"""Ethical Goal 1 — Human Decision Authority (Deontology)
AI must not automatically administer antibiotics."""

def ethical_human_in_loop(alert, clinician_override):
    """
    AI cannot directly act.
    Human must confirm.
    """
    if alert and not clinician_override:
        return False
    return True

"""Ethical Goal 2 — Automation Bias Detection (Virtue Ethics, phronesis)
If clinicians always follow alerts blindly, practical wisdom is displaced."""

def detect_over_reliance(alerts, clinician_actions):
    """
    Measure blind compliance rate.
    """
    compliance_count = 0

    for a, c in zip(alerts, clinician_actions):
        if a and c:
            compliance_count += 1

    rate = compliance_count / len(alerts)
    return rate > 0.9  # threshold for over-reliance

"""Ethical Goal 3 — False Positive Burden (Utilitarianism, harm minimisation)
High alert rate on low-risk patients degrades net population benefit."""

def evaluate_false_positive_rate(alerts, actual_sepsis):
    false_positives = 0
    total_non_sepsis = 0

    for a, s in zip(alerts, actual_sepsis):
        if not s:
            total_non_sepsis += 1
            if a:
                false_positives += 1

    if total_non_sepsis == 0:
        return 0

    return false_positives / total_non_sepsis
