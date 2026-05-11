**Weekly Report — Kenji Tanaka**
**Week 8 | Long Video Visual Question Answering**

---

**Summary of Progress**

Progress this week was slower than expected due to a persistent out-of-memory problem I have not been able to resolve. I have working code but cannot run experiments at the video lengths my dataset requires.

**Dataset Description**

My dataset is the LongVideoQA benchmark, which consists of documentary segments averaging 8 to 15 minutes in duration. The QA pairs require understanding events that span the full length of the video — for example, "How did the narrator's opinion of the subject change from the beginning to the end?" These questions cannot be answered from any local segment; they require global temporal understanding.

The average video in my evaluation set is 11.3 minutes at 24 fps with 1-second frame sampling, yielding approximately 680 frames per video. This is substantially more frames than standard short-video VQA benchmarks.

**Out-of-Memory Problem**

When I load a full video (680 frames) and attempt to run simultaneous frame processing (all frames attending to all other frames via self-attention), I immediately hit OOM on my A100 80GB setup. The attention matrix for 680 frames is 680×680 = 462,400 attention weights per head, and with 32 heads and 8 layers the total memory for attention scores alone is:

462,400 × 32 heads × 8 layers × 2 bytes (FP16) ≈ 236GB

This is obviously infeasible. I need to reduce memory somehow.

**Attempted Approaches**

1. **Gradient checkpointing**: Reduced activation memory by 40%, but attention score computation itself remains the bottleneck. Still OOM.
2. **Reducing to 8 frames**: The model runs, but performance on questions requiring global understanding is obviously poor (essentially random).
3. **Sliding window of 64 frames**: Model runs, performance is better than 8 frames but still poor on cross-segment questions. The model cannot answer "how did X change from beginning to end" when it can only see 64 frames at a time.

None of these approaches solve my actual problem, which is that I need the model to have some meaningful representation of the entire 680-frame video without the quadratic memory cost.

**Literature Review**

I've been reading about temporal compression methods. Most papers focus on videos shorter than 3 minutes. I haven't found a method that handles 8-15 minute videos satisfactorily. The methods that work for short videos tend to assume temporal locality — that nearby frames are more important than distant ones — but my questions explicitly require long-range temporal understanding.

I'm also looking at sparse attention patterns (attending to a subset of key frames rather than all frames) but selecting the right key frames without seeing the question seems difficult.

**Related Work Gap**

There is a notable gap in the literature: long-form video VQA (>5 minutes) is mostly unsolved. Papers that claim to solve "long video understanding" typically use videos of 2-5 minutes at most. My 8-15 minute setting appears to be genuinely novel.

**Next Steps**

I need to find a way to handle 680-frame inputs within 80GB GPU memory. Either:
(a) A compression method that preserves long-range temporal information (the problem with sliding windows)
(b) An architecture change that avoids the quadratic attention scaling
(c) A smarter frame sampling strategy that doesn't assume temporal locality

I'd welcome any suggestions from the team on this.

**Open Questions**

- Is there any attention approximation method that provably preserves long-range dependencies while reducing quadratic complexity?
- Has anyone seen a method that handles 600+ frame videos effectively for QA tasks requiring temporal reasoning?
