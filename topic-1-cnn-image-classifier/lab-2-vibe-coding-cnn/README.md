# Lab 2: Train Image Recognition CNN with Vibe-Coding


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-vibe-coding-cnn/lab-2-vibe-coding-cnn.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-vibe-coding-cnn/lab-2-vibe-coding-cnn-gradio.ipynb)

## Overview

This lab walks you through building a CIFAR-10 image classifier using a **vibe-coding workflow** -- an iterative approach where you prompt an AI assistant, generate code, test results, and refine until you reach your target performance. The notebook uses **Keras 3 with the PyTorch backend**.

## Prerequisites

- Python 3.9+
- Keras 3 with PyTorch backend installed
- NumPy, Matplotlib, Pandas

Install dependencies:

```bash
pip install keras torch numpy matplotlib pandas
```

## Step-by-Step Guide

### Step 1: Understand the Vibe-Coding Workflow

Read through the overview of the prompt-generate-test-refine cycle. This is the core methodology you will apply throughout the lab.

### Step 2: Build a Baseline Model

- Load and preprocess the CIFAR-10 dataset.
- Build a simple Sequential CNN with two convolutional blocks.
- Train for 10 epochs and observe the training/validation accuracy curves.
- This baseline gives you a reference point to improve upon.

### Step 3: Vibe-Coding Iteration 1 -- Improve Architecture

- Deepen the network: increase filters from 32 to 64 to 128.
- Add `BatchNormalization` after each convolutional layer.
- Replace `Flatten` with `GlobalAveragePooling2D` to reduce parameters.
- Add `Dropout` for regularisation.
- Train and compare with the baseline.

### Step 4: Vibe-Coding Iteration 2 -- Tune Hyperparameters

- Add callbacks: `EarlyStopping`, `ReduceLROnPlateau`, and `ModelCheckpoint`.
- Train for up to 30 epochs with early stopping (patience=5).
- The best model weights are saved automatically.

### Step 5: Compare All Iterations

- Build a summary table with validation accuracy for each iteration.
- Plot all training curves on a single chart to visualize improvement.

### Step 6: Save the Best Model

- Save the final model in `.keras` format.
- Verify that the saved model loads correctly and produces predictions.

## Expected Outcome

By the end of this lab you will have iteratively improved a CNN from a simple baseline to a tuned architecture, experiencing the vibe-coding workflow firsthand.
