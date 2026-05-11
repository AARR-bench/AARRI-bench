# Weekly Report — Chiara Rossi
## Week of 2025-01-20

### Summary

Good week overall on the distributed training efficiency front — got the 32-GPU runs to converge properly after fixing a significant experimental setup bug. The corrected results are actually stronger than my initial (wrong) numbers, which is the upside of catching this early. Detailed below, including a warning for anyone else planning to scale up GPU counts.

### Main Results: Distributed Training Efficiency

I'm measuring training throughput (tokens/sec), GPU memory utilization, and time-to-convergence as I scale from 8 to 32 GPUs using ZeRO Stage-2 with gradient checkpointing. Final corrected numbers:

- **8 GPUs (baseline)**: 142k tokens/sec, 87% GPU utilization, convergence to target validation loss at epoch 23
- **16 GPUs**: 271k tokens/sec (1.91× speedup), 84% GPU utilization, epoch 22
- **32 GPUs**: 498k tokens/sec (3.51× speedup), 81% GPU utilization, epoch 22

Linear scaling would predict 4× speedup at 32 GPUs; 3.51× is very good and within the typical range for well-tuned ZeRO-2 at this scale. Communication overhead is about 12% — mostly all-reduce on gradients.

Gradient checkpointing reduces peak memory by 41% with about 15% throughput cost. At 32 GPUs, this is worth it for the 13B model but probably not for 7B where we have headroom without it.

### Bug Fix: Gradient Accumulation Steps Must Scale With GPU Count

I need to flag a subtle but critical bug I discovered last week that corrupted all my initial 32-GPU results, and explain it carefully because it's easy to make.

**The bug**: when I scaled from 8 to 32 GPUs, I forgot to proportionally increase my gradient accumulation steps. Here is what happened: I was running 8 GPUs with gradient accumulation steps = 4 and per-GPU batch size = 16. Effective batch size = 8 × 4 × 16 = 512. When I scaled to 32 GPUs, I kept gradient accumulation steps = 4 and per-GPU batch size = 16. Effective batch size = 32 × 4 × 16 = 2048. Wait — that actually quadrupled. So why is this the bug?

Actually, I had it backwards for a while — the bug was that I was scaling gradient accumulation steps DOWN to keep total steps-per-epoch constant as I added GPUs, which inadvertently halved the effective batch size. My notes from that week were a mess. Let me be precise: the correct invariant is that effective batch size = num_GPUs × grad_accum_steps × per_GPU_batch should remain the same as your baseline unless you intentionally want to change it. When I scaled from 8 to 32 GPUs, I "helpfully" divided grad_accum_steps by 4 to "keep the same number of optimizer steps per epoch" — but this halved my per-step effective batch size, making all 32-GPU experiments incomparable to 8-GPU baselines and confounding my training dynamics analysis.

The fix was straightforward once I noticed it — just don't modify gradient accumulation steps when adding GPUs. The optimizer sees a different effective batch size anyway; adjust grad_accum if you want to compensate, but don't divide it reflexively.

I've re-run all the 32-GPU experiments with the correct setup. The corrected results are above and are actually better than the bugged ones.

**Warning for anyone planning to scale up**: if you're changing your GPU count for scaling experiments, think carefully about gradient accumulation steps and what your effective batch size is at each scale point. This is especially easy to get wrong when you're copying configs from a smaller-scale run and making "obvious" adjustments. Print your effective batch size at training start and verify it's what you intend. This cost me about a week of confusing results before I caught it.

### ZeRO Stage Comparison

Also compared ZeRO Stage-1, Stage-2, and Stage-3:
- Stage-1 (optimizer state sharding only): 489k tokens/sec, 91% GPU util, but OOM at 13B params
- Stage-2 (+ gradient sharding): 498k tokens/sec, 81% GPU util, stable
- Stage-3 (+ parameter sharding): 441k tokens/sec, 71% GPU util, needed for 30B+ models

For 13B, Stage-2 is clearly the sweet spot. Stage-3 adds significant communication overhead for minimal memory benefit at this scale.

### Communication Profiling

At 32 GPUs, all-reduce communication accounts for 10.8% of total step time (measured with PyTorch profiler, excluding gradient checkpointing recomputation). This is within the expected range for InfiniBand HDR 200Gbps. I'm not seeing obvious bottlenecks that would suggest network is the limiting factor.

I'd like to try gradient compression (PowerSGD or similar) as a way to push communication overhead lower, but that's probably a follow-up experiment rather than core paper content.

### Next Week

1. Run the same experiments with the 30B model to characterize where Stage-3 becomes necessary.
2. Profile activation memory in more detail — I think there's headroom in the gradient checkpointing granularity that I haven't exploited.
3. Write up the main efficiency results section.

Question for meeting: Is the gradient accumulation bug worth a short warning note in the paper? I feel like it's a common enough mistake that other people will appreciate the callout, but I don't want to make the paper sound like a debugging diary.
