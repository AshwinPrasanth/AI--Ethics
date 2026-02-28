# scenarios.py

"""
Synthetic patient scenarios used to evaluate
functional and ethical behaviour of the
simulated sepsis risk model.

These are simplified abstractions and do not
represent clinically validated cases.
"""


def high_risk_patient():
    """
    Clear septic profile:
    - High fever
    - Tachycardia
    - Elevated lactate
    - Hypotension
    Ground truth: septic
    """
    return {
        "temperature": 39.0,
        "heart_rate": 120,
        "lactate": 4.0,
        "wbc": 18,
        "systolic_bp": 85,
        "prior_antibiotics": False,
        "actual_sepsis": True
    }


def moderate_risk_patient():
    """
    Borderline inflammatory profile.
    May or may not cross alert threshold
    depending on configuration.
    Ground truth: non-septic
    """
    return {
        "temperature": 38.0,
        "heart_rate": 100,
        "lactate": 2.0,
        "wbc": 14,
        "systolic_bp": 100,
        "prior_antibiotics": False,
        "actual_sepsis": False
    }


def false_positive_patient():
    """
    Mild inflammatory presentation.
    Should ideally not trigger alert.
    Ground truth: non-septic
    """
    return {
        "temperature": 38.0,
        "heart_rate": 95,
        "lactate": 1.5,
        "wbc": 13,
        "systolic_bp": 110,
        "prior_antibiotics": False,
        "actual_sepsis": False
    }


def aggressive_false_positive():
    """
    Strong inflammatory vitals but no strong sepsis marker.
    Designed to test threshold sensitivity and alert fatigue.
    Ground truth: non-septic
    """
    return {
        "temperature": 39.8,
        "heart_rate": 130,
        "lactate": 1.4,   # not strongly septic
        "wbc": 18,
        "systolic_bp": 95,
        "prior_antibiotics": False,
        "actual_sepsis": False
    }
