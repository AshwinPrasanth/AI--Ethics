# Chapter 6: Teammate 2 Says...

## Selected Argument

This chapter argues against Claude's Non-action 2 in Argument 3, which proposed replacing mandatory pre-deployment fairness testing with conditional deployment accompanied by post-deployment monitoring. This argument contains a false cause fallacy and it attributes the impossibility of pre-deployment fairness testing to an epistemic limitation that does not exist. Because the fallacy is the basis for the entire conditional deployment position, Action 1 mandating subgroup fairness testing as a pre-deployment requirement is the correct position.

---
## Ethical Principle

School: Deontological ethics (principle of equal treatment) with utilitarian justice considerations.

Principle:
Patients with equivalent clinical states must receive equivalent diagnostic evaluation regardless of demographic subgroup.

Operational constraint:
If two patients exhibit equivalent clinical indicators for sepsis, the system must produce equivalent alert decisions regardless of age group.

Violation condition:
If two clinically equivalent patients receive different alert outcomes solely due to subgroup membership, the fairness constraint is violated.

---

## The Fallacy: False Cause

Claude's Non-action 2 implies that the reason for deferring fairness testing to the post-deployment phase is that the violation cannot be known in advance. The argument runs: a model with imperfect subgroup performance may still reduce net sepsis mortality compared to no decision support, so conditional deployment with post-deployment surveillance is a proportionate response to an uncertainty that cannot be resolved before going live.

This is a false cause fallacy. The claimed cause of deferral epistemic impossibility is not the actual cause. Fairness violations are formally detectable before deployment. The Z3 verification layer in this project demonstrates this directly:

```python
def unsat_fairness_violation():
    s = z3.Solver()
    Equivalent_Group = z3.Bool("Equivalent_Group")
    elderly_alert = z3.Bool("elderly_alert")
    young_alert = z3.Bool("young_alert")

    s.assert_and_track(
        z3.Implies(Equivalent_Group, elderly_alert == young_alert),
        "Fairness_Symmetry"
    )
    s.assert_and_track(Equivalent_Group, "Equivalent_Group_True")
    s.assert_and_track(elderly_alert, "Elderly_Alert_True")
    s.assert_and_track(z3.Not(young_alert), "Young_Alert_False")

    result = s.check()
    if result == z3.unsat:
        print("Unsat Core:", s.unsat_core())
```

This returns UNSAT with core `[Elderly_Alert_True, Equivalent_Group_True, Fairness_Symmetry, Young_Alert_False]`. The violation scenario is formally proven to be logically inconsistent with the fairness constraint before any patient is involved. Xu et al. [2] further identify the absence of formal verification as a specific research gap in AI-based CDSS ethics, noting that ethical compliance is seldom enforced through logic-based constraints which is precisely what this implementation provides. The epistemic precondition for Claude's conditional deployment argument is false.

---

## The Wrong Counterfactual

Claude's argument also rests on a second error. The claim that a model with imperfect subgroup performance may still reduce net sepsis mortality compared to no decision support at all uses the wrong comparison class. The alternative to a fairness-tested model is not an empty clinical environment. Most hospital systems deploying the ESM already operate structured sepsis screening protocols, early warning scores, and nursing assessment frameworks [3]. Vasey et al. [4] (DECIDE-AI) explicitly caution that high retrospective accuracy does not guarantee clinical benefit or safety in real-world deployment, and that ethical evaluation must account for the existing standard of care rather than a zero baseline. The net benefit calculation Claude implies only holds if the counterfactual is nothing, which it is not.

---

## Post-Deployment Monitoring Is Not a Safeguard

Having removed the epistemic justification for deferral and corrected the counterfactual, what remains of Non-action 2 is a governance process that collects evidence of harm from patients who are already being managed under the untested system. Čartolovni et al. [5] identify this accountability gap directly: responsibility for harm in AI-based decision support is often unclear across clinicians, developers, and institutions, and frameworks that defer fairness assessment to post-deployment monitoring effectively make that ambiguity permanent during the observation period. The patients harmed during monitoring are not data points in a quality improvement exercise. They are people who did not receive a timely alert because the institution chose not to test for the disparity before deployment.

The justice principle identified under Goal D1 in Chapter 2 requires that foreseeable disparate impacts be identified before they occur, not after. Elderly patients present particular physiological challenges like blunted fever responses, atypical inflammatory markers, baseline comorbidities that may systematically suppress ESM scores [1]. This is not an unpredictable edge case. It is a foreseeable risk that the pre-deployment formal verification layer in this project is specifically designed to detect.

---

## Conclusion

Claude's Non-action 2 rests on a false cause fallacy: the claim that fairness violations cannot be known before deployment. The Z3 verification layer in this project formally refutes that claim. With the fallacy removed, the conditional deployment position has no epistemic justification, uses the wrong counterfactual, and treats foreseeable harm to elderly patients as an administrative cost. Action 1 is correct — subgroup fairness testing must be a pre-deployment requirement, not a post-deployment observation.
