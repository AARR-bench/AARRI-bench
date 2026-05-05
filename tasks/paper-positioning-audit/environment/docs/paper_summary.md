# Paper Summary

Paper nickname: CodaFuse

The paper proposes Confidence-Gated Cross-Modal Distillation for multimodal segmentation. The central idea is to use a strong optical teacher to provide soft spatial cues, while a second sensor branch is trained only where the teacher is uncertain or where the auxiliary sensor appears reliable.

The method has three main pieces:

- a confidence map from the optical teacher;
- a sensor-reliability gate computed from low-level auxiliary-sensor statistics;
- a distillation loss that is stronger in uncertain optical regions and weaker where the auxiliary branch appears noisy.

The authors frame the method as a practical way to add a second modality without redesigning the whole segmentation backbone. The introduction emphasizes "low-overhead adaptation", "teacher-guided fusion", and "uncertainty-aware supervision".

The paper's discussion section suggests that confidence-gated distillation may be a useful template for teams that already have a strong single-modality or teacher-student baseline.
