**From:** David Okonkwo
**To:** Advisor
**Date:** January 14, 2025, 2:33 PM
**Subject:** Training run failure — NaN loss starting epoch 4

---

Hi,

Sorry to write with a problem instead of good news. My transformer training run is failing with NaN loss starting at epoch 4, and I've been debugging for 8 hours without a fix. Hoping you can point me in the right direction.

**Setup**

- Model: 12-layer transformer encoder (BERT-style), hidden_dim=768, 12 attention heads
- Task: multi-class text classification, 47 classes
- Training data: n=120,000 samples
- Optimizer: AdamW, lr=2e-4, weight_decay=0.01
- Scheduler: linear warmup 500 steps then cosine decay
- Batch size: 32
- Hardware: single A100 40GB

**The problem**

Training was completely stable for the first 3 epochs (loss going from 3.85 → 2.41 → 1.98). Then:

- Epoch 4, step 1: loss = 1.96
- Epoch 4, step 47: loss = 1.94
- Epoch 4, step 48: loss = NaN
- Epoch 4, step 49+: all NaN from here on

The NaN appears suddenly and never recovers. Once it starts, all subsequent batches are NaN.

**Stacktrace (relevant portion):**

```
Traceback (most recent call last):
  File "train.py", line 247, in training_loop
    loss = criterion(logits, labels)
  File "/usr/local/lib/python3.10/dist-packages/torch/nn/modules/loss.py", line 1179, in forward
    return F.cross_entropy(input, target, weight=self.weight, ...)
RuntimeError: Function 'NllLossBackward0' returned nan values in its 0th output.

During backward pass:
  torch/autograd/__init__.py:197: UserWarning: Grad computed invalid (NaN/Inf) for parameter 'encoder.layer.11.attention.self.query.weight' (grad has 12 NaN values out of 589824)
  torch/autograd/__init__.py:197: UserWarning: Grad computed invalid (NaN/Inf) for parameter 'encoder.layer.11.attention.self.key.weight' (grad has 23 NaN values out of 589824)
  torch/autograd/__init__.py:197: UserWarning: Grad computed invalid (NaN/Inf) for parameter 'encoder.layer.11.attention.output.dense.weight' (grad has 8 NaN values out of 589824)
```

**What I've tried**

1. Checked for NaN in input data: no NaN found in any input batch
2. Reduced learning rate to 5e-5: same behavior, NaN still appears at roughly the same point
3. Added gradient clipping (max_norm=1.0): still NaN
4. Reduced batch size to 16: same result
5. Checked that epoch 4 is not using a different data subset than epochs 1-3: confirmed same shuffle seed

**Observations**

The NaN first appears in the last transformer layer (layer 11), specifically in the attention weights. This makes me think it might be an exploding attention issue rather than a data issue. The warmup schedule finished at step 500, and the NaN starts at approximately epoch 4, step 48 — which is around global step 3,648. This is after the warmup, so scheduler issues seem unlikely.

I also noticed that right before the NaN batch, there was a batch where the loss dipped unusually low (1.61, vs typical 1.93-1.97 in that epoch). This might have been a "lucky" batch that pushed gradients to an extreme point.

**Question**

Is this gradient explosion? Should I be using a more aggressive gradient clip (like 0.1 instead of 1.0)? Or is there something else I'm missing? I have a paper deadline in 3 weeks and this is my main experiment.

Thanks,
David
