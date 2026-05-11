# Weekly Report — Week 2
**Student:** Sofia Andersson
**Role:** Reward Model Training
**Date:** 2025-01-13 to 2025-01-17

---

## Summary

Received Batch 1 from Ziqian (1,247 pairs). Ran full training but hit an unexpected val loss plateau at step ~800. Despite trying multiple learning rates and regularization settings, I cannot get below val_loss = 0.89. Very confused.

## Training Run Details

Used the full 1,247-pair dataset (80/10/10 train/val/test split):
- Train: 997 pairs
- Val: 125 pairs
- Test: 125 pairs

Training parameters:
- Backbone: `microsoft/deberta-v3-large`
- Max sequence length: 256 tokens
- Batch size: 8
- Learning rate: 3e-5 (AdamW)
- Weight decay: 0.01
- Warmup steps: 100
- Total steps: 1,500

**Results:** Loss decreased normally until step ~800, then plateaued at val_loss ≈ 0.89. Final val accuracy: 0.603.

## Learning Rate Sweep

Systematically tried three learning rates:

| LR | Peak Val Loss | Plateau Step | Final Val Loss |
|----|--------------|--------------|---------------|
| 1e-5 | 0.97 | step 600 | 0.91 |
| 3e-5 | 0.89 | step 800 | 0.89 |
| 5e-5 | 0.93 | step 500 | 0.93 |

3e-5 performs best but still hits the plateau. I also tried cosine LR scheduling — no improvement.

## Potential Causes (my current hypotheses)

1. **Dataset too small?** 997 training pairs may be insufficient for DeBERTa-v3-large (334M params). Waiting for more data from Ziqian.
2. **Data noise?** Reward models are known to be sensitive to annotation noise. Talked to Ziqian — he says IAA is 0.73, which seems fine.
3. **Sequence length?** Some dialogue texts might be getting cut off at 256 tokens. Haven't investigated fully.

## Training Instability

One thing I noticed: a few training batches produce unusually high loss spikes that then drop back down. This seems like numerical instability or possibly a bad batch. I've added gradient clipping (max_norm=1.0) to address this.

## Next Steps

- Get more data from Ziqian (Batch 2)
- Investigate whether longer sequence length helps
- Try weight decay tuning
- Consider label smoothing
