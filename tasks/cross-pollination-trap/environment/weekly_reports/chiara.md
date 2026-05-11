**Weekly Report — Chiara Rossi**
**Week 7 | Large-Scale Distributed Training**

---

**Summary of Progress**

Successfully scaled from 8 to 32 GPUs after fixing a critical gradient accumulation bug. Training is now stable and generalization performance matches the 8-GPU baseline.

**The Bug: Gradient Accumulation Must Scale with GPU Count**

When I moved from 8 to 32 GPUs, I kept accumulation_steps = 8. This silently quadrupled the effective batch size (from 256 to 1024 samples per step), causing the model to converge to a worse solution — generalization dropped 4.2 points on the held-out evaluation set.

The fix: at 32 GPUs, I set accumulation_steps = 2 to maintain the same effective batch size of 32 × 4 × 2 = 256 samples. After this fix, training dynamics matched the 8-GPU baseline exactly.

**The Rule**

When scaling GPU count by a factor K, scale accumulation_steps down by K (or equivalently, scale batch_size_per_GPU down by K). This keeps effective batch size constant. Failing to do this is a silent, hard-to-detect error — the model trains to completion but generalizes worse.

I've mentioned this to Hanyu, who is planning a 32-GPU run next week. He said he'd check his configuration before running.

**Communication Overhead**

AllReduce communication takes 23% of step time at 32 GPUs. Not a bottleneck yet but will be at 64 GPUs.

**Open Questions**

- Is gradient compression worth implementing for the 64-GPU scale?
- Does accumulation_steps scaling interact with learning rate warmup schedules?
