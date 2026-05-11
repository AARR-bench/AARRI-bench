# Weekly Report — Week 2
**Student:** Arjun Patel
**Role:** PPO Fine-tuning
**Date:** 2025-01-13 to 2025-01-17

---

## Summary

Started PPO fine-tuning with Sofia's RM v3 checkpoint. Immediately seeing very high KL divergence — reaching 15–20 after just 2 epochs. Tried adjusting the KL penalty coefficient β from 0.1 to 0.5 to 1.0, but KL remains uncontrolled. My current hypothesis is that the reward model is not converged enough.

## PPO Training Results

Using RM v3 checkpoint (val_acc=0.612, val_loss=0.88).

**Run 1 (β=0.1):**
- Epoch 1: avg reward=0.23, KL=4.2 → 8.7 (escalating)
- Epoch 2: avg reward=0.18, KL=12.4 → 18.3
- Stopped: policy clearly diverging

**Run 2 (β=0.5):**
- Epoch 1: avg reward=0.21, KL=3.8 → 9.1
- Epoch 2: avg reward=0.16, KL=13.2 → 19.4
- Stopped: same issue

**Run 3 (β=1.0):**
- Epoch 1: avg reward=0.19, KL=3.5 → 7.2
- Epoch 2: avg reward=0.14, KL=10.8 → 16.7
- Stopped: still diverging, just slightly slower

## KL Divergence Analysis

KL divergence escalating monotonically is a bad sign. In standard PPO-RLHF, KL should stay bounded — it's penalized by the β coefficient. If it keeps climbing, either:
1. The β is too low (I'm penalizing too weakly)
2. The reward model is providing inconsistent gradients, confusing the policy
3. There's a bug in my KL computation

I've verified my KL computation against the TRL reference implementation and it matches. I've also confirmed the β penalty is being correctly subtracted from the reward. So I suspect hypothesis 2: the RM is noisy.

Spoke with Sofia — she acknowledged her RM is plateau-ing at val_loss=0.89 and accuracy=0.61, which is not ideal. I'm going to try a higher β next week and see if that helps.

## Why I'm Using Running Stats Normalization

My reward normalization uses a running exponential moving average (momentum=0.99) rather than per-batch normalization. I want to document this choice since it differs from some implementations: per-batch normalization (dividing each batch's rewards by its own standard deviation) causes instability in KL-penalized PPO because the normalization scale changes every batch, making the effective β inconsistent. Running stats gives a stable normalization baseline. This choice is based on Ziegler et al. 2019, Appendix C.

## Next Steps

- Try β values in range 0.5–5.0 (systematic sweep)
- Ask Sofia to share the RM v4 checkpoint once available
- Investigate whether longer warmup helps
