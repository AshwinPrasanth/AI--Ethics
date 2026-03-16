# Ethical Validation of a Real World Clinical AI System

## Case Study: Epic Sepsis Model (ESM)

---

## Overview

This project performs a structured ethical validation of a real-world deployed AI system: the **Epic Sepsis Model (ESM)**, a predictive Clinical Decision Support System (CDSS) used in U.S. hospitals for early sepsis detection.

Unlike typical machine learning projects that focus on improving predictive performance, this repository evaluates whether a high-performing clinical AI system can introduce ethical and responsibility risks at the system level.

The project examines:

* How performance-optimized models influence clinician behavior
* Whether human decision authority is preserved in AI-assisted workflows
* How ethical goals can be translated into formal, testable constraints
* Where responsibility gaps emerge in safety-critical environments

The system under study is deployed at national scale and directly influences clinical decision-making.

---

## Why This Matters

Sepsis is a life-threatening condition with a mortality rate of **15–40%**. Delayed antibiotic treatment significantly increases mortality risk.

The Epic Sepsis Model:

* Uses ~80 clinical and demographic features
* Trained on ~500,000 patient encounters
* Achieves:

  * **AUC:** 0.834
  * **Sensitivity:** 86.0%
  * **Specificity:** 80.8%
* Associated with a **44% reduction in odds of sepsis-related mortality** after alert implementation

  * (OR 0.56; 95% CI 0.39–0.80)

Despite strong predictive performance:

* The model is proprietary
* Internal decision logic is opaque
* Alerts influence clinician behavior
* Clinicians remain legally responsible

This creates a structural human–AI responsibility asymmetry.

This project formalizes and evaluates that asymmetry.

---

## Core Research Question

> How can ethical properties of a deployed AI-assisted clinical system be expressed as formal constraints and validated independently of model performance?

---

## Repository Structure

```
epic-ethical-validation/
│
├── functional_validation.py
├── ethical_validation.py
├── z3_ethics_verification.py
├── model.py
├── scenarios.py
├── utils.py
├── audit.log
└── README.md
```

---

## 1. System and Stakeholder Analysis

The Epic Sepsis Model is treated as a socio-technical system rather than merely a predictive model.

This includes:

* Identification of primary and secondary stakeholders
* Separation of functional vs ethical goals
* Explicit modeling of performance trade-offs
* Responsibility boundary analysis

The system is evaluated as deployed infrastructure embedded in hospital workflows.

---

## 2. Ethical Goal Formalization

Three ethical frameworks are translated into operational constraints. Each goal specifies a named principle, a measurable condition, and a violation trigger.

### Utilitarian Ethics (Mill, harm minimisation and greatest aggregate benefit)

| Goal | Principle | Measurable Condition | Violation Trigger |
|------|-----------|----------------------|-------------------|
| U1: Minimise preventable mortality | Greatest aggregate benefit: the alert system is ethically justified only if mortality reduction across the treated population outweighs the aggregate harm caused by false positive alerts | Odds ratio of sepsis mortality in the alert-active period must remain below 1.0 (published: OR 0.56, 95% CI 0.39–0.80) | True positive response rate falls below pre-implementation baseline |
| U2: Control false positive burden | Harm minimisation: cumulative false positive burden must not reduce clinician responsiveness to genuine alerts | Clinician override rate must not exceed 70% across consecutive alert sessions | Override rate > 70% or statistically significant increase in time to antibiotic administration |

### Deontological Ethics (Kant, respect for rational agency and rule-based governance)

| Goal | Principle | Measurable Condition | Violation Trigger |
|------|-----------|----------------------|-------------------|
| D1: Preserve clinician epistemic access | Kantian duty of non-deception: a clinician held legally responsible for a clinical decision must have meaningful epistemic access to the basis of the information that prompted that decision | For every alert fired, the clinician must be able to access the top contributing feature variables and their directional influence on the score | Any alert fired without feature-level explanation — violated for 100% of alerts in the current ESM deployment |
| D2: Enforce governance accountability | Rule-based governance: Alert(A) implies Acknowledged(C, T) — every alert must be formally acknowledged by a responsible clinician within response window T | For all alerts A, a clinician acknowledgement C must exist within window T | Any alert passing without documented acknowledgement within the response window — verified formally using Z3 SMT |

### Virtue Ethics (Aristotle, phronesis and professional competence)

| Goal | Principle | Measurable Condition | Violation Trigger |
|------|-----------|----------------------|-------------------|
| V1: Prevent automation bias | Phronesis: the system must support rather than displace the exercise of practical clinical wisdom | Clinician compliance rate with alerts must not exceed 90% without documented independent clinical assessment | Compliance rate > 90% without independent assessment documentation |
| V2: Prevent clinical deskilling | Maintenance of professional competence: repeated uncritical reliance on AI alerts degrades the diagnostic calibration required for safe independent practice over time | Independent override decisions must not fall below a defined minimum frequency per clinician per month | Override rate below minimum threshold per clinician per defined period |

---

## 3. Simulation-Based Ethical Validation

`ethical_validation.py` simulates system-level behavior under controlled scenarios:

### Functional Properties

* Continuous risk scoring
* Threshold-based alert triggering
* Sensitivity-focused screening behavior

### Ethical Risk Scenarios

Each scenario is linked to the ethical goal it operationalises:

| Scenario | Ethical Goal | School |
|----------|--------------|--------|
| False positive amplification | U2 | Utilitarianism |
| Alert fatigue accumulation | U2 | Utilitarianism |
| Automation bias (over-reliance) | V1 | Virtue Ethics |
| Automation neglect (under-reliance) | V1 | Virtue Ethics |
| Responsibility gap detection | D1 | Deontological |
| Governance constraint violation | D2 | Deontological |
| Data quality failure handling | D2 | Deontological |
| Subgroup fairness check | D1 | Deontological |

This layer models how ethical failures can emerge even when predictive metrics remain strong.

Run:

```bash
python3 epic-ethical-validation/ethical_validation.py
```

---

## 4. Formal Ethical Verification (Z3 SMT Layer)

Beyond simulation, the project includes a formal verification layer using the Z3 SMT solver.

Ethical constraints are encoded as logical formulas and analyzed for satisfiability.

Each formally verified case is linked to a named ethical goal and principle:

| Case | Result | Ethical Goal | Formal Constraint |
|------|--------|--------------|-------------------|
| Duty of care consistency | SAT | D2 | Alert AND GroundTruth implies ClinicianResponded |
| Capacity conflict (triage deadlock) | UNSAT | U1 | Ethical_Treat_A AND Ethical_Treat_B contradicts Capacity_Constraint |
| Fairness symmetry violation | UNSAT | D1 | EquivalentGroup implies elderly_alert == young_alert — violated by differential alert outcomes |
| Governance violation | UNSAT | D2 | Alert implies Acknowledged — violated by unacknowledged alert |

UNSAT results confirm that the ethical violation is a logical contradiction rather than an empirical observation. Violations are therefore detectable before deployment, not only after adverse outcomes occur.

Run:

```bash
python3 epic-ethical-validation/z3_ethics_verification.py
```

---

## Technical Stack

* Python
* Structured scenario simulation
* Constraint-based ethical validation
* SMT-based formal verification (Z3)
* Unsat core conflict analysis
* Reproducible test execution

The implementation prioritizes:

* Clear system modeling
* Explicit ethical constraint definition
* Traceable validation logic
* Separation of behavioral and formal verification layers

---

## Key Contributions

This project demonstrates:

* System-level ethical analysis beyond model accuracy
* Formal translation of ethical theory into executable constraints
* Behavioral modeling of human–AI interaction risks
* Structural conflict diagnosis using SMT solving
* Ethical validation independent of proprietary model internals

It evaluates AI as deployed infrastructure — not merely as a statistical artifact.

---

## Why This Project Is Different

Most AI repositories focus on:

* Improving predictive performance
* Adding explainability modules
* Benchmark optimization

This project focuses on:

Ensuring that AI systems do not silently erode human responsibility while improving outcomes.

In safety-critical domains, performance metrics are necessary.

They are not sufficient.

---
