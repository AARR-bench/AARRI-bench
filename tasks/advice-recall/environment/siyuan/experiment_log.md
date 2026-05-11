# Siyuan Jiang — Experiment Log
## Task: TCGA-LUNG Subtype Classification (LUAD vs LUSC)
## Backbone: ViT-L/16, pretrained on ImageNet-1K (timm: vit_large_patch16_224)
## Dataset: TCGA-LUNG, 1,024 slides, 256×256 patches at 20× magnification
## Start date: 2024-01-05

---

| Run | Date | LR | Optimizer | Batch | Scheduler | Augmentation | Weight Decay | Label Smooth | Drop Path | Val Acc (%) | Notes |
|-----|------|-----|-----------|-------|-----------|--------------|-------------|-------------|-----------|-------------|-------|
| 01 | Jan 05 | 1e-4 | AdamW | 64 | warmup-cosine (5%) | flip+rotation | 0.01 | — | — | 61.3 | Baseline run, 50 epochs |
| 02 | Jan 06 | 3e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rotation | 0.01 | — | — | 61.9 | Longer warmup per advisor |
| 03 | Jan 07 | 1e-4 | AdamW | 64 | step (γ=0.1@20,40) | flip+rotation | 0.01 | — | — | 60.8 | Step decay, not helpful |
| 04 | Jan 07 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rotation | 0.01 | — | — | 62.4 | Best so far at this point |
| 05 | Jan 08 | 3e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rotation | 0.05 | — | — | 62.3 | Weight decay 0.05, no change |
| 06 | Jan 08 | 3e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rotation | 0.01 | — | — | 62.1 | 100-epoch run, peaked ~ep60 |
| 07 | Jan 12 | 1e-4 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | — | — | 61.7 | Added color jitter+random erasing |
| 08 | Jan 12 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | — | — | 62.0 | Strong aug, lower LR |
| 09 | Jan 13 | 3e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | 0.1 | — | 62.0 | Label smoothing added |
| 10 | Jan 14 | 1e-4 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | 0.1 | — | 61.8 | LS + higher LR, no gain |
| 11 | Jan 15 | 5e-5 | AdamW | 32 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | 0.1 | — | 61.4 | Smaller batch, slightly worse |
| 12 | Jan 16 | 5e-5 | AdamW | 128 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | — | — | 62.2 | Larger batch, moderate |
| 13 | Jan 19 | 5e-5 | AdamW | 256 | warmup-cosine (10%) | flip+rot+jitter+erase | 0.01 | — | — | 62.1 | Batch 256 per advisor |
| 14 | Jan 20 | 3e-5 | AdamW | 256 | warmup-cosine (20%) | flip+rot+jitter+erase | 0.01 | — | — | 61.9 | Longer warmup + big batch |
| 15 | Jan 20 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 62.7 | Mixup helps slightly! |
| 16 | Jan 21 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.4) | 0.01 | — | — | 62.3 | Higher alpha worse |
| 17 | Jan 21 | 3e-5 | AdamW | 256 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 62.9 | Best so far: mixup+big batch |
| 18 | Jan 22 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.05 | 0.1 | — | 62.5 | Combined regularization |
| 19 | Jan 22 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter | 0.01 | — | — | 62.1 | Weighted class sampling |
| 20 | Jan 23 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 62.1 | Focal loss γ=2 |
| 21 | Jan 24 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | 0.1 | 62.5 | Drop path rate 0.1 |
| 22 | Jan 24 | 3e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | 0.1 | 62.8 | Drop path + lower LR |
| 23 | Jan 25 | 5e-5 | Lion | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 61.9 | Lion optimizer |
| 24 | Jan 25 | 3e-4 | Lion | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 61.3 | Lion needs higher LR, worse |
| 25 | Jan 26 | 5e-5 | AdaGrad | 64 | warmup-cosine (10%) | flip+rot+jitter | 0.01 | — | — | 61.1 | AdaGrad, poor |
| 26 | Jan 26 | 5e-5 | RMSprop | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 61.6 | RMSprop, below baseline |
| 27 | Jan 27 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 62.2 | Partial fine-tune last 4 blocks |
| 28 | Jan 27 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 61.7 | ViT-B/16 ImageNet (smaller model) |
| 29 | Jan 28 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2) | 0.01 | — | — | 62.2 | Gradient clip max_norm=1.0 |
| 30 | Jan 28 | 3e-5 | AdamW | 128 | warmup-cosine (20%) | flip+rot+jitter+mixup(0.2) | 0.05 | 0.1 | 0.1 | 62.4 | All regularization combined |
| 31 | Jan 28 | 5e-5 | AdamW | 64 | warmup-cosine (10%) | flip+rot+jitter+mixup(0.2)+TTA | 0.01 | — | — | 63.2 | **Best: Mixup + TTA** |

---

## Summary Statistics
- **Configurations tried**: 31
- **Best val accuracy**: 63.2% (Run 31, Mixup + TTA)
- **Worst val accuracy**: 60.8% (Run 03, step decay)
- **Mean val accuracy**: 62.0%
- **Standard deviation**: 0.48%
- **Range**: 60.8% — 63.2%

---

## Personal Notes

**Week 1 (Jan 5-7):** Getting the pipeline set up. First results lower than expected but professor says it's just the starting point. Will tune.

**Week 2 (Jan 8-14):** Added augmentation per professor's suggestion. Still not moving much. Tried many scheduler variants. Everything clustering around 61-62%.

**Week 3 (Jan 15-22):** Systematic grid search over LR × batch × augmentation. Mixup helps a tiny bit (62.7%). Best result so far 62.9%. Starting to worry. Literature shows 78-85%, I'm 15 points behind with no clear path forward.

**Week 4 (Jan 23-28):** Tried multiple optimizers — Lion, AdaGrad, RMSprop — all worse or similar. Gradient clipping, stochastic depth, partial fine-tuning — nothing breaks through 63%. 31 configs now. Best is 63.2%. I don't know what else to try. Is the problem me, or is the problem the approach? I keep thinking about whether I should just switch projects entirely.
