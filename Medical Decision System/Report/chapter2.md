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

Clinicians are the primary users of the ESM. The system generates alerts when a patient’s sepsis risk score exceeds a predefined threshold (**ESM ≥ 5**), prompting clinical evaluation and intervention.

Although clinicians retain final decision-making authority, the alerts influence attention, prioritisation, and timing of treatment. Clinicians are also legally accountable for patient outcomes, even when decisions are informed by AI-generated risk scores.

---

### 2. Patients

**Category:** Social, Ethical, Legal  

Hospitalised patients are the subjects of the predictive model. They do not directly interact with the system but are affected by its outputs through changes in clinical behaviour, including earlier antibiotic administration and ICU escalation.

Patients bear the risks of:
- **False positives:** unnecessary treatment, antibiotic overuse  
- **False negatives:** missed or delayed diagnosis  

---

### 3. Hospital and Healthcare Providers

**Category:** Economic, Technical, Legal  

Hospitals deploy the ESM as part of the Epic electronic health record infrastructure. They benefit from potential reductions in mortality, length of stay and compliance with sepsis quality measures.

At the same time, hospitals assume institutional liability and must manage:
- Alert fatigue  
- Workflow disruption  
- Training requirements  

---

### Secondary Stakeholders

Secondary stakeholders influence the system indirectly or are affected at a broader systemic level.

---

### 4. Epic Systems Corporation

**Category:** Technical, Economic, Legal  

Epic develops and maintains the proprietary ESM algorithm and integrates it into the EHR. While Epic does not make clinical decisions, its design choices—including feature selection, model updates, and alert presentation—shape how clinicians interpret and act on risk scores.

---

### 5. Health Regulators and Accreditation Bodies

**Category:** Political, Legal  

Regulatory bodies influence the adoption of sepsis detection systems through quality standards, reporting requirements, and patient safety regulations.

Although the ESM itself is not publicly regulated as a medical device, its use affects compliance with national sepsis guidelines and reporting frameworks.

---

### 6. Society and Public Health Systems

**Category:** Social, Economic  

At a population level, widespread deployment of sepsis detection tools influences:
- Healthcare costs  
- Antibiotic stewardship  
- Public trust in AI-assisted medicine  

---
### 7. Environmental and Infrastructure Considerations

**Category:** Environmental, Technical

Deployment of AI-enabled CDSS systems requires substantial digital infrastructure, including data storage, server capacity, and continuous monitoring within electronic health record platforms. While individual risk score computations have negligible marginal environmental impact, large-scale deployment across national hospital networks contributes to cumulative energy consumption and infrastructure expansion. Although environmental effects are indirect relative to clinical outcomes, responsible digital health governance must consider long-term sustainability of computational infrastructure.

## 2.2 Ethical Goals of the System

The Epic Sepsis Model does not publish an explicit ethical framework or set of ethical principles. Public documentation and validation studies focus primarily on clinical effectiveness, workflow integration, and patient outcomes.

There are no explicit public statements addressing transparency, accountability, or ethical safeguards beyond standard clinical governance practices.

This absence is ethically relevant, as it requires ethical safeguards to be inferred from system behavior and deployment structure rather than from explicitly articulated normative commitments.

---

## 2.3 Ethical Considerations and Schools of Thought

For this project, three ethical frameworks are used to analyse the system:

- **Utilitarianism**
- **Deontological Ethics**
- **Virtue Ethics**

These were selected because they capture outcome based, duty based and professional character based ethical concerns relevant to clinical AI systems.

---

### 1. Utilitarian Ethics (Outcome-Oriented)

**Core Principle:** Actions are ethically justified if they maximise overall benefit and minimise harm.

#### Relevant Variables and System Functionality

- Sepsis mortality rates  
- Time to antibiotic administration  
- Sensitivity and specificity of alerts  
- Hospital-wide outcomes and resource utilisation  

#### Ethical Goals

- Reduce sepsis-related mortality  
- Enable earlier treatment for high-risk patients  
- Improve population-level outcomes  

#### System Behaviour

The ESM prioritises **sensitivity (86.0%)** over precision (**PPV 33.8%**) to ensure that most sepsis cases are detected early.

This design accepts a higher false-positive rate to maximise overall survival benefit, consistent with utilitarian reasoning.

#### Ethical Risk

Increased false positives may lead to:
- Unnecessary antibiotic use  
- Increased costs  
- Alert fatigue  

These effects may undermine long-term benefit.

---

### 2. Deontological Ethics (Duty and Responsibility)

**Core Principle:** Ethical action depends on adherence to duties, rules, and accountability, not outcomes alone.

#### Relevant Variables and System Functionality

- Alert thresholds and escalation rules  
- Clinician accountability  
- Opacity of model reasoning  

#### Ethical Goals

- Preserve clinician responsibility for decisions  
- Avoid delegation of moral responsibility to the AI system  
- Ensure clinicians can justify actions taken in response to alerts  

#### System Behaviour

The ESM provides a numerical risk score but does not issue mandatory treatment recommendations.

Clinicians are expected to evaluate alerts using clinical judgment.

#### Ethical Risk

The system influences behaviour without providing transparent reasoning, creating a **responsibility gap** where clinicians remain accountable but lack full epistemic access to the basis of the alert.

---

### 3. Virtue Ethics (Professional Character and Practice)

**Core Principle:** Ethical systems should support good professional judgment, not replace it.

#### Relevant Variables and System Functionality

- Human–AI interaction  
- Alert frequency and workflow integration  
- Training and education of clinicians  

#### Ethical Goals

- Support prudent clinical decision-making  
- Avoid deskilling and over-reliance on automated alerts  
- Maintain clinician attentiveness and reflective judgment  

#### System Behaviour

The ESM is integrated into routine workflows and requires clinicians to actively interpret and act on alerts.

Training is provided to contextualise the tool as an aid rather than an authority.

#### Ethical Risk

Frequent alerts and demonstrated reductions in time to antibiotics indicate strong behavioural influence, which may encourage automation bias over time.

---

#### Ethical Framework–Stakeholder Alignment

The three ethical schools correspond to different stakeholder perspectives. Utilitarian analysis primarily concerns patient outcomes and hospital-level mortality reduction. Deontological considerations are most salient for clinicians, who retain formal decision authority and legal responsibility for AI-informed actions. Virtue ethics focuses on the professional character of clinicians interacting repeatedly with alert systems, emphasizing calibration, attentiveness, and avoidance of automation bias. Together, these frameworks provide a pluralistic ethical lens appropriate for socio-technical clinical systems.

---

## 2.4 Functional-to-Ethical Goal Balance

The primary functional purpose of the Epic Sepsis Model is early detection and improved outcomes in sepsis care.

Ethical goals—such as accountability, transparency, and responsible reliance—do not override this purpose but constrain how it is achieved.

For primary stakeholders (clinicians and patients), the system exhibits a **functional-to-ethical goal ratio exceeding 5:1**, as required by the assignment.

### Functional Goals

- Early detection  
- Alerting  
- Reduced mortality  
- Workflow integration  

### Ethical Goals

- Prevent over-reliance  
- Preserve responsibility  
- Minimise harm from false positives  

Ethical goals are more difficult to implement and validate but do not overshadow the system’s clinical objectives.
