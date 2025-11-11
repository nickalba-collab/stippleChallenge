# Quick Start Guide

## Step 1: Place Your Image

Place your headshot image at:
```
assets/headshot.png
```

**Supported formats:** PNG, JPG, JPEG

## Step 2: Run the Stippling

### Option A: Use the quick script
```bash
python run_stippling.py
```

### Option B: Run directly
```bash
python -m stipple.runner --image assets/headshot.png --make_comparison
```

### Option C: Run with custom settings
```bash
python -m stipple.runner \
    --image assets/headshot.png \
    --percentage 0.1 \
    --sigma 1.0 \
    --max_size 512 \
    --make_comparison \
    --seed 42
```

## Step 3: Check Results

After running, check the `outputs/` folder:
- `stipple.png` - Final stippled image
- `progressive.gif` - Animation showing stipples being added
- `comparison.png` - Side-by-side comparison (if --make_comparison was used)

## Parameters Explained

- `--percentage 0.08` - Fraction of pixels to stipple (8% coverage)
- `--sigma 0.9` - Repulsion distance (higher = more spacing between dots)
- `--max_size 512` - Resize image so longest side is 512px (speeds up processing)
- `--frame_increment 100` - GIF frames every 100 points
- `--seed 42` - Random seed for reproducible results

## Troubleshooting

**Image not found?**
- Make sure your image is at `assets/headshot.png`
- Or use `--image path/to/your/image.png` to specify a different path

**Want higher quality?**
- Increase `--max_size` (e.g., `--max_size 1024`)
- Increase `--percentage` for more dots (e.g., `--percentage 0.12`)

**Want different spacing?**
- Increase `--sigma` for wider spacing (e.g., `--sigma 1.5`)
- Decrease `--sigma` for tighter spacing (e.g., `--sigma 0.5`)

