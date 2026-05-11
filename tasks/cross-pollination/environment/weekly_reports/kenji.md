# Weekly Report — Kenji Tanaka
## Week of 2025-01-20

### Summary

Benchmark results are coming together for the shorter video categories, but I'm still hitting a hard wall on the 4-minute+ test cases due to memory constraints. I have a workaround in place but it's hurting my numbers on the harder subset. Flagging this as the main blocker for this week.

### VideoQA Benchmark Results (EgoSchema and ActivityNet-QA)

I'm evaluating on two benchmarks: EgoSchema (which has videos up to 3 minutes) and a custom long-video extension of ActivityNet-QA that I constructed with videos from 3–10 minutes. The short-video results are solid:

- EgoSchema (≤3 min): accuracy 68.3% on multiple choice, BLEU-4 35.1% on open-ended generation
- ActivityNet-QA standard split (≤2 min average): accuracy 72.1%
- My long-video extension (3–5 min): accuracy 61.4%
- My long-video extension (5–10 min): accuracy 53.7%

The accuracy drop from the ≤3 minute videos to the 5–10 minute videos is about 15 percentage points, which is more than I expected. Some of this is genuinely harder questions (longer videos have more complex causal chains), but some of it I suspect is my memory workaround (below).

### The Memory Problem

Here is the main issue. Processing videos longer than about 4 minutes while keeping all frames in context simultaneously causes my model to run out of memory on the A100 80GB. The model needs to process all frames simultaneously to build its cross-frame attention, and at 8 frames per second for a 4-minute video, that's roughly 1,920 frames — each frame being a 256-token sequence after the vision encoder. The total sequence length exceeds what fits in memory.

My current workaround is to crop all input videos to the first 4 minutes before feeding them to the model. This obviously discards content from the later parts of longer videos, which is exactly where the questions often focus. I expect this is responsible for a significant fraction of the 5–10 minute accuracy drop.

I've looked into FlashAttention-2 as a potential fix — and it helps with the attention computation itself, but the KV cache still blows up because I'm keeping every frame in context. FlashAttention makes the attention step faster and somewhat more memory-efficient, but doesn't reduce the fundamental memory requirement enough to fit 8+ minute videos.

I've also considered a sliding window approach — processing the video in temporal chunks and somehow aggregating results. But it seems like reducing the frames would hurt quality too much, and I'm not sure how to combine the chunk-level outputs into a coherent answer for questions that span the full video. I haven't found a clean solution in the literature yet.

If anyone has thoughts on this, I would genuinely appreciate them. This feels like the main obstacle between my current results and what the benchmark actually requires.

### Model Variants Tested

Tried three model variants this week:
- **Baseline (LongVA-7B)**: 68.3% on EgoSchema, OOM on 4+ minutes
- **LLaVA-NeXT-Video-34B**: slightly better (69.1% on EgoSchema) but even worse on memory — OOM on 3+ minutes
- **Video-LLaMA-2 with memory-efficient attention**: 66.8% on EgoSchema, survives to 5 minutes before OOM but at the cost of 2.3% accuracy

Video-LLaMA-2 is interesting because its memory-efficient attention buys me one extra minute before OOM, but the quality cost isn't worth it for the benchmark comparison.

### Data Construction for the Long-Video Extension

The long-video test set I built has 412 examples from 3–10 minute ActivityNet clips. I annotated question-answer pairs manually with the help of two undergraduate research assistants. Inter-annotator agreement was κ=0.73 (substantial agreement). The questions explicitly require information from different temporal positions in the video to ensure we're testing genuine long-range comprehension.

One issue: the 5–10 minute category only has 87 examples right now, which may be too small for stable benchmark estimates. I need to annotate more. Will prioritize this next week.

### Infrastructure Notes

Running on 2×A100 80GB. Even with two GPUs and model parallelism, the memory bottleneck is on the attention side (both GPUs filled) rather than parameter memory. This rules out adding more GPUs as a simple fix unless I fundamentally change how I handle the temporal sequence.

### Next Week

1. Annotate more 5–10 minute examples to get to at least 200 in that category.
2. Investigate whether there's a chunking/aggregation approach that doesn't sacrifice too much on span-crossing questions.
3. Run ablations with different frame sampling rates (8 fps vs 4 fps vs 2 fps) to see if I can buy memory headroom that way without destroying accuracy.

Question for meeting: Is there a known approach for handling very long video sequences that doesn't require keeping all frames in context simultaneously? I feel like I must be missing something obvious, because the current workaround is clearly not going to work for the final benchmark numbers.
