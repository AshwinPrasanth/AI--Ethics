# risk_model.py

"""
Simplified risk scoring abstraction for a sepsis CDSS.
This does NOT represent the real Epic Sepsis Model.
It approximates a sub-symbolic weighted aggregation
to enable ethical validation testing.

Ethical framework note:
    This module provides the functional layer that the ethical validation layer
    (ethical_validation.py) and formal verification layer (z3_ethics_verification.py)
    operate on. The functions here correspond to the following ethical goals:

    compute_risk_score   -> supports Goals U1, U2 (Utilitarian, outcome-based scoring)
    generate_explanation -> supports Goal D1 (Deontological, clinician epistemic access)
    trigger_alert        -> supports Goals D2, U1 (alert governance and mortality reduction)
    evaluate_threshold   -> supports Goals U1 vs U2 (sensitivity vs false positive trade-off)

    The generate_explanation function is particularly significant. In this simulation
    it always returns a value, which means the responsibility_gap check in
    ethical_validation.py never triggers. This is an acknowledged abstraction gap:
    in the real ESM deployment no feature-level explanation is provided to clinicians,
    meaning Goal D1 (Kantian duty of non-deception) is violated for 100 percent of
    alerts in production. The Z3 layer handles formal verification of this principle
    independently of this simulation.
"""


def compute_risk_score(patient):
    """
    Simulated sub-symbolic risk scoring function.
    Uses weighted aggregation to approximate learned model behavior.

    Goal U1: Minimise Preventable Sepsis Mortality
    School: Utilitarianism (greatest aggregate benefit)

    This function abstracts the ESM's learned inference process as a weighted
    aggregation across five clinical variables. The weights approximate the
    relative contribution of each feature to sepsis risk, consistent with
    published clinical literature on sepsis presentation. The function supports
    Goal U1 by providing a risk estimate that enables early alert triggering
    and reduced time to antibiotic administration.

    Goal U2: Control False Positive Burden
    School: Utilitarianism (harm minimisation)

    The scaling and aggregation approach also directly influences the false
    positive rate. A score that aggregates multiple weakly elevated variables
    may produce alerts for patients without sepsis, contributing to alert
    fatigue. The trade-off between sensitivity and specificity is operationalised
    in evaluate_threshold below.
    """
    # Basic input validation
    required_keys = [
        "temperature",
        "heart_rate",
        "lactate",
        "wbc",
        "systolic_bp"
    ]
    for key in required_keys:
        if key not in patient or patient[key] is None:
            raise ValueError(f"Missing required feature: {key}")

    # Weighted aggregation (approximation of learned model)
    score = (
        0.8 * patient["temperature"] +
        0.6 * patient["heart_rate"] +
        1.2 * patient["lactate"] +
        0.5 * patient["wbc"] -
        0.7 * patient["systolic_bp"]
    )

    # Scale to interpretable range
    return max(score / 10, 0)


def generate_explanation(patient):
    """
    Simulated feature contribution explanation.
    Approximates post-hoc interpretability.

    Goal D1: Preserve Clinician Epistemic Access
    School: Deontological Ethics (Kant, respect for rational agency)

    Principle: A clinician held legally and morally responsible for a clinical
    decision must have meaningful epistemic access to the basis of the information
    that prompted that decision. This function simulates the feature-level
    explanation that would satisfy Goal D1 by returning the directional
    contribution of each input variable to the final risk score.

    Simulation limitation: This function always returns a non-None explanation,
    so the responsibility_gap check in ethical_validation.py always receives
    explanation_available=True and never triggers a violation. This does not
    reflect the real ESM deployment, in which no such explanation is provided
    to bedside clinicians. The simulation therefore understates the D1 violation.
    This limitation is acknowledged explicitly in Chapter 3 and the Z3 layer
    provides formal verification of the accountability gap independently.
    """
    return {
        "temperature_contribution": 0.8 * patient["temperature"] / 10,
        "heart_rate_contribution": 0.6 * patient["heart_rate"] / 10,
        "lactate_contribution": 1.2 * patient["lactate"] / 10,
        "wbc_contribution": 0.5 * patient["wbc"] / 10,
        "bp_contribution": -0.7 * patient["systolic_bp"] / 10
    }


def trigger_alert(risk_score, threshold=5):
    """
    Alert fires when risk exceeds threshold.
    Default threshold aligns with validation study abstraction.

    Goal D2: Enforce Governance Accountability
    School: Deontological Ethics (rule-based governance)

    Every alert fired by this function must be formally acknowledged by a
    responsible clinician. The governance_check constraint in
    ethical_validation.py enforces the rule: Alert(A) -> Acknowledged(C, T).
    An alert that passes without acknowledgement constitutes a violation of
    Goal D2 and is verified formally using Z3 SMT.

    Goal U1: Minimise Preventable Sepsis Mortality
    School: Utilitarianism (greatest aggregate benefit)

    The default threshold of 5 corresponds to the ESM deployment threshold
    used in the published validation study, at which sensitivity is 86 percent
    and PPV is 33.8 percent. This threshold represents the institutional
    decision that early detection of true positives outweighs the burden of
    false positives at the population level.
    """
    return risk_score >= threshold


def evaluate_threshold(patient, threshold):
    """
    Evaluate alert behavior under different threshold configurations.
    Used to simulate utilitarian trade-off analysis.

    Goal U1 vs U2: Sensitivity vs False Positive Burden Trade-off
    School: Utilitarianism (greatest aggregate benefit vs harm minimisation)

    This function operationalises the tension between U1 and U2 identified
    in Chapter 2. Lowering the threshold increases sensitivity (supports U1)
    but raises the false positive rate (violates U2). Raising the threshold
    reduces false positive burden (supports U2) but risks missing genuine
    sepsis cases (violates U1).

    Thresholds evaluated in simulate_threshold_tradeoff:
        4  -> high sensitivity, high false positive burden
        5  -> deployed default, institutional balance point
        7  -> high specificity, reduced sensitivity

    This trade-off cannot be resolved by system design alone and requires
    institutional threshold governance involving clinicians, patients, and
    ethics review.
    """
    score = compute_risk_score(patient)
    return score >= threshold
