**Weekly Report — Amara Diallo**
**Week 7 | Video Temporal Attention Optimization**

---

**Summary of Progress**

Experiments are complete. My temporal window compression method (T_window=32) achieves 42% memory reduction and 1.7x speedup with only -0.4 BLEU loss on the ActivityNet QA benchmark. I'm preparing the paper draft.

**Results by Video Duration**

I ran a careful ablation by video duration because I suspected the T=32 window would interact with video length:

- Videos <60 seconds (n=412): T=32 causes BLEU loss of −0.4. Acceptable.
- Videos 1–5 minutes (n=203): T=32 causes BLEU loss of −1.9. Borderline.
- Videos >5 minutes (n=87): T=32 causes BLEU loss of −4.8. Substantial degradation.

**This shortcut is specific to short videos.** The ActivityNet benchmark is dominated by videos under 3 minutes, which is why the overall result looks strong. I would NOT apply T=32 for long-form content — the BLEU loss is too large to be acceptable in any application I can think of. My paper will clearly scope the contribution to short videos (<3 minutes).

**Training Stability: BF16 Switch**

I had a separate issue with training instability — loss spikes at step ~3000. After debugging, I found FP16 mixed precision was overflowing in the attention layer during high-gradient-norm steps. Switching to BF16 (larger dynamic range, same 16-bit width) eliminated the spikes entirely. I'd recommend BF16 to anyone doing attention-heavy finetuning with variable gradient norms.

**Open Questions**

- Is there a dynamic T_window approach that degrades gracefully for longer videos?
- Does the temporal window method generalize to other video encoders?
