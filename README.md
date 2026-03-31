# Reconstructing Time-Varying EEG with Local Graphs and ADMM

**A comprehensive approach to EEG signal reconstruction using Local Graph Signal Smoothness and Alternating Direction Method of Multipliers**

[![Course](https://img.shields.io/badge/Course-22MAT220-blue)](.)
[![Institution](https://img.shields.io/badge/Institution-Amrita%20Vishwa%20Vidyapeetham-green)](.)
[![Year](https://img.shields.io/badge/Year-2025-orange)](.)

---

## Team Members

**TEAM - 3**

- **B Sainath Reddy** (CB.SC.U4AIE24309)
- **K Pushpak Siva Sai** (CB.SC.U4AIE24328)
- **P Manohar** (CB.SC.U4AIE24339)
- **P Sai Mrudula** (CB.SC.U4AIE24340)

**Institution**: Amrita Vishwa Vidyapeetham, School of Artificial Intelligence, Coimbatore Campus

**Course**: 22MAT220 Mathematics For Computing

**Academic Year**: 2025

---

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [Methodology](#methodology)
4. [Results and Analysis](#results-and-analysis)
5. [Conclusion](#conclusion)

---

## Abstract

Electroencephalography (EEG) signals capture the brain's electrical activity and play a crucial role in both neuroscience and clinical diagnostics. However, accurately reconstructing EEG signals remains a major challenge due to issues like signal loss and noise interference during data acquisition. This paper leverages the intrinsic structure of EEG signals and proposes an efficient reconstruction method based on **Local Graph Signal Smoothness (LGS)**. 

We first introduce the concept of LGS, which models relationships according to distinct functional regions of the cerebral cortex. Recognizing that an improperly defined graph can weaken reconstruction performance, we further propose a **joint graph learning and EEG signal reconstruction optimization framework**. Since this optimization problem is not jointly convex, we employ the **Alternating Direction Method of Multipliers (ADMM)** to solve it efficiently. 

**Experimental results demonstrate that the proposed LGS-based approach significantly outperforms existing benchmark methods in EEG signal reconstruction. Moreover, our method achieves a higher Signal-to-Noise Ratio (SNR) and a lower Root Mean Square Error (RMSE), confirming its superior reconstruction accuracy and robustness.**

---

## Introduction

The human brain is an incredibly intricate system, and countless studies have been conducted to uncover its inner workings. Among the tools used to study it, electroencephalography (EEG) has proven to be particularly effective, as it records neural activity with excellent temporal precision through a network of electrodes placed across the scalp.

Despite its usefulness, EEG recordings are often contaminated by observational noise—such as electromyographic interference or movement artifacts—and may also suffer from signal loss. These imperfections result in incomplete or noisy data, which can significantly affect signal quality. In medical contexts, degraded EEG signals can lead to inaccurate diagnoses and reduce both the accuracy and efficiency of clinical decision-making. Consequently, **reconstructing reliable EEG signals from partial and corrupted measurements is crucial for preserving the fidelity and diagnostic value of EEG analysis.**

### Classical Reconstruction Approaches

A number of classical reconstruction approaches have been proposed, including:
- **Maximum Likelihood (ML)** method
- **Robust Multichannel Reconstruction (RCLR)**
- **Alternating Direction Method of Multipliers (ADMM)-based** techniques
- **Robust Wavelet Transform (WT)**
- **Myriad filtering**
- **Independent Component Analysis (ICA)**

While these techniques have shown reasonable performance, they tend to overlook the underlying structure and dependencies inherent in EEG data.

### Graph-Based Approaches

To address this limitation, **graph-based approaches** have recently gained popularity in the field of biomedical signal processing. Through the framework of **Graph Signal Processing (GSP)**, it becomes possible to analyze and reconstruct signals by leveraging both local and global correlations encoded in an irregular graph structure.

### Our Contribution

Building upon the successful application of graph learning and GSP in brain mapping, this work proposes a new method for reconstructing **time-varying EEG signals based on Local Graph Signal Smoothness (LGS)**. The method defines LGS according to distinct functional regions of the cerebral cortex and uses ADMM to efficiently solve the resulting non-convex optimization problem.

---

## Methodology

### System Overview

![System Architecture](Figure1.png)

**Figure 1**: The schematic overview of the proposed LSG-based method

### Signal Model

The incomplete EEG signals are modeled as:

```
Y = J ⊙ X* + V
```

Where Y is observed signal, J is sampling operator, X* is true signal, and V is noise.

### Functional Brain Region Decomposition

EEG signals are divided into five regions:
- **Frontal region**: X_F (Motor and cognitive functions)
- **Parietal region**: X_P (Sensory processing)
- **Temporal region**: X_T (Auditory and memory processing)
- **Occipital region**: X_O (Visual processing)
- **Central region**: X_C (Motor and sensory coordination)

### Mathematical Framework

#### Graph Representation

```
G = (V, E, W)
```

- V: vertices (EEG electrodes)
- E: edges between electrodes
- W: adjacency matrix

#### Graph Laplacian

```
L := diag(W1) - W
```

#### Smoothness of Graph Signals

```
f(X) = Tr[(XD)^⊤ L (XD)]
```

Where D is the temporal difference operator.

### Local Graph Signal Smoothness (LGS)

For each region k, learn the graph Laplacian L_k by minimizing:

```
min Tr(Z_k L_k Z_k^⊤) + α||L_k||_F^2, s.t. Tr(L_k) = N_k
```

### Joint Optimization Framework

```
min Tr(Z_k L_k Z_k^⊤) + α||L_k||_F^2 + β||X̃_k||_* + γ||JX̃_k - X̃||_F^2
s.t. Tr(L_k) = N_k
```

**Terms**:
- **Tr(Z_k^⊤ L_k Z_k)**: Graph smoothness
- **α||L_k||_F^2**: Frobenius regularization
- **β||X̃_k||_***: Nuclear norm (low-rank promotion)
- **γ||J ⊙ X̃_k - X̃_k||_F^2**: Data fidelity

### ADMM Solution

Alternates between:
1. **L_k-Subproblem**: Update graph Laplacian matrices
2. **X_k-Subproblem**: Update reconstructed EEG signals
3. **Multiplier Update**: Update Lagrange multipliers

---

## Results and Analysis

### High-Fidelity EEG Signal Reconstruction

![EEG Reconstruction Results](1.jpg)

**Figure 2**: EEG Signal Reconstruction Results for Channels 10, 50, and 100 at 40% data corruption.

The reconstructed signal (red) is virtually indistinguishable from the original signal (blue), demonstrating:
- Accurate signal restoration
- Effective denoising
- Superior interpolation capabilities

### Quantitative Performance Metrics

| Missing Data (%) | RMSE   | NMSE    | SNR (dB) |
|------------------|--------|---------|----------|
| 10               | 0.3630 | 0.01394 | **18.81**|
| 20               | 0.3608 | 0.02753 | 15.78    |
| 30               | 0.3527 | 0.03867 | 14.19    |
| 40               | **0.3396** | 0.04707 | 13.34    |
| 50               | 0.3583 | 0.06581 | 11.90    |
| 60               | 0.3612 | 0.07988 | 11.03    |
| 70               | 0.3560 | 0.09146 | 10.42    |
| 80               | 0.3592 | 0.10643 | 9.84     |
| 90               | 0.3568 | 0.11844 | 9.34     |

**Key Observations**:
- **Lowest RMSE**: 0.340 at 40% missing data
- **Highest SNR**: 18.81 dB at 10% missing data
- **Robust Performance**: SNR of 9.34 dB at 90% missing data
- **Error Stability**: RMSE confined to [0.340, 0.363]

### Comparative Superiority and Validation

![Validation Results](3.jpg)

**Figure 3**: Validation performance comparison between Vectorized ADMM and Baseline Zero-Filling.

**Performance Comparison**:
- **Baseline Method (Zero-Filling)**: RMSE ≈ 1.0
- **Vectorized ADMM**: RMSE ≈ 0.35
- **Error Reduction**: **~65% improvement**

This demonstrates the effectiveness of learned structural constraints.

### Learned Local Graph Topology

![Learned Graph Adjacency Matrices](2.jpg)

**Figure 4**: Learned Local Graph Adjacency Matrices for five brain regions showing sparse topology and concentrated high-weight clusters (yellow).

**Adjacency Matrix Characteristics**:

- **Sparse Topology**: Zero or near-zero weights (dark purple)
- **Concentrated High-Weight Clusters**: Yellow and green regions reveal strong localized channel coupling
- **Regional Insights**: Occipital and Central regions show distinct functional clustering

---

## Key Findings

✓ **Superior Accuracy**: ~65% error reduction vs. baseline

✓ **Robust Performance**: Stable with 90% missing data

✓ **Excellent Signal Quality**: SNR of 9.34 dB at extreme data loss

✓ **Data-Driven Learning**: Identifies meaningful local graph structures

✓ **Anatomically Motivated**: Regional decomposition aligns with brain organization

---

## Conclusion

In this work, we propose a reconstruction method for time-varying EEG signals that leverages **local graph smoothness**. We employ **local graph learning** to capture signal smoothness within distinct functional brain regions.

We introduce a **joint graph learning and EEG signal reconstruction approach** (LGS-based method), solved efficiently using **ADMM**. The algorithm alternates between:
- Updating graph Laplacian matrices
- Reconstructing EEG signals
- Updating Lagrange multipliers

**Experimental results** demonstrate that the **proposed method outperforms existing benchmark techniques** in accurately reconstructing EEG signals.

### Key Advantages

✓ **Anatomically Motivated**: Leverages functional segmentation of cerebral cortex

✓ **Joint Learning**: Simultaneously learns graph structure and reconstructs signals

✓ **Robust**: Maintains performance with extreme data loss

✓ **Efficient**: ADMM provides computationally efficient optimization

✓ **Interpretable**: Learned graph structures provide neuroscience insights

---

## Applications

- **Medical Diagnostics**: Improved EEG signal quality for accurate diagnosis
- **Brain-Computer Interfaces (BCIs)**: Cleaner signal processing
- **Neuroscience Research**: Understanding brain connectivity
- **Clinical Decision-Making**: Enhanced reliability of EEG analysis
- **Artifact Removal**: Effective noise and artifact removal

---

## References

### Key Methodologies

- **Alternating Direction Method of Multipliers (ADMM)**: Efficient distributed optimization
- **Graph Laplacian Learning**: Data-driven discovery of graph structures
- **Low-Rank Matrix Recovery**: Leverages signal redundancy
- **Graph Signal Processing (GSP)**: Analysis on irregular graph-structured domains

---

## License

This project is part of academic research at **Amrita Vishwa Vidyapeetham**.

---

**Last Updated**: March 31, 2025

**Repository**: [EEG-Reconstruction-With-ADMM](https://github.com/Mrudula-itsjuzme/EEG-Reconstruction-With-ADMM)

**Course**: 22MAT220 Mathematics For Computing  
**Institution**: Amrita Vishwa Vidyapeetham  
**Academic Year**: 2025
