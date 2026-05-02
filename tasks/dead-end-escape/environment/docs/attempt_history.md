# Attempt History

- Baseline: DINOv3 teacher + MiT-B2 student, no decoupling, no contrastive loss. CAU-Flood val mIoU: 58.4.
- Attempt A: add contrastive loss only. CAU-Flood val mIoU: 55.1. Boundary F1: 61.0.
- Attempt B: add semantic/modality decoupling plus contrastive loss. CAU-Flood val mIoU: 52.8. Boundary F1: 59.3.
- Attempt C: replace CE with focal loss because the team suspected boundary imbalance. CAU-Flood val mIoU: 53.0. Boundary F1: 59.9.
- Attempt D: add 8-epoch warmup for the teacher-student branch. CAU-Flood val mIoU: 53.4. Boundary F1: 60.1.
- Attempt E: increase decoupling weight from 0.2 to 0.8. CAU-Flood val mIoU: 50.9. RGB-SAR alignment score became worse.
- Attempt F: increase contrastive weight from 0.1 to 0.5. CAU-Flood val mIoU: 51.6. DINO feature similarity collapsed for mixed flood/non-flood patches.

One note from the experiment owner: "If decoupling is really useful, it is strange that contrastive-only already hurts and decoupling makes it worse."
