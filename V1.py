import numpy as np
from numpy.linalg import inv, norm
import matplotlib.pyplot as plt
import mne  # For handling raw EEG data
from scipy.io import loadmat  # For loading .mat files
from scipy.spatial.distance import cdist # For calculating distances

# --- Performance Metrics ---

def calculate_nmse(original_signal, reconstructed_signal):
    """Calculates the Normalized Mean Square Error (NMSE)."""
    original_norm_sq = norm(original_signal, 'fro')**2
    if original_norm_sq == 0: return np.inf
    return norm(original_signal - reconstructed_signal, 'fro')**2 / original_norm_sq

def calculate_snr(original_signal, error_signal):
    """Calculates the Signal-to-Noise Ratio (SNR) in dB."""
    signal_power = norm(original_signal, 'fro')**2
    error_power = norm(error_signal, 'fro')**2
    if error_power == 0: return np.inf
    return 10 * np.log10(signal_power / error_power)

# --- Graph Construction ---

def construct_anatomical_laplacian(positions, sigma=15.0):
    """
    Constructs a graph Laplacian based on the physical distance between electrodes.
    """
    dist_matrix = cdist(positions, positions)
    adjacency = np.exp(-dist_matrix**2 / (2 * sigma**2))
    np.fill_diagonal(adjacency, 0) # No self-loops
    degree = np.diag(adjacency.sum(axis=1))
    laplacian = degree - adjacency
    return laplacian

# --- Core ADMM Algorithm ---

def admm_graph_reconstruction(noisy_signal, graph_indices, laplacians, lambda_reg, rho, iterations):
    """
    Performs EEG signal reconstruction using pre-computed graph Laplacians.
    """
    num_channels, num_samples = noisy_signal.shape
    X = np.copy(noisy_signal)
    Z = np.copy(noisy_signal)
    U = np.zeros_like(noisy_signal)

    print("Pre-calculating matrix inversions for ADMM...")
    precomputed_inverses = {}
    for i, indices in enumerate(graph_indices):
        laplacian = laplacians[i]
        matrix_to_invert = 2 * lambda_reg * laplacian + rho * np.identity(laplacian.shape[0])
        precomputed_inverses[i] = inv(matrix_to_invert)

    print(f"\nStarting ADMM for {iterations} iterations...")
    for it in range(iterations):
        X = (noisy_signal + rho * (Z - U)) / (1 + rho)
        A = X + U
        for i, indices in enumerate(graph_indices):
            A_i = A[indices, :]
            inv_matrix = precomputed_inverses[i]
            Z[indices, :] = rho * inv_matrix @ A_i
        U = U + X - Z
        if (it + 1) % 10 == 0:
            print(f"  - Iteration {it+1}/{iterations} complete.")

    print("ADMM reconstruction finished!\n")
    return Z

# --- Main execution script ---
if __name__ == "__main__":
    # --- 1. Define File Paths ---
    raw_file_path = '/Users/manoharpaturi/Desktop/MFC_S3/archive/EEG_128channels_ERP_lanzhou_2015/EEG_128channels_ERP_lanzhou_2015/02010002erp 20150416 1131.raw'
    chan_info_path = '/Users/manoharpaturi/Desktop/MFC_S3/archive/EEG_128channels_ERP_lanzhou_2015/EEG_128channels_ERP_lanzhou_2015/chan_info_egi_128.mat'

    # --- 2. Load and Pre-process EEG Data ---
    try:
        raw = mne.io.read_raw_egi(raw_file_path, preload=True, verbose=False)
        print(f"✅ Successfully loaded raw EEG data.")
    except Exception as e:
        print(f"❌ Error loading EEG data: {e}")
        exit()

    raw.filter(l_freq=1., h_freq=40., verbose=False)
    start_sample, stop_sample = raw.time_as_index([10, 12]) # 2-second chunk
    original_eeg = raw.get_data(start=start_sample, stop=stop_sample)[:128, :]
    print(f"Extracted a data segment of shape: {original_eeg.shape}")

    # --- 3. Load Electrode Positions and Create Anatomical Graphs ---
    try:
        chan_info = loadmat(chan_info_path)
        chanlocs = chan_info['chanlocs'][0]
        positions = np.array([[c[1][0][0], c[2][0][0], c[3][0][0]] for c in chanlocs])[:128]
        print("✅ Successfully loaded electrode positions.")
    except Exception as e:
        print(f"❌ Error loading channel info: {e}")
        exit()
        
    channel_groups = [np.arange(0, 32), np.arange(32, 64), np.arange(64, 96), np.arange(96, 128)]
    
    print("Constructing anatomical graph Laplacians for each brain region...")
    anatomical_laplacians = []
    for indices in channel_groups:
        group_positions = positions[indices, :]
        # FIX: Corrected the typo in the function name here
        anatomical_laplacians.append(construct_anatomical_laplacian(group_positions))

    # --- 4. Define Parameters & Add Noise ---
    NOISE_LEVEL = 0.2
    LAMBDA_REG = 0.01 # Tuned down from 0.1 to prevent oversmoothing
    RHO = 0.5        
    ITERATIONS = 150 

    signal_power = np.mean(original_eeg**2)
    noise_std = np.sqrt(signal_power) * NOISE_LEVEL
    noise = np.random.normal(0, noise_std, original_eeg.shape)
    noisy_eeg = original_eeg + noise
    
    # --- 5. Run ADMM Reconstruction ---
    reconstructed_eeg = admm_graph_reconstruction(
        noisy_signal=noisy_eeg,
        graph_indices=channel_groups,
        laplacians=anatomical_laplacians,
        lambda_reg=LAMBDA_REG,
        rho=RHO,
        iterations=ITERATIONS
    )

    # --- 6. Evaluate and Visualize ---
    initial_nmse = calculate_nmse(original_eeg, noisy_eeg)
    final_nmse = calculate_nmse(original_eeg, reconstructed_eeg)
    initial_snr = calculate_snr(original_eeg, noise)
    final_snr = calculate_snr(original_eeg, original_eeg - reconstructed_eeg)

    print("--- Performance Metrics ---")
    print(f"Noisy Signal:      NMSE = {initial_nmse:.4f}, SNR = {initial_snr:.2f} dB")
    print(f"Reconstructed Signal: NMSE = {final_nmse:.4f}, SNR = {final_snr:.2f} dB")
    print("---------------------------")

    channel_to_plot = 10
    time_axis = np.arange(original_eeg.shape[1])
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    fig.suptitle(f'ADMM Reconstruction for Channel {channel_to_plot} (Tuned Lambda)', fontsize=16)

    min_val, max_val = np.min(noisy_eeg[channel_to_plot, :]), np.max(noisy_eeg[channel_to_plot, :])
    y_margin = (max_val - min_val) * 0.1
    
    axes[0].plot(time_axis, original_eeg[channel_to_plot, :], 'k-', label='Original Signal')
    axes[0].set(title='Original Clean Signal', ylabel='Amplitude (µV)', ylim=(min_val - y_margin, max_val + y_margin))
    axes[0].legend()
    
    axes[1].plot(time_axis, noisy_eeg[channel_to_plot, :], 'b-', label=f'Noisy (SNR: {initial_snr:.2f} dB)')
    axes[1].set(title='Signal with Added Noise', ylabel='Amplitude (µV)', ylim=(min_val - y_margin, max_val + y_margin))
    axes[1].legend()
    
    axes[2].plot(time_axis, reconstructed_eeg[channel_to_plot, :], 'r-', label=f'Reconstructed (SNR: {final_snr:.2f} dB)')
    axes[2].set(title='Reconstructed Signal via ADMM', xlabel='Time Samples', ylabel='Amplitude (µV)', ylim=(min_val - y_margin, max_val + y_margin))
    axes[2].legend()
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()