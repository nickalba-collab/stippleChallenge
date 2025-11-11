#!/usr/bin/env python
"""Script to run stippling with a specific image path."""

import subprocess
import sys
import os

# Your image path (handles spaces and quotes)
IMAGE_PATH = r"C:\Users\Nicho\OneDrive\Pictures\Screenshots\Screenshot 2024-04-23 101359.png"

# Check if image exists
if not os.path.exists(IMAGE_PATH):
    print(f"Error: Image not found at {IMAGE_PATH}")
    print(f"\nPlease check the path and update IMAGE_PATH in this script.")
    sys.exit(1)

# Run stippling with default parameters
print(f"Running stippling on: {IMAGE_PATH}")
print("=" * 60)

cmd = [
    sys.executable,
    "-m", "stipple.runner",
    "--image", IMAGE_PATH,  # Python handles the path correctly
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

