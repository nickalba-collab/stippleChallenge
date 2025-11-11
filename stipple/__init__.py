"""Blue-noise stippling package for converting images to stippled artwork."""

__version__ = "0.1.0"

from .importance import compute_importance
from .blue_noise import toroidal_gaussian_kernel, void_and_cluster
from .viz import make_comparison_figure, make_progressive_gif

__all__ = [
    "compute_importance",
    "toroidal_gaussian_kernel",
    "void_and_cluster",
    "make_comparison_figure",
    "make_progressive_gif",
]

