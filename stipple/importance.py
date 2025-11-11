"""Importance map computation for blue-noise stippling."""

import numpy as np
from typing import Tuple, Optional


def compute_importance(
    image: np.ndarray,
    extreme_downweight: float = 0.3,
    dark_threshold: float = 0.2,
    light_threshold: float = 0.8,
    dark_sigma: float = 0.15,
    light_sigma: float = 0.15,
    mid_tone_center: float = 0.65,
    mid_tone_sigma: float = 0.2,
    mid_tone_boost: float = 1.5,
) -> np.ndarray:
    """
    Compute importance map from grayscale image.

    The importance map determines where stipples should be placed. It:
    1. Inverts brightness (dark areas get high importance)
    2. Smoothly downweights very dark (<0.2) and very light (>0.8) regions
    3. Boosts mid-tones (centered around 0.65)
    4. Normalizes to [0, 1]

    Args:
        image: Grayscale image in [0, 1] range, shape (H, W)
        extreme_downweight: Minimum weight for extreme values (default: 0.3)
        dark_threshold: Threshold for dark region downweighting (default: 0.2)
        light_threshold: Threshold for light region downweighting (default: 0.8)
        dark_sigma: Gaussian sigma for dark region downweighting (default: 0.15)
        light_sigma: Gaussian sigma for light region downweighting (default: 0.15)
        mid_tone_center: Center of mid-tone boost (default: 0.65)
        mid_tone_sigma: Sigma for mid-tone boost Gaussian (default: 0.2)
        mid_tone_boost: Multiplicative boost factor for mid-tones (default: 1.5)

    Returns:
        Importance map in [0, 1] range, shape (H, W)
    """
    # Invert brightness: dark areas become high importance
    inverted = 1.0 - image

    # Smooth downweight very dark regions
    # Weight transitions smoothly from 1.0 at dark_threshold to extreme_downweight at 0
    dark_distances = np.maximum(0, dark_threshold - image) / dark_sigma
    dark_weights = extreme_downweight + (1.0 - extreme_downweight) * np.exp(
        -0.5 * dark_distances ** 2
    )
    # For pixels above threshold, weight should be 1.0
    dark_weights = np.where(image >= dark_threshold, 1.0, dark_weights)

    # Smooth downweight very light regions
    # Weight transitions smoothly from 1.0 at light_threshold to extreme_downweight at 1
    light_distances = np.maximum(0, image - light_threshold) / light_sigma
    light_weights = extreme_downweight + (1.0 - extreme_downweight) * np.exp(
        -0.5 * light_distances ** 2
    )
    # For pixels below threshold, weight should be 1.0
    light_weights = np.where(image <= light_threshold, 1.0, light_weights)

    # Combine dark and light downweighting (take minimum to be conservative)
    extreme_weights = np.minimum(dark_weights, light_weights)

    # Apply extreme downweighting
    importance = inverted * extreme_weights

    # Mid-tone boost: enhance importance in mid-tone range
    mid_tone_gaussian = np.exp(-0.5 * ((image - mid_tone_center) / mid_tone_sigma) ** 2)
    mid_tone_factor = 1.0 + (mid_tone_boost - 1.0) * mid_tone_gaussian
    importance = importance * mid_tone_factor

    # Normalize to [0, 1]
    importance_min = importance.min()
    importance_max = importance.max()
    if importance_max > importance_min:
        importance = (importance - importance_min) / (importance_max - importance_min)
    else:
        importance = np.ones_like(importance)

    return importance

