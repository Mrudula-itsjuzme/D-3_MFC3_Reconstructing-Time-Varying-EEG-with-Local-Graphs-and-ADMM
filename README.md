# EEG Reconstruction with ADMM

Reconstructing Time-Varying EEG Signals with Local Graphs and Alternating Direction Method of Multipliers

## Overview

This project proposes an efficient method for reconstructing incomplete and noisy EEG (Electroencephalography) signals by leveraging local graph signal smoothness (LGS) and the Alternating Direction Method of Multipliers (ADMM). The approach simultaneously learns graph topology and reconstructs EEG signals across distinct functional regions of the cerebral cortex.

## Problem Statement

EEG signals capture the brain's electrical activity and play a crucial role in neuroscience research and clinical diagnostics. However, accurate EEG signal reconstruction remains challenging due to:

- **Signal Loss**: Incomplete measurements during data acquisition
- **Noise Interference**: Observational noise (e.g., electromagnetic interference, movement artifacts)
- **Data Corruption**: Degraded signals can lead to inaccurate diagnoses and reduced clinical decision-making efficiency

Existing classical reconstruction approaches (ML, RCLR, ADMM-based techniques, Wavelet Transform, Myriad filtering, ICA) tend to overlook the underlying structure and dependencies inherent in EEG data.

## Methodology

### Key Concepts

#### 1. **Local Graph Signal Smoothness (LGS)**
EEG signals are modeled as graphs where:
- **Vertices**: Represent EEG electrode locations
- **Edges**: Encode physiological relationships between brain regions
- **Graph Laplacian**: Captures the signal structure for each region

The approach divides EEG signals into **5 functional regions**:
- **Frontal Region** (X_F)
- **Parietal Region** (X_P)
- **Temporal Region** (X_T)
- **Occipital Region** (X_O)
- **Central Region** (X_C)

Each region is modeled with its own learned local graph and Laplacian matrix.

#### 2. **Joint Optimization Framework**
The problem formulation is:

```
min Tr(Z_k L_k Z_k^T) + α||L_k||_F^2 + β||X̃_k||_* + γ||JX̃_k - X̃||_F^2
s.t. Tr(L_k) = N_k
```

Where:
- **L_k**: Graph Laplacian for region k
- **X̃_k**: Reconstructed EEG signal
- **Z_k**: Normalized signal matrix (X_k ⊙ D)
- **J**: Sampling operator
- **||·||_***: Nuclear norm (promotes low-rank structure)
- **α, β, γ**: Regularization parameters

#### 3. **ADMM Solver**
Since the optimization problem is non-convex in both L_k and X̃_k, the ADMM algorithm alternates between:
- **L_k-subproblem**: Update graph Laplacian matrices
- **X_k-subproblem**: Update reconstructed EEG signals
- **Multiplier Updates**: Update Lagrange multipliers

The algorithm iterates until convergence, efficiently solving the coupled optimization problem.

### Signal Model

The observed EEG signal is modeled as:
```
X = J ⊙ X* + V
```

Where:
- **X**: Observed noisy/incomplete signal
- **X***: True underlying signal
- **J**: Sampling operator (binary mask for missing data)
- **V**: Additive Gaussian noise

## Results and Analysis

### Performance Metrics
The proposed LGS-based approach demonstrates:
- **Higher Signal-to-Noise Ratio (SNR)** compared to benchmark methods
- **Lower Root Mean Square Error (RMSE)**
- **Superior reconstruction accuracy and robustness**

### Key Advantages
1. **Anatomically Motivated**: Leverages functional segmentation of the cerebral cortex
2. **Joint Learning**: Simultaneously learns graph structure and reconstructs signals
3. **Region-Specific**: Captures localized correlations within brain regions
4. **Efficient Solving**: ADMM provides computationally efficient optimization

## Technical Highlights

### Notations
- **A, a**: Matrix and vector
- **vec(A)**: Vectorized form
- **||A||_F**: Frobenius norm
- **||A||_***: Nuclear norm
- **A ⊙ B**: Hadamard (element-wise) product
- **D**: Temporal difference operator

### Graph Laplacian Properties
The graph Laplacian L satisfies:
- **Symmetry**: L = L^T
- **Zero row-sum**: L1 = 0
- **Non-negativity**: L_ij ≥ 0 for i ≠ j

### ADMM Subproblems

#### L_k-Subproblem
Solves for the graph Laplacian while keeping X̃_k fixed, using the augmented Lagrangian approach.

#### X_k-Subproblem
Updates the reconstructed signal while keeping L_k fixed, with solutions derived through matrix vectorization and standard linear algebra.

#### Parameter Update
Updates Lagrange multipliers and penalty factors for convergence.

## Implementation Details

### Vectorization Strategy
To efficiently handle the optimization:
- Only upper-triangular and diagonal elements of symmetric Laplacians are learned
- Matrix problems are converted to vector form for computational efficiency
- Exploitation of matrix structure (symmetry, sparsity) for faster computation

### Convergence Criteria
The algorithm converges when:
- Primal residuals fall below threshold
- Dual residuals fall below threshold
- Relative tolerance conditions are satisfied

## Applications

- **Medical Diagnostics**: Improved EEG signal quality for accurate diagnosis
- **Brain-Computer Interfaces (BCIs)**: Cleaner signal processing
- **Neuroscience Research**: Better understanding of brain connectivity
- **Clinical Decision-Making**: Enhanced reliability of EEG analysis

## Authors

- **BSainath Reddy** (CB.SC.U4AIE24309)
- **KPushpak Siva Sai** (CB.SC.U4AIE24328)
- **PManohar** (CB.SC.U4AIE24339)
- **PSai Mrudula** (CB.SC.U4AIE24340)

**Institution**: Amrita Vishwa Vidyapeetham, School of Artificial Intelligence, Coimbatore Campus

**Course**: 22MAT220 Mathematics For Computing

**Academic Year**: 2025

## Related Work

The project builds upon successful applications of:
- Graph Signal Processing (GSP) in EEG analysis
- Laplacian-based denoising algorithms
- Electrical brain source reconstruction
- Graph learning techniques in biomedical signal processing

## References

Key methodologies:
- **Graph Signal Processing (GSP)**: Analyzes and reconstructs signals leveraging local and global correlations
- **Alternating Direction Method of Multipliers (ADMM)**: Efficient distributed optimization algorithm
- **Graph Laplacian Learning**: Data-driven discovery of graph structures from observations
- **Low-Rank Matrix Recovery**: Exploits redundancy in signals from same underlying structure

## Future Work

- Validation on larger clinical EEG datasets
- Extension to multi-subject studies
- Real-time implementation for clinical systems
- Comparison with deep learning-based reconstruction methods
- Analysis of learned graph topologies for neuroscience insights

## License

This project is part of academic research at Amrita Vishwa Vidyapeetham.

---

**Last Updated**: 2025

For questions or collaborations, please reach out to the authors.
