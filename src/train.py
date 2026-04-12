"""Training pipeline for the dot color classifier."""

import argparse
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from src.data import DotDataset
from src.model import DotClassifier


def train(
    n_samples=2000,
    epochs=10,
    batch_size=32,
    lr=1e-3,
    val_split=0.2,
    output_path="model.pth",
    device=None,
):
    """Train the :class:`DotClassifier` and save the best weights.

    Parameters
    ----------
    n_samples : int
        Total synthetic samples to generate.
    epochs : int
        Number of training epochs.
    batch_size : int
        Mini-batch size.
    lr : float
        Learning rate for Adam optimiser.
    val_split : float
        Fraction of data reserved for validation.
    output_path : str
        Where to save the trained model weights.
    device : str or None
        ``"cpu"``, ``"cuda"``, etc.  Auto-detected if ``None``.

    Returns
    -------
    DotClassifier
        The trained model (on CPU).
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    print(f"Using device: {device}")
    print(f"Generating {n_samples} synthetic samples …")

    dataset = DotDataset(n_samples=n_samples)
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    model = DotClassifier().to(device)
    criterion = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)

    best_val_acc = 0.0

    for epoch in range(1, epochs + 1):
        # --- train ---
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimiser.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimiser.step()
            running_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)
        train_loss = running_loss / total
        train_acc = correct / total

        # --- validate ---
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total += labels.size(0)
        val_acc = val_correct / val_total

        print(
            f"Epoch {epoch}/{epochs}  "
            f"train_loss={train_loss:.4f}  train_acc={train_acc:.3f}  "
            f"val_acc={val_acc:.3f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), output_path)

    print(f"\nBest validation accuracy: {best_val_acc:.3f}")
    print(f"Model saved to {output_path}")

    model.load_state_dict(torch.load(output_path, weights_only=True))
    model.cpu()
    return model


def main():
    parser = argparse.ArgumentParser(description="Train dot color classifier")
    parser.add_argument("--samples", type=int, default=2000, help="Number of training samples")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--output", type=str, default="model.pth", help="Output model path")
    args = parser.parse_args()

    train(
        n_samples=args.samples,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
