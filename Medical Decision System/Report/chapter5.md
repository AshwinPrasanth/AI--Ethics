# Chapter 5: Teammate 1 Says

## Selected Argument

This chapter argues against Claude's Position 1 in Argument 2, which claimed that opacity in the Epic Sepsis Model is ethically defensible because clinicians interpreting an AI risk score are in the same position as clinicians interpreting a laboratory result.

---

## Why the Analogy Fails

A troponin assay measures a single, directly observable biological quantity through a validated biochemical process with well documented error sources. When a troponin result is inconsistent with clinical presentation, the clinician can reason about why: reagent degradation, sample timing, haemolysis. The source of error is traceable.

The ESM score is a different kind of object entirely. It is a learned inference from a proprietary model combining roughly 80 variables through statistical relationships that are not disclosed. Those relationships reflect patterns in historical training data that may encode past care inequities, documentation biases, or population specific confounders. When the ESM is systematically wrong for a particular patient group, that error is invisible at the point of care. A clinician cannot interrogate a bias they cannot observe, and population level metrics like 86% sensitivity tell them nothing about whether this alert, for this patient, is reliable.

The two situations are not structurally similar. One error is traceable. The other is not.

---

## The Accountability Consequence

Under the current ESM design, clinicians bear full legal and moral responsibility for outcomes while being denied access to the reasoning behind the alerts they act on. This is the responsibility gap formalised in the implementation as E4:

```python
def responsibility_gap(alert, explanation_available):
    if alert and not explanation_available:
        return True
    return False
```

In the real ESM deployment, `explanation_available` would be False for every alert the system generates. The gap is not an edge case, it is the standard operating condition. Claude's position argues this is acceptable because aggregate performance statistics provide sufficient calibration. They do not. If a clinician dismisses an alert and the patient deteriorates, their clinical defence requires articulating what they assessed and why they disagreed with the score. An opaque system provides no basis for the second part of that defence. The clinician is accountable for a decision they cannot fully reason about, in response to an alert whose basis they cannot access.

---

## Conclusion

Accepting Claude's position would provide ethical cover for a system that asks clinicians to bear full accountability while denying them the information that accountability requires. That asymmetry is not a minor design limitation. In a safety critical clinical setting, it is a structural failure.
