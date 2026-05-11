# Lab Meeting Notes — Week 3

**Date:** January 6–7, 2025
**Attendees:** (see individual sessions below)
**Notetaker:** Advisor

---

## Group Meeting — Monday, January 6, 10:00–11:00 AM

**Present:** All lab members (Yuhang, Elena, Marcus, Priya, Selin)

### Standing agenda

- Lab housekeeping: reminder to push experiment configs to shared repo
- Grant reporting deadline: February 15 — preliminary results needed by Feb 1
- Reading group: next week covering Snell et al. (2024) test-time scaling survey

### Brief updates (round table, 2 min each)

- **Yuhang:** Running ablations on fixed-budget inference baselines. Seeing some interesting variance patterns across problem difficulty levels.
- **Elena:** Starting fresh direction after the previous contrastive learning project wrapped. Doing literature review on test-time compute.
- **Marcus:** Dataset curation, ETA 2 weeks.
- **Priya:** First model checkpoint done, evaluating on ARC.
- **Selin:** Paper revision in progress.

---

## Individual Meeting — Yuhang Zhao (Monday, January 6, 2:00–3:00 PM)

**Present:** Advisor, Yuhang

### Summary

Yuhang walked through his current results on fixed-budget inference. We discussed the observation that accuracy variance is much higher on hard problems (AMC/AIME level) than easy problems. I noted that this is consistent with compute being the binding constraint on hard problems while easy problems may actually suffer from over-generation (overthinking, model second-guessing correct answers).

**Suggested direction:** I proposed that Yuhang explore whether *difficulty-adaptive compute allocation* could address this asymmetry. The hypothesis is that a difficulty classifier at inference time could route easy problems to a small budget and hard problems to a large budget, potentially improving average accuracy while reducing total FLOPs. Yuhang seemed excited about this and said he had enough baseline results to test it quickly.

**Action items:**
- Yuhang: Implement difficulty classifier + adaptive budget routing. Target: run pilot experiment by Jan 10.
- Advisor: Send Yuhang the Snell et al. paper and relevant citations on compute-optimal inference.

---

## Individual Meeting — Elena Rodriguez (Tuesday, January 7, 10:30–11:30 AM)

**Present:** Advisor, Elena

### Summary

Elena is at the start of a new research direction after wrapping up her previous project. She described her interest in the test-time compute scaling literature and asked for direction on where there are open problems.

We discussed several options:
1. Scaling laws for reasoning — too crowded right now
2. Process reward models — already well-covered by existing work
3. **Difficulty-adaptive token budget allocation** — I suggested this as a potentially tractable and underexplored direction. The key open question is whether a lightweight difficulty estimator can be trained to make allocation decisions that improve aggregate accuracy. Elena was enthusiastic.

I framed it as: "Easy problems may not need more tokens — in fact they might be hurt by over-generation. Hard problems are likely token-starved at typical budgets. If you can route compute adaptively, you might get the best of both worlds."

**Action items:**
- Elena: Background reading on test-time compute scaling. Formalize the hypothesis. Set up a pilot experiment framework by end of week.
- Advisor: Point Elena to relevant papers (sent follow-up email with 4 citations).

---

## Notes

Both Yuhang and Elena are working in adjacent areas. I should monitor for overlap in the coming weeks and facilitate communication if their results converge on the same finding. For now they are at different stages and using different implementation approaches.

---

*Next lab meeting: Monday, January 13, 10:00 AM*
