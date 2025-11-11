# Blue Noise Stippling

A Python implementation of blue-noise stippling using a modified void-and-cluster algorithm with importance mapping.

## Overview

This project converts grayscale images into stippled artwork using blue-noise distribution. The algorithm places dots in a way that:
- Maintains even spatial distribution (blue noise)
- Preserves tonal structure through importance mapping
- Avoids clumps and regular grid patterns
- Produces visually pleasing results

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

1. Place your input image at `assets/headshot.png`

2. Run the stippling algorithm:
```bash
python -m stipple.runner --image assets/headshot.png
```

This will generate:
- `outputs/stipple.png` - The final stippled image
- `outputs/progressive.gif` - Animation showing stipples being added progressively

## Usage

### Basic Usage

```bash
python -m stipple.runner --image assets/headshot.png --percentage 0.08 --sigma 0.9
```

### Create Comparison Figure

```bash
python -m stipple.runner --image assets/headshot.png --make_comparison
```

This creates a 3-panel comparison showing the original image, importance map, and stippled result.

### Parameter Sweep

```bash
python -m stipple.runner --image assets/headshot.png --sweep
```

This runs multiple parameter combinations and creates a grid comparison in `outputs/sweep.png`.

### All Options

```bash
python -m stipple.runner \
    --image assets/headshot.png \
    --percentage 0.08 \
    --sigma 0.9 \
    --content_bias 0.9 \
    --noise_scale_factor 0.1 \
    --frame_increment 100 \
    --max_size 512 \
    --out_dir outputs \
    --make_comparison \
    --seed 42
```

### Parameters

- `--image`: Path to input image (default: `assets/headshot.png`)
- `--percentage`: Fraction of pixels to stipple (default: `0.08`)
- `--sigma`: Gaussian kernel sigma for repulsion (default: `0.9`)
- `--content_bias`: Bias toward importance map (default: `0.9`)
- `--noise_scale_factor`: Scale factor for annealing noise (default: `0.1`)
- `--frame_increment`: Number of points between GIF frames (default: `100`)
- `--max_size`: Maximum size for longest side (default: `512`)
- `--out_dir`: Output directory (default: `outputs`)
- `--make_comparison`: Create comparison figure
- `--sweep`: Run parameter sweep
- `--seed`: Random seed for reproducibility

## Method

### Importance Mapping

The algorithm computes an importance map that determines where stipples should be placed:

1. **Brightness Inversion**: Dark areas get high importance (more stipples)
2. **Extreme Downweighting**: Very dark (<0.2) and very light (>0.8) regions are smoothly downweighted
3. **Mid-tone Boost**: Mid-tones (centered around 0.65) are enhanced
4. **Normalization**: Final map is normalized to [0, 1]

### Blue-Noise Algorithm

The void-and-cluster algorithm places stipples iteratively:

1. **Energy Field**: Initialized as `-importance * content_bias`
2. **First Point**: Selected near image center (minimum energy)
3. **Iterative Placement**: Each subsequent point is placed at the minimum energy location
4. **Repulsion**: After placement, a toroidal Gaussian kernel is added to the energy field
5. **Avoidance**: Selected pixels are set to +inf to prevent reselection

The toroidal (wraparound) kernel ensures even distribution across image boundaries.

## GitHub Pages

To enable GitHub Pages:

1. Generate the stippling outputs:
   ```bash
   python -m stipple.runner --image assets/headshot.png --make_comparison
   ```

2. Copy outputs to `docs/` directory for GitHub Pages:
   ```bash
   # On Unix/Mac:
   cp -r outputs docs/
   # On Windows:
   xcopy outputs docs\outputs\ /E /I
   ```
   Or manually copy the `outputs` folder to `docs/outputs`.

3. Push the repository to GitHub

4. Go to Settings → Pages
5. Select source: `main` branch, `/docs` folder
6. The site will be available at `https://<username>.github.io/<repo-name>`

The documentation is in `docs/index.md` and will be automatically rendered by Jekyll. The images are referenced from `docs/outputs/`.

## Project Structure

```
.
├── stipple/              # Package code
│   ├── __init__.py
│   ├── importance.py     # Importance map computation
│   ├── blue_noise.py     # Blue-noise stippling algorithm
│   ├── runner.py         # CLI interface
│   └── viz.py            # Visualization utilities
├── assets/               # Input images
│   └── headshot.png
├── outputs/              # Generated artifacts
├── docs/                 # GitHub Pages documentation
│   └── index.md
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── pyproject.toml       # Project configuration
```

## License

See LICENSE file for details.

