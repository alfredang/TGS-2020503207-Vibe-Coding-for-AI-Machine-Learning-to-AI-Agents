# Lab 3: High-Accuracy Transfer Learning Model

## Overview

This lab builds a complete, production-quality transfer learning pipeline using MobileNetV2 on the full CIFAR-10 dataset (10 classes). You will incorporate data augmentation, a structured training pipeline, comprehensive evaluation metrics, and model saving. The goal is to achieve the highest possible accuracy through best practices in transfer learning.

## Learning Objectives

- Build a complete transfer learning pipeline with data augmentation
- Train on the full CIFAR-10 dataset with 10 classes
- Evaluate model performance using confusion matrices and classification reports
- Visualize correct and incorrect predictions to understand model behavior
- Save and load trained models
- Build a Gradio interface displaying top-5 predictions with confidence scores

## Key Concepts

- **Data Augmentation**: Applying random transformations (flip, rotation, zoom) to increase effective dataset size
- **Confusion Matrix**: A table showing true vs predicted labels for all classes
- **Classification Report**: Per-class precision, recall, and F1-score
- **Top-K Predictions**: Showing the K most likely classes with their confidence scores

## Pipeline Architecture

```
Input Image (32x32x3) -> Resize to (96x96x3)
    -> Data Augmentation (RandomFlip, RandomRotation, RandomZoom)
    -> MobileNetV2 (frozen/fine-tuned, no top) -> Feature Maps
    -> GlobalAveragePooling2D -> 1280-dim vector
    -> Dropout(0.3)
    -> Dense(128, relu)
    -> Dropout(0.2)
    -> Dense(10, softmax) -> 10-class Classification
```

## Dataset

- **CIFAR-10** (full): 10 classes (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)
- Training: 50,000 images
- Testing: 10,000 images

## Requirements

- Python 3.13+
- Keras 3 with PyTorch backend
- torchvision
- scikit-learn
- Gradio
- NumPy, Matplotlib, Seaborn

## How to Run

1. Open `lab-3-high-accuracy-transfer.ipynb` in Google Colab or locally
2. Run all cells sequentially
3. The final section launches a Gradio interface for interactive testing

## Expected Results

- Feature extraction baseline: ~85-90% accuracy on full CIFAR-10
- After fine-tuning: ~90-93% accuracy
- Confusion matrix reveals which classes are most commonly confused
