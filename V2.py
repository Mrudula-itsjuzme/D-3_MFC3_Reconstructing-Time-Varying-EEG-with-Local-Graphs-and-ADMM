import numpy as np
from pathlib import Path
import os

# --------------------
# 1. Safe loading of .raw EEG file with trimming excess samples
# --------------------
def load_eeg_file_trim(filepath, n_channels=128):
    data = np.fromfile(filepath, dtype=np.float32)
    n_samples = data.size // n_channels
    data = data[:n_channels * n_samples]  # trim extra stray samples if any
    return data.reshape((n_channels, n_samples))

# ----------------------------
# 2. Partition electrodes into brain regions (replace with your exact indices)
# ----------------------------
frontal   = list(range(0, 26))
central   = list(range(26, 54))
parietal  = list(range(54, 71))
temporal  = list(range(71, 99))
occipital = list(range(99, 128))

region_map = {
    'frontal': frontal,
    'central': central,
    'parietal': parietal,
    'temporal': temporal,
    'occipital': occipital
}

# -----------------------------
# 3. Temporal difference operator matrix for time dimension T
# -----------------------------
def temporal_diff_operator(T):
    D = -np.eye(T) + np.eye(T, k=1)
    return D[:, :-1]

# ---------------------------------
# 4. Proximal operator for nuclear norm with stability safeguards
# ---------------------------------
def prox_nuclear(M, tau, epsilon=1e-8, max_retry=2):
    M = M.copy()
    for attempt in range(max_retry):
        try:
            U, S, Vt = np.linalg.svd(M, full_matrices=False)
            S_shrink = np.maximum(S - tau, 0)
            return U @ np.diag(S_shrink) @ Vt
        except np.linalg.LinAlgError:
            M += epsilon * (10 ** attempt) * np.eye(M.shape[0], M.shape[1])
    raise RuntimeError("SVD did not converge after retries.")

# --------------------------
# 5. ADMM iterative reconstruction for one brain region
# --------------------------
def admm_region(X_obs, J, max_iter=30, tol=1e-4, alpha=0.1, beta=0.5, psi=1.0, rho=1.0):
    N, T = X_obs.shape
    D = temporal_diff_operator(T)  # Could be used to enhance Laplacian update if implemented

    X_hat = X_obs.copy()
    P = X_hat.copy()
    theta = np.zeros_like(X_hat)
    # Initialize Laplacian matrix for the region; here simple diagonal for numerical stability
    L = np.eye(N)

    for it in range(max_iter):
        # Update reconstructed signals X_hat for each timepoint
        A = L + psi * np.diag(J.sum(axis=1)) + rho * np.eye(N)
        for t in range(T):
            rhs = psi * (J[:, t] * X_obs[:, t]) + rho * (P[:, t] - theta[:, t] / rho)
            X_hat[:, t] = np.linalg.solve(A, rhs)

        # Placeholder Laplacian update (for demonstration)
        # Replace with detailed vectorized Laplacian update from the paper for improved reconstruction
        L = np.diag(X_hat.var(axis=1) + alpha)

        # Nuclear norm proximal update of P with numerical safeguard
        P = prox_nuclear(X_hat + theta / rho, beta / rho)

        # Dual variable update
        theta += rho * (X_hat - P)

        # Check convergence
        if np.linalg.norm(X_hat - P, 'fro') < tol:
            print(f"Region converged after {it+1} iterations.")
            break

    return X_hat

# -----------------------------
# 6. Accuracy metrics computation
# -----------------------------
def compute_snr_nmse(X_true, X_rec):
    """
    Compute SNR (dB) and NMSE between reconstructed and ground truth EEG matrices.
    """
    error = X_true - X_rec
    nmse = np.linalg.norm(error, 'fro')**2 / np.linalg.norm(X_true, 'fro')**2
    snr = 10 * np.log10(np.linalg.norm(X_true, 'fro')**2 / np.linalg.norm(error, 'fro')**2)
    return snr, nmse

# -----------------------------------
# 7. Main script to load data, run ADMM, reconstruct full EEG, and validate
# -----------------------------------
if __name__ == "__main__":
    file_path = "/Users/manoharpaturi/Desktop/MFC_S3/archive/EEG_128channels_ERP_lanzhou_2015/EEG_128channels_ERP_lanzhou_2015/02010002erp 20150416 1131.raw"
    eeg = load_eeg_file_trim(file_path, n_channels=128)
    print("Loaded EEG shape:", eeg.shape)  # e.g., (128, 231330)

    # Select manageable time window for processing to ensure stability
    T_window = 500
    eeg_seg = eeg[:, :T_window]

    full_rec = np.zeros((128, T_window))
    rng = np.random.default_rng(42)  # Seed for reproducibility

    for region_name, idx in region_map.items():
        X_region = eeg_seg[idx, :]

        # Create binary mask with 50% missing samples randomly simulated
        J = (rng.random(X_region.shape) > 0.5).astype(float)
        X_obs = np.nan_to_num(X_region * J)  # Safely handle NaNs from multiplication

        print(f"Reconstructing region: {region_name} ({len(idx)} channels)")
        X_rec = admm_region(X_obs, J, max_iter=30)

        # Place reconstructed region back into full 128-channel matrix
        full_rec[idx, :] = X_rec

    print("Full reconstructed EEG shape:", full_rec.shape)

    # Compute accuracy metrics comparing reconstruction to ground truth
    snr, nmse = compute_snr_nmse(eeg_seg, full_rec)
    print(f"\n=== Reconstruction Accuracy ===")
    print(f"SNR (dB): {snr:.2f}")
    print(f"NMSE    : {nmse:.6f}")

    # Save reconstructed EEG for further analysis if needed
    np.save("reconstructed_eeg_window.npy", full_rec)
