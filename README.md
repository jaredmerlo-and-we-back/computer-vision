# computer-vision

A neural network that classifies colored dots in images as one of two colors (red vs. blue by default).

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model (generates synthetic data automatically)
python -m src.train --samples 2000 --epochs 10

# Predict on a single image
python -m src.predict path/to/image.png

# Predict on a directory of images
python -m src.predict path/to/images/
```

## Project structure

```
src/
  data.py      – Synthetic data generation & PyTorch dataset
  model.py     – DotClassifier CNN architecture
  train.py     – Training pipeline
  predict.py   – Inference on new images
```

## How it works

1. **Data generation** (`src/data.py`): Creates 32×32 images each containing a
   single colored dot on a noisy gray background. Class 0 dots are reddish;
   class 1 dots are bluish. Color, size, and position vary randomly.
2. **Model** (`src/model.py`): A small CNN (two conv layers + two FC layers)
   that takes a 32×32 RGB image and outputs logits for two classes.
3. **Training** (`src/train.py`): Trains with Adam and cross-entropy loss,
   tracks validation accuracy, and saves the best weights to `model.pth`.
4. **Inference** (`src/predict.py`): Loads a trained model and predicts the dot
   color for one or more images.

## Customising the colors

Pass a custom `class_colors` dict when generating data:

```python
from src.data import DotDataset

custom = {
    0: {"center": (0, 180, 0), "variation": 30},   # green
    1: {"center": (200, 200, 0), "variation": 30},  # yellow
}
dataset = DotDataset(n_samples=2000, class_colors=custom)
```

## Training options

| Flag | Default | Description |
|------|---------|-------------|
| `--samples` | 2000 | Number of synthetic training images |
| `--epochs` | 10 | Training epochs |
| `--batch-size` | 32 | Mini-batch size |
| `--lr` | 0.001 | Learning rate |
| `--output` | `model.pth` | Path to save model weights |