"""Neural network model for dot color classification."""

import torch.nn as nn


class DotClassifier(nn.Module):
    """Small CNN that classifies a 32×32 RGB image as one of two classes.

    Architecture
    ------------
    conv(3→16) → ReLU → pool →
    conv(16→32) → ReLU → pool →
    flatten → fc(32*8*8 → 64) → ReLU → fc(64 → 2)
    """

    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
