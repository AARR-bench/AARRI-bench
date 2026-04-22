#!/bin/bash

cat > /app/proposal.txt << 'EOF'
# Long-Form Video Generation: Feasible Research Proposal

## Problem Understanding

The core bottleneck in long-form video generation is the spatio-temporal attention mechanism in 3D diffusion models. When processing long frame sequences (e.g., 1+ minute at 24fps), the attention computation exhibits quadratic complexity in sequence length, causing VRAM to grow exponentially. With only 96GB total VRAM across 4x RTX 4090 GPUs, even a single batch of long sequences with attention mechanisms would require prohibitive memory—far exceeding our hardware capacity.

Additionally, maintaining temporal consistency across such long sequences is extremely challenging, as the model must learn coherent motion and scene dynamics over extended time horizons.

## Proposed Solution: Autoregressive Temporal LoRA with Sliding Window

### Core Idea

Rather than attempting to process the entire 1+ minute sequence at once, we propose a **modular, autoregressive approach** that leverages existing short-form video models:

1. **Freeze the backbone**: Use pre-trained SVD (Stable Video Diffusion) or AnimateDiff as a frozen feature extractor and decoder. These models are optimized for 16-25 frame generation and require only 6-8GB VRAM.

2. **Train lightweight Temporal LoRA**: Introduce a low-rank adapter module that learns temporal dynamics in the latent space. LoRA modules are extremely parameter-efficient (typically <1% of model parameters), requiring minimal VRAM for training.

3. **Autoregressive generation with sliding window**: Generate video in overlapping chunks:
   - Generate frames 0-24 using SVD + LoRA
   - Use frame 24 as the conditioning frame for the next chunk (frames 12-36)
   - Repeat with 50% overlap to ensure smooth transitions
   - Blend overlapping regions using simple cross-fade or learned blending

4. **Optional: Keyframe + Interpolation pipeline**: For even lower compute:
   - Train a sparse keyframe generator (e.g., 8 keyframes per 60 seconds)
   - Use RIFE or FILM (2-3GB VRAM each) to interpolate intermediate frames
   - This reduces training burden to only ~10% of frames

### Technical Feasibility

**Implementation Steps:**

1. **Phase 1 (Month 1-2)**:
   - Implement LoRA adapter for SVD's temporal layers
   - Create sliding window inference pipeline
   - Collect ~100 hours of short video clips for training

2. **Phase 2 (Month 2-4)**:
   - Train Temporal LoRA on collected data (batch size 2, ~50 hours training on 4x 4090)
   - Implement smooth blending between chunks
   - Evaluate temporal consistency metrics (optical flow, LPIPS)

3. **Phase 3 (Month 4-6)**:
   - Optimize inference speed and memory usage
   - Experiment with keyframe + interpolation variant
   - Benchmark against baselines

**Resource Requirements:**

- **VRAM**: ~12GB per GPU during training (SVD 8GB + LoRA 2GB + overhead 2GB) → fits comfortably on 4x 24GB GPUs
- **Storage**: ~500GB for training data + 100GB for model checkpoints = 600GB total (well within 1.8TB available)
- **Training time**: ~50-100 hours on 4x 4090 (feasible within 6 months)
- **Inference**: ~2-3 seconds per 24-frame chunk on single GPU

**Existing Components Reused:**
- SVD or AnimateDiff (frozen backbone)
- RIFE/FILM for optional interpolation
- Standard PyTorch LoRA implementations

**New Components to Develop:**
- Temporal LoRA adapter module (~500 lines of code)
- Sliding window inference pipeline (~300 lines)
- Blending/transition logic (~200 lines)

### Expected Outcomes

**Success Metrics:**

1. **Temporal Consistency**: Measure optical flow magnitude between consecutive frames (target: <2 pixels/frame)
2. **Visual Quality**: LPIPS score on interpolated frames (target: <0.15)
3. **Length**: Successfully generate 60+ second videos without visible artifacts
4. **Efficiency**: Inference speed >10 fps on single GPU

**Deliverables:**
- Trained Temporal LoRA checkpoint
- Open-source inference code
- Benchmark results on standard video datasets
- Ablation studies on window size, overlap, and blending strategies

### Why This Approach Works

1. **Respects constraints**: Uses only 12GB VRAM during training, fits within 2TB storage
2. **Leverages existing work**: Reuses proven short-form models rather than building entirely new architectures
3. **Realistic timeline**: Focused scope achievable in 3-6 months
4. **Modular design**: Each component (LoRA, sliding window, interpolation) can be developed and tested independently
5. **Scalable**: Can be extended with better backbones or more sophisticated blending as resources allow

This approach trades off some theoretical elegance (full end-to-end 3D attention) for practical feasibility, which is the hallmark of good research under constraints.
EOF
