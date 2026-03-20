# Chapter 6: Teammate 2 Says

## Selected Argument

This chapter argues against Claude's Non-action 2 in Argument 3, which proposed that mandatory pre-deployment fairness testing should be replaced by conditional deployment accompanied by post-deployment monitoring. This position is ethically indefensible, and the formal verification implemented in this project demonstrates why.

---

## Claude's Position and Its Central Claim

Claude argued that requiring fairness testing before deployment risks becoming a barrier that keeps demonstrably useful tools out of clinical practice. The preferred alternative was conditional deployment: release the system alongside a post-deployment surveillance protocol stratified by age, and trigger review if performance disparities exceed predefined tolerances. This was framed as a proportionate, pragmatic middle ground.

The argument rests on two claims. First, that a model with imperfect subgroup performance may still reduce net sepsis mortality compared to no decision support at all. Second, that post-deployment monitoring is a responsible mechanism for identifying and correcting fairness violations over time. Both claims are flawed.

---

## The Counterfactual Is Wrong

The comparison Claude makes is between a fairness-untested model and no clinical decision support whatsoever. This is not the real choice. Most hospital systems deploying the ESM already operate structured sepsis screening protocols, early warning scores, and nursing assessment frameworks. The counterfactual is not an empty clinical environment. It is an environment with existing, if imperfect, decision support that does not carry the same untested subgroup risk.

The utilitarian calculation Claude implies, that deploying without fairness testing is justified by net population benefit, only holds if the baseline is zero. It does not hold against an existing standard of care.

---

## Post-Deployment Monitoring Is Not a Safeguard

The more serious problem is what conditional deployment actually means in practice. A post-deployment surveillance protocol collects outcome data from patients who are already being managed under the untested system. If the model systematically underscores elderly patients with atypical sepsis presentation, those patients receive delayed or missed alerts while the institution accumulates the evidence needed to confirm the disparity. The monitoring process does not prevent that harm. It measures it retrospectively.

Claude's framing uses the language of surveillance and tolerances, which gives the impression of a rigorous governance process. What it describes is accepting foreseeable differential harm to a specific patient population as the price of early deployment, and then documenting the consequences.

---

## The Violation Is Detectable Before Deployment

The strongest objection to Claude's position is that the epistemic justification for post-deployment monitoring does not hold. Claude implies that the fairness violation cannot be known in advance and must therefore be detected through real-world observation. The Z3 verification layer in this project shows otherwise.

The fairness constraint is encoded as a logical formula and verified formally before any patient data is involved:

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

This returns UNSAT with the core:

```
[Elderly_Alert_True, Equivalent_Group_True, Fairness_Symmetry, Young_Alert_False]
```

The violation scenario, two clinically equivalent patients receiving different alert outcomes, is formally proven to be logically inconsistent with the fairness constraint before a single real patient is involved. The precondition for Claude's argument, that the violation cannot be known in advance, is false. Pre-deployment formal verification closes exactly the epistemic gap that Claude uses to justify deferring the test to the post-deployment phase.

---

## Conclusion

Conditional deployment does not balance pragmatism against principle. It defers a test that can be conducted before deployment and accepts the harm that accrues in the interim as an administrative inevitability. The justice principle requires that foreseeable disparate impacts be identified before they occur, not after. The implementation in this project demonstrates that the necessary verification is technically feasible. Claude's Non-action 2 has no remaining justification.
