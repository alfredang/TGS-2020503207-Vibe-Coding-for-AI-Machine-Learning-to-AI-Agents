# Lab 1: Feature Extraction with Pre-trained Models

## Overview

In this lab, you will learn how to use pre-trained models as feature extractors for image classification. Instead of training a deep neural network from scratch, you will leverage MobileNetV2 (pre-trained on ImageNet) and only train a small classification head on top. This technique is called **feature extraction** and is one of the most common forms of transfer learning.

## Learning Objectives

- Understand the concept of transfer learning and feature extraction
- Load a pre-trained MobileNetV2 model without the top classification layer
- Freeze the base model weights to prevent them from updating during training
- Add a custom classification head for binary classification
- Train only the new head layers on CIFAR-10 data (airplane vs automobile)
- Compare feature extraction performance against training from scratch
- Build a Gradio interface for interactive image classification

## Key Concepts

- **Transfer Learning**: Reusing a model trained on one task for a different but related task
- **Feature Extraction**: Using the learned representations from a pre-trained model without modifying them
- **Frozen Layers**: Setting `trainable = False` on layers to prevent weight updates during training
- **Classification Head**: A small set of layers added on top of a feature extractor for a specific task

## Architecture

```
Input Image (32x32x3) -> Resize to (96x96x3)
    -> MobileNetV2 (frozen, no top) -> Feature Maps
    -> GlobalAveragePooling2D -> 1280-dim vector
    -> Dropout(0.2)
    -> Dense(1, sigmoid) -> Binary Classification
```

## Dataset

- **CIFAR-10** (subset): Only airplane (class 0) and automobile (class 1)
- Training: ~10,000 images
- Testing: ~2,000 images

## Requirements

- Python 3.13+
- Keras 3 with PyTorch backend
- torchvision
- Gradio
- NumPy, Matplotlib

## How to Run

1. Open `lab-1-feature-extraction.ipynb` in Google Colab or locally
2. Run all cells sequentially
3. The final section launches a Gradio interface for interactive testing

## Expected Results

- Feature extraction model should achieve ~90%+ accuracy in just 5 epochs
- Training from scratch (same architecture but random weights) will achieve significantly lower accuracy in the same number of epochs
