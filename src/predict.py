"""Run inference on an image (or a directory of images) using a trained model."""

import argparse
import os

import torch
from PIL import Image

from src.data import DEFAULT_TRANSFORM
from src.model import DotClassifier

CLASS_NAMES = {0: "color_0 (red)", 1: "color_1 (blue)"}


def load_model(weights_path="model.pth", device=None):
    """Load a trained :class:`DotClassifier` from disk.

    Parameters
    ----------
    weights_path : str
        Path to the saved ``.pth`` file.
    device : str or None
        Target device.  Auto-detected if ``None``.

    Returns
    -------
    tuple[DotClassifier, torch.device]
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    model = DotClassifier().to(device)
    model.load_state_dict(
        torch.load(weights_path, map_location=device, weights_only=True)
    )
    model.eval()
    return model, device


def predict_image(image_path, model, device, transform=None):
    """Return the predicted class index and confidence for a single image.

    Parameters
    ----------
    image_path : str
        Path to the input image.
    model : DotClassifier
        Trained model.
    device : torch.device
        Device the model lives on.
    transform : callable or None
        Transform applied to the image; defaults to
        :data:`src.data.DEFAULT_TRANSFORM`.

    Returns
    -------
    tuple[int, float]
        ``(predicted_class, confidence)``
    """
    if transform is None:
        transform = DEFAULT_TRANSFORM

    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)
        confidence, predicted = probs.max(1)

    return predicted.item(), confidence.item()


def predict_directory(image_dir, model, device):
    """Predict all ``.png`` / ``.jpg`` images in *image_dir*."""
    results = []
    for fname in sorted(os.listdir(image_dir)):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(image_dir, fname)
            cls, conf = predict_image(path, model, device)
            results.append((fname, cls, conf))
            print(f"{fname}: {CLASS_NAMES.get(cls, cls)}  (confidence {conf:.2%})")
    return results


def main():
    parser = argparse.ArgumentParser(description="Predict dot color from image(s)")
    parser.add_argument("input", help="Path to an image file or directory")
    parser.add_argument(
        "--model", type=str, default="model.pth", help="Path to trained model weights"
    )
    args = parser.parse_args()

    model, device = load_model(args.model)

    if os.path.isdir(args.input):
        predict_directory(args.input, model, device)
    else:
        cls, conf = predict_image(args.input, model, device)
        print(f"Prediction: {CLASS_NAMES.get(cls, cls)}  (confidence {conf:.2%})")


if __name__ == "__main__":
    main()
