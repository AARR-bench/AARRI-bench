# Current Project Goal

The group is building an RGB+SAR flood segmentation system on `FloodSAR-Target`. The current baseline is a teacher-student encoder with a lightweight SAR adapter. The next project meeting will decide whether to add confidence-gated distillation, pursue a smaller adapter-only change, or pause this direction.

Constraints:

- the target deployment setting is heterogeneous RGB+SAR, not RGB+depth or RGB+thermal;
- the team can afford one controlled ablation sprint, not a full architecture rewrite;
- a useful external paper can still be valuable as inspiration even if it is not a good direct recipe;
- the decision should not be based only on a pooled average across unrelated modality settings.
