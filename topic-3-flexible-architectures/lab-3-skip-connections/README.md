# Lab 3: Skip Connections / Residual Blocks

## Overview

This lab explores skip connections and residual blocks, the key innovation behind ResNet architectures. You will learn why deep networks suffer from the vanishing gradient problem and how residual connections solve it, then build a mini-ResNet from scratch.

## Learning Objectives

- Understand the vanishing gradient problem in deep networks
- Implement a reusable `residual_block(x, filters)` helper function
- Build a mini-ResNet using Conv2D, BatchNormalization, Add, and ReLU
- Visualize complex architectures with `keras.utils.plot_model()`
- Compare residual networks against plain networks of equivalent depth

## Dataset

- **CIFAR-10**: 60,000 32x32 color images across 10 classes

## Architecture

```
Input ──> Conv2D ──> ResBlock(32) ──> ResBlock(64) ──> ResBlock(128) ──> GlobalAvgPool ──> Dense ──> Output
```

Each residual block contains:
```
x ──> Conv2D ──> BatchNorm ──> ReLU ──> Conv2D ──> BatchNorm ──> Add(x, shortcut) ──> ReLU
```

## Key Concepts

1. **Vanishing gradients** - Gradients shrink exponentially as they backpropagate through many layers
2. **Skip connections** - Direct pathways that allow gradients to flow unimpeded
3. **Residual learning** - Learning the residual F(x) = H(x) - x instead of H(x) directly
4. **Identity mapping** - When filters change, a 1x1 convolution projects the shortcut

## Prerequisites

- Python 3.13+
- Keras 3 with PyTorch backend
- Completion of Labs 1 and 2

## How to Run

1. Open `lab-3-skip-connections.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface to classify images with the mini-ResNet

## File Structure

```
lab-3-skip-connections/
├── README.md
└── lab-3-skip-connections.ipynb
```
