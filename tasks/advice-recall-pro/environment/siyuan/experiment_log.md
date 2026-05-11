# Experiment Log — Siyuan Jiang
## Task: TCGA-LUNG WSI Classification (LUAD vs LUSC)
## Backbone: ViT-L/16 (ImageNet-21k pretrained, unless noted)
## Total configurations run: 47

---

## Summary Statistics

| Metric | Min | Max | Mean | Best |
|--------|-----|-----|------|------|
| Val Accuracy | 58.2% | 63.6% | 61.4% | 63.6% (Run 46) |
| Val AUROC | 0.791 | 0.831 | 0.811 | 0.831 (Run 47) |

Despite 6 weeks of systematic search across 47 configurations, performance remains bounded in the 61–63.6% accuracy range. Ensemble of top-3 runs yields 63.4% accuracy and 0.826 AUROC.

---

## Experiment Table (Selected runs)

| Run | Backbone | LR | BS | Augmentation | Aggregation | Optimizer | Epochs | Val Acc | Val AUROC | Notes |
|-----|----------|----|----|-------------|-------------|-----------|--------|---------|-----------|-------|
| 01 | ViT-L/16 | 2e-5 | 32 | Basic | MeanPool | AdamW | 20 | 58.3% | 0.791 | Baseline |
| 02 | ViT-L/16 | 5e-6 | 32 | Basic | MeanPool | AdamW | 20 | 59.8% | 0.798 | Freeze first 12 layers |
| 03 | ViT-L/16 | 1e-5 | 32 | Basic | MeanPool | AdamW | 20 | 60.2% | 0.803 | No freezing |
| 04 | ViT-L/16 | 1e-5 | 32 | +Rotation+Flip | MeanPool | AdamW | 20 | 61.3% | 0.809 | |
| 05 | ViT-L/16 | 1e-5 | 32 | +StainNorm | MeanPool | AdamW | 20 | 61.7% | 0.811 | Macenko norm |
| 06 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 20 | 62.1% | 0.814 | |
| 07 | ViT-L/16 | 5e-6 | 16 | +StainNorm+Aug | AttnPool | AdamW | 30 | 61.9% | 0.812 | |
| 08 | ViT-L/16 | 2e-5 | 16 | +StainNorm+Aug | AttnPool | AdamW | 30 | 62.0% | 0.813 | |
| 09 | ViT-L/16 | 1e-5 | 64 | +StainNorm+Aug | AttnPool | AdamW | 20 | 61.8% | 0.811 | |
| 10 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | SGD | 30 | 62.4% | 0.817 | SGD momentum=0.9 |
| 11 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | SGD | 50 | 62.8% | 0.818 | CyclicLR |
| 12 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 60 | 62.9% | 0.819 | Long training |
| 13 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 20 | 62.3% | 0.815 | 256px patches |
| 14 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 20 | 60.8% | 0.804 | 256px, no stain |
| 15 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 20 | 62.7% | 0.818 | FocalLoss γ=2 |
| 16 | ViT-L/16 | 1e-5 | 32 | +StainNorm+MixUp | AttnPool | AdamW | 20 | 63.1% | 0.820 | |
| 17 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug+MixUp | AttnPool | AdamW | 30 | 63.3% | 0.822 | |
| 18 | Ensemble-3 | — | — | — | AttnPool | — | — | 63.4% | 0.826 | Best single result |
| 19 | ViT-L/16 | 1e-5 | 32 | +Multi-scale 10x+20x | AttnPool | AdamW | 20 | 63.1% | 0.821 | |
| 20 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | MeanPool | AdamW | 20 | 62.0% | 0.813 | LabelSmooth ε=0.1 |
| 21 | ViT-B/16 | 1e-5 | 32 | +StainNorm+Aug | AttnPool | AdamW | 20 | 61.8% | 0.810 | Smaller backbone |
| 22 | ViT-B/16 | 2e-5 | 32 | +StainNorm+Aug | ABMIL | AdamW | 20 | 63.2% | 0.822 | Attention-based MIL |
| 23 | ViT-L/16 | 1e-5 | 32 | +StainNorm+Aug | ABMIL | AdamW | 20 | 63.4% | 0.825 | |
| 24–46 | ViT-L/16 | various | various | various | various | various | various | 61.2–63.5% | 0.807–0.829 | Additional sweeps |
| 46 | ViT-L/16 | 8e-6 | 32 | +StainNorm+Aug+MixUp | ABMIL | AdamW | 25 | 63.6% | 0.829 | Best individual run |
| 47 | Ensemble-5 | — | — | — | — | — | — | 63.4% | 0.831 | Best AUROC |

---

## Observations

1. Performance is bounded in a narrow range regardless of hyperparameter choice
2. Architecture variants (pooling, MIL) contribute marginal improvements
3. Data augmentation contributes +1-2% but doesn't escape the plateau
4. The ceiling at ~63.6% accuracy / 0.831 AUROC is consistent across all approaches
5. The UNI paper (Chen et al. 2023) specifically reports ViT-L/16 ImageNet achieves 62.3% on this task — consistent with our results

**Conclusion:** The performance ceiling is a function of the ImageNet-pretrained backbone, not hyperparameter choices. Domain-adapted pretraining appears necessary to achieve >85% performance on this task.
