#!/usr/bin/env python
"""Quick script to run stippling on your headshot image."""

import subprocess
import sys
import os

# Path to your image
IMAGE_PATH = "assets/headshot.png"

# Check if image exists
if not os.path.exists(IMAGE_PATH):
    print(f"Error: Image not found at {IMAGE_PATH}")
    print(f"\nPlease place your image at: {IMAGE_PATH}")
    print(f"Or update IMAGE_PATH in this script to point to your image.")
    sys.exit(1)

# Run stippling with default parameters
print(f"Running stippling on: {IMAGE_PATH}")
print("=" * 60)

cmd = [
    sys.executable,
    "-m", "stipple.runner",
    "--image", IMAGE_PATH,
    "--percentage", "0.08",
    "--sigma", "0.9",
    "--content_bias", "0.9",
    "--noise_scale_factor", "0.1",
    "--frame_increment", "100",
    "--max_size", "512",
    "--make_comparison",
    "--seed", "42"
]

subprocess.run(cmd)

print("\n" + "=" * 60)
print("Done! Check the outputs:")
print("  - outputs/stipple.png")
print("  - outputs/progressive.gif")
print("  - outputs/comparison.png")

