**Weekly Report — Hanyu Wei**
**Week 8 | Speculative Decoding for LLM Inference**

---

**Summary of Progress**

This week I finalized the experimental evaluation of my speculative decoding pipeline using a 7B-parameter draft model paired with a 70B target model. The overall throughput improvement reached 2.3x on standard benchmark prompts, which is within the range reported in the original Leviathan et al. paper. I am reasonably confident the implementation is correct.

**Draft Model Acceptance Rate Analysis**

The core metric for speculative decoding is the token acceptance rate α — the fraction of draft tokens accepted by the target model. I measured α = 0.71 on math reasoning tasks and α = 0.68 on code generation. These are consistent with what I expected given the draft-target model family mismatch (I am using a different pretraining corpus).

The variance of α across batches was high initially: σ = 0.34, meaning some batches got nearly all tokens accepted and others got very few. This made wall-clock throughput highly variable and hard to benchmark reliably.

**Sampling Strategy Experiments**

To investigate the acceptance rate variance, I tried three sampling configurations:

1. Greedy decoding (temperature T=0): α = 0.74 ± 0.04. Low variance, but output quality degraded (outputs were repetitive).
2. Temperature sampling (T=0.9): α = 0.69 ± 0.31. High variance — the target model's temperature sampling introduced a lot of randomness that interacted badly with the draft model's deterministic rollout.
3. Nucleus sampling (top-p = 0.9, T = 0.7): α = 0.71 ± 0.12. This was the most interesting result. The acceptance rate mean was similar to temperature sampling, but the variance dropped dramatically from σ = 0.34 to σ = 0.12. I was not expecting this — nucleus sampling restricts the vocabulary to high-probability tokens, which apparently reduces the tail risk of the draft model proposing tokens that are very unlikely under the target model.

I mentioned this nucleus sampling observation to Xiaohang in our corridor conversation; he said it was interesting but didn't see an immediate connection to his work.

**Architecture Experiments**

I tried two draft model architectures: a pruned version of the target (every other layer removed) and a separately trained smaller model. The pruned version gives α = 0.74 but is slow to run because the weight dimensions are still large. The separately trained smaller model gives α = 0.71 but is 4x faster to run as a draft. Net throughput: 2.3x vs 1.9x. Separately trained wins.

**Memory Usage**

Current GPU memory footprint: target model 140GB (2x A100 80GB), draft model 14GB. I load the draft model on the second GPU alongside the second shard of the target. No OOM issues at current batch sizes.

**Upcoming Plans**

Next week I have two major changes planned. First, I intend to scale the speculative decoding pipeline to a 32-GPU cluster to evaluate throughput at production scale — I expect roughly linear scaling in throughput since the draft and target model can be more aggressively parallelized. Second, as a memory optimization, I plan to apply INT8 quantization to the draft model. The draft model is accessed frequently (once per speculative step), so reducing its memory footprint from 14GB to ~7GB would free up GPU memory for larger batch sizes. I have not used quantization in this project before, so this will be a first implementation.

**Open Questions**

- Does the nucleus sampling variance reduction generalize to other draft-target model pairs, or is it specific to my architecture combination?
- At 32-GPU scale, will the communication overhead of distributed draft model rollout dominate the throughput gains?
- Is INT8 quantization for the draft model safe without additional calibration? I've seen conflicting advice about whether calibration is needed for 8-bit vs 4-bit.
