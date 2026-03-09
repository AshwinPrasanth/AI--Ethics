# Chapter 5: Teammate 1 Says...

## Selected Argument

This chapter argues against Claude's Position 1 in Argument 2, which defended the opacity of the Epic Sepsis Model by claiming that clinicians interpreting an AI risk score are in a structurally similar position to clinicians interpreting a laboratory result. This analogy is false, and accepting it conceals a specific accountability failure that affects every alert the system generates.

---

## The Analogy Does Not Hold

Claude's argument rests on the claim that a clinician does not need to understand the internal mechanics of a diagnostic tool to act appropriately on its output. The troponin example is used to support this: a clinician acts on an elevated troponin without understanding the chemistry of the assay, and that is considered acceptable practice.

The distinction that matters is not whether the clinician understands the mechanics. It is whether the source of error is traceable when the tool is wrong. A troponin result is a direct measurement of a biological quantity with documented, investigable failure modes: reagent degradation, sample haemolysis, assay interference from skeletal muscle troponin. When a troponin is anomalous or inconsistent with presentation, the clinician and the laboratory can reason about why.

The ESM score is a learned inference from a proprietary model trained on approximately 500,000 historical encounters, combining roughly 80 variables through undisclosed statistical relationships. Those relationships may encode documentation biases, historical care inequities, or population specific confounders from the original training environment. When the ESM is systematically wrong for a particular patient group, that error is invisible at the point of care. There is no equivalent of checking the reagent batch or the sample timing. The clinician receives a number with no accessible basis for disagreement.

Claude's analogy equates these two situations. They are not equivalent.

---

## What the Analogy Conceals

The practical consequence of accepting Claude's position is that clinicians are left accountable for decisions they cannot fully reason about. This is not an abstract concern. Consider the scenario the ESM is most likely to produce it: a clinician receives an alert for an elderly patient with atypical presentation, assesses the patient independently, and decides the score does not reflect the clinical picture. They document their reasoning and do not escalate. The patient later deteriorates.

In that situation, the clinician's defence depends on articulating not only what they observed but why they disagreed with the score. Under an opaque system, the second part of that defence has no grounding. The clinician cannot say what the model weighted, what features drove the score, or whether the model had ever been validated on patients with this presentation. They acted on clinical judgement alone, in response to a signal whose basis they were never given access to.

This is the condition Claude's position treats as acceptable. It is not the same as acting on a troponin without knowing the biochemistry. It is acting on an inference without knowing what was inferred or why.

---

## The Structural Nature of the Gap

The responsibility gap is not a scenario that occasionally arises. It is the default operating state of the system. The E4 constraint in the ethical validation layer captures this directly:

```python
def responsibility_gap(alert, explanation_available):
    if alert and not explanation_available:
        return True
    return False
```

In the real ESM deployment, `explanation_available` is False for every alert the system fires. The model does not expose feature level reasoning to clinicians. The function therefore returns True, meaning a responsibility gap exists, on every single alert. This is not an edge case that careful clinical practice can avoid. It is a structural property of how the system is designed and deployed.

Claude argues that population level metrics such as 86% sensitivity and 33.8% PPV provide sufficient calibration for clinicians to act responsibly under these conditions. Population level statistics describe how the model performs across a patient population. They say nothing about the basis for any individual alert. A clinician told the model has 86% sensitivity knows that roughly one in seven sepsis cases will be missed overall. They do not know whether this patient is in that one in seven, or why. That gap is not closed by statistical disclosure.

---

## An Internal Contradiction

Position 1 also contradicts what Claude acknowledged in Argument 4. The defence of opacity depends on clinicians consciously using population level metrics, 86% sensitivity, 33.8% PPV, to calibrate their response to each alert. But in Argument 4, Claude accepted that clinicians under time pressure and fatigue default to following alerts without independent assessment. These two pictures of clinical behaviour cannot both be true. Position 1 assumes a reflective, statistically informed clinician weighing probabilities at the bedside. Argument 4 describes the actual clinician: cognitively loaded and prone to following the alert. Claude cannot use the first picture to justify opacity while accepting the second as the operational reality.

---

## Conclusion

The lab test analogy fails because it treats traceability of error as irrelevant to accountability. It is not. Clinicians can act responsibly under uncertainty when the nature of that uncertainty is accessible to them. What the ESM creates is uncertainty whose source is proprietary, undisclosed, and structurally inaccessible. Accepting Claude's position means accepting that as a sufficient basis for full clinical accountability. It is not.
