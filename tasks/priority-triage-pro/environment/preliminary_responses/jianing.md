Hi Jianing,

Great work on the calibration results! ECE=0.003 is impressive — your three-method ensemble (temperature scaling + Platt scaling + isotonic regression) is clearly working very well. The KL=0.003 between your calibration and test sets confirms they're well-matched distributions, which validates that your calibration approach generalizes.

To answer your questions:
- Reliability diagrams: I'd include aggregate plus 2-3 representative pathology classes (highest and lowest calibration). 14 separate diagrams would crowd the paper.
- Paper contribution level: ECE=0.003 on a medical imaging task is strong enough to be a main contribution, especially with the multi-method comparison.

Looking forward to seeing the paper draft!
