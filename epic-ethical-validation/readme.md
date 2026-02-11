# Ethical Validation of an AI-Based Clinical Decision Support System

This repository contains a simplified simulation of a real-world AI-based Clinical Decision Support System (CDSS), modeled after the Epic Sepsis Model (ESM).

The objective is **not** to reproduce the proprietary model, but to:

- Simulate risk scoring and alert generation  
- Explicitly encode ethical goals  
- Detect and log ethical failure scenarios  
- Validate both functional and ethical goals through executable scripts  

---

# 📁 Directory Structure

    epic-ethical-validation/
    │
    ├── functional_validation.py
    ├── ethical_validation.py
    ├── risk_model.py
    ├── scenarios.py
    ├── audit.log
    └── README.md

---

# 📂 File Descriptions

## 1️⃣ `risk_model.py`

Core risk scoring logic.

- Implements a simplified weighted scoring function  
- Mimics sub-symbolic predictive behavior  
- Computes a numerical sepsis risk score  
- Triggers alert if score ≥ predefined threshold  

**Key functions:**

- `compute_risk_score(patient_data)`  
- `trigger_alert(score, threshold)`  

This file represents the AI model abstraction.

---

## 2️⃣ `scenarios.py`

Defines structured test cases used for validation.

Includes:

- `high_risk_patient()` → true positive case  
- `moderate_risk_patient()` → true negative case  
- `aggressive_false_positive()` → high vitals but not septic  
- `over_reliance_case()` → clinician blindly accepts alert  
- `under_reliance_case()` → clinician ignores alert  

This file encodes domain situations to test both functional and ethical goals.

---

## 3️⃣ `functional_validation.py`

Validates **functional goals** of the system.

Checks:

- Risk score computation  
- Alert triggering  
- Threshold behavior  

**Example output:**

    High Risk Score: 5.75
    Alert Triggered: True

    Moderate Risk Score: 2.98
    Alert Triggered: False

Confirms that:

- High-risk patients generate alerts  
- Low-risk patients do not  
- Threshold logic behaves as intended  

---

## 4️⃣ `ethical_validation.py`

Validates **ethical goals** through controlled failure scenarios.

Implements detection for:

### ✅ False Positive Detection

Simulates alert triggered in a non-septic case.

Example:

    False Positive Test - Score: 5.402
    Alert: True
    FPR: 1.0

Represents:

- Alert fatigue risk  
- Sensitivity vs specificity trade-off  

---

### ⚠ Over-Reliance Detection

Simulates blind clinician acceptance.

Example:

    Over-reliance detected: True

Represents:

- Automation bias  
- Delegated responsibility risk  

---

### ⚠ Under-Reliance Detection

Simulates clinician ignoring valid alert.

Example:

    Under-reliance detected - Alert: True, Clinician responded: False

Represents:

- Automation neglect  
- Missed intervention risk  

---

## 5️⃣ `audit.log`

Automatic logging file.

Records:

- Alert events  
- Ethical violations  
- Over-reliance and under-reliance warnings  
- False positive occurrences  

Example log entry:

    WARNING - False positive detected - Potential alert fatigue risk.
    WARNING - Under-reliance detected - Alert: True, Clinician responded: False

Provides traceability and accountability simulation.

---

# ⚙ How to Run

### Functional validation

    python functional_validation.py

### Ethical validation

    python ethical_validation.py

---

# What This Implementation Demonstrates

This simulation shows:

- How alert-based AI systems operate in practice  
- How ethical goals can be formalized into testable conditions  
- How failures (false positives, automation bias, neglect) can be detected programmatically  
- How audit logging improves transparency  

The implementation transforms abstract ethical principles into executable validation checks.

---

# Scope

This is a simplified, pedagogical simulation inspired by real-world CDSS systems.  
It does not use real patient data and does not replicate proprietary algorithms.

Its purpose is to demonstrate:

- Ethical-by-design validation  
- Human–AI interaction risks  
- Constraint-based ethical checking in safety-critical systems  
