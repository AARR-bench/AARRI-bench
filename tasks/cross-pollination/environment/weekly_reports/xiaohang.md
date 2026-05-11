# Weekly Report — Xiaohang Xu
## Week of 2025-01-20

### Summary

Main focus this week was evaluating different eviction strategies for dynamic KV cache compression, benchmarking against the SnapKV baseline. I have solid average-case numbers now, but I've hit a fundamental variability problem that's blocking production deployment design. Still working on how to address it.

### KV Cache Eviction Strategy Comparison

I implemented and evaluated four eviction strategies on top of our attention-score-based cache manager, using LLaMA-3.1-8B and LLaMA-3.1-70B as target models:

1. **Score-based eviction** (SnapKV baseline): evict KV pairs with lowest cumulative attention score. Average memory savings: 38.7%.
2. **Recency-weighted score**: combine attention score with recency signal (exponential decay, half-life = 64 tokens). Memory savings: 41.2%, slight perplexity degradation (+0.3 on WikiText-2).
3. **Hybrid eviction with importance clustering**: cluster KV pairs by key embedding similarity, then evict least-important cluster representative. Memory savings: 35.1%, best quality metrics.
4. **Adaptive budget**: dynamically allocate cache budget per attention head based on entropy of attention distribution. Memory savings: 44.8%, but implementation complexity is high and it adds ~12ms latency overhead.

Overall, recency-weighted scoring (strategy 2) gives the best tradeoff and is my current recommendation for the paper. It matches or slightly exceeds SnapKV on memory savings with acceptable quality cost.

### The Variance Problem

Here is what's actually keeping me up at night. The memory savings per sequence vary wildly — anywhere from 18% to 61% depending on the input. I've been reporting the average (39%) but this is misleading for production use.

Specifically: short structured inputs (factual QA, classification prompts) tend toward 18–25% savings because the model attends broadly across the full context and there are few low-score tokens to evict. Long conversational or document-summarization inputs get 50–61% savings because the attention pattern is sparse and concentrated. The variance is not noise — it's systematic. But it means I can't give a single reliable number to an infrastructure team trying to size memory budgets.

The practical consequence: if you provision GPU memory assuming 39% savings, you'll OOM on the inputs that only achieve 18% savings. If you provision assuming worst-case 18% savings, you get almost none of the benefit. And the input characteristics that predict which regime you'll be in are not easily knowable at request-dispatch time.

I've been averaging over this variance to report a clean number in the paper, but for production systems this is a real problem. I've looked at the literature on variance reduction in dynamic memory allocation schemes and haven't found a clean solution. The closest work is on adaptive prefill/decode separation (e.g., Sarathi-Serve), but they don't address KV cache variance specifically.

I need to either (a) find a way to reduce the variance so the average is more reliable, or (b) develop a per-request predictor that estimates cache savings before generation, enabling smarter provisioning. Option (b) feels like a second paper. I'm not sure what to do.

### Accuracy / Quality Benchmarks

On MMLU (5-shot): strategy 2 achieves 72.1% vs 72.8% for the full-KV baseline (LLaMA-3.1-8B). On HumanEval: 62.4% vs 63.1%. On MT-Bench: 7.82/10 vs 7.97/10. These are acceptable degradations. The quality numbers are fine — the variance issue is purely about memory provisioning, not model quality.

### Baseline Comparison

SnapKV (baseline): 38.2% average savings, score-based. My best method: 41.2% average savings, recency-weighted. Improvement is modest but real. I can probably squeeze another 2–3% with tuning.

For memory latency overhead: my implementation adds 2.1ms per decode step on 8B (vs 1.4ms for SnapKV) — still acceptable.

### Infrastructure Notes

Running on 2×A100 80GB. Memory profiling tool is working well now — I built a per-sequence tracker that logs the actual KV cache budget used at each step, which is where the variance numbers above come from.

### Next Week

1. Try to characterize the per-sequence variance more precisely — is it predictable from input length alone, or do content features matter?
2. Start drafting the eviction strategy comparison as a paper section.
3. Investigate whether there's a learned predictor that can estimate savings before generation starts.

Question for meeting: Is the variance problem something I should address in the paper explicitly, or just report averages and note that variance is high? I worry reviewers will ask about it either way.
