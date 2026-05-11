# Weekly Report — Week 1
**Student:** Sofia Andersson
**Date:** 2025-01-06 to 2025-01-10
**Project:** Medical Dialogue RLHF — Reward Model Training

## Summary

Set up the reward model training infrastructure this week. Waiting on the final annotation dataset from Ziqian. Used the pilot batch (160 pairs) to validate the training pipeline end-to-end.

## Model Architecture

Base model: `DeBERTa-v3-large` (fine-tuned from HuggingFace hub)
Training objective: Bradley-Terry pairwise preference loss
Pooling: [CLS] token representation
Output: single scalar reward score

## Pilot Training Run

Trained on the 160-pair pilot batch to verify the pipeline:
- Batch size: 16
- Learning rate: 2e-5 (linear warmup 100 steps, cosine decay)
- Epochs: 5
- Validation split: 20% (32 pairs)

Results on pilot data:
- Step 100: val_loss = 0.512
- Step 200: val_loss = 0.471
- Step 300: val_loss = 0.448 (below threshold — good sign)

The pipeline is working. Loss is decreasing smoothly. Looking forward to training on the full 1,459-pair dataset.

## Infrastructure Notes

Training runs on 2x A100 40GB GPUs. Full training on 1,459 pairs should take approximately 3 hours. Will begin as soon as Ziqian delivers the production dataset.

## Plan for Week 2

- Receive full annotation dataset from Ziqian
- Train RM v3 on full dataset
- Run validation and deliver checkpoint to Arjun
