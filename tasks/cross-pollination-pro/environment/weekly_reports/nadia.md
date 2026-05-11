**Weekly Report — Nadia Petrov**
**Week 8 | LLM Weight Quantization for Inference**

---

**Summary of Progress**

This week I completed a systematic characterization of numerical instability in INT4 and INT8 weight quantization for transformer inference. The key finding is a gradient variance threshold above which quantized models become numerically unstable during fine-tuning.

**Background**

My project is deploying quantized LLMs for inference on edge hardware with limited memory. INT8 weight quantization reduces model size by 2x vs FP32; INT4 reduces by 4x. Both are widely used, but I was seeing mysterious NaN losses during fine-tuning that didn't occur with FP16 weights.

**Root Cause: Gradient Variance Threshold**

After extensive debugging, I identified that the NaN losses occur when the variance of input gradients to a quantized layer exceeds a threshold. When gradients are large and variable, the quantization error (rounding to the nearest representable INT value) interacts badly with the gradient update, sometimes producing values outside the representable range.

I ran a systematic sweep varying the gradient variance σ² artificially (by adding controlled noise to gradients in a test setup) and measuring stability:

| Per-Layer Input Gradient Variance (σ²) | INT8 Stability | INT4 Stability |
|---------------------------------------|----------------|----------------|
| σ² ≤ 0.05 | Stable (0/20 NaN) | Stable (0/20 NaN) |
| 0.05 < σ² ≤ 0.10 | Stable (0/20 NaN) | Marginal (3/20 NaN) |
| 0.10 < σ² ≤ 0.15 | Stable (0/20 NaN) | Unstable (14/20 NaN) |
| σ² > 0.15 | Unstable (8/20 NaN) | Unstable (20/20 NaN) |

*Footnote: All experiments at batch size 32, learning rate 1e-4, AdamW. σ² measured as mean L2 variance across layer inputs over 10 steps. "NaN" means training collapsed within 200 steps. The threshold σ²>0.15 is where INT8 reliability drops below 60% — below this threshold INT8 is reliable for practical use.*

The critical threshold for INT8 is σ² > 0.15 per layer. Below this threshold, INT8 quantization is reliable. Above it, training is likely to collapse.

**Fix: Per-Layer Gradient Clipping**

I implemented per-layer gradient clipping that adaptively clips gradient variance to stay below σ² = 0.12 (a 20% safety margin below the threshold). This is different from standard gradient norm clipping (which clips the global L2 norm): I clip per-layer, after the fact, by scaling down layers whose gradient variance exceeds the threshold.

With per-layer clipping, NaN losses were eliminated entirely across all my test cases. Learning rate warmup also helps independently.

**INT4 vs INT8 Comparison**

My recommendation:
- INT8: Use with confidence if gradient variance is controlled (σ² < 0.15). Very good accuracy-compression tradeoff.
- INT4: Only use if gradient variance is very low (σ² < 0.05) or if you don't need fine-tuning (inference-only deployments). Too risky for fine-tuning at higher gradient variances.

**Practical Implication**

The gradient variance threshold generalizes across model families (I tested LLaMA-7B, Mistral-7B, and a ViT-L). It appears to be a general property of low-bit quantization under high-gradient-variance conditions, not specific to any architecture.

For models being fine-tuned in settings where gradient variance is naturally low (large batches, late training stages), INT8 is safe. For models with high gradient variance (small batches, early training, tasks with highly variable output distributions), extra caution is needed.

**Next Steps**

- Extend to INT2 (extreme compression for edge deployment)
- Investigate whether the gradient variance threshold changes with model size
- Write paper draft describing the threshold phenomenon and per-layer clipping fix

**Open Questions**

- Is there a theoretical explanation for why the threshold is approximately 0.15? It seems empirically consistent but I don't have a derivation.
- Does the threshold change if I use a different quantization scheme (symmetric vs asymmetric)?
