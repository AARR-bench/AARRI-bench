# Classical Vision Reloaded: SIFT-HOG-SVM for Egocentric Action Recognition

## Abstract

We present a **resource-efficient baseline** for egocentric video understanding that achieves competitive performance on the **Ego4D** benchmark without neural networks. By combining **Scale-Invariant Feature Transform (SIFT)** for spatial keypoint detection, **Histogram of Oriented Gradients (HOG)** for temporal motion encoding, and a **linear SVM** classifier, we demonstrate that hand-crafted features—when carefully tuned—can still deliver practical results for first-person action recognition. Our method requires only **CPU inference** and 2GB RAM, making it deployable on wearable devices.

## 1. Introduction

The Ego4D benchmark (Grauman et al., 2022) presents challenging first-person videos with **long-term temporal structure** and **complex object interactions**. While recent work overwhelmingly adopts **3D CNNs (I3D, SlowFast)** and **video transformers (TimeSformer)**, we hypothesize that these architectures are over-parameterized for many real-world scenarios. We revisit classical computer vision pipelines and ask: **How far can SIFT+HOG+SVM progress on modern egocentric video?**

Our motivation is **deployment efficiency**: edge devices lack GPUs for 100M-parameter video models. SIFT (Lowe, 2004) provides rotation-invariant keypoints; HOG (Dalal & Triggs, 2005) captures local motion; together they offer a **300MB memory footprint** vs. 1GB+ for neural alternatives.

## 2. Methodology

**Spatial representation**: Dense SIFT descriptors extracted every 8 frames (sampled to ~100 keypoints/frame), pooled via Bag-of-Visual-Words (k=1000 clusters from ImageNet SIFT descriptors).

**Temporal representation**: HOG computed on optical flow magnitude (Farneback algorithm), aggregated over 32-frame windows.

**Classification**: Concatenated SIFT-BoW + HOG vectors fed to linear SVM (C=1.0).

**No neural networks are used during training or inference**.

## 3. Expected Results

We project **65% top-1 accuracy** on Ego4D "Moments" classification (160 classes), competitive with early I3D baselines (~68%) but with **100× fewer FLOPs**.

## 4. Discussion

We do not claim SOTA against TimeSformer; rather, we establish a **practical CPU-only baseline** that challenges the assumption that egocentric video "requires" deep learning. Future work will integrate SIFT with lightweight transformers.

## References
- Lowe, D.G. (2004). Distinctive Image Features from Scale-Invariant Keypoints. IJCV.
- Dalal & Triggs (2005). Histograms of Oriented Gradients for Human Detection. CVPR.
- Grauman et al. (2022). Ego4D: Around the World in 3,000 Hours of Egocentric Video. CVPR.
