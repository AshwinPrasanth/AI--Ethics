# Chapter 2: Stakeholder Identification

The Epic Sepsis Model (ESM) operates within a complex hospital environment involving clinical personnel, patients, healthcare institutions, and technology providers. As a deployed AI-enabled Clinical Decision Support System (CDSS), its ethical impact arises from interactions between these stakeholders rather than from the predictive model alone.

This chapter identifies the primary and secondary stakeholders affected by the system and maps them across social, technical, economic, environmental, political and legal dimensions.

---

## 2.1 Stakeholders of the Epic Sepsis Model

### Primary Stakeholders

Primary stakeholders are those who directly interact with the system or are directly affected by its outputs.

---

### 1. Clinicians (Physicians and Nurses)

**Category:** Social, Technical, Legal

Clinicians are the primary users of the ESM. The system generates alerts when a patient's sepsis risk score exceeds a predefined threshold (ESM ≥ 5), prompting clinical evaluation and intervention.

Although clinicians retain final decision-making authority, the alerts influence attention, prioritisation, and timing of treatment. Clinicians are also legally accountable for patient outcomes, even when decisions are informed by AI-generated risk scores.

---

### 2. Patients

**Category:** Social, Ethical, Legal

Hospitalised patients are the subjects of the predictive model. They do not directly interact with the system but are affected by its outputs through changes in clinical behaviour, including earlier antibiotic administration and ICU escalation.

Patients bear the risks of false positives (unnecessary treatment, antibiotic overuse) and false negatives (missed or delayed diagnosis).

---

### 3. Hospital and Healthcare Providers

**Category:** Economic, Technical, Legal

Hospitals deploy the ESM as part of the Epic EHR infrastructure. They benefit from potential reductions in mortality, length of stay, and compliance with sepsis quality measures. At the same time, hospitals assume institutional liability and must manage alert fatigue, workflow disruption, and training requirements.

---

### Secondary Stakeholders

---

### 4. Epic Systems Corporation

**Category:** Technical, Economic, Legal

Epic develops and maintains the proprietary ESM algorithm. Its design choices including feature selection, model updates and alert presentation shape how clinicians interpret and act on risk scores.

---

### 5. Health Regulators and Accreditation Bodies

**Category:** Political, Legal

Regulatory bodies influence adoption of sepsis detection systems through quality standards, reporting requirements, and patient safety regulations. Although the ESM is not publicly regulated as a medical device, its use affects compliance with national sepsis guidelines.

---

### 6. Society and Public Health Systems

**Category:** Social, Economic

At a population level, widespread deployment of sepsis detection tools influences healthcare costs, antibiotic stewardship, and public trust in AI-assisted medicine.

---

### 7. Environmental and Infrastructure Considerations

**Category:** Environmental, Technical

Large scale deployment across hospital networks contributes to cumulative energy consumption and infrastructure expansion. While individual risk score computations have negligible marginal environmental impact, responsible digital health governance must consider long-term sustainability of computational infrastructure.

---

## 2.2 Ethical Goals of the System

The Epic Sepsis Model does not publish an explicit ethical framework or set of ethical principles. Public documentation and validation studies focus primarily on clinical effectiveness, workflow integration, and patient outcomes.

There are no explicit public statements addressing transparency, accountability, or ethical safeguards beyond standard clinical governance practices.

This absence is ethically relevant, as it requires ethical safeguards to be inferred from system behaviour and deployment structure rather than from explicitly articulated normative commitments.

---

## 2.3 Ethical Considerations and Schools of Thought

For this project, three ethical frameworks are used to analyse the system:

- **Utilitarianism**
- **Deontological Ethics**
- **Virtue Ethics**

These were selected because they capture outcome-based, duty-based, and professional character-based ethical concerns relevant to clinical AI systems.

---

### 1. Utilitarian Ethics (Outcome-Oriented)

**Core Principle:** Actions are ethically justified if they maximise overall benefit and minimise harm across all affected parties (Bentham, Mill).

#### Relevant Variables and System Functionality

- Sepsis mortality rates across the patient population
- Time to antibiotic administration per alert
- False positive rate (FPR) and its burden on clinical workflow
- Hospital-wide resource utilisation

#### Ethical Goal U1: Minimise Preventable Sepsis Mortality

**Actionable Principle (Utilitarian — Greatest Aggregate Benefit):** The ESM alert system is ethically justified only if the reduction in sepsis-related mortality across the treated population outweighs the aggregate harm caused by false positive alerts, including unnecessary antibiotic administration, increased costs, and alert fatigue-induced inattention. Vasey et al. [4] (DECIDE-AI) demonstrate that ethical risks in AI-based CDSS frequently arise from deployment failures rather than model errors, meaning the utilitarian calculation must be evaluated continuously in real-world conditions, not only at the point of validation.

**Measurable Condition:** The system satisfies this principle if the odds ratio of sepsis-related mortality in the alert-active period remains below 1.0 at a statistically significant level (p < 0.05). The published validation study [1] reports OR = 0.56 (95% CI 0.39–0.80), satisfying this condition at the studied institution.

**Violation Trigger:** If post-deployment monitoring reveals that the false positive burden has increased clinician override rates to the point where true positive alerts are being systematically ignored, the net utility calculation is violated. Specifically, if the proportion of true positive alerts acted upon falls below the proportion in the pre-implementation period, the system no longer produces net benefit and the utilitarian justification for its deployment fails.

#### Ethical Goal U2: Control False Positive Burden

**Actionable Principle (Utilitarian — Harm Minimisation):** The false positive rate must be controlled such that the cumulative harm of unnecessary interventions does not outweigh the benefit of early detection. A system with sensitivity optimised at 86.0% and PPV of 33.8% accepts that approximately two in three alerts are false positives [1]. This trade-off is ethically acceptable only if alert fatigue does not reduce the clinical response rate to true positive alerts. Shwedeh and Alzoubi [2] demonstrate empirically that over-reliance and alert fatigue emerge specifically in high-pressure deployment environments where governance and oversight are insufficient, reinforcing that this condition must be actively monitored rather than assumed.

**Measurable Condition:** Alert fatigue is operationally defined as a clinician override rate exceeding 70% across consecutive alert sessions. If this threshold is crossed, the PPV of acted-upon alerts falls below the level required for net population benefit.

**Violation Trigger:** Override rate > 70% across a rolling window of alerts, or a statistically significant increase in time-to-antibiotic following the introduction of the alert system.

---

### 2. Deontological Ethics (Duty and Responsibility)

**Core Principle:** Ethical action is determined by adherence to duties and rules, independent of outcomes. Agents must be treated as rational ends in themselves, not merely as means (Kant, *Groundwork of the Metaphysics of Morals*).

#### Relevant Variables and System Functionality

- Availability of model reasoning to clinicians
- Clinician legal and moral accountability for alert-informed decisions
- Governance requirement for alert acknowledgement

#### Ethical Goal D1: Preserve Clinician Epistemic Access (Duty of Non-Deception)

**Actionable Principle (Kantian — Respect for Rational Agency):** A clinician who is held legally and morally responsible for a clinical decision must have meaningful epistemic access to the basis of the information that prompted that decision. Denying access to model reasoning while retaining accountability violates the Kantian duty to treat rational agents as ends in themselves, the clinician is reduced to a conduit for automated output rather than a deliberating professional. Amann et al. [6] establish that lack of explainability causes systems nominally classified as decision support to drift toward decision determining, undermining meaningful human oversight. Xu et al. [2] further argue that interpretability is a fundamental ethical requirement for AI-based CDSS, not an optional feature, and that post-hoc explanation methods alone are insufficient to guarantee accountability. Čartolovni et al. [4] identify the resulting accountability gap where formal responsibility remains with the clinician while practical epistemic control has shifted to the AI as the dominant ethical concern in the AI-based medical decision support literature.

**Measurable Condition:** The system satisfies this principle if, for every alert fired, the clinician can access at minimum the top contributing feature variables and their directional influence on the score. The current ESM does not satisfy this condition, feature-level reasoning is not exposed to bedside clinicians.

**Violation Trigger:** Any alert fired without accompanying feature-level explanation constitutes a violation of this principle. In the current deployment, this condition is violated for 100% of alerts.

#### Ethical Goal D2: Enforce Governance Accountability (Duty of Institutional Responsibility)

**Actionable Principle (Deontological — Rule-Based Governance):** Every alert fired by the system must be formally acknowledged by a responsible clinician. An unacknowledged alert represents a failure of the institutional duty of care, the system has identified a patient at risk and no accountable agent has accepted responsibility for the assessment.

**Measurable Condition:** Governance is satisfied if and only if: for all alerts A fired by the system, there exists a corresponding clinician acknowledgement C within a defined response window T. Formally: Alert(A) → Acknowledged(C, T).

**Violation Trigger:** Any alert that passes without documented clinician acknowledgement within the response window violates this rule. This is operationalised as the governance_check constraint in the implementation and verified formally using Z3 SMT.

---

### 3. Virtue Ethics (Professional Character and Practice)

**Core Principle:** Ethical systems should cultivate and support good professional character such as practical wisdom (phronesis), attentiveness, and calibrated judgement rather than replace them (Aristotle, *Nicomachean Ethics*).

#### Relevant Variables and System Functionality

- Clinician override and compliance patterns over time
- Alert frequency and its effect on attentiveness
- Long-term effect of AI-assisted workflows on clinical skill

#### Ethical Goal V1: Prevent Automation Bias and Preserve Clinical Prudence

**Actionable Principle (Virtue Ethics — Phronesis):** A clinical AI system must be designed and deployed in a way that supports rather than displaces the exercise of practical wisdom. Automation bias — the tendency to follow AI output without independent assessment — directly undermines phronesis. A system that produces this effect at scale is ethically deficient regardless of its population-level mortality benefit. Panigutti et al. [7] provide empirical evidence that AI explanations systematically increase human reliance on AI advice regardless of whether that reliance improves decision accuracy, demonstrating that the problem of automation bias cannot be resolved by adding explanations alone. Čartolovni et al. [5] identify automation bias and deskilling as the most clinician-specific ethical risks in AI-based medical decision support, directly implicating virtue ethics as the relevant framework.

**Measurable Condition:** Automation bias is operationally present if the clinician compliance rate with alerts defined as the proportion of alerts followed without documented independent clinical assessment exceeds 90% across a rolling observation window.

**Violation Trigger:** Compliance rate > 90% without documented independent assessment, operationalised as the detect_over_reliance constraint in the implementation (threshold: compliance_rate > 0.9).

#### Ethical Goal V2: Prevent Clinical Deskilling

**Actionable Principle (Virtue Ethics — Maintenance of Professional Competence):** Repeated reliance on AI-generated alerts without active clinical reasoning constitutes a long-term threat to the professional competence required for safe independent practice. Clinicians who have not practiced independent sepsis assessment over an extended period may lose the diagnostic calibration that makes meaningful human oversight possible. Čartolovni et al. [5] explicitly identify deskilling and loss of epistemic authority as physician-specific ethical risks in AI-based decision support, distinct from automation bias a clinician may not be biased in any given moment but may have cumulatively lost the skill required for genuine independent assessment.

**Measurable Condition:** Deskilling risk is flagged if clinician independent override decisions, cases where a clinician actively disagrees with and documents a reasoned rejection of an alert fall below a defined minimum frequency per clinician per month.

**Violation Trigger:** Independent override rate < minimum threshold per clinician per defined period, indicating habitual passive compliance rather than active clinical engagement.

---

## 2.4 Values

### Stakeholder Values and Alignment

| Stakeholder | Primary Values | Alignment with Ethical Goals | Conflict |
|---|---|---|---|
| Clinicians | Professional autonomy, accountability, patient safety | D1, D2, V1, V2 | Conflicts with Epic's proprietary opacity (D1) |
| Patients | Timely treatment, equitable care, safety | U1, U2, D1 | No direct conflict — benefit from all goals |
| Hospitals | Efficiency, liability reduction, compliance | U1, U2, D2 | Cost of explainability features conflicts with U2 |
| Epic Systems | Proprietary protection, commercial viability | None stated publicly | Directly conflicts with D1 (transparency) |
| Regulators | Safety, standardisation, accountability | D2, U1 | May conflict with speed of deployment |
| Society | Equitable access, antibiotic stewardship | U2, V1 | Alert fatigue burden conflicts with U2 |

### Values Requiring Negotiation

The most significant value conflict is between Epic's commercial interest in maintaining proprietary opacity and the deontological requirement for clinician epistemic access (D1). These cannot be simultaneously satisfied in the current deployment. Resolving this conflict requires either mandatory explainability regulation or contractual transparency obligations in hospital procurement.

A secondary conflict exists between the utilitarian justification for high sensitivity (U1) and the harm minimisation requirement (U2). Maximising sensitivity necessarily increases false positive burden. This trade-off cannot be resolved by system design alone, it requires institutional threshold governance involving clinicians, patients and ethics review.

### Prioritisation

Patient safety values take precedence, as patients are the population most directly harmed by system failures and least able to advocate within the deployment structure. Clinician professional values are second, as they are the responsible agents whose judgement the system most directly affects. Institutional and commercial values, while legitimate, must not override the first two categories.

---

## 2.5 Functional-to-Ethical Goal Balance

The primary functional purpose of the Epic Sepsis Model is early detection and improved outcomes in sepsis care. Ethical goals constrain how that purpose is achieved rather than overriding it.

For primary stakeholders, functional goals significantly outnumber ethical constraints, reflecting the system's clinical purpose while ensuring ethical safeguards remain enforceable.

**Functional Goals:** Early detection, threshold-based alerting, reduced mortality, workflow integration, antibiotic timing improvement.

**Ethical Goals:** Prevent over-reliance (V1), preserve epistemic access (D1), enforce governance accountability (D2), control false positive burden (U2), prevent clinical deskilling (V2).

Ethical goals are more difficult to implement and validate but do not overshadow the system's clinical objectives.
