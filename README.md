# EEG Reconstruction with ADMM

**Reconstructing Time-Varying EEG Signals with Local Graphs and Alternating Direction Method of Multipliers**

[![Course](https://img.shields.io/badge/Course-22MAT220-blue)](.)
[![Institution](https://img.shields.io/badge/Institution-Amrita%20Vishwa%20Vidyapeetham-green)](.)
[![Year](https://img.shields.io/badge/Year-2025-orange)](.)

## Overview

This project proposes an efficient method for reconstructing incomplete and noisy EEG (Electroencephalography) signals by leveraging **Local Graph Signal Smoothness (LGS)** and the **Alternating Direction Method of Multipliers (ADMM)**. The approach simultaneously learns graph topology and reconstructs EEG signals across distinct functional regions of the cerebral cortex, achieving superior reconstruction accuracy and robustness.

**Key Achievement**: ~65% reduction in reconstruction error compared to baseline methods, with SNR of 9.34 dB at 90% missing data.

## Problem Statement

EEG signals capture the brain's electrical activity and play a crucial role in neuroscience research and clinical diagnostics. However, accurate EEG signal reconstruction remains challenging due to:

- **Signal Loss**: Incomplete measurements during data acquisition
- **Noise Interference**: Observational noise (electromagnetic interference, movement artifacts)
- **Data Corruption**: Degraded signals lead to inaccurate diagnoses and reduced clinical efficiency

Existing classical reconstruction approaches (ML, RCLR, ADMM-based techniques, Wavelet Transform, Myriad filtering, ICA) overlook the underlying structure and dependencies inherent in EEG data.

## System Architecture

![EEG Reconstruction Pipeline](Figure1.png)

The proposed LGS-based method follows this pipeline:

1. **EEG Recording**: N electrodes capture brain activity
2. **Observation Model**: Noisy/incomplete signal Y = J ⊙ X* + V
3. **Regional Decomposition**: Signals divided into 5 functional brain regions
4. **Graph Learning**: Learn local graph topology for each region (G_F, G_P, G_T, G_O, G_C)
5. **Joint Optimization**: Simultaneously reconstruct signals and learn graph structures
6. **Signal Integration**: Combine regional reconstructions into complete EEG signal

## Methodology

### Key Concepts

#### 1. **Local Graph Signal Smoothness (LGS)**

EEG signals are modeled as graphs where:
- **Vertices**: Represent EEG electrode locations (N electrodes)
- **Edges**: Encode physiological relationships between brain regions
- **Graph Laplacian (L)**: Captures the signal structure for each region

The method divides EEG signals into **5 functional brain regions**:
- **Frontal Region** (X_F) - Motor and cognitive functions
- **Parietal Region** (X_P) - Sensory processing
- **Temporal Region** (X_T) - Auditory and memory processing
- **Occipital Region** (X_O) - Visual processing
- **Central Region** (X_C) - Motor and sensory coordination

Each region is modeled with its own learned local graph and Laplacian matrix (L_F, L_P, L_T, L_O, L_C).

#### 2. **Joint Optimization Framework**

The optimization problem formulation:

```
min Tr(Z_k L_k Z_k^T) + α||L_k||_F^2 + β||X̃_k||_* + γ||JX̃_k - X̃||_F^2
s.t. Tr(L_k) = N_k
```

**Terms and their significance:**

- **Tr(Z_k L_k Z_k^T)**: Graph smoothness term - ensures connected nodes have similar signal values
- **α||L_k||_F^2**: Frobenius norm regularization - controls Laplacian magnitude and numerical stability
- **β||X̃_k||_***: Nuclear norm - promotes low-rank structure in reconstructed signals
- **γ||JX̃_k - X̃||_F^2**: Data fidelity term - ensures reconstruction fidelity to observations
- **Tr(L_k) = N_k**: Normalization constraint - prevents degenerate solutions

**Parameters:**
- **L_k**: Graph Laplacian for region k
- **X̃_k**: Reconstructed EEG signal
- **Z_k = X_k ⊙ D**: Normalized signal matrix (temporal differences)
- **J**: Sampling operator (binary mask for missing data)
- **D**: Temporal difference operator
- **α, β, γ**: Regularization parameters

#### 3. **ADMM Solver**

Since the optimization problem is **non-convex** in both L_k and X̃_k, the ADMM algorithm alternates between:

**L_k-Subproblem**: Update graph Laplacian matrices
- Solves for L_k while keeping X̃_k fixed
- Uses augmented Lagrangian approach
- Enforces symmetry, zero row-sum, and non-negativity constraints

**X_k-Subproblem**: Update reconstructed EEG signals
- Updates X̃_k while keeping L_k fixed
- Uses matrix vectorization for computational efficiency
- Incorporates soft-thresholding for nuclear norm

**Multiplier Update**: Update Lagrange multipliers for constraint enforcement
- Adjusts dual variables for convergence

The algorithm iterates until convergence criteria are satisfied.

### Signal Model

The observed EEG signal is:
```
X = J ⊙ X* + V
```

Where:
- **X**: Observed noisy/incomplete signal
- **X***: True underlying signal
- **J**: Sampling operator (1 for observed, 0 for missing)
- **V**: Additive Gaussian noise
- **⊙**: Hadamard (element-wise) product

## Results and Analysis

### High-Fidelity Signal Reconstruction

Visual assessment confirms the model's ability to accurately restore EEG signal fidelity. At 40% random data corruption, the reconstructed signal (red) aligns nearly perfectly with the original signal (blue) across all channels.

**Key Observations:**
- Reconstructed signal virtually indistinguishable from original
- Effective denoising through GCTV regularization
- Successfully interpolates between scattered observed samples
- Clean estimates that track original signal behavior

### Quantitative Performance Metrics

| Missing Data (%) | RMSE   | NMSE    | SNR (dB) |
|------------------|--------|---------|----------|
| 10               | 0.3630 | 0.01394 | 18.81    |
| 20               | 0.3608 | 0.02753 | 15.78    |
| 30               | 0.3527 | 0.03867 | 14.19    |
| 40               | 0.3396 | 0.04707 | 13.34    |
| 50               | 0.3583 | 0.06581 | 11.90    |
| 60               | 0.3612 | 0.07988 | 11.03    |
| 70               | 0.3560 | 0.09146 | 10.42    |
| 80               | 0.3592 | 0.10643 | 9.84     |
| 90               | 0.3568 | 0.11844 | **9.34** |

**Performance Highlights:**
- **Lowest RMSE**: 0.340 at 40% missing data
- **Highest SNR**: 18.81 dB at 10% missing data
- **Robust Performance**: Maintains SNR of 9.34 dB even at 90% data loss
- **Error Stability**: RMSE confined to [0.340, 0.363] across all missing percentages

### Comparative Superiority

**Vectorized ADMM vs. Zero-Filling Baseline:**
- **ADMM RMSE**: ~0.35 across all missing percentages
- **Baseline RMSE**: ~1.0 across all missing percentages
- **Error Reduction**: **~65% improvement** over baseline method
- **Key Insight**: Learned structural constraints are critical for successful reconstruction

### Learned Graph Topology Insights

The ADMM's L-subproblem learns the graph Laplacian that best describes spatial connectivity within each brain region.

**Adjacency Matrix Characteristics (Fig. 2):**
- **Sparse topology**: Dominated by zero or near-zero weights (dark regions)
- **Concentrated clusters**: High-magnitude weights (yellow/green) reveal localized channel coupling
- **Regional insights**: 
  - Occipital region shows distinct, large clustering
  - Central region displays tightly knit functional groups
  - Sparse structure prevents overfitting and identifies significant edges

**Neuroscience Implications:**
- Data-driven identification of non-trivial connectivity patterns
- Captures intrinsic electrophysiological relationships between adjacent channels
- Validates anatomically-motivated regional decomposition

## Technical Highlights

### Vectorization Strategy

To efficiently handle the optimization:
- Only upper-triangular and diagonal elements of symmetric Laplacians are learned
- Matrix problems converted to vector form for computational efficiency
- Exploitation of matrix structure (symmetry, sparsity) for faster computation

### Vectorized Variables

| Vector | Description | Dimension |
|--------|-------------|-----------|
| uL_k   | Upper-triangular part of L_k | N_k(N_k-1)/2 × 1 |
| dL_k   | Diagonal of L_k | N_k × 1 |
| ẑ_k    | Upper-triangular part of Ẑ_k Ẑ_k^T | N_k(N_k-1)/2 × 1 |
| dẐ_k   | Diagonal of Ẑ_k Ẑ_k^T | N_k × 1 |
| ĝ_k    | Vectorized reconstructed signal Ẋ_k | N_k T × 1 |
| p_k    | Vectorized auxiliary variable P_k | N_k T × 1 |

### Convergence Criteria

The algorithm converges when:
- Primal residuals fall below threshold: ||Ax - b|| < ε_pri
- Dual residuals fall below threshold: ||A^T λ|| < ε_dual
- Relative tolerance conditions satisfied

### Graph Laplacian Properties

The graph Laplacian L satisfies:
- **Symmetry**: L = L^T
- **Zero row-sum**: L1 = 0 (where 1 is all-ones vector)
- **Non-negativity**: L_ij ≥ 0 for i ≠ j
- **Trace Constraint**: Tr(L) = N (normalization)

## Implementation Details

### Algorithm Overview

```
ADMM Algorithm for Joint EEG Reconstruction and Graph Learning:

Initialize: L_k^(0), X̃_k^(0), Λ^(0), ρ > 0
while not converged:
    # L_k-subproblem: Update Laplacian
    L_k^(c+1) ← argmin Tr(Z_k L_k Z_k^T) + α||L_k||_F^2
                + augmented_lagrangian_terms
    
    # X_k-subproblem: Update reconstructed signal
    X̃_k^(c+1) ← argmin β||X̃_k||_* + γ||JX̃_k - X_k||_F^2
                 + augmented_lagrangian_terms
    
    # Update dual variables
    Λ^(c+1) ← Λ^(c) + ρ(primal_residual)
    
    # Check convergence
    c ← c + 1
```

### Key Implementation Features

1. **Sparse Matrix Operations**: Efficient handling of sparse Laplacian and adjacency matrices
2. **Soft-Thresholding**: Nuclear norm minimization via iterative soft-thresholding
3. **Matrix Vectorization**: Vector-form updates for computational speed
4. **Constraint Handling**: Projection onto Laplacian constraint set
5. **Numerical Stability**: Regularization prevents ill-conditioning

## Applications

- **Medical Diagnostics**: Improved EEG signal quality for accurate diagnosis of epilepsy, sleep disorders, and neurological conditions
- **Brain-Computer Interfaces (BCIs)**: Cleaner signal processing for more reliable BCI systems
- **Neuroscience Research**: Better understanding of brain connectivity and functional organization
- **Clinical Decision-Making**: Enhanced reliability of EEG analysis in clinical settings
- **Artifact Removal**: Effective removal of noise and artifacts while preserving genuine neural activity

## Authors

**Team - 3**

- **B Sainath Reddy** (CB.SC.U4AIE24309)
- **K Pushpak Siva Sai** (CB.SC.U4AIE24328)
- **P Manohar** (CB.SC.U4AIE24339)
- **P Sai Mrudula** (CB.SC.U4AIE24340)

**Institution**: Amrita Vishwa Vidyapeetham, School of Artificial Intelligence, Coimbatore Campus

**Course**: 22MAT220 Mathematics For Computing

**Academic Year**: 2025

## Related Work

The project builds upon successful applications of:
- **Graph Signal Processing (GSP)**: Analyzes and reconstructs signals leveraging local and global correlations in irregular graph structures
- **Laplacian-based Denoising**: Exploits graph structure for noise suppression
- **Electrical Brain Source Reconstruction**: Anatomically-motivated signal processing
- **Graph Learning**: Data-driven discovery of graph structures from observations
- **Low-Rank Matrix Recovery**: Exploits signal redundancy from underlying structure

## Key References

**Methodologies:**
- **Alternating Direction Method of Multipliers (ADMM)**: Efficient distributed optimization algorithm for convex and non-convex problems
- **Graph Laplacian Learning**: Data-driven discovery and optimization of graph structures
- **Low-Rank Matrix Recovery**: Leverages redundancy in signals from same underlying structure
- **Graph Signal Processing (GSP)**: Analyzes signals on irregular graph-structured domains
- **Regional Graph Decomposition**: Anatomically-motivated functional segmentation

## Future Work

- **Clinical Validation**: Validation on larger clinical EEG datasets from diverse patient populations
- **Multi-Subject Studies**: Extension to multi-subject studies for group-level analysis
- **Real-Time Implementation**: Optimization for real-time clinical systems
- **Deep Learning Comparison**: Comparison with deep learning-based reconstruction methods
- **Graph Topology Analysis**: In-depth analysis of learned graph topologies for neuroscience insights
- **Artifact-Specific Handling**: Specialized handling for different types of artifacts
- **Adaptive Parameters**: Automatic regularization parameter tuning
- **Scalability**: Extension to high-density electrode arrays

## Limitations and Challenges

- Non-convex optimization problem requires careful initialization
- Computational complexity increases with number of channels and time samples
- Regularization parameters require careful tuning
- Graph learning effectiveness depends on signal characteristics
- Method assumes regional independence (can be extended for global constraints)

## License

This project is part of academic research at Amrita Vishwa Vidyapeetham.

---

**Last Updated**: 2025

For questions, collaborations, or technical inquiries, please reach out to the authors.

**Repository**: [EEG-Reconstruction-With-ADMM](https://github.com/Mrudula-itsjuzme/EEG-Reconstruction-With-ADMM)
