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

## 1️⃣ System & Stakeholder Analysis

The Epic Sepsis Model is treated as a socio-technical system rather than merely a predictive model.

This includes:

* Identification of primary and secondary stakeholders
* Separation of functional vs ethical goals
* Explicit modeling of performance trade-offs
* Responsibility boundary analysis

The system is evaluated as deployed infrastructure embedded in hospital workflows.

---

## 2️⃣ Ethical Goal Formalization

Three ethical frameworks are translated into operational constraints:

| Ethical Framework | Operational Interpretation                                       |
| ----------------- | ---------------------------------------------------------------- |
| **Utilitarian**   | Mortality reduction must not depend on excessive false positives |
| **Deontological** | Final decision authority must remain with clinicians             |
| **Virtue Ethics** | System must not induce automation bias or deskilling             |

Ethical reasoning is converted into executable validation logic rather than abstract philosophical discussion.

---

## 3️⃣ Simulation-Based Ethical Validation

`ethical_validation.py` simulates system-level behavior under controlled scenarios:

### Functional Properties

* Continuous risk scoring
* Threshold-based alert triggering
* Sensitivity-focused screening behavior

### Ethical Risk Scenarios

* False positive amplification
* Alert fatigue accumulation
* Automation bias (over-reliance)
* Automation neglect (under-reliance)
* Responsibility gap detection
* Governance constraint violations
* Data quality failure handling
* Subgroup fairness checks

This layer models how ethical failures can emerge even when predictive metrics remain strong.

Run:

```bash
python3 epic-ethical-validation/ethical_validation.py
```

---

## 4️⃣ Formal Ethical Verification (Z3 SMT Layer)

Beyond simulation, the project includes a formal verification layer using the Z3 SMT solver.

Ethical constraints are encoded as logical formulas and analyzed for satisfiability.

This layer demonstrates:

* **SAT cases** — ethical consistency is achievable
* **UNSAT cases** — structural ethical conflicts
* **Unsat Core extraction** — minimal contradictory constraint diagnosis

Formally verified cases include:

* Duty-of-care consistency
* Governance rule violations
* Fairness symmetry violations
* Resource capacity conflicts

This elevates ethical evaluation from behavioral simulation to formal logical verification.

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
