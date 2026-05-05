# Modality Note

RGB and SAR should not be treated as if they were just interchangeable channels.

Observed properties:

- RGB inputs are radiometrically normalized and behave like natural-image intensity data.
- SAR inputs have very different statistics, including speckle, gain variation, and heavier distribution shift across scenes.
- Shared raw normalization across RGB and SAR previously produced unstable activation ranges.

Task-specific considerations:

- Temporal ordering still matters because the task is change-aware segmentation.
- The RGB stream is the earlier observation and the SAR stream is the later observation.
- Collapsing modality and time structure too early makes it harder to tell whether failures come from modality mismatch, timestamp confusion, or both.
