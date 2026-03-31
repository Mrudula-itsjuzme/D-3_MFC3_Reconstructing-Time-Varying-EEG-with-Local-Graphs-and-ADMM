# Reconstructing Time-Varying EEG with Local Graphs and ADMM

[![Course](https://img.shields.io/badge/Course-22MAT220-blue)](.)
[![Institution](https://img.shields.io/badge/Amrita%20Vishwa%20Vidyapeetham-AI-green)](.)
[![Year](https://img.shields.io/badge/Year-2025-orange)](.)

## Team

- **B Sainath Reddy** (CB.SC.U4AIE24309)
- **K Pushpak Siva Sai** (CB.SC.U4AIE24328)
- **P Manohar** (CB.SC.U4AIE24339)
- **P Sai Mrudula** (CB.SC.U4AIE24340)

**Amrita Vishwa Vidyapeetham** | School of Artificial Intelligence | 2025

---

## Abstract

Electroencephalography (EEG) signals capture brain electrical activity crucial for neuroscience and clinical diagnostics. However, accurate reconstruction remains challenging due to signal loss and noise interference. This paper proposes an efficient reconstruction method using **Local Graph Signal Smoothness (LGS)** and **Alternating Direction Method of Multipliers (ADMM)**. We introduce LGS modeling relationships across distinct functional brain regions and propose joint graph learning and signal reconstruction. Experimental results show **superior performance: ~65% error reduction, SNR of 9.34 dB at 90% missing data**.

---

## Introduction

EEG recordings are contaminated by noise (electromyographic interference, movement artifacts) and signal loss, resulting in incomplete data affecting clinical decision-making. Classical approaches (ML, RCLR, WT, ICA) overlook inherent EEG structure and dependencies.

**Graph-based approaches** leverage Graph Signal Processing (GSP) to model EEG relationships through graphs where electrodes are vertices and edges represent physiological connections. This work proposes **Local Graph Signal Smoothness (LGS)** for region-specific reconstruction across functional brain areas (Frontal, Parietal, Temporal, Occipital, Central) using ADMM for efficient non-convex optimization.

---

## System Overview

![System Architecture](images/Figure1.png)

**Figure 1**: LSG-based method pipeline

### Signal Model

```
Y = J ⊙ X* + V
```

- **Y**: Observed signal | **J**: Sampling operator | **X***: True signal | **V**: Noise

### Brain Regions

- **Frontal** (X_F): Motor & cognitive
- **Parietal** (X_P): Sensory processing
- **Temporal** (X_T): Auditory & memory
- **Occipital** (X_O): Visual processing
- **Central** (X_C): Motor & sensory coordination

---

## Methodology

### Graph Representation

```
G = (V, E, W)
```

- **V**: Vertices (N electrodes)
- **E**: Edges between electrodes
- **W**: Adjacency matrix (edge weights)

### Graph Laplacian

```
L := diag(W1) - W
```

### Signal Smoothness

```
f(X) = Tr[(XD)^⊤ L (XD)]
```

Where D is the temporal difference operator.

### Local Graph Signal Smoothness

For each region k:

```
min Tr(Z_k L_k Z_k^⊤) + α||L_k||_F^2,  s.t. Tr(L_k) = N_k
```

### Joint Optimization

```
min Tr(Z_k L_k Z_k^⊤) + α||L_k||_F^2 + β||X̃_k||_* + γ||JX̃_k - X||_F^2
s.t. Tr(L_k) = N_k
```

**Terms:**
- **Tr(Z_k^⊤ L_k Z_k)**: Graph smoothness
- **α||L_k||_F^2**: Frobenius regularization
- **β||X̃_k||_***: Nuclear norm (low-rank)
- **γ||JX̃_k - X||_F^2**: Data fidelity

### ADMM Algorithm

Alternates between:
1. **L_k-Subproblem**: Update graph Laplacian
2. **X_k-Subproblem**: Update reconstructed signals
3. **Multiplier Update**: Enforce constraints

Vectorizes only upper-triangular and diagonal elements for efficiency.

---

## Results

### High-Fidelity Reconstruction

![EEG Reconstruction](images/1.jpg)

**Figure 2**: Signal reconstruction at 40% data corruption

### Performance Metrics

| Missing (%) | RMSE   | NMSE    | SNR (dB) |
|-------------|--------|---------|----------|
| 10          | 0.3630 | 0.01394 | 18.81    |
| 20          | 0.3608 | 0.02753 | 15.78    |
| 30          | 0.3527 | 0.03867 | 14.19    |
| 40          | **0.3396** | 0.04707 | 13.34 |
| 50          | 0.3583 | 0.06581 | 11.90    |
| 60          | 0.3612 | 0.07988 | 11.03    |
| 70          | 0.3560 | 0.09146 | 10.42    |
| 80          | 0.3592 | 0.10643 | 9.84     |
| 90          | 0.3568 | 0.11844 | 9.34     |

**Key Results:**
- Lowest RMSE: 0.340 (40% missing)
- Highest SNR: 18.81 dB (10% missing)
- Robust at 90% missing: 9.34 dB SNR

### Validation Comparison

![Validation](images/3.jpg)

**Figure 3**: ADMM vs. Baseline (Zero-Filling)

- **ADMM RMSE**: ~0.35
- **Baseline RMSE**: ~1.0
- **Improvement**: **~65% error reduction**

### Learned Graph Topology

![Graph Matrices](images/2.jpg)

**Figure 4**: Learned adjacency matrices for five brain regions

**Characteristics:**
- Sparse topology (dark regions)
- High-weight clusters (yellow) = strong coupling
- Occipital & Central regions show distinct clustering

---

## Key Findings

✓ ~65% error reduction vs. baseline  
✓ Stable performance at 90% missing data  
✓ SNR of 9.34 dB at extreme data loss  
✓ Data-driven graph learning captures brain organization  
✓ Joint optimization outperforms fixed graphs  

---

## Conclusion

We propose an LGS-based method for time-varying EEG reconstruction leveraging local graph smoothness across functional brain regions. The joint graph learning and signal reconstruction framework, solved via ADMM, outperforms existing benchmarks with superior accuracy and robustness.

**Advantages:**
- Anatomically motivated regional decomposition
- Simultaneous graph learning and reconstruction
- Robust to extreme data loss
- Computationally efficient
- Interpretable results

---

## Applications

- Medical diagnostics (epilepsy, sleep disorders)
- Brain-computer interfaces
- Neuroscience research
- Clinical decision-making
- Artifact removal

---

## References

- **ADMM**: Efficient distributed optimization
- **Graph Laplacian Learning**: Data-driven structure discovery
- **Low-Rank Recovery**: Signal redundancy exploitation
- **Graph Signal Processing**: Analysis on irregular domains

---

## License

Academic research at Amrita Vishwa Vidyapeetham

**Last Updated**: March 31, 2025  
**Repository**: [EEG-Reconstruction-With-ADMM](https://github.com/Mrudula-itsjuzme/EEG-Reconstruction-With-ADMM)
