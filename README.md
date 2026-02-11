# Ethical Validation of a Real-World Clinical AI System  
## Case Study: Epic Sepsis Model (ESM)

---

## Overview

This project performs a structured ethical validation of a real-world deployed AI system: the Epic Sepsis Model (ESM), a predictive Clinical Decision Support System used in U.S. hospitals for early sepsis detection.

Unlike typical ML projects that focus on improving predictive performance, this repository evaluates whether a high-performing clinical AI system can introduce ethical and responsibility risks at the system level.

This work examines:

- How performance-optimized models influence clinician behavior  
- Whether human decision authority is preserved in AI-assisted workflows  
- How ethical goals can be translated into formal, testable constraints  
- Where responsibility gaps emerge in safety-critical environments  

The system under study is deployed at scale in U.S. hospitals.

---

## Why This Matters

Sepsis has a mortality rate of **15–40%**, and delayed antibiotic treatment significantly increases risk of death.

The Epic Sepsis Model:

- Uses ~80 clinical and demographic features  
- Trained on ~500,000 patient encounters  
- Achieves:
  - **AUC:** 0.834  
  - **Sensitivity:** 86.0%  
  - **Specificity:** 80.8%  
- Associated with a **44% reduction in odds of sepsis-related mortality** after alert implementation  
  - (OR 0.56; 95% CI 0.39–0.80)

Despite strong performance:

- The model is proprietary  
- Internal decision logic is opaque  
- Alerts influence clinician behavior  
- Clinicians remain legally responsible  

This creates a structural human–AI responsibility asymmetry.

This project formalizes and evaluates that risk.

---

## Core Research Question

> How can we formally validate whether an AI-assisted clinical system preserves human responsibility and safe decision-making behavior?

---

## Repository Structure

### 1️⃣ Stakeholder & System Analysis (Implemented)

- Structured identification of primary and secondary stakeholders  
- Functional vs ethical goal separation  
- Explicit modeling of performance trade-offs  
- Responsibility boundary analysis  

The system is treated as a socio-technical deployment — not merely a predictive model.

---

### 2️⃣ Ethical Goal Formalization (Implemented)

Three ethical frameworks are translated into operational constraints:

| Ethical Framework | Operational Interpretation |
|------------------|----------------------------|
| **Utilitarian** | Mortality reduction must not depend on excessive false positives |
| **Deontological** | Final decision authority must remain with clinicians |
| **Virtue Ethics** | System must not induce automation bias |

Ethical reasoning is converted into structured validation logic rather than abstract discussion.

---

### 3️⃣ Constraint Validation & Simulation (In Development)

Planned validation components include:

#### Functional Validation
- Alert threshold behavior modeling  
- Sensitivity/Specificity trade-off simulation  
- Threshold optimization stress tests  

#### Ethical Validation
- Alert frequency stress testing  
- False-positive amplification scenarios  
- Automation bias modeling  
- Responsibility gap detection logic  

The objective is to simulate system-level behavior under varying operational conditions without requiring access to proprietary model internals.

---

### 4️⃣ Failure Case Demonstrations (In Development)

Planned demonstrations include scenarios where:

- High sensitivity increases alert fatigue  
- False positives drive unnecessary intervention  
- Decision authority shifts toward algorithm-driven behavior  
- Ethical goals fail while performance metrics remain strong  

These cases aim to illustrate how performance improvements can coexist with ethical degradation.

---

## Technical Stack

- Python  
- Constraint modeling logic  
- Simulation-based system validation  
- Structured scenario testing  

The implementation prioritizes:

- Clear system modeling  
- Traceable logic  
- Explicit ethical constraint definition  
- Reproducibility  

---

## Key Contributions

This project demonstrates:

- System-level thinking beyond model accuracy  
- Formal translation of ethical theory into executable constraints  
- Analysis of AI influence on human decision behavior  
- Risk modeling in safety-critical AI deployment  

It evaluates AI as deployed infrastructure — not merely as a statistical model.

---

## Technical Domains Explored

- AI system analysis  
- Human–AI interaction modeling  
- Ethical constraint formalization  
- Safety-critical risk assessment  
- Structured technical documentation  

---

## Why This Project Is Different

Most AI repositories focus on:

- Improving predictive performance  
- Adding explainability modules  
- Benchmark optimization  

This project focuses on:

Ensuring AI systems do not silently erode human responsibility while improving outcomes.

In safety-critical domains, performance metrics are necessary.

They are not sufficient.

---

## Future Extensions

- Formal verification using SMT solvers (e.g., Z3)  
- Dynamic threshold optimization under ethical constraints  
- Behavioral modeling of clinician reliance  
- Real-time monitoring dashboards for ethical risk signals  
