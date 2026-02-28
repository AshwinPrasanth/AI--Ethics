# Chapter 3: Implementation

## Repository

Source code is available at: **https://github.com/AshwinPrasanth/AI--Ethics**

The repository contains a simplified executable simulation of a sepsis risk scoring and alert system structurally modeled on the Epic Sepsis Model (ESM). The objective is not model replication, but ethical formalization and constraint validation.

---

# 3.1 Description of Approach

## 3.1.1 Model Abstraction

The Epic Sepsis Model is a proprietary, data-driven predictive system trained on approximately 500,000 encounters and incorporating ~80 clinical variables. Its internal feature weights, architecture, and training pipeline are undisclosed.

The implemented system does **not** attempt architectural reproduction. Instead, it preserves the following operational invariants of the deployed ESM:

1. Continuous numerical risk scoring
2. Threshold-based alert triggering ($\geq 5$)
3. Integration into clinician workflow
4. Screening-oriented behavior (high sensitivity)
5. Non-zero false positive possibility
6. Human-in-the-loop decision authority

The implementation therefore represents a structural abstraction of a sub-symbolic CDSS, sufficient for ethical validation experiments.

---

## 3.1.2 Domain Representation

Each synthetic inpatient case is represented by the vector:

$$
x = (T, HR, Lactate, WBC, SBP, PriorAntibiotics)
$$

Where:

* $T$: Temperature  
* $HR$: Heart rate  
* $Lactate$: Serum lactate  
* $WBC$: White blood cell count  
* $SBP$: Systolic blood pressure  
* $PriorAntibiotics$: Binary indicator  

These variables are clinically associated with sepsis physiology and represent a reduced subset of ESM inputs.

The risk score is computed as:

$$
Score = \sum_i w_i x_i
$$

with fixed weights $w_i$. This is not intended to approximate the proprietary ESM model, but to simulate sub-symbolic aggregation of heterogeneous clinical signals.

---

## 3.1.3 Functional Goal Encoding

### Goal F1: Continuous Risk Stratification

The system produces a real-valued risk score per patient instance.

Validation:

* High-risk synthetic instances yield $Score \geq 5$
* Moderate-risk instances yield $Score < 5$

This verifies discriminative scoring behavior.

---

### Goal F2: Deterministic Alert Trigger

Alert condition:

$$
Alert = (Score \geq 5)
$$

The threshold value (5) aligns with the cut-point selected in published ESM external validation.

Execution confirms:

* Alert = True for high-risk cases
* Alert = False for moderate-risk cases

---

### Goal F3: Workflow Activation

If $Alert = True$, the system simulates:

* Escalation to clinician
* Decision node requiring response

This models the operational reality that ESM alerts trigger workflow actions within the EHR.

---

## 3.1.4 Ethical Goal Formalization

Ethical goals are encoded as executable constraint checks.

---

### E1: False Positive Minimization (Alert Fatigue Risk)

Condition:

$$
Alert = True \land GroundTruth = False
$$

The system computes:

$$
FPR = \frac{FP}{FP + TN}
$$

If $FPR > 0$, alert fatigue risk is flagged and logged.

This operationalizes the ethical concern that screening-optimized systems may generate unnecessary escalations.

---

### E2: Over-Reliance Detection (Automation Bias)

Condition:

$$
Alert = True \land ClinicianAction = AutomaticAcceptance \land GroundTruth = False
$$

If satisfied, the system flags automation bias.

This models delegation without verification and captures epistemic over-dependence on AI output.

---

### E3: Under-Reliance Detection (Automation Neglect)

Condition:

$$
Alert = True \land ClinicianAction = Ignore
$$

This violates the safety-support function of the system.

The system returns:

$$
EthicalGoalSatisfied = False
$$

This encodes failure of justified intervention despite elevated risk.

---

### E4: Auditability Constraint

All events are recorded in:
`audit.log`


Logged events include:

* False positive detections
* Over-reliance scenarios
* Under-reliance scenarios

This simulates institutional accountability infrastructure present in real EHR deployments.

---

## 3.1.5 Validation Architecture

Two independent execution modules are provided:

* `functional_validation.py`
* `ethical_validation.py`

Functional validation confirms:

* Score generation correctness
* Threshold enforcement

Ethical validation confirms:

* Detectability of failure modes
* Logging of violations
* Non-zero FPR scenario generation
* Dual-sided reliance failure simulation

---

## 3.1.6 Scope Delimitation

The implementation does not:

* Replicate proprietary weighting
* Perform ROC optimization
* Estimate AUC
* Perform calibration analysis
* Model causal mortality effects

Instead, it provides:

* Formalized goal definitions
* Executable ethical constraints
* Reproducible violation scenarios

The contribution lies in ethical constraint encoding, not predictive modeling.

---

# 3.2 Evidence

Execution of:
`python functional_validation.py`

Demonstrates:

* Correct threshold-triggered alerts
* Risk score discrimination

Execution of:
`python ethical_validation.py`


Demonstrates:

* Over-reliance detection
* False positive generation ($FPR > 0$)
* Under-reliance violation
* Logged audit trace

Screenshots included in this chapter document:

1. Functional output traces
2. Ethical violation flags
3. `audit.log` entries

---

# Implementation Summary

This chapter demonstrates:

* Structural abstraction of a deployed AI-CDSS
* Explicit formalization of functional goals
* Explicit formalization of ethical goals
* Programmatic detection of ethical violations
* Audit-trace generation for accountability

The system therefore operationalizes ethical evaluation as executable verification rather than post-hoc commentary.
> **Important:** The simulation preserves the decision-structural properties of the Epic Sepsis Model while abstracting away proprietary internals. This allows ethical goals to be formalized and validated in a controlled environment without misrepresenting the real system’s architecture.
