"""Command-line interface for blue-noise stippling."""

import argparse
import numpy as np
from PIL import Image
import os
from pathlib import Path
from typing import Optional

from .importance import compute_importance
from .blue_noise import void_and_cluster
from .viz import make_comparison_figure, make_progressive_gif


def load_image(
    image_path: str, max_size: Optional[int] = None, grayscale: bool = True
) -> np.ndarray:
    """
    Load and preprocess image for stippling.

    Args:
        image_path: Path to input image
        max_size: Maximum size for longest side (default: None, no resize)
        grayscale: Convert to grayscale (default: True)

    Returns:
        Grayscale image in [0, 1] range, shape (H, W)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}\n"
            f"Please place your input image at: {image_path}"
        )

    # Load image
    img = Image.open(image_path)

    # Convert to grayscale if needed
    if grayscale:
        if img.mode != "L":
            img = img.convert("L")

    # Resize if needed
    if max_size is not None:
        w, h = img.size
        if max(w, h) > max_size:
            if w > h:
                new_w, new_h = max_size, int(h * max_size / w)
            else:
                new_w, new_h = int(w * max_size / h), max_size
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Convert to numpy array and normalize to [0, 1]
    img_array = np.array(img, dtype=np.float32) / 255.0

    return img_array


def save_stipple_image(stipple: np.ndarray, output_path: str, dpi: int = 300) -> None:
    """
    Save stipple image as PNG.

    Args:
        stipple: Stipple image (1=white, 0=black), shape (H, W)
        output_path: Path to save the image
        dpi: Resolution for saved image (default: 300)
    """
    # Convert to uint8: 0 = black, 255 = white
    stipple_uint8 = (stipple * 255).astype(np.uint8)

    # Save as PNG
    img = Image.fromarray(stipple_uint8)
    img.save(output_path, dpi=(dpi, dpi))


def run_stippling(
    image_path: str,
    output_dir: str = "outputs",
    percentage: float = 0.08,
    sigma: float = 0.9,
    content_bias: float = 0.9,
    noise_scale_factor: float = 0.1,
    frame_increment: int = 100,
    max_size: Optional[int] = 512,
    make_comparison: bool = False,
    seed: Optional[int] = None,
) -> None:
    """
    Run blue-noise stippling pipeline.

    Args:
        image_path: Path to input image
        output_dir: Output directory for results
        percentage: Fraction of pixels to stipple
        sigma: Gaussian kernel sigma for repulsion
        content_bias: Bias toward importance map
        noise_scale_factor: Scale factor for annealing noise
        frame_increment: Number of points between GIF frames
        max_size: Maximum size for longest side
        make_comparison: Whether to create comparison figure
        seed: Random seed for reproducibility
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    print(f"Loading image: {image_path}")
    image = load_image(image_path, max_size=max_size)

    print(f"Image shape: {image.shape}")

    # Compute importance map
    print("Computing importance map...")
    importance = compute_importance(image)

    # Generate stippling
    print(f"Generating stippling ({percentage*100:.1f}% coverage)...")
    stipple, samples = void_and_cluster(
        importance,
        percentage=percentage,
        sigma=sigma,
        content_bias=content_bias,
        noise_scale_factor=noise_scale_factor,
        seed=seed,
    )

    print(f"Placed {len(samples)} stipples")

    # Save stipple image
    stipple_path = os.path.join(output_dir, "stipple.png")
    print(f"Saving stipple image: {stipple_path}")
    save_stipple_image(stipple, stipple_path)

    # Create progressive GIF
    gif_path = os.path.join(output_dir, "progressive.gif")
    print(f"Creating progressive GIF: {gif_path}")
    make_progressive_gif(samples, image.shape, gif_path, frame_increment=frame_increment)

    # Create comparison figure if requested
    if make_comparison:
        comparison_path = os.path.join(output_dir, "comparison.png")
        print(f"Creating comparison figure: {comparison_path}")
        make_comparison_figure(image, importance, stipple, comparison_path)

    print("Done!")


def run_sweep(
    image_path: str,
    output_dir: str = "outputs",
    max_size: Optional[int] = 512,
    seed: Optional[int] = None,
) -> None:
    """
    Run parameter sweep and create comparison grid.

    Args:
        image_path: Path to input image
        output_dir: Output directory for results
        max_size: Maximum size for longest side
        seed: Random seed for reproducibility
    """
    import matplotlib.pyplot as plt

    # Load image
    print(f"Loading image: {image_path}")
    image = load_image(image_path, max_size=max_size)

    # Compute importance map
    print("Computing importance map...")
    importance = compute_importance(image)

    # Parameter combinations to try
    param_combos = [
        {"percentage": 0.05, "sigma": 0.7, "name": "Sparse, Small"},
        {"percentage": 0.08, "sigma": 0.9, "name": "Default"},
        {"percentage": 0.12, "sigma": 1.1, "name": "Dense, Large"},
        {"percentage": 0.08, "sigma": 0.5, "name": "Tight Repulsion"},
        {"percentage": 0.08, "sigma": 1.5, "name": "Wide Repulsion"},
        {"percentage": 0.15, "sigma": 0.9, "name": "Very Dense"},
    ]

    # Create grid of results
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, params in enumerate(param_combos):
        print(f"Running: {params['name']} (percentage={params['percentage']}, sigma={params['sigma']})")
        stipple, _ = void_and_cluster(
            importance,
            percentage=params["percentage"],
            sigma=params["sigma"],
            content_bias=0.9,
            noise_scale_factor=0.1,
            seed=seed,
        )

        axes[idx].imshow(stipple, cmap="gray", vmin=0, vmax=1)
        axes[idx].set_title(f"{params['name']}\n{params['percentage']*100:.0f}%, σ={params['sigma']}")
        axes[idx].axis("off")

    plt.tight_layout()
    sweep_path = os.path.join(output_dir, "sweep.png")
    print(f"Saving sweep comparison: {sweep_path}")
    plt.savefig(sweep_path, dpi=150, bbox_inches="tight")
    plt.close()

    print("Sweep complete!")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Blue-noise stippling using modified void-and-cluster algorithm"
    )
    parser.add_argument(
        "--image",
        type=str,
        default="assets/headshot.png",
        help="Path to input image (default: assets/headshot.png)",
    )
    parser.add_argument(
        "--percentage",
        type=float,
        default=0.08,
        help="Fraction of pixels to stipple (default: 0.08)",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=0.9,
        help="Gaussian kernel sigma for repulsion (default: 0.9)",
    )
    parser.add_argument(
        "--content_bias",
        type=float,
        default=0.9,
        help="Bias toward importance map (default: 0.9)",
    )
    parser.add_argument(
        "--noise_scale_factor",
        type=float,
        default=0.1,
        help="Scale factor for annealing noise (default: 0.1)",
    )
    parser.add_argument(
        "--frame_increment",
        type=int,
        default=100,
        help="Number of points between GIF frames (default: 100)",
    )
    parser.add_argument(
        "--max_size",
        type=int,
        default=512,
        help="Maximum size for longest side (default: 512)",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default="outputs",
        help="Output directory (default: outputs)",
    )
    parser.add_argument(
        "--make_comparison",
        action="store_true",
        help="Create comparison figure (original, importance, stipple)",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run parameter sweep and create comparison grid",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: None)",
    )

    args = parser.parse_args()

    if args.sweep:
        run_sweep(
            args.image,
            output_dir=args.out_dir,
            max_size=args.max_size,
            seed=args.seed,
        )
    else:
        run_stippling(
            image_path=args.image,
            output_dir=args.out_dir,
            percentage=args.percentage,
            sigma=args.sigma,
            content_bias=args.content_bias,
            noise_scale_factor=args.noise_scale_factor,
            frame_increment=args.frame_increment,
            max_size=args.max_size,
            make_comparison=args.make_comparison,
            seed=args.seed,
        )


if __name__ == "__main__":
    main()

