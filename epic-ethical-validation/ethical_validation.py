# ethical_validation.py

"""
Ethical validation layer for simplified AI-based sepsis decision support system.

This module evaluates whether the system satisfies explicitly defined ethical goals:
- Prevent over-reliance (automation bias)
- Detect under-reliance (automation neglect)
- Monitor false positives
- Evaluate threshold trade-offs
- Detect responsibility gaps
- Monitor alert fatigue
- Enforce governance constraints
"""

import logging

# -----------------------------
# Global State
# -----------------------------

alert_counter = 0

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# Imports
# -----------------------------

from model import (
    compute_risk_score,
    trigger_alert,
    generate_explanation,
    evaluate_threshold
)

from scenarios import (
    high_risk_patient,
    false_positive_patient,
    aggressive_false_positive
)

from utils import (
    ethical_human_in_loop,
    detect_over_reliance,
    evaluate_false_positive_rate
)

# -----------------------------
# Ethical Monitoring Functions
# -----------------------------

def alert_fatigue_monitor(alert):
    global alert_counter
    if alert:
        alert_counter += 1

    if alert_counter > 5:
        return True
    return False


def governance_check(alert, clinician_acknowledged):
    if alert and not clinician_acknowledged:
        return False
    return True


def responsibility_gap(alert, explanation_available):
    if alert and not explanation_available:
        return True
    return False


def reliance_check(alert, clinician_action):
    if alert and clinician_action:
        return "Blind Compliance"
    elif alert and not clinician_action:
        return "Under-reliance"
    elif not alert and clinician_action:
        return "Overtreatment"
    return "Calibrated"


# -----------------------------
# Simulation Scenarios
# -----------------------------

def simulate_over_reliance():
    alerts = [True, True, True, True]
    clinician_actions = [True, True, True, True]

    logging.warning("Over-reliance scenario detected.")
    print("Over-reliance detected:",
          detect_over_reliance(alerts, clinician_actions))


def simulate_under_reliance():
    patient = high_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    clinician_override = False  # clinician ignores alert

    ethical_ok = ethical_human_in_loop(alert, clinician_override)

    logging.warning(
        f"Under-reliance detected - Alert: {alert}, "
        f"Clinician responded: {clinician_override}"
    )

    print("Under-reliance scenario:")
    print("Alert:", alert)
    print("Clinician responded:", clinician_override)
    print("Ethical goal satisfied:", ethical_ok)


def simulate_false_positive_case():
    patient = false_positive_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    alerts = [alert]
    actual = [False]

    fpr = evaluate_false_positive_rate(alerts, actual)
    print("False Positive Rate:", fpr)


def simulate_true_false_positive():
    patient = aggressive_false_positive()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    actual_sepsis = False

    alerts = [alert]
    actual = [actual_sepsis]

    fpr = evaluate_false_positive_rate(alerts, actual)

    logging.info(
        f"False Positive Test - Score: {score}, "
        f"Alert: {alert}, FPR: {fpr}"
    )

    print("Aggressive False Positive Score:", score)
    print("Alert Triggered:", alert)
    print("False Positive Rate:", fpr)


def simulate_threshold_tradeoff():
    print("\n--- Threshold Trade-Off Simulation ---")

    patient = aggressive_false_positive()
    actual_sepsis = False

    for threshold in [4, 5, 7]:
        alert = evaluate_threshold(patient, threshold)

        alerts = [alert]
        actual = [actual_sepsis]

        fpr = evaluate_false_positive_rate(alerts, actual)

        print(f"Threshold: {threshold}")
        print(f"Alert Triggered: {alert}")
        print(f"False Positive Rate: {fpr}")
        print("-" * 30)


# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":

    print("\n--- Over-reliance Scenario ---")
    simulate_over_reliance()

    print("\n--- Basic False Positive Case ---")
    simulate_false_positive_case()

    print("\n--- Aggressive False Positive Case ---")
    simulate_true_false_positive()

    print("\n--- Under-reliance Scenario ---")
    simulate_under_reliance()

    print("\n--- Responsibility Gap Test ---")
    patient = high_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    explanation = generate_explanation(patient)
    explanation_available = explanation is not None

    gap = responsibility_gap(alert, explanation_available)

    print("Alert:", alert)
    print("Explanation available:", explanation_available)
    print("Responsibility gap detected:", gap)

    simulate_threshold_tradeoff()

    print("\n--- Reliance Calibration Test ---")
    reliance = reliance_check(alert=alert, clinician_action=True)
    print("Reliance type:", reliance)

    print("\n--- Alert Fatigue Simulation ---")
    alert_counter = 0
    for _ in range(6):
        fatigue = alert_fatigue_monitor(alert=True)
    print("Alert fatigue triggered:", fatigue)

    print("\n--- Governance Check ---")
    gov = governance_check(alert=alert, clinician_acknowledged=False)
    print("Governance constraint satisfied:", gov)
