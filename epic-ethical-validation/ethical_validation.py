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

Ethical framework:
    Each function in this module operationalises a named ethical principle drawn
    from one of three schools: Utilitarianism, Deontological Ethics, or Virtue Ethics.
    The mapping is as follows:

    alert_fatigue_monitor   -> Goal U2  (Utilitarian, harm minimisation)
    governance_check        -> Goal D2  (Deontological, rule-based governance)
    responsibility_gap      -> Goal D1  (Deontological, Kantian duty of non-deception)
    reliance_check          -> Goal V1  (Virtue Ethics, phronesis)
    simulate_group_fairness -> Goal D1  (Deontological, equal treatment)
    simulate_over_reliance  -> Goal V1  (Virtue Ethics, phronesis)
    simulate_under_reliance -> Goal V1  (Virtue Ethics, phronesis)
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
    aggressive_false_positive,
    corrupted_patient,
    elderly_high_risk_patient, young_high_risk_patient
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
    """
    Goal U2: Control False Positive Burden
    School: Utilitarianism (Mill, principle of harm minimisation)

    Principle: The cumulative burden of false positive alerts must not reduce
    clinician responsiveness to genuine warnings. Alert fatigue is operationally
    defined as more than 5 consecutive alerts being fired within a session.

    Violation condition: alert_counter > 5 indicates the system is generating
    alerts at a rate likely to produce reflexive dismissal, degrading net
    population benefit and violating the utilitarian harm minimisation principle.
    """
    global alert_counter
    if alert:
        alert_counter += 1

    if alert_counter > 5:
        return True
    return False


def governance_check(alert, clinician_acknowledged):
    """
    Goal D2: Enforce Governance Accountability
    School: Deontological Ethics (rule-based governance, duty of institutional responsibility)

    Principle: Every alert fired by the system must be formally acknowledged by
    a responsible clinician. An unacknowledged alert represents a failure of the
    institutional duty of care.

    Operational constraint: Alert(A) -> Acknowledged(C, T)
    For all alerts A, there must exist a clinician acknowledgement C within
    response window T.

    Violation condition: governance_check returns False when an alert has been
    fired but no clinician acknowledgement is recorded. This is verified formally
    using Z3 SMT in z3_ethics_verification.py.
    """
    if alert and not clinician_acknowledged:
        return False
    return True


def responsibility_gap(alert, explanation_available):
    """
    Goal D1: Preserve Clinician Epistemic Access
    School: Deontological Ethics (Kant, respect for rational agency)

    Principle: A clinician held legally and morally responsible for a clinical
    decision must have meaningful epistemic access to the basis of the information
    that prompted that decision. Denying access to model reasoning while retaining
    accountability violates the Kantian duty to treat rational agents as ends in
    themselves.

    Operational constraint: For every alert fired, the clinician must be able to
    access at minimum the top contributing feature variables and their directional
    influence on the score.

    Violation condition: responsibility_gap returns True when an alert is fired
    without an accompanying explanation. In the current ESM deployment,
    explanation_available is False for every alert, meaning this condition is
    violated for 100 percent of alerts in production.

    Known simulation limitation: generate_explanation() always returns a value
    in this simulation, so explanation_available is always True here. This means
    the responsibility gap is never triggered in simulation. This is an acknowledged
    abstraction gap. The Z3 governance constraint in z3_ethics_verification.py
    handles the formal verification of this principle independently.
    """
    if alert and not explanation_available:
        return True
    return False


def reliance_check(alert, clinician_action):
    """
    Goal V1: Prevent Automation Bias and Preserve Clinical Prudence
    School: Virtue Ethics (Aristotle, phronesis)

    Principle: A clinical AI system must support rather than displace the exercise
    of practical wisdom. Automation bias, the tendency to follow AI output without
    independent assessment, directly undermines phronesis.

    Operational constraint: Clinician compliance rate with alerts must not exceed
    90 percent without documented independent clinical assessment.

    Violation condition: "Blind Compliance" is returned when a clinician follows
    every alert without independent assessment, indicating automation bias.
    "Under-reliance" is returned when a clinician ignores a genuine alert,
    indicating automation neglect. Both represent failures of calibrated
    professional judgement.
    """
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
    """
    Goal V1: Prevent Automation Bias
    School: Virtue Ethics (phronesis)

    Simulates a scenario where a clinician follows every alert without independent
    assessment. Compliance rate of 4/4 = 100 percent exceeds the 90 percent
    violation threshold defined in Chapter 2, Goal V1.
    """
    alerts = [True, True, True, True]
    clinician_actions = [True, True, True, True]

    logging.warning("Over-reliance scenario detected.")
    print("Over-reliance detected:",
          detect_over_reliance(alerts, clinician_actions))


def simulate_under_reliance():
    """
    Goal V1: Prevent Automation Neglect
    School: Virtue Ethics (phronesis)

    Simulates a scenario where a clinician ignores a genuine high-risk alert.
    Under-reliance is the complementary failure to automation bias: where V1
    requires active engagement with alerts, ignoring them entirely also represents
    a failure of calibrated clinical judgement.
    """
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
    """
    Goal U2: Control False Positive Burden
    School: Utilitarianism (harm minimisation)

    Simulates a patient who does not have sepsis but receives a borderline score.
    Computes the false positive rate to evaluate whether the alert burden is within
    operationally acceptable limits (FPR below the threshold at which alert fatigue
    begins to degrade clinician responsiveness).
    """
    patient = false_positive_patient()
    score = compute_risk_score(patient)
    alert = trigger_alert(score)

    alerts = [alert]
    actual = [False]

    fpr = evaluate_false_positive_rate(alerts, actual)
    print("False Positive Rate:", fpr)


def simulate_true_false_positive():
    """
    Goal U2: Control False Positive Burden
    School: Utilitarianism (harm minimisation)

    Simulates an aggressive false positive case where a patient with elevated
    individual risk markers but no actual sepsis triggers an alert. Logs the
    score, alert status, and false positive rate for audit purposes.
    """
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
    """
    Goal U1 vs U2: Sensitivity vs False Positive Burden Trade-off
    School: Utilitarianism (greatest aggregate benefit vs harm minimisation)

    This simulation operationalises the tension between U1 and U2. Raising the
    threshold reduces false positive burden (U2) but risks missing genuine sepsis
    cases (U1). Lowering the threshold maximises sensitivity (U1) but increases
    alert fatigue risk (U2). The trade-off cannot be resolved by system design
    alone and requires institutional threshold governance.

    Thresholds tested: 4 (high sensitivity), 5 (deployed default), 7 (high specificity)
    """
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


def simulate_data_quality_failure():
    """
    Goal D2: Governance and Data Integrity
    School: Deontological Ethics (institutional duty of care)

    Simulates a patient record with corrupted or missing data (temperature=None).
    A system that fires alerts based on corrupted inputs violates the institutional
    duty of care by producing outputs that cannot be considered reliable. This
    scenario tests whether the system handles data quality failures gracefully
    rather than propagating corrupt inputs into clinical decisions.
    """
    print("\n--- Data Quality Failure Scenario ---")

    try:
        patient = corrupted_patient()
        score = compute_risk_score(patient)
        alert = trigger_alert(score)

    except ValueError as e:
        logging.error(f"Data quality failure detected: {e}")
        print("Data quality failure detected:", e)


def simulate_group_fairness():
    """
    Goal D1: Equal Treatment Across Subgroups
    School: Deontological Ethics (principle of equal treatment, justice)

    Principle: Patients with equivalent clinical states must receive equivalent
    diagnostic evaluation regardless of demographic subgroup. Formally:
    EquivalentClinicalState -> Alert(elderly) == Alert(young)

    Violation condition: If elderly_alert != young_alert for patients with
    equivalent clinical parameters, the system produces differential treatment
    on the basis of age, violating the equal treatment principle.

    This constraint is verified formally using Z3 SMT in z3_ethics_verification.py,
    where the UNSAT core [Elderly_Alert_True, Equivalent_Group_True,
    Fairness_Symmetry, Young_Alert_False] demonstrates the violation is
    detectable before deployment.
    """
    print("\n--- Fairness Across Subgroups ---")

    elderly = elderly_high_risk_patient()
    young = young_high_risk_patient()

    elderly_score = compute_risk_score(elderly)
    young_score = compute_risk_score(young)

    elderly_alert = trigger_alert(elderly_score)
    young_alert = trigger_alert(young_score)

    print("Elderly Alert:", elderly_alert)
    print("Young Alert:", young_alert)

    if elderly_alert != young_alert:
        logging.warning("Fairness violation detected: unequal treatment across groups.")
        print("Fairness violation detected.")
    else:
        print("No subgroup disparity detected.")


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

    simulate_data_quality_failure()
    simulate_group_fairness()
