# ethical_validation.py
import logging

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from model import compute_risk_score, trigger_alert, generate_explanation
from scenarios import high_risk_patient, false_positive_patient, aggressive_false_positive
from utils import ethical_human_in_loop, detect_over_reliance, evaluate_false_positive_rate

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


def simulate_over_reliance():
    alerts = [True, True, True, True]
    clinician_actions = [True, True, True, True]
    logging.warning("Over-reliance scenario detected.")
    print("Over-reliance detected:", detect_over_reliance(alerts, clinician_actions))

def simulate_under_reliance():
    patient = high_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    clinician_override = False  # clinician ignores alert

    ethical_ok = ethical_human_in_loop(alert, clinician_override)
    logging.warning(f"Under-reliance detected - Alert: {alert}, Clinician responded: {clinician_override}")
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
    
    actual_sepsis = False  # ground truth

    alerts = [alert]
    actual = [actual_sepsis]

    fpr = evaluate_false_positive_rate(alerts, actual)
    logging.info(f"False Positive Test - Score: {score}, Alert: {alert}, FPR: {fpr}")
    print("Aggressive False Positive Score:", score)
    print("Alert Triggered:", alert)
    print("False Positive Rate:", fpr)

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

    gap = responsibility_gap(alert=alert, explanation_available=explanation_available)

    print("Alert:", alert)
    print("Explanation available:", explanation_available)
    print("Responsibility gap detected:", gap)

    print("\n--- Reliance Calibration Test ---")
    reliance = reliance_check(alert=alert, clinician_action=True)
    print("Reliance type:", reliance)

    print("\n--- Alert Fatigue Simulation ---")
    global alert_counter
    alert_counter = 0  # reset

    for i in range(6):
        fatigue = alert_fatigue_monitor(alert=True)

    print("Alert fatigue triggered:", fatigue)

    print("\n--- Governance Check ---")
    gov = governance_check(alert=alert, clinician_acknowledged=False)
    print("Governance constraint satisfied:", gov)
