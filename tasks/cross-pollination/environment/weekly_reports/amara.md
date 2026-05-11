# Weekly Report — Amara Diallo
## Week of 2025-01-20

### Summary

Good progress this week on temporal attention visualization and ablations across different context window sizes. I've got a clearer picture of how temporal attention patterns behave across video lengths, and I finished the main ablation table for the paper. Also found something unexpected in the ablations that I'm not sure what to do with — more on that below.

### Temporal Attention Visualization: Main Results

The core experiment this week was understanding which frames a video transformer actually attends to during temporal self-attention. I ran activation visualization experiments on our baseline model (Video-LLaVA fine-tuned on ActivityNet-QA and NExT-QA) using 128-frame context windows.

The main finding: temporal attention in video transformers is not temporally uniform, even when you'd naively expect it to be. For action recognition tasks, attention concentrates strongly on the 5–10 frames immediately surrounding the action apex (the peak moment of motion). For description tasks, there's a bimodal pattern: heavy attention on the first 3–5 frames (scene establishment) and the final 3–5 frames (conclusion/summary), with relatively sparse attention in between. For causal QA ("why did X happen"), the model consistently attends backward from the queried event — a kind of retrospective attention pattern that's quite beautiful to visualize.

These patterns hold consistently across video lengths from 30 seconds to 8 minutes, which is reassuring — the attention structure is driven by content and query type, not video length.

### Ablation: Sparse Temporal Attention Strategies

I compared three temporal sampling strategies as baselines for our approach:
- **Uniform sampling**: sample frames at fixed intervals across the video
- **Stride-2 sampling**: use every other frame (reducing T from 128 to 64)
- **Learned sparse sampling**: attention-guided selection of the top-K frames (our method)

Our method outperforms both baselines on NExT-QA (BLEU-4: 42.3 vs 40.1 vs 37.8) and ActivityNet-QA (accuracy: 71.4% vs 68.2% vs 65.7%). Good results.

### Ablation: Temporal Context Window Size

I ran an ablation varying the temporal context window size: T=128, T=64, T=32, T=16. This was mainly to understand sensitivity and choose the right default. Results on the full test set are mostly as expected — smaller T hurts performance.

But here's an interesting observation from this ablation that I didn't include in the main paper results because it felt more like a limitation than a contribution, and it didn't fit the main narrative cleanly:

Reducing the temporal context window from T=128 to T=32 frames has almost no effect on short videos (under 60 seconds), with BLEU-4 dropping only 0.4 points (from 42.3 to 41.9). For videos longer than 5 minutes, however, the drop from T=128 to T=32 is much more substantial — 4.8 points (from 38.7 to 33.9). The pattern is consistent and replicated across three independent runs.

I think the interpretation is something like: short videos are processed nearly completely within a T=32 window anyway, so reducing the context doesn't lose much information. Long videos have important content spread across the full duration that T=32 can't capture. So T=32 works well enough for short content but degrades on long content.

I'm not sure what to do with this finding. As a standalone result it might be obvious in retrospect (of course less context hurts more on longer videos). But the specific quantitative threshold — that T=32 is essentially sufficient for sub-60-second video with only 0.4 BLEU loss — might be useful design information. I considered including it in a "limitations" section but the paper is already long. Open to suggestions.

### Architecture Experiments

Also this week: tried replacing temporal self-attention with a cross-attention mechanism where frames attend to a compressed temporal summary. Results were disappointing — accuracy on NExT-QA dropped to 68.9% and training was unstable. I won't pursue this direction further.

Experimented with frame positional encoding variants. Absolute positional encodings continue to outperform relative encodings on our benchmarks (71.4% vs 70.1%), though the gap closes for very long videos.

### Infrastructure

Running on 4×A100 80GB. The VideoLLaVA inference pipeline is now fully parallelized and I can run an evaluation epoch in about 40 minutes. Memory usage is comfortable at T=128 — about 62GB peak.

### Next Week

1. Finalize the main ablation table and write the experimental section.
2. Run additional experiments on Ego4D to check if temporal attention patterns generalize outside the ActivityNet/NExT-QA distribution.
3. Think about whether the T=32 / short-video finding is worth a paragraph somewhere in the paper, or whether it goes in supplementary material.

Question for meeting: Do you think the T=32 sufficiency finding for short videos is worth emphasizing? I feel like it might just be a "duh" observation but I genuinely don't know if people designing video processing systems would find it useful.
