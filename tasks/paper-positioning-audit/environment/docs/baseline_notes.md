# Baseline Notes

These are notes from the reading group, not an official review.

- `HeteroSeg-2025` is the strongest current internal baseline for the group's RGB/SAR flood experiments.
- `PatchFuse-2022` is the older baseline that appears most often in the paper's narrative examples.
- `CodaFuse` uses the same nominal backbone family as `HeteroSeg-2025`, but the released table also marks an additional pretraining stage on a mixed auxiliary-sensor corpus.
- The authors report a strong average number, but that average pools RGB+depth, RGB+thermal, and RGB+SAR datasets.
- One student noted that confidence-gated distillation could fit our teacher-student setup. Another noted that the target flood setting is not the dataset where the method looks strongest.
