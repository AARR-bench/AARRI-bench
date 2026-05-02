# Method Description

The proposed method is a two-stream RGB+SAR segmentation system.

Design sketch:

- RGB uses the pretrained RGB backbone.
- SAR enters through a lightweight adapter branch before it is fused with RGB features.
- The notes from the original method emphasize that the SAR adapter is meant to learn a sensor-specific projection.
- Fusion is described after shallow modality-specific processing, where RGB and SAR features are already in a comparable representation space.
