**Weekly Report — Chiara Rossi**
**Week 8 | Large-Scale Distributed Training**

---

**Summary of Progress**

This week I successfully scaled my training setup from 8 GPUs to 32 GPUs and fixed a critical bug in my gradient accumulation configuration. I'm also observing an interesting side effect related to gradient variance that I don't fully understand yet.

**Background**

My project is training a large vision-language model (3B parameters) on a synthetic instruction-following dataset. The previous 8-GPU setup was producing consistent results. Scaling to 32 GPUs was necessary to meet the training timeline, but it introduced several new problems.

**Critical Bug: Gradient Accumulation Not Scaled with GPU Count**

When I moved from 8 to 32 GPUs, I forgot to adjust the gradient accumulation steps. At 8 GPUs, I had accumulation_steps = 8, giving an effective batch size of 8 GPUs × 4 samples/GPU × 8 steps = 256 samples. When I added more GPUs (32) without changing accumulation_steps, the effective batch size jumped to 32 × 4 × 8 = 1024 samples. This is a 4x larger batch than I intended, and the model converged to a different (worse) solution — generalization on the held-out evaluation set dropped by 4.2 points.

The fix was to scale accumulation steps down proportionally: at 32 GPUs with the same target effective batch size (256), I need accumulation_steps = 2 (since 32 × 4 × 2 = 256). After this fix, training dynamics matched the 8-GPU baseline and generalization recovered.

The lesson: **when scaling GPU count, gradient accumulation steps must scale inversely to keep effective batch size constant**.

**Communication Overhead Profiling**

At 32 GPUs, AllReduce communication takes 23% of step time vs 8% at 8 GPUs. This is manageable but notable. I'm using NCCL with ring AllReduce; bandwidth is the bottleneck (not latency). Gradient compression would help but I haven't implemented it.

**Interesting Side Effect: Gradient Variance Reduction at Scale**

One thing I noticed at 32 GPUs (with the corrected accumulation_steps = 2 and effective batch size = 256) is that the microbatch gradient variance has decreased substantially compared to 8-GPU runs. Specifically, I measured the L2 norm variance of gradients across microbatches within a step:

- 8 GPUs, accumulation_steps=8, effective batch=256: gradient variance σ² = 0.42 per layer (averaged)
- 32 GPUs, accumulation_steps=2, effective batch=256: gradient variance σ² = 0.11 per layer

That's roughly a 4x reduction in gradient variance, consistent with the 4x increase in the number of accumulation steps? Wait — actually, at 32 GPUs, accumulation_steps went DOWN from 8 to 2. So what's driving the variance reduction?

I think the answer is: each "microbatch" at 32 GPUs is actually computed across 32 × 4 = 128 samples simultaneously (one parallel forward pass), vs 8 × 4 = 32 samples at 8 GPUs. Even though accumulation_steps is smaller, each gradient estimate at 32 GPUs is averaged over 4x more samples. So the gradient variance reduction is roughly 1/√4 = 0.5 relative to 8-GPU microbatch variance... wait, I'm confusing myself. Let me think more carefully.

In any case, the empirical observation is clear: gradient variance per microbatch decreased by ~4x when scaling from 8 to 32 GPUs at the same effective batch size. The reduction is roughly proportional to the number of GPUs participating in each microbatch gradient computation. I'm writing this up as an "interesting side effect" to investigate further — I don't fully understand the theory but the empirical result is consistent.

**Numerical Stability at Scale**

One surprise: certain layers experienced gradient norm spikes at 32 GPUs that I didn't see at 8 GPUs. I suspect this is related to accumulated floating-point rounding differences across 32 GPUs. I added gradient norm clipping (max_norm=1.0) which resolved it.

**Next Steps**

- Scale to 64 GPUs (stretch goal)
- Profile communication overhead with gradient compression
- Understand the gradient variance reduction phenomenon theoretically

**Open Questions**

- Is the gradient variance reduction at scale a well-known phenomenon? I couldn't find a paper that specifically discusses this for vision-language models.
- Does the reduced gradient variance have implications for numerical stability in quantization?
