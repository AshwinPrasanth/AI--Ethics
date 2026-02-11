# scenarios.py

def high_risk_patient():
    return {
        "temperature": 39,
        "heart_rate": 120,
        "lactate": 4,
        "wbc": 18,
        "systolic_bp": 85,
        "prior_antibiotics": False
    }


def moderate_risk_patient():
    return {
        "temperature": 38,
        "heart_rate": 100,
        "lactate": 2,
        "wbc": 14,
        "systolic_bp": 100,
        "prior_antibiotics": False
    }


def false_positive_patient():
    return {
        "temperature": 38,
        "heart_rate": 95,
        "lactate": 1.5,
        "wbc": 13,
        "systolic_bp": 110,
        "prior_antibiotics": False
    }

def aggressive_false_positive():
    """
    High inflammatory vitals but no strong sepsis marker.
    Designed to trigger alert without confirmed sepsis.
    """
    return {
        "temperature": 39.8,
        "heart_rate": 130,
        "lactate": 1.4,       # still not septic-level
        "wbc": 18,
        "systolic_bp": 95,
        "prior_antibiotics": False
    }
