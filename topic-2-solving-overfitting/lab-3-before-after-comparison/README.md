# Lab 3: Before/After Comparison


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-3-before-after-comparison/lab-3-before-after-comparison.ipynb)

## Objective

Conduct a systematic comparison of multiple model variants to quantify the impact of different regularization strategies, visualize results side-by-side, and build an interactive prediction tool.

## What You Will Learn

- How to systematically compare model architectures
- How to create informative multi-panel comparison plots
- How to build summary tables with key metrics
- How to interpret confidence scores across model variants
- How different regularization strategies affect prediction quality

## Prerequisites

- Completion of Lab 1 and Lab 2
- Python 3.13+
- Keras 3 with PyTorch backend

## Dataset

**Fashion-MNIST** -- 70,000 grayscale images (28x28) across 10 clothing categories.

## Model Variants

1. **Baseline** -- Large dense network with no regularization (overfits heavily)
2. **Dropout Only** -- Baseline + Dropout(0.5) layers
3. **Augmentation Only** -- CNN with data augmentation (RandomFlip, RandomRotation)
4. **All Combined** -- CNN with Dropout + BatchNorm + Data Augmentation + L2 Regularization + Early Stopping

## Steps

### Step 1: Environment Setup

Install required packages and configure Keras with PyTorch backend.

### Step 2: Prepare Data

Load Fashion-MNIST and prepare both flat and image-shaped versions for different model architectures.

### Step 3: Define and Train All Four Variants

Train each model variant for a consistent number of epochs, capturing training histories.

### Step 4: Plot 2x2 Learning Curves Grid

Create a 2x2 subplot grid showing training vs. validation loss and accuracy curves for each variant side by side.

### Step 5: Create Summary Table

Build a pandas DataFrame summarizing:
- Best validation accuracy
- Overfitting gap (final train accuracy - final val accuracy)
- Best epoch (based on validation loss)
- Total trainable parameters

### Step 6: Interactive Gradio Interface

- Dropdown to select a model variant
- Display sample predictions with confidence bars
- Show the model's prediction alongside the true label

## How to Run

1. Open `lab-3-before-after-comparison.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface at the end to compare predictions across models

## Expected Results

| Model Variant | Val Accuracy | Overfitting Gap |
|---|---|---|
| Baseline | ~88% | ~10-12% |
| Dropout Only | ~89% | ~3-5% |
| Augmentation Only | ~90% | ~2-4% |
| All Combined | ~91% | ~1-2% |

The combined model should achieve the highest validation accuracy with the smallest overfitting gap, demonstrating that multiple regularization techniques work synergistically.
