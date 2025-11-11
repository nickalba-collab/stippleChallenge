"""Visualization utilities for stippling results."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from typing import List, Tuple, Optional
import os


def make_comparison_figure(
    original: np.ndarray,
    importance: np.ndarray,
    stipple: np.ndarray,
    output_path: str,
    dpi: int = 150,
) -> None:
    """
    Create a 3-panel comparison figure (original, importance, stipple).

    Args:
        original: Original grayscale image, shape (H, W)
        importance: Importance map, shape (H, W)
        stipple: Stipple image (1=white, 0=black), shape (H, W)
        output_path: Path to save the figure
        dpi: Resolution for saved figure (default: 150)
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Original image
    axes[0].imshow(original, cmap="gray", vmin=0, vmax=1)
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    # Importance map
    im = axes[1].imshow(importance, cmap="viridis", vmin=0, vmax=1)
    axes[1].set_title("Importance Map")
    axes[1].axis("off")
    plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

    # Stipple
    axes[2].imshow(stipple, cmap="gray", vmin=0, vmax=1)
    axes[2].set_title("Stippled Result")
    axes[2].axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close()


def make_progressive_gif(
    samples: List[Tuple[int, int, float]],
    image_shape: Tuple[int, int],
    output_path: str,
    frame_increment: int = 100,
    dpi: int = 100,
    fps: int = 10,
) -> None:
    """
    Create a progressive GIF showing stipples being added over time.

    Args:
        samples: List of (y, x, intensity) tuples in order of placement
        image_shape: (H, W) shape of the output image
        output_path: Path to save the GIF
        frame_increment: Number of points between frames (default: 100)
        dpi: Resolution for frames (default: 100)
        fps: Frames per second for GIF (default: 10)
    """
    H, W = image_shape

    # Determine frame indices
    num_samples = len(samples)
    frame_indices = []
    for i in range(0, num_samples, frame_increment):
        frame_indices.append(i)
    # Always include the last frame
    if frame_indices[-1] != num_samples - 1:
        frame_indices.append(num_samples - 1)

    # Create figure for GIF
    fig, ax = plt.subplots(figsize=(W / dpi, H / dpi), dpi=dpi)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.invert_yaxis()  # Image coordinates: y increases downward
    ax.set_facecolor("white")

    # Try using matplotlib's PillowWriter first
    try:
        writer = PillowWriter(fps=fps)
        with writer.saving(fig, output_path, dpi=dpi):
            for frame_idx in frame_indices:
                ax.clear()
                ax.set_xlim(0, W)
                ax.set_ylim(0, H)
                ax.set_aspect("equal")
                ax.axis("off")
                ax.invert_yaxis()
                ax.set_facecolor("white")

                # Plot all points up to and including this frame
                if frame_idx >= 0:
                    frame_samples = samples[: frame_idx + 1]
                    if frame_samples:
                        y_coords = [s[0] for s in frame_samples]
                        x_coords = [s[1] for s in frame_samples]

                        # Plot black dots
                        ax.scatter(
                            x_coords,
                            y_coords,
                            c="black",
                            s=1,
                            marker="o",
                            alpha=1.0,
                            edgecolors="none",
                        )

                writer.grab_frame()

        plt.close(fig)

    except Exception as e:
        # Fallback: try imageio if available
        plt.close(fig)
        try:
            import imageio

            # Create frames using imageio
            frames = []
            for frame_idx in frame_indices:
                # Create a white image
                frame = np.ones((H, W, 3), dtype=np.uint8) * 255

                # Draw black dots
                if frame_idx >= 0:
                    frame_samples = samples[: frame_idx + 1]
                    for y, x, _ in frame_samples:
                        # Ensure coordinates are within bounds
                        y = max(0, min(H - 1, int(y)))
                        x = max(0, min(W - 1, int(x)))
                        frame[y, x] = [0, 0, 0]

                frames.append(frame)

            imageio.mimsave(output_path, frames, fps=fps, loop=0)
        except ImportError:
            raise RuntimeError(
                f"Could not create GIF: {e}. Please install imageio: pip install imageio"
            )

