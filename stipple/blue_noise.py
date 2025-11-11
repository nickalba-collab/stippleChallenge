"""Blue-noise stippling using modified void-and-cluster algorithm."""

import numpy as np
from typing import Tuple, Optional, List


def toroidal_gaussian_kernel(
    size: int, sigma: float, normalize: bool = True
) -> np.ndarray:
    """
    Create a Gaussian kernel for toroidal (wraparound) convolution.

    The kernel is a regular Gaussian that will be applied with toroidal
    wrapping when used in the energy field. This ensures even distribution
    across image boundaries.

    Args:
        size: Kernel size (should be odd for symmetry)
        sigma: Gaussian standard deviation (in pixels)
        normalize: If True, normalize kernel to sum to 1 (default: True)

    Returns:
        Gaussian kernel of shape (size, size)
    """
    # Ensure size is odd
    if size % 2 == 0:
        size += 1

    center = size // 2

    # Create coordinate arrays
    y, x = np.ogrid[:size, :size]

    # Compute Euclidean distances from center
    dy = y - center
    dx = x - center
    distances = np.sqrt(dy ** 2 + dx ** 2)

    # Gaussian function
    kernel = np.exp(-0.5 * (distances / sigma) ** 2)

    # Normalize so kernel sums to 1
    if normalize:
        kernel = kernel / kernel.sum()

    return kernel


def void_and_cluster(
    importance: np.ndarray,
    percentage: float = 0.08,
    sigma: float = 0.9,
    content_bias: float = 0.9,
    noise_scale_factor: float = 0.1,
    seed: Optional[int] = None,
) -> Tuple[np.ndarray, List[Tuple[int, int, float]]]:
    """
    Generate blue-noise stippling using modified void-and-cluster algorithm.

    The algorithm places stipples iteratively by:
    1. Initializing energy field as -importance * content_bias
    2. Selecting first point near center (minimum energy)
    3. Iteratively selecting points at minimum energy locations
    4. After each selection, adding Gaussian repulsion kernel to energy field
    5. Setting selected pixel to +inf to avoid reselection

    Args:
        importance: Importance map in [0, 1], shape (H, W)
        percentage: Fraction of pixels to stipple (default: 0.08)
        sigma: Gaussian kernel sigma for repulsion (default: 0.9)
        content_bias: Bias toward importance map (default: 0.9)
        noise_scale_factor: Scale factor for annealing noise (default: 0.1)
        seed: Random seed for reproducibility (default: None)

    Returns:
        Tuple of:
        - Binary stipple image (1=white background, 0=black dot), shape (H, W)
        - List of sample tuples (y, x, intensity) in order of placement
    """
    if seed is not None:
        np.random.seed(seed)

    H, W = importance.shape
    num_points = int(H * W * percentage)

    # Initialize energy field: negative importance (so high importance = low energy)
    energy = -importance * content_bias

    # Create repulsion kernel
    # Kernel size should be large enough to cover repulsion distance
    kernel_size = int(6 * sigma) + 1
    if kernel_size % 2 == 0:
        kernel_size += 1
    repulsion_kernel = toroidal_gaussian_kernel(kernel_size, sigma, normalize=False)

    # Scale kernel to appropriate magnitude (larger = stronger repulsion)
    repulsion_kernel = repulsion_kernel * (sigma ** 2)

    # Find center of image for first point
    center_y, center_x = H // 2, W // 2

    # Sample points iteratively
    samples: List[Tuple[int, int, float]] = []
    stipple_image = np.ones((H, W), dtype=np.float32)  # 1 = white background

    # For progressive visualization, we'll track all samples
    for i in range(num_points):
        # Find minimum energy location
        if i == 0:
            # First point: pick near center
            # Search in a small region around center
            search_radius = min(H, W) // 4
            y_min = max(0, center_y - search_radius)
            y_max = min(H, center_y + search_radius)
            x_min = max(0, center_x - search_radius)
            x_max = min(W, center_x + search_radius)

            local_energy = energy[y_min:y_max, x_min:x_max]
            min_idx = np.unravel_index(np.argmin(local_energy), local_energy.shape)
            y, x = y_min + min_idx[0], x_min + min_idx[1]
        else:
            # Add small annealed noise to break ties and add variation
            noise = np.random.randn(H, W) * noise_scale_factor * (1.0 - i / num_points)
            energy_with_noise = energy + noise

            # Find global minimum
            min_idx = np.unravel_index(np.argmin(energy_with_noise), energy_with_noise.shape)
            y, x = min_idx

        # Record sample
        intensity = importance[y, x]
        samples.append((y, x, intensity))

        # Place stipple (0 = black dot)
        stipple_image[y, x] = 0.0

        # Add repulsion: circular convolution with wraparound
        # Roll kernel so center aligns with (y, x)
        ky, kx = repulsion_kernel.shape
        ky_center, kx_center = ky // 2, kx // 2

        # Compute kernel placement with toroidal wrapping
        for ky_offset in range(ky):
            for kx_offset in range(kx):
                # Relative position from kernel center
                dy = ky_offset - ky_center
                dx = kx_offset - kx_center

                # Target position with toroidal wrapping
                target_y = (y + dy) % H
                target_x = (x + dx) % W

                # Add repulsion energy
                energy[target_y, target_x] += repulsion_kernel[ky_offset, kx_offset]

        # Set selected pixel to +inf to prevent reselection
        energy[y, x] = np.inf

    # Convert to binary: 1 = white, 0 = black dot
    # For output, we want white background with black dots
    # stipple_image is already 1 (white) with 0 (black) at dot locations
    return stipple_image, samples

