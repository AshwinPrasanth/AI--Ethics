# Chapter 5: Teammate 1 Says...

## Selected Argument

This chapter argues against Claude's Position 1 in Argument 2, which claimed that opacity in the Epic Sepsis Model is ethically defensible because clinicians interpreting an AI risk score are in the same position as clinicians interpreting a laboratory result. This argument rests on a false analogy fallacy. Because the fallacy undermines the entire defence of opacity, Position 2 that opacity is ethically unacceptable when accountability remains with the clinician is the correct position.

---

## Ethical Principle

**School:** Deontological ethics (accountability and responsibility)

**Principle:**
A clinician who is held legally and morally responsible for a clinical decision must have meaningful epistemic access to the basis of the information that informed that decision.

**Operational constraint:**
If an AI system generates a clinical alert, the clinician must be able to access the reasoning or contributing factors that produced the alert.

**Violation condition:**
If the system produces alerts without any explanation or accessible reasoning, the clinician’s responsibility cannot be justified. Under these conditions the system creates a responsibility gap between formal authority and practical epistemic control.

---

## The Fallacy: False Analogy

Claude's Position 1 draws a structural equivalence between interpreting an ESM alert and interpreting a troponin result. The argument is that in both cases the clinician acts on a tool output without understanding its internal mechanics, and that this is considered acceptable practice. The analogy fails because the two situations have categorically different error structures.

A troponin result is a direct measurement of a biological quantity with documented, investigable failure modes: reagent degradation, sample haemolysis, assay interference from skeletal muscle troponin. When a troponin is anomalous or inconsistent with clinical presentation, the clinician and the laboratory can reason about why. The source of error is traceable and, in principle, correctable.

The ESM score is a learned inference from a proprietary model trained on approximately 500,000 historical encounters, combining roughly 80 variables through undisclosed statistical relationships [1]. Those relationships may encode documentation biases, historical care inequities, or population-specific confounders. When the ESM is systematically wrong for a particular patient group, that error is invisible at the point of care. Xu et al. [2] establish that this opacity is not a minor limitation but a fundamental ethical problem: post-hoc explanations and population-level metrics are insufficient to guarantee accountability in sub-symbolic CDSS. There is no equivalent of checking the reagent batch. The clinician receives a number with no accessible basis for disagreement.

Equating these two situations is a false analogy. One error is traceable. The other is structurally inaccessible.

---

## What the Fallacy Conceals

The practical consequence of accepting Claude's false analogy is that the responsibility gap is rendered invisible. Amann et al. [6] demonstrate that lack of explainability causes systems nominally classified as decision support to drift toward decision determining — the clinician retains formal authority while practical epistemic control has shifted to the model. Claude's analogy imports the legitimacy of an established diagnostic measurement onto a system with fundamentally different accountability implications, concealing this drift.

Consider the scenario the ESM is most likely to produce: a clinician receives an alert for an elderly patient with atypical presentation, assesses the patient independently, and decides the score does not reflect the clinical picture. They document their reasoning and do not escalate. The patient later deteriorates. The clinician's defence requires articulating not only what they observed but why they disagreed with the score. Under an opaque system, the second part of that defence has no grounding. This is not analogous to acting on a troponin without knowing the biochemistry. It is acting on an inference without knowing what was inferred or why — precisely the condition Čartolovni et al. [5] identify as the dominant accountability gap in AI-based medical decision support.

---

## The Structural Nature of the Gap

The responsibility gap is therefore not an exceptional scenario but a structural feature of the deployment architecture, not an edge case. The E4 constraint formalises this directly:

```python
def responsibility_gap(alert, explanation_available):
    if alert and not explanation_available:
        return True
    return False
```

In current published descriptions of the ESM deployment, clinicians are not provided with feature-level explanations for alerts, meaning `explanation_available` is effectively False in practice. The function therefore returns True whenever an alert is triggered. Claude argues that population-level metrics such as 86% sensitivity and 33.8% PPV provide sufficient calibration. They do not. Population statistics describe aggregate model behaviour, they say nothing about the basis for any individual alert, which is what a clinician needs to exercise the independent judgement that accountability requires.

---

## An Internal Contradiction

Claude's Position 1 also contradicts what Claude acknowledged in Argument 4. The defence of opacity depends on clinicians consciously using population-level metrics to calibrate their response to each alert. But in Argument 4, Claude accepted that clinicians under time pressure and fatigue default to following alerts without independent assessment. Panigutti et al. [7] provide empirical confirmation: explanations systematically increase human reliance on AI advice regardless of whether reliance improves accuracy, meaning the calibrated reflective clinician that Position 1 assumes is not the clinician that real deployment produces. These two pictures of clinical behaviour are incompatible. Claude cannot use the first to justify opacity while accepting the second as the operational reality.

---

## Conclusion

The lab test analogy is a false analogy fallacy. It treats traceability of error as irrelevant to accountability when it is central to it. Because the fallacy is the load-bearing element of Position 1, the entire defence of opacity collapses with it. Position 2 is correct: opacity is ethically unacceptable when clinicians bear full accountability for decisions whose basis they cannot access. The responsibility gap is not a theoretical concern — it is a structural feature of every alert the system fires.

