# functional_validation.py

"""
Functional validation of the simplified sepsis risk model.

This module verifies that the system satisfies its
primary functional objective:
    Early detection of high-risk sepsis patients.
"""

from model import compute_risk_score, trigger_alert
from scenarios import high_risk_patient, moderate_risk_patient

THRESHOLD = 5


def validate_high_risk_detection():
    """
    Functional Goal:
    A clinically high-risk patient must trigger an alert.
    """
    patient = high_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score, THRESHOLD)

    print("High Risk Score:", score)
    print("Alert Triggered:", alert)

    assert alert is True, "High-risk patient was not detected."


def validate_moderate_risk_behavior():
    """
    Functional Goal:
    A moderate-risk patient should not trigger an alert
    under the selected threshold.
    """
    patient = moderate_risk_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score, THRESHOLD)

    print("Moderate Risk Score:", score)
    print("Alert Triggered:", alert)

    assert alert is False, "Moderate-risk patient incorrectly triggered alert."


if __name__ == "__main__":
    print("\n--- Functional Validation ---")
    validate_high_risk_detection()
    validate_moderate_risk_behavior()
