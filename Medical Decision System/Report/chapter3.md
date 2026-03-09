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

This implementation does not attempt model reproduction. Instead, it preserves the operational invariants that define the system's decision structure:

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

$$x = (T, HR, Lactate, WBC, SBP, PriorAntibiotics)$$

Where:

- $T$: Temperature
- $HR$: Heart rate
- $Lactate$: Serum lactate
- $WBC$: White blood cell count
- $SBP$: Systolic blood pressure
- $PriorAntibiotics$: Binary indicator

These variables represent a reduced clinically meaningful subset of ESM inputs.

The risk score is computed as:

$$Score = \sum_i w_i x_i$$

with fixed weights $w_i$. The purpose is not predictive realism, but simulation of sub-symbolic weighted aggregation of heterogeneous physiological signals.

---

## 3.1.3 Functional Goal Encoding

Functional goals are encoded in `functional_validation.py`.

---

### F1: Continuous Risk Stratification

The system produces a real-valued risk score for each patient.

Validation:

- High-risk synthetic cases → $Score \geq 5$
- Moderate-risk synthetic cases → $Score < 5$

This confirms discriminative behavior.

---

### F2: Deterministic Alert Trigger

Alert condition:

$$Alert = (Score \geq 5)$$

The threshold of 5 aligns with the published ESM validation cut-point.

Validation confirms:

- Alert = True for high-risk patients
- Alert = False for moderate-risk patients

---

### F3: Workflow Activation

If $Alert = True$, the system simulates:

- Escalation to clinician
- Decision node requiring response

This models the real-world operational role of ESM alerts in hospital EHR workflows.

---

## 3.1.4 Ethical Goal Formalization (Simulation Layer)

Ethical goals are encoded as executable constraint checks in `ethical_validation.py`.

---

### E1: False Positive Monitoring (Utilitarian Trade-Off)

Condition:

$$Alert = True \land GroundTruth = False$$

False Positive Rate is computed as:

$$FPR = \frac{FP}{FP + TN}$$

If $FPR > 0$, alert fatigue risk is flagged and logged.

This models the trade-off between sensitivity optimization and unnecessary intervention.

---

### E2: Over-Reliance Detection (Automation Bias)

Condition:

$$Alert = True \land ClinicianAction = Accept \land GroundTruth = False$$

This detects blind compliance with AI output and captures epistemic over-dependence.

---

### E3: Under-Reliance Detection (Automation Neglect)

Condition:

$$Alert = True \land ClinicianAction = Ignore$$

If triggered, the system reports:

$$EthicalGoalSatisfied = False$$

This encodes failure to act under elevated risk.

---

### E4: Responsibility Gap Detection

Condition:

$$Alert = True \land ExplanationUnavailable$$

This models the epistemic asymmetry where clinicians remain accountable without interpretive access.

**Known abstraction limitation:** In the implementation, `generate_explanation()` always returns a feature contribution dictionary, meaning `ExplanationUnavailable` is always False and the responsibility gap is never triggered in simulation. This is a deliberate abstraction boundary: the real ESM does not expose its internal reasoning to clinicians, meaning in deployment the gap would be present. The Z3 layer addresses this structurally. This limitation is acknowledged rather than obscured.

---

### E5: Alert Fatigue Monitoring

Repeated alerts are accumulated across a session.

If alert frequency exceeds a defined threshold (counter > 5), fatigue risk is flagged.

This models workflow burden accumulation over time.

---

### E6: Governance Constraint

Condition:

$$Alert \rightarrow Acknowledged$$

If violated, governance failure is reported and logged. This encodes the institutional requirement that no alert may be silently ignored without clinician acknowledgement.

---

### E7: Data Quality Failure

Corrupted or incomplete patient inputs trigger exceptions and logging.

This models infrastructural and deployment-level ethical risk. When `temperature: None` is passed, a `ValueError` is raised and caught, and the failure is written to `audit.log`.

---

### E8: Age-Based Fairness Scenario

Two clinically equivalent patients differing only in age category (elderly vs young) are evaluated.

Fairness condition:

$$EquivalentClinicalState \rightarrow (Alert_{elderly} = Alert_{young})$$

If unequal outcomes occur, subgroup disparity is flagged and logged.

**Note on simulation output:** Because the current scoring function does not incorporate `age_group` as a weighted feature, both patients receive identical scores and the simulation returns no disparity. This is expected and correct behavior for the simulation layer. The fairness *violation* scenario is handled formally in the Z3 layer, which proves that equivalent clinical state combined with different alert outcomes is logically unsatisfiable under the fairness constraint.

---

## 3.1.5 Formal Logical Verification (Z3 SMT Layer)

Beyond simulation, selected ethical constraints are encoded as logical formulas and analyzed using the Z3 SMT solver in `z3_ethics_verification.py`.

This layer verifies structural properties of the ethical rule set. Constraints are registered using `assert_and_track`, enabling UNSAT core extraction — identification of the minimal set of constraints responsible for a logical contradiction.

---

### SAT Case: Duty-of-Care Consistency

$$( Alert \land GroundTruth) \rightarrow ClinicianResponded$$

Z3 returns SAT when obligations are satisfied, demonstrating logical consistency. The model confirms that the system *can* operate ethically — duty-of-care constraints are simultaneously satisfiable when the clinician responds to a valid alert.

---

### UNSAT Case: Capacity Conflict

Two ethical mandates:

$$Treat_A \land Treat_B$$

Physical constraint:

$$\neg(Treat_A \land Treat_B)$$

Z3 returns UNSAT and extracts the minimal Unsat Core:

- `Ethical_Treat_A`
- `Ethical_Treat_B`
- `Capacity_Constraint`

This models triage deadlock under resource scarcity. Removing any single constraint from the core resolves the contradiction, isolating where ethical trade-offs must be made.

---

### UNSAT Case: Age-Based Fairness Violation

$$EquivalentClinicalState \rightarrow (Alert_{elderly} = Alert_{young})$$

Violation scenarios produce UNSAT. Unsat Core isolates:

- `Elderly_Alert_True`
- `Equivalent_Group_True`
- `Fairness_Symmetry`
- `Young_Alert_False`

This demonstrates that differential alert outcomes for clinically equivalent patients are structurally incompatible with the fairness constraint — not merely a runtime anomaly but a logical impossibility.

---

### UNSAT Case: Governance Violation

$$Alert \rightarrow Acknowledged$$

If alert occurs without acknowledgement, Z3 returns UNSAT and identifies the violated rule. Unsat Core:

- `Governance_Rule`
- `Alert_Occurred`
- `No_Acknowledgement`

---

### Architectural Significance

The SMT layer:

- Detects structural ethical contradictions
- Extracts minimal conflicting constraint sets
- Distinguishes behavioral violation from logical impossibility
- Complements simulation-based evaluation

Simulation identifies empirical failure modes. SMT verification proves structural properties of the ethical rule set. Together they provide complementary coverage: one empirical, one formal.

---

## 3.1.6 Scope Delimitation

The implementation does not:

- Replicate proprietary ESM weighting
- Perform ROC optimization
- Estimate AUC
- Model mortality causality
- Perform calibration analysis
- Use temporal logic (LTL/CTL)

Temporal operators were not introduced because the abstraction models discrete decision states rather than infinite execution traces. The system focuses on threshold-based decision structure and constraint consistency.

---

# 3.2 Points of Conflict

This section identifies the value conflicts that prompted substantive revisions to the architectural and design decisions made during implementation.

---

## Conflict 1: Fairness vs. Clinical Equivalence

**Original design decision:** The initial scoring model treated all patients identically, using only physiological variables (temperature, heart rate, lactate, WBC, systolic blood pressure). No subgroup differentiation was modeled or tested.

**Value conflict identified:** During stakeholder analysis in Chapter 2, deontological and virtue ethics considerations raised the question of whether a system that does not explicitly test for subgroup equity could inadvertently produce discriminatory outcomes — particularly for elderly patients, who may present with atypical sepsis physiology. The absence of fairness testing is itself an ethical risk.

**Design change:** Two additional synthetic patient scenarios were introduced — `elderly_high_risk_patient()` and `young_high_risk_patient()` — with identical clinical values but different age group labels. A fairness check was added to the simulation layer (E8) and a formal fairness symmetry constraint was encoded in the Z3 layer.

**Stakeholders who benefit:** Patients, particularly elderly patients whose atypical presentations may be underweighted in real predictive models. Regulators and accreditation bodies who require evidence of non-discriminatory system behavior.

**Residual limitation acknowledged:** The current scoring function does not use `age_group` as a feature, so the simulation always returns equivalent outcomes. The Z3 layer formally proves what would happen *if* the system produced unequal outcomes, demonstrating the detection mechanism is structurally sound even where the simulation cannot trigger it.

---

## Conflict 2: Transparency vs. Proprietary Opacity

**Original design decision:** The initial abstraction included a `generate_explanation()` function that returned feature contribution values, treating interpretability as an available capability.

**Value conflict identified:** This misrepresented the real ESM, which does not expose its internal reasoning to clinicians. The deontological concern around accountability — clinicians being responsible for decisions they cannot fully explain — required the abstraction to reflect this opacity rather than paper over it.

**Design change:** The E4 responsibility gap constraint was retained but its behavior was documented as a known abstraction limitation. The Z3 layer was extended to formally model the governance and accountability constraints that the simulation layer could not fully instantiate. This preserves intellectual honesty about what the abstraction can and cannot demonstrate.

**Stakeholders who benefit:** Clinicians, who retain explicit acknowledgement that accountability gaps exist in the real system. Patients, whose safety depends on clinicians understanding the limits of AI-generated scores.

---

## Conflict 3: Sensitivity Optimization vs. Alert Fatigue

**Original design decision:** The alert threshold was fixed at Score ≥ 5, mirroring the published ESM validation cut-point, without analysis of how threshold variation affects ethical outcomes.

**Value conflict identified:** The utilitarian analysis in Chapter 2 identified that optimizing for sensitivity (minimising missed sepsis cases) necessarily increases false positives, which accumulates alert burden on clinicians over time. This is a direct value conflict between population-level mortality benefit and individual clinician workflow sustainability.

**Design change:** A threshold trade-off simulation was added (`simulate_threshold_tradeoff()`), evaluating alert behavior at thresholds of 4, 5, and 7. An alert fatigue counter (E5) was added to accumulate alert frequency and flag when the threshold is exceeded. The audit log records both false positive events and fatigue warnings, enabling retrospective analysis of burden accumulation.

**Stakeholders who benefit:** Clinicians, whose alert burden is made visible and measurable. Hospitals, which can use threshold configuration as a governance lever. Patients, indirectly, through clinicians who remain attentive rather than desensitised.

---

# 3.3 Evidence

## Functional Validation Output

Execution of:

```
python functional_validation.py
```

**Output:**

```
--- Functional Validation ---
High Risk Score: 5.750000000000001
Alert Triggered: True
Moderate Risk Score: 2.9800000000000013
Alert Triggered: False
```

A clinically high-risk patient profile produces a score of 5.75, correctly triggering an alert. A moderate-risk profile scores 2.98, correctly suppressing the alert. The separation either side of the threshold of 5 is deliberate — synthetic scenarios are fixed by design for reproducibility. This validates functional goals **F1** (continuous risk stratification) and **F2** (deterministic alert trigger).

> 📸 *[Insert screenshot: functional_validation.py terminal output]*

---

## Ethical Validation Output

Execution of:

```
python ethical_validation.py
```

**Output:**

```
--- Over-reliance Scenario ---
Over-reliance detected: True

--- Basic False Positive Case ---
False Positive Rate: 0.0

--- Aggressive False Positive Case ---
Aggressive False Positive Score: 5.402000000000001
Alert Triggered: True
False Positive Rate: 1.0

--- Under-reliance Scenario ---
Alert: True
Clinician responded: False
Ethical goal satisfied: False

--- Responsibility Gap Test ---
Alert: True
Explanation available: True
Responsibility gap detected: False

--- Threshold Trade-Off Simulation ---
Threshold: 4  | Alert: True  | FPR: 1.0
Threshold: 5  | Alert: True  | FPR: 1.0
Threshold: 7  | Alert: False | FPR: 0.0

--- Reliance Calibration Test ---
Reliance type: Blind Compliance

--- Alert Fatigue Simulation ---
Alert fatigue triggered: True

--- Governance Check ---
Governance constraint satisfied: False

--- Data Quality Failure Scenario ---
Data quality failure detected: Missing required feature: temperature

--- Fairness Across Subgroups ---
Elderly Alert: True
Young Alert: True
No subgroup disparity detected.
```

**Interpretation by ethical goal:**

| Output | Ethical Goal | Result |
|---|---|---|
| Over-reliance detected: True | E2 — Automation Bias | Violation detected |
| Basic FPR: 0.0 | E1 — False Positive Monitoring | No alert fired (correct — mild vitals below threshold) |
| Aggressive FPR: 1.0 | E1 — False Positive Monitoring | Violation flagged and logged |
| Ethical goal satisfied: False | E3 — Under-reliance | Violation detected |
| Responsibility gap: False | E4 — Responsibility Gap | Abstraction limitation (see 3.1.4) |
| Alert fatigue: True | E5 — Alert Fatigue | Violation flagged |
| Governance satisfied: False | E6 — Governance | Violation detected |
| Data quality failure | E7 — Data Quality | Exception caught and logged |
| No subgroup disparity | E8 — Fairness | Simulation equivalent; Z3 handles formal case |

> 📸 *[Insert screenshot: ethical_validation.py terminal output]*

---

## Z3 Formal Verification Output

Execution of:

```
python z3_ethics_verification.py
```

**Output:**

```
--- SAT: Duty of Care Scenario ---
Solver result: sat
Model: [Alert = True,
        ClinicianResponded = True,
        Duty_of_Care = True,
        GroundTruth = True]

--- UNSAT: Capacity Conflict ---
Solver result: unsat
Unsat Core: [Ethical_Treat_A, Ethical_Treat_B, Capacity_Constraint]

--- UNSAT: Fairness Violation ---
Solver result: unsat
Unsat Core: [Elderly_Alert_True,
             Equivalent_Group_True,
             Fairness_Symmetry,
             Young_Alert_False]

--- UNSAT: Governance Violation ---
Solver result: unsat
Unsat Core: [Governance_Rule, No_Acknowledgement, Alert_Occurred]
```

The SAT result confirms that the ethical rule set is logically consistent under compliant behaviour — duty-of-care constraints can be simultaneously satisfied. The three UNSAT results prove that fairness violations, triage deadlock, and governance failures are not merely detectable at runtime but are logically impossible to reconcile with their respective ethical constraints. UNSAT core extraction identifies the minimal responsible constraint sets, enabling targeted conflict diagnosis rather than requiring exhaustive search.

> 📸 *[Insert screenshot: z3_ethics_verification.py terminal output]*

---

## Audit Log

```
2026-02-28 17:46:42,891 - WARNING  - Over-reliance scenario detected.
2026-02-28 17:46:42,892 - INFO     - False Positive Test - Score: 5.402, Alert: True, FPR: 1.0
2026-02-28 17:46:42,892 - WARNING  - Under-reliance detected - Alert: True, Clinician responded: False
2026-03-02 10:23:27,524 - WARNING  - Over-reliance scenario detected.
2026-03-02 10:23:27,524 - INFO     - False Positive Test - Score: 5.402, Alert: True, FPR: 1.0
2026-03-02 10:23:27,525 - WARNING  - Under-reliance detected - Alert: True, Clinician responded: False
2026-03-02 10:23:27,525 - ERROR    - Data quality failure detected: Missing required feature: temperature
2026-03-02 10:26:22,738 - WARNING  - Over-reliance scenario detected.
2026-03-02 10:26:22,738 - INFO     - False Positive Test - Score: 5.402, Alert: True, FPR: 1.0
2026-03-02 10:26:22,738 - WARNING  - Under-reliance detected - Alert: True, Clinician responded: False
2026-03-02 10:26:22,738 - ERROR    - Data quality failure detected: Missing required feature: temperature
```

The audit log provides a persistent, timestamped accountability trace of ethical violations detected across multiple runs. Repeated entries across dates confirm that the test scenarios are deterministic by design — synthetic patient cases are fixed for reproducibility, not randomised. The log records over-reliance warnings, false positive events, under-reliance violations, and data quality failures. This models the audit trail that a real deployed CDSS would be expected to maintain for governance and incident review purposes.

> 📸 *[Insert screenshot: audit.log file content]*

---

# Implementation Summary

This implementation provides:

- Structural abstraction of a deployed AI-CDSS
- Explicit encoding of functional goals
- Executable ethical constraint formalization
- Behavioral violation detection
- Formal SMT-based consistency verification
- Unsat core conflict diagnosis
- Age-based subgroup fairness modeling
- Audit-trace accountability simulation

The system operationalizes ethical evaluation as constraint verification rather than post-hoc commentary. The abstraction preserves the decision-structural properties of the Epic Sepsis Model while avoiding misrepresentation of proprietary internals. Known abstraction limitations — particularly around responsibility gap detection and fairness simulation — are explicitly acknowledged rather than obscured, and are addressed through complementary formal verification.
