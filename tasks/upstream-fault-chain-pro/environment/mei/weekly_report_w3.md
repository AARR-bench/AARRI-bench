# Weekly Report — Week 3
**Student:** Mei Lin
**Role:** Model Evaluation & Analysis
**Date:** 2025-01-20 to 2025-01-24

---

## Summary

Set up evaluation infrastructure and ran initial evaluation of the fine-tuned model (PPO checkpoint from Arjun) on the held-out medical dialogue test set. Overall accuracy: 71.2%. Below our target of 80% but not catastrophically bad for a first pass.

## Background

I joined the project this week as the evaluation specialist. My role is to assess the quality of the RLHF-fine-tuned model on the held-out test set and analyze failure modes.

I received:
- The fine-tuned model checkpoint from Arjun (a PPO checkpoint from an early run before KL escalation)
- The held-out test set: 500 medical dialogue examples (withheld from all training data)
- Evaluation metrics specification from the supervisor

## Evaluation Infrastructure

Set up evaluation pipeline:
1. Load fine-tuned model (and SFT baseline for comparison)
2. For each test example, generate a response
3. Score response quality along three dimensions:
   - **Clinical correctness**: verified by a medical expert scoring rubric
   - **Patient-friendliness**: readability score + terminology simplicity
   - **Appropriateness**: does the response give appropriate next steps?
4. Combine into a single accuracy score (binary: acceptable vs. not acceptable, where acceptable = clinically correct AND appropriate)

## Initial Results

Overall accuracy: **71.2%** (356/500 examples rated acceptable)

Breakdown by query type:
| Query Category | N | Accuracy |
|---------------|---|---------|
| Symptom description | 187 | 73.8% |
| Medication questions | 124 | 68.5% |
| Follow-up queries | 89 | 74.2% |
| Emergency triage | 48 | 60.4% |
| General health info | 52 | 75.0% |

The emergency triage category is concerning (60.4%) — these are high-stakes queries where incorrect guidance could be harmful.

## Comparison with SFT Baseline

SFT baseline (pre-RLHF): 68.4% overall accuracy.
Fine-tuned model: 71.2% overall accuracy.
Improvement: +2.8 percentage points.

This is modest. Given that PPO training had KL divergence issues (according to Arjun), I'm not surprised the improvement is small.

## Next Steps

- Analyze performance stratification by query characteristics
- Look at time-of-day and other metadata-based breakdowns
- Identify specific failure modes to provide actionable feedback
- Compare response quality qualitatively on selected examples
