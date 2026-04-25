# Module 2: Cross-Stream Interaction Timing

Choose one interaction strategy.

## `fusion_before_backbone`

- Perform cross-stream fusion before the main backbone

## `fusion_after_shallow_stage`

- Extract shallow features first
- Then perform cross-stream fusion

## `fusion_at_intermediate_stage`

- Keep the streams separate through the early feature stages
- Fuse only at an intermediate feature level
