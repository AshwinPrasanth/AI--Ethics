# ethical_validation.py
import logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from model import compute_risk_score, trigger_alert
from scenarios import high_risk_patient, false_positive_patient, aggressive_false_positive
from utils import ethical_human_in_loop, detect_over_reliance, evaluate_false_positive_rate


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



if __name__ == "__main__":
    simulate_over_reliance()
    simulate_false_positive_case()
    simulate_true_false_positive()
    simulate_under_reliance()


