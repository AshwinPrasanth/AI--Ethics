# Chapter 3: Implementation

## Repository

Source code is available at:

**[https://github.com/AshwinPrasanth/AI--Ethics](https://github.com/AshwinPrasanth/AI--Ethics)**

The repository contains a structured simulation and formal verification framework modeling the decision-structural properties of the Epic Sepsis Model (ESM). The objective is not architectural replication of the proprietary system, but formalization and validation of functional and ethical properties.

The implementation consists of two validation layers:

1. **Behavioral simulation layer**
2. **Formal logical verification layer (Z3 SMT)**

Together, they operationalize ethical evaluation as executable constraint verification.

---

# 3.1 Description of Approach

---

## 3.1.1 Model Abstraction

The Epic Sepsis Model is a proprietary, data-driven predictive system trained on approximately 500,000 patient encounters and incorporating ~80 clinical variables. Its internal architecture, feature weighting, and training pipeline are not publicly disclosed.

This implementation does not attempt model reproduction. Instead, it preserves the operational invariants that define the system’s decision structure:

1. Continuous numerical risk scoring
2. Threshold-based alert triggering (Score ≥ 5)
3. Screening-oriented behavior (high sensitivity design)
4. Non-zero false positive possibility
5. Human-in-the-loop decision authority
6. Integration into clinician workflow

The system therefore represents a structural abstraction of a sub-symbolic Clinical Decision Support System (CDSS), sufficient for ethical validation experiments.

---

## 3.1.2 Domain Representation

Each synthetic inpatient instance is represented as:

$$
x = (T, HR, Lactate, WBC, SBP, PriorAntibiotics)
$$

Where:

* $$T$$: Temperature
* $$HR$$: Heart rate
* $$Lactate$$: Serum lactate
* $$WBC$$: White blood cell count
* $$SBP$$: Systolic blood pressure
* $$PriorAntibiotics$$: Binary indicator

These variables represent a reduced clinically meaningful subset of ESM inputs.

The risk score is computed as:

$$
Score = \sum_i w_i x_i
$$

with fixed weights $$w_i$$. The purpose is not predictive realism, but simulation of sub-symbolic weighted aggregation of heterogeneous physiological signals.

---

# 3.1.3 Functional Goal Encoding

Functional goals are encoded in `functional_validation.py`.

---

### F1: Continuous Risk Stratification

The system produces a real-valued risk score for each patient.

Validation:

* High-risk synthetic cases → $$Score \geq 5$$
* Moderate-risk synthetic cases → $$Score < 5$$

This confirms discriminative behavior.

---

### F2: Deterministic Alert Trigger

Alert condition:

$$
Alert = (Score \geq 5)
$$

The threshold of 5 aligns with the published ESM validation cut-point.

Validation confirms:

* Alert = True for high-risk patients
* Alert = False for moderate-risk patients

---

### F3: Workflow Activation

If $$Alert = True$$, the system simulates:

* Escalation to clinician
* Decision node requiring response

This models the real-world operational role of ESM alerts in hospital EHR workflows.

---

# 3.1.4 Ethical Goal Formalization (Simulation Layer)

Ethical goals are encoded as executable constraint checks in `ethical_validation.py`.

---

## E1: False Positive Monitoring (Utilitarian Trade-Off)

Condition:

$$
Alert = True \land GroundTruth = False
$$

False Positive Rate is computed as:

$$
FPR = \frac{FP}{FP + TN}
$$

If $$FPR > 0$$, alert fatigue risk is flagged and logged.

This models the trade-off between sensitivity optimization and unnecessary intervention.

---

## E2: Over-Reliance Detection (Automation Bias)

Condition:

$$
Alert = True \land ClinicianAction = Accept \land GroundTruth = False
$$

This detects blind compliance with AI output and captures epistemic over-dependence.

---

## E3: Under-Reliance Detection (Automation Neglect)

Condition:

$$
Alert = True \land ClinicianAction = Ignore
$$

If triggered, the system reports:

$$
EthicalGoalSatisfied = False
$$

This encodes failure to act under elevated risk.

---

## E4: Responsibility Gap Detection

Condition:

$$
Alert = True \land ExplanationUnavailable
$$

This models the epistemic asymmetry where clinicians remain accountable without interpretive access.

---

## E5: Alert Fatigue Monitoring

Repeated alerts are accumulated.

If alert frequency exceeds a defined threshold, fatigue risk is flagged.

This models workflow burden accumulation.

---

## E6: Governance Constraint

Condition:

$$
Alert \rightarrow Acknowledged
$$

If violated, governance failure is reported.

---

## E7: Data Quality Failure

Corrupted or incomplete patient inputs trigger exceptions and logging.

This models infrastructural and deployment-level ethical risk.

---

## E8: Age-Based Fairness Scenario

Two clinically equivalent patients differing only in age category $$elderly vs young$$ are evaluated.

Fairness condition:

$$
EquivalentClinicalState \rightarrow (Alert_{elderly} = Alert_{young})
$$

If unequal outcomes occur, subgroup disparity is flagged.

This models potential age-based bias.

---

# 3.1.5 Formal Logical Verification (Z3 SMT Layer)

Beyond simulation, selected ethical constraints are encoded as logical formulas and analyzed using the Z3 SMT solver in `z3_ethics_verification.py`.

This layer verifies structural properties of the ethical rule set.

---

## SAT Case: Duty-of-Care Consistency

$$
(Alert \land GroundTruth) \rightarrow ClinicianResponded
$$

Z3 returns SAT when obligations are satisfied, demonstrating logical consistency.

---

## UNSAT Case: Capacity Conflict

Two ethical mandates:

$$
Treat_A \land Treat_B
$$

Physical constraint:

$$
\neg (Treat_A \land Treat_B)
$$

Z3 returns UNSAT and extracts the minimal Unsat Core:

* Ethical_Treat_A
* Ethical_Treat_B
* Capacity_Constraint

This models triage deadlock under scarcity.

---

## UNSAT Case: Age-Based Fairness Violation

$$
EquivalentClinicalState \rightarrow (Alert_{elderly} = Alert_{young})
$$

Violation scenarios produce UNSAT.

Unsat Core isolates:

* Fairness_Symmetry
* Equivalent_Group_True
* Conflicting alert assignments

This demonstrates structural subgroup asymmetry.

---

## UNSAT Case: Governance Violation

$$
Alert \rightarrow Acknowledged
$$

If alert occurs without acknowledgement, Z3 returns UNSAT and identifies the violated rule.

---

## Architectural Significance

The SMT layer:

* Detects structural ethical contradictions
* Extracts minimal conflicting constraint sets
* Distinguishes behavioral violation from logical impossibility
* Complements simulation-based evaluation

Simulation identifies empirical failure modes.
SMT verification proves structural properties of the ethical rule set.

---

# 3.1.6 Scope Delimitation

The implementation does not:

* Replicate proprietary ESM weighting
* Perform ROC optimization
* Estimate AUC
* Model mortality causality
* Perform calibration analysis
* Use temporal logic (LTL/CTL)

Temporal operators were not introduced because the abstraction models discrete decision states rather than infinite execution traces.

The system focuses on threshold-based decision structure and constraint consistency.

---

# 3.2 Evidence

Execution of:

```
python functional_validation.py
```

Demonstrates:

* Correct threshold enforcement
* Discriminative scoring behavior

Execution of:

```
python ethical_validation.py
```

Demonstrates:

* False positive generation
* Automation bias detection
* Under-reliance violation
* Governance failure
* Data quality failure
* Age-based fairness scenario
* Logged audit traces

Execution of:

```
python z3_ethics_verification.py
```

Demonstrates:

* SAT duty-of-care consistency
* UNSAT capacity conflict
* UNSAT age-based fairness violation
* UNSAT governance violation
* Unsat core extraction

Screenshots included in this chapter document:

1. Functional validation traces
2. Ethical violation outputs
3. Z3 UNSAT core outputs
4. `audit.log` entries

---

# Implementation Summary

This implementation provides:

* Structural abstraction of a deployed AI-CDSS
* Explicit encoding of functional goals
* Executable ethical constraint formalization
* Behavioral violation detection
* Formal SMT-based consistency verification
* Unsat core conflict diagnosis
* Age-based subgroup fairness modeling
* Audit-trace accountability simulation

The system operationalizes ethical evaluation as constraint verification rather than post-hoc commentary.

The abstraction preserves the decision-structural properties of the Epic Sepsis Model while avoiding misrepresentation of proprietary internals.

