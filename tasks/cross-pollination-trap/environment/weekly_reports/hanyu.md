**Weekly Report — Hanyu Wei**
**Week 7 | Speculative Decoding for LLM Inference**

---

**Summary of Progress**

This week I completed the evaluation of my speculative decoding pipeline. The overall throughput improvement is 2.3x on standard prompts using a 7B draft model paired with a 70B target. I'm satisfied with this result.

**Acceptance Rate Analysis**

Token acceptance rate α = 0.71 on math tasks, α = 0.68 on code generation. The main issue was variance: σ = 0.34 across batches, making throughput highly variable and hard to benchmark.

I tried three sampling strategies. Greedy decoding (T=0) gave α=0.74±0.04 — low variance but repetitive outputs. Temperature sampling (T=0.9) gave α=0.69±0.31 — high variance. Nucleus sampling (top-p=0.9, T=0.7) gave α=0.71±0.12. The nucleus sampling approach was most interesting: it matched temperature sampling's mean acceptance rate but reduced variance by 3x. I believe this is because restricting the vocabulary to high-probability tokens reduces the tail risk of the draft model producing tokens the target model finds very unlikely.

**Upcoming Plans**

Next week I'm scaling to a 32-GPU cluster. I'll need to revisit my gradient accumulation configuration. I remember Chiara mentioning something about a bug she hit when scaling GPU count — I should ask her before making the move.
