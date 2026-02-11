# functional_validation.py

from model import compute_risk_score, trigger_alert
from scenarios import high_risk_patient, moderate_risk_patient


THRESHOLD = 5


def validate_high_risk_detection():
    patient = high_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score, THRESHOLD)

    print("High Risk Score:", score)
    print("Alert Triggered:", alert)

    assert alert is True, "High-risk patient not detected."


def validate_moderate_risk_behavior():
    patient = moderate_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score, THRESHOLD)

    print("Moderate Risk Score:", score)
    print("Alert Triggered:", alert)


if __name__ == "__main__":
    validate_high_risk_detection()
    validate_moderate_risk_behavior()
