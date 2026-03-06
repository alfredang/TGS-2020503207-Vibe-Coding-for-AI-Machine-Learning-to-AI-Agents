# Lab 2: Multi-Input Model


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-2-multi-input-model/lab-2-multi-input-model.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-2-multi-input-model/lab-2-multi-input-model-gradio.ipynb)

## Overview

This lab demonstrates how to build models that accept multiple different inputs using the Keras Functional API. You will create a model that combines image data with synthetic metadata to improve classification accuracy on CIFAR-10.

## Learning Objectives

- Design multi-input architectures with separate processing branches
- Generate and use synthetic metadata features (mean brightness, standard deviation, edge count)
- Merge heterogeneous data streams using `Concatenate`
- Train models with dictionary-style inputs
- Compare single-input vs multi-input model performance

## Dataset

- **CIFAR-10 images**: 32x32 color images (10 classes)
- **Synthetic metadata**: Engineered features computed from each image using NumPy
  - Mean brightness
  - Standard deviation
  - Edge count (via simple gradient computation)

## Architecture

```
Image Input ──> Conv2D layers ──> GlobalAveragePooling2D ──┐
                                                           ├──> Concatenate ──> Dense ──> Output
Metadata Input ──> Dense layers ───────────────────────────┘
```

## Prerequisites

- Python 3.13+
- Keras 3 with PyTorch backend
- Completion of Lab 1 (Functional API Basics)

## How to Run

1. Open `lab-2-multi-input-model.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface to upload images and enter metadata values for predictions

## File Structure

```
lab-2-multi-input-model/
├── README.md
└── lab-2-multi-input-model.ipynb
```
