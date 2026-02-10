# Chapter 1: Introduction

Sepsis is a life-threatening condition caused by a dysregulated host response to infection and is associated with high mortality and substantial healthcare costs. In hospitalized patients, sepsis occurs in approximately 2–6% of admissions, with reported mortality rates ranging from 15% to 40% depending on severity and timeliness of intervention.

Clinical evidence consistently shows that earlier identification and treatment, particularly timely administration of antibiotics significantly reduce mortality. As a result, healthcare systems have increasingly adopted AI-enabled Clinical Decision Support Systems (CDSS) to assist clinicians in early detection and risk stratification of sepsis.

This project focuses on a real-world, deployed AI-enabled CDSS, ie. the Epic Sepsis Model (ESM) Inpatient Predictive Analytic Tool, which is integrated into the Epic electronic health record (EHR) system. Epic Systems is the largest EHR provider in the United States, with systems serving approximately 54% of patients nationwide, making ESM one of the most widely deployed AI-based decision support tools in clinical practice.

The ESM is designed to continuously monitor hospitalized patients and generate a numerical risk score indicating the likelihood of sepsis, enabling earlier clinical intervention.

Unlike experimental or research-only models, the ESM operates in live hospital environments and directly influences clinical workflows. Its outputs are used to trigger alerts to nurses and physicians when a predefined risk threshold is exceeded, thereby shaping diagnostic attention, treatment prioritization, and escalation decisions. As such, the ESM represents a safety-critical AI system whose ethical implications extend beyond model accuracy to issues of trust, accountability, over-reliance and human–AI collaboration.

---

## Key Features of the System

The Epic Sepsis Model is a data-driven, sub-symbolic AI system implemented within a commercial electronic health record platform. It is proprietary; however, published validation studies provide sufficient evidence to characterize its technical structure and behavior.

### AI Technology and Model Characteristics

- **Model type:** Data-driven predictive model (sub-symbolic)  
- **Input features:** Approximately 80 clinical and demographic variables, including vital signs, laboratory results, comorbidities, and patient demographics  
- **Training data:** Developed using approximately 500,000 patient encounters  
- **Output:** A continuously updated numerical sepsis risk score  
- **Deployment:** Fully integrated into the Epic EHR, operating in real time on hospitalized patients  

The ESM does not rely on explicit clinical rules, symbolic reasoning, or hand-crafted knowledge representations. Instead, patient data are combined and weighted according to learned statistical relationships to produce a risk score. While the system can surface which variables contributed most to an elevated score, its internal decision logic is not fully transparent to end users, placing it firmly in the category of sub-symbolic, black-box clinical decision support.

---

## Operational Threshold and Performance

In the validation study conducted at a 746-bed academic medical center, an alert threshold of **ESM ≥ 5** was selected using receiver operating characteristic (ROC) curve analysis. At this threshold, the model demonstrated:

- **Area Under ROC Curve (AUC):** 0.834  
- **Sensitivity:** 86.0%  
- **Specificity:** 80.8%  
- **Positive Predictive Value (PPV):** 33.8%  
- **Negative Predictive Value (NPV):** 98.1%  

These results indicate that the ESM is optimized as a screening tool, prioritizing sensitivity and early detection rather than definitive diagnosis [epic_sepsis_base].

---

# 1.1 Functional Goals of the System

The primary functional goal of the Epic Sepsis Model is early identification of hospitalized patients at risk of developing sepsis, enabling clinicians to initiate timely evaluation and treatment. This goal is operationalized through continuous risk scoring and automated alerting within the EHR.

More specifically, the system is designed to:

### 1. Detect elevated sepsis risk earlier than routine clinical recognition

By continuously analyzing patient data, the ESM aims to identify deterioration before overt clinical signs prompt clinician action.

### 2. Prompt timely clinical intervention

When the ESM score exceeds the alert threshold, clinicians are notified and expected to assess the patient, consider sepsis protocols, and initiate appropriate management.

### 3. Reduce time to antibiotic administration

In the post-implementation phase of the validation study, the median time from alert to antibiotic administration decreased from 150 minutes to 90 minutes, and the proportion of patients receiving antibiotics within three hours increased from 55.6% to 69.8%.

### 4. Improve patient outcomes, particularly mortality

Among patients with ESM scores ≥ 5 who had not already received antibiotics, implementation of the alert system was associated with a 44% reduction in the odds of in-hospital sepsis-related mortality (odds ratio 0.56; 95% CI 0.39–0.80).

### 5. Integrate seamlessly into existing clinical workflows

The system is embedded within the Epic EHR and requires no separate interface, enabling widespread deployment with minimal disruption.

---

## Ethical Relevance of the Functional Design

Although the ESM demonstrably improves early intervention and is associated with reduced mortality, its design raises ethical challenges that extend beyond functional performance.

The system produces risk scores that significantly influence clinician behavior, yet its internal reasoning is largely opaque. Clinicians remain legally and morally responsible for decisions, while the AI system shapes attention, urgency, and treatment timing. This creates potential risks of automation bias, over-reliance, and accountability gaps—particularly in high-stakes clinical contexts.

These ethical considerations motivate the focus of this project: not on building a new predictive model, but on explicitly identifying ethical goals, formalizing them as constraints or checks, and demonstrating—through targeted scripts and validation cases—when such goals may or may not be satisfied.
