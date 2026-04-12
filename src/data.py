"""Synthetic data generation and dataset utilities for dot color classification.

Generates images containing a single colored dot on a noisy background.
Each dot is labeled as class 0 or class 1 based on its color.
"""

import os
import random

import numpy as np
from PIL import Image, ImageDraw
from torch.utils.data import Dataset
from torchvision import transforms


# Default color palettes for the two classes.
# Class 0: reddish dots, Class 1: bluish dots.
DEFAULT_CLASS_COLORS = {
    0: {"center": (200, 50, 50), "variation": 40},
    1: {"center": (50, 50, 200), "variation": 40},
}

DEFAULT_TRANSFORM = transforms.Compose(
    [
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)


def _random_color(center, variation):
    """Return an RGB tuple randomly perturbed around *center*."""
    return tuple(
        max(0, min(255, c + random.randint(-variation, variation))) for c in center
    )


def _random_background(size, noise_level=30):
    """Create a noisy gray background image of the given *size*."""
    base = 128
    arr = np.full((*size, 3), base, dtype=np.uint8)
    noise = np.random.randint(-noise_level, noise_level + 1, arr.shape, dtype=np.int16)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def generate_dot_image(
    image_size=64,
    dot_radius_range=(4, 10),
    label=None,
    class_colors=None,
):
    """Generate a single image with one colored dot and return ``(image, label)``.

    Parameters
    ----------
    image_size : int
        Width and height of the square image in pixels.
    dot_radius_range : tuple[int, int]
        Min and max radius for the dot.
    label : int or None
        Force a specific class label (0 or 1). If ``None``, chosen at random.
    class_colors : dict or None
        Mapping of label → ``{"center": (R,G,B), "variation": int}``.
        Defaults to red vs. blue.

    Returns
    -------
    tuple[PIL.Image.Image, int]
    """
    if class_colors is None:
        class_colors = DEFAULT_CLASS_COLORS
    if label is None:
        label = random.randint(0, 1)

    color_spec = class_colors[label]
    dot_color = _random_color(color_spec["center"], color_spec["variation"])
    radius = random.randint(*dot_radius_range)

    margin = radius + 2
    cx = random.randint(margin, image_size - margin)
    cy = random.randint(margin, image_size - margin)

    img = _random_background((image_size, image_size))
    draw = ImageDraw.Draw(img)
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=dot_color,
    )
    return img, label


def generate_dataset(output_dir, n_samples=1000, **kwargs):
    """Generate images on disk organised into class sub-directories.

    The layout is compatible with ``torchvision.datasets.ImageFolder``::

        output_dir/
            0/
                0000.png
                ...
            1/
                0000.png
                ...
    """
    os.makedirs(output_dir, exist_ok=True)
    for cls in (0, 1):
        os.makedirs(os.path.join(output_dir, str(cls)), exist_ok=True)

    counters = {0: 0, 1: 0}
    for _ in range(n_samples):
        img, label = generate_dot_image(**kwargs)
        fname = f"{counters[label]:04d}.png"
        img.save(os.path.join(output_dir, str(label), fname))
        counters[label] += 1


class DotDataset(Dataset):
    """In-memory dataset of synthetic dot images.

    Parameters
    ----------
    n_samples : int
        Number of images to generate.
    transform : callable or None
        Torchvision transform to apply to each image.
    **kwargs
        Forwarded to :func:`generate_dot_image`.
    """

    def __init__(self, n_samples=1000, transform=None, **kwargs):
        self.transform = transform or DEFAULT_TRANSFORM
        self.samples = [generate_dot_image(**kwargs) for _ in range(n_samples)]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img, label = self.samples[idx]
        if self.transform:
            img = self.transform(img)
        return img, label
