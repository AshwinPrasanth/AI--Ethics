# AI Ethics — Epic Sepsis Model Ethical Validation Framework

## Overview

This repository contains a structured simulation and formal verification framework modelling the decision-structural properties of the **Epic Sepsis Model (ESM)** — an AI-based Clinical Decision Support System (CDSS) integrated into the Epic Electronic Health Record (EHR), deployed across approximately 54% of US hospitals.

The objective is not to replicate the proprietary ESM. Instead, the framework formalises and validates the **functional and ethical properties** of a threshold-based, sub-symbolic CDSS through two complementary layers:

1. **Behavioural simulation layer** — executable ethical constraint checks
2. **Formal logical verification layer** — Z3 SMT-based constraint verification

---

## Repository Structure

```
.
├── model.py                  # Risk scoring abstraction and alert logic
├── scenarios.py              # Synthetic patient profiles
├── utils.py                  # Ethical goal utility functions
├── functional_validation.py  # Functional goal validation
├── ethical_validation.py     # Ethical constraint simulation
├── z3_ethics_verification.py # Formal SMT verification using Z3
└── audit.log                 # Runtime ethical violation audit trail
```

---

## File Descriptions

### `model.py`
Implements the simplified sepsis risk scoring abstraction. Does not replicate proprietary ESM weights. Simulates sub-symbolic weighted aggregation of clinical variables.

**Key functions:**
- `compute_risk_score(patient)` — computes a weighted risk score from patient features; raises `ValueError` on missing or corrupted inputs
- `trigger_alert(risk_score, threshold=5)` — fires an alert when score meets or exceeds the threshold, aligned with the published ESM cut-point
- `generate_explanation(patient)` — returns simulated feature contribution values approximating post-hoc interpretability
- `evaluate_threshold(patient, threshold)` — evaluates alert behaviour under alternative threshold configurations

**Domain representation:**

$$Score = \sum_i w_i x_i$$

where inputs are: Temperature, Heart Rate, Lactate, WBC, Systolic BP, Prior Antibiotics.

---

### `scenarios.py`
Defines synthetic inpatient profiles used across functional and ethical validation. All cases are fixed by design for reproducibility.

| Function | Profile | Ground Truth |
|---|---|---|
| `high_risk_patient()` | High fever, tachycardia, elevated lactate, hypotension | Septic |
| `moderate_risk_patient()` | Borderline inflammatory markers | Non-septic |
| `false_positive_patient()` | Mild inflammatory presentation | Non-septic |
| `aggressive_false_positive()` | Strong vitals, low lactate | Non-septic |
| `corrupted_patient()` | Missing temperature value | N/A |
| `elderly_high_risk_patient()` | Identical to high risk, age group: elderly | N/A |
| `young_high_risk_patient()` | Identical to high risk, age group: young | N/A |

---

### `utils.py`
Implements the three core ethical utility functions used by the simulation layer.

- `ethical_human_in_loop(alert, clinician_override)` — **E1 / Deontological:** enforces that AI cannot act without human confirmation
- `detect_over_reliance(alerts, clinician_actions)` — **E2 / Virtue Ethics:** flags blind compliance rate exceeding 90%
- `evaluate_false_positive_rate(alerts, actual_sepsis)` — **E3 / Utilitarian:** computes FPR across a set of alert/outcome pairs

---

### `functional_validation.py`
Validates the two primary functional goals of the system.

```
python functional_validation.py
```

| Goal | Test | Expected Result |
|---|---|---|
| F1 — Risk stratification | High-risk patient | Score ≥ 5 |
| F2 — Alert trigger | Moderate-risk patient | Score < 5, no alert |

**Sample output:**
```
High Risk Score: 5.75   → Alert Triggered: True
Moderate Risk Score: 2.98 → Alert Triggered: False
```

---

### `ethical_validation.py`
Simulates eight ethical constraint scenarios. Violations are logged to `audit.log` with timestamps.

```
python ethical_validation.py
```

| Constraint | Ethical School | Scenario |
|---|---|---|
| E1 — False Positive Monitoring | Utilitarian | Aggressive false positive patient |
| E2 — Over-reliance Detection | Virtue Ethics | All alerts blindly accepted |
| E3 — Under-reliance Detection | Deontological | Alert fired, clinician ignores |
| E4 — Responsibility Gap | Deontological | Alert fired, no explanation available |
| E5 — Alert Fatigue | Utilitarian | Alert counter exceeds threshold |
| E6 — Governance Constraint | Deontological | Alert fired, not acknowledged |
| E7 — Data Quality Failure | Deontological | Corrupted patient input |
| E8 — Age-Based Fairness | Deontological | Elderly vs young equivalent patients |

**Known limitation — E4:** `generate_explanation()` always returns a value in this abstraction, so the responsibility gap is never triggered in simulation. In real ESM deployment, the gap is always present as the model does not expose internal reasoning. The Z3 layer addresses this structurally.

**Known limitation — E8:** The scoring function does not use `age_group` as a feature, so simulation always returns equivalent outcomes. The fairness violation scenario is handled formally in `z3_ethics_verification.py`.

---

### `z3_ethics_verification.py`
Encodes selected ethical constraints as logical formulas and verifies them using the Z3 SMT solver. Uses `assert_and_track` for named constraint registration, enabling UNSAT core extraction.

```
python z3_ethics_verification.py
```

| Case | Result | Constraint Verified |
|---|---|---|
| Duty of Care | SAT | `(Alert ∧ GroundTruth) → ClinicianResponded` |
| Capacity Conflict | UNSAT | `Treat_A ∧ Treat_B ∧ ¬(Treat_A ∧ Treat_B)` |
| Fairness Violation | UNSAT | `EquivalentGroup → (Alert_elderly = Alert_young)` |
| Governance Violation | UNSAT | `Alert → Acknowledged` |

**Sample output:**
```
SAT:   [Alert=True, ClinicianResponded=True, Duty_of_Care=True, GroundTruth=True]
UNSAT: [Ethical_Treat_A, Ethical_Treat_B, Capacity_Constraint]
UNSAT: [Elderly_Alert_True, Equivalent_Group_True, Fairness_Symmetry, Young_Alert_False]
UNSAT: [Governance_Rule, No_Acknowledgement, Alert_Occurred]
```

UNSAT core extraction identifies the **minimal set of constraints** responsible for each contradiction, enabling targeted conflict diagnosis.

---

### `audit.log`
A persistent, timestamped log of ethical violations detected at runtime. Generated automatically by `ethical_validation.py`.

**Log levels used:**
- `INFO` — false positive events with score and FPR
- `WARNING` — over-reliance, under-reliance, fairness violations
- `ERROR` — data quality failures

**Sample entries:**
```
2026-03-02 10:23:27,524 - WARNING - Over-reliance scenario detected.
2026-03-02 10:23:27,524 - INFO    - False Positive Test - Score: 5.402, Alert: True, FPR: 1.0
2026-03-02 10:23:27,525 - WARNING - Under-reliance detected - Alert: True, Clinician responded: False
2026-03-02 10:23:27,525 - ERROR   - Data quality failure detected: Missing required feature: temperature
```

Repeated entries across dates confirm deterministic test cases. The log models the audit trail a real deployed CDSS would be expected to maintain for governance and incident review.

---

## Installation

```bash
pip install z3-solver
```

No other dependencies beyond the Python standard library.

---

## Running the Framework

```bash
# Functional validation
python functional_validation.py

# Ethical constraint simulation
python ethical_validation.py

# Formal SMT verification
python z3_ethics_verification.py
```

---

## Design Scope

This framework does **not**:
- Replicate proprietary ESM feature weights
- Perform ROC optimisation or AUC estimation
- Model mortality causality
- Use temporal logic (LTL/CTL)

It **does**:
- Preserve the decision-structural properties of a deployed AI-CDSS
- Encode functional and ethical goals as executable constraints
- Detect ethical violations through behavioural simulation
- Prove structural ethical properties through formal SMT verification
- Extract minimal conflict sets from UNSAT ethical constraint combinations
- Maintain a persistent audit trail of violations

---

## Reference

Cull, J., Brevetta, R., Gerac, J., Kothari, S., and Blackhurst, D. (2023). Epic Sepsis Model Inpatient Predictive Analytic Tool: A Validation Study. *Crit Care Explor*, 5(7), e0941. PMID: 37405252. https://doi.org/10.1097/CCE.0000000000000941
