# Weekly Report — Week 3
**Student:** Arjun Patel
**Role:** PPO Fine-tuning
**Date:** 2025-01-20 to 2025-01-24

---

## Summary

Systematically swept 12 different β values (KL penalty coefficient) from 0.05 to 5.0. KL divergence is still escalating above 10 in every run. Tried reducing learning rate. Considering whether there is a deeper upstream issue with the reward signal.

## β Sweep Results

| Run | β | Max KL (Ep 1) | Max KL (Ep 2) | Final Reward |
|-----|---|--------------|--------------|-------------|
| R01 | 0.05 | 22.4 | — | 0.31 |
| R02 | 0.10 | 18.3 | — | 0.26 |
| R03 | 0.20 | 15.7 | — | 0.22 |
| R04 | 0.30 | 13.4 | — | 0.19 |
| R05 | 0.50 | 11.2 | — | 0.17 |
| R06 | 0.75 | 10.8 | — | 0.15 |
| R07 | 1.00 | 10.3 | — | 0.14 |
| R08 | 1.50 | 10.1 | — | 0.12 |
| R09 | 2.00 | 10.0 | — | 0.11 |
| R10 | 2.50 | 9.8 | — | 0.10 |
| R11 | 3.00 | 9.7 | — | 0.09 |
| R12 | 5.00 | 9.5 | — | 0.07 |

All runs stopped at Epoch 1 due to KL exceeding my safety threshold of 15 (or approaching it). Even at β=5.0, KL reaches 9.5 — still above the 5–6 range I'd expect for healthy PPO training.

The pattern is strange: increasing β reduces KL but doesn't stop the escalation. In normal PPO-RLHF, once β is large enough, the KL stays bounded. Here, there seems to be a constant upward pressure on KL that no β value can fully compensate for.

## Reward Signal Analysis

I added reward logging and observed that the standard deviation of rewards within a batch is **σ ≈ 2.1**, which is very high. A well-calibrated reward model should produce rewards with σ in the range 0.5–1.0 for batches of diverse responses. The high variance suggests the RM is assigning very different rewards to similar responses — exactly what you'd expect from a poorly calibrated RM.

This high-variance reward signal is what's driving the KL escalation: the policy sees wildly inconsistent reward gradients and can't find a stable learning direction.

## Learning Rate Adjustment

Tried reducing learning rate from 1e-6 to 1e-7 — marginal improvement but KL still escalates. The problem is the reward signal, not the optimization dynamics.

## Theory

My current understanding: Sofia's RM has val_acc=0.61, meaning it's wrong 39% of the time on preference pairs. When the RM is wrong, it rewards worse responses and penalizes better ones. The policy then learns to produce responses that the RM incorrectly rates highly, which are different from the responses the reference policy would produce — causing KL to increase. With 39% error rate in the RM, no β value can fully compensate.

## Next Steps

- Get the RM v4 checkpoint from Sofia (trained on Batch 1+2)
- If RM v4 doesn't improve significantly, need to escalate this issue
- Consider whether the data quality feeding into the RM is the root cause
