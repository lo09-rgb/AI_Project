# ================================================================
# GAN-MNIST
# Author: Aayushman Baral
# Description:
# A simple Generative Adversarial Network (GAN) implemented
# using PyTorch to generate handwritten digits from the
# MNIST dataset.
# ================================================================

import os
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader


# ================================================================
# Hyperparameters
# ================================================================

BATCH_SIZE = 64
LATENT_DIM = 100
LEARNING_RATE = 0.0002
EPOCHS = 50

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Running on: {DEVICE}")


# ================================================================
# Dataset
# ================================================================

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

dataset = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=transform
)

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)


# ================================================================
# Generator
# ================================================================

class Generator(nn.Module):

    def __init__(self):

        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(LATENT_DIM, 128),
            nn.ReLU(True),

            nn.Linear(128, 256),
            nn.ReLU(True),

            nn.Linear(256, 512),
            nn.ReLU(True),

            nn.Linear(512, 1024),
            nn.ReLU(True),

            nn.Linear(1024, 784),
            nn.Tanh()

        )

    def forward(self, x):

        output = self.model(x)

        output = output.view(-1, 1, 28, 28)

        return output


# ================================================================
# Discriminator
# ================================================================

class Discriminator(nn.Module):

    def __init__(self):

        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(784, 512),
            nn.LeakyReLU(0.2),

            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),

            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),

            nn.Linear(128, 1),
            nn.Sigmoid()

        )

    def forward(self, x):

        x = x.view(-1, 784)

        return self.model(x)


# ================================================================
# Create Models
# ================================================================

generator = Generator().to(DEVICE)
discriminator = Discriminator().to(DEVICE)


# ================================================================
# Loss Function
# ================================================================

criterion = nn.BCELoss()


# ================================================================
# Optimizers
# ================================================================

g_optimizer = optim.Adam(
    generator.parameters(),
    lr=LEARNING_RATE,
    betas=(0.5, 0.999)
)

d_optimizer = optim.Adam(
    discriminator.parameters(),
    lr=LEARNING_RATE,
    betas=(0.5, 0.999)
)


# ================================================================
# Create Output Folder
# ================================================================

os.makedirs("generated_images", exist_ok=True)
# ================================================================
# Training Loop
# ================================================================

print("\nStarting Training...\n")

for epoch in range(EPOCHS):

    generator.train()
    discriminator.train()

    for batch_index, (real_images, _) in enumerate(loader):

        # ------------------------------------------------------------
        # Prepare Real Images
        # ------------------------------------------------------------

        real_images = real_images.to(DEVICE)

        current_batch_size = real_images.size(0)

        real_labels = torch.ones(
            current_batch_size,
            1,
            device=DEVICE
        )

        fake_labels = torch.zeros(
            current_batch_size,
            1,
            device=DEVICE
        )

        # ============================================================
        # Train Discriminator
        # ============================================================

        d_optimizer.zero_grad()

        # ----- Real Images -----

        real_predictions = discriminator(real_images)

        real_loss = criterion(
            real_predictions,
            real_labels
        )

        # ----- Fake Images -----

        noise = torch.randn(
            current_batch_size,
            LATENT_DIM,
            device=DEVICE
        )

        fake_images = generator(noise)

        fake_predictions = discriminator(
            fake_images.detach()
        )

        fake_loss = criterion(
            fake_predictions,
            fake_labels
        )

        d_loss = real_loss + fake_loss

        d_loss.backward()

        d_optimizer.step()

        # ============================================================
        # Train Generator
        # ============================================================

        g_optimizer.zero_grad()

        noise = torch.randn(
            current_batch_size,
            LATENT_DIM,
            device=DEVICE
        )

        generated_images = generator(noise)

        predictions = discriminator(
            generated_images
        )

        # Generator wants discriminator
        # to believe fake images are REAL

        g_loss = criterion(
            predictions,
            real_labels
        )

        g_loss.backward()

        g_optimizer.step()

        # ============================================================
        # Display Training Progress
        # ============================================================

        if batch_index % 100 == 0:

            print(
                f"Epoch [{epoch + 1}/{EPOCHS}] "
                f"Batch [{batch_index}/{len(loader)}] "
                f"D Loss: {d_loss.item():.4f} "
                f"G Loss: {g_loss.item():.4f}"
            )
# ================================================================
# Training Loop
# ================================================================

print("\nStarting Training...\n")

for epoch in range(EPOCHS):

    generator.train()
    discriminator.train()

    for batch_index, (real_images, _) in enumerate(loader):

        # ------------------------------------------------------------
        # Prepare Real Images
        # ------------------------------------------------------------

        real_images = real_images.to(DEVICE)

        current_batch_size = real_images.size(0)

        real_labels = torch.ones(
            current_batch_size,
            1,
            device=DEVICE
        )

        fake_labels = torch.zeros(
            current_batch_size,
            1,
            device=DEVICE
        )

        # ============================================================
        # Train Discriminator
        # ============================================================

        d_optimizer.zero_grad()

        # ----- Real Images -----

        real_predictions = discriminator(real_images)

        real_loss = criterion(
            real_predictions,
            real_labels
        )

        # ----- Fake Images -----

        noise = torch.randn(
            current_batch_size,
            LATENT_DIM,
            device=DEVICE
        )

        fake_images = generator(noise)

        fake_predictions = discriminator(
            fake_images.detach()
        )

        fake_loss = criterion(
            fake_predictions,
            fake_labels
        )

        d_loss = real_loss + fake_loss

        d_loss.backward()

        d_optimizer.step()

        # ============================================================
        # Train Generator
        # ============================================================

        g_optimizer.zero_grad()

        noise = torch.randn(
            current_batch_size,
            LATENT_DIM,
            device=DEVICE
        )

        generated_images = generator(noise)

        predictions = discriminator(
            generated_images
        )

        # Generator wants discriminator
        # to believe fake images are REAL

        g_loss = criterion(
            predictions,
            real_labels
        )

        g_loss.backward()

        g_optimizer.step()

        # ============================================================
        # Display Training Progress
        # ============================================================

        if batch_index % 100 == 0:

            print(
                f"Epoch [{epoch + 1}/{EPOCHS}] "
                f"Batch [{batch_index}/{len(loader)}] "
                f"D Loss: {d_loss.item():.4f} "
                f"G Loss: {g_loss.item():.4f}"
            )
