# Data Description

Each sample contains:

- RGB image values scaled to `[0, 1]`
- one SAR log-intensity channel, usually between `-18` and `4`
- a domain label indicating source or target region

Dataset profiling note:

- RGB channel means are close to common natural-image preprocessing assumptions.
- SAR log-intensity values are centered near `-8.0` with a rough scale of `4.0`.
- In several failed internal runs, SAR activations became tiny when preprocessing compressed most SAR values into an extreme range.
