# Lab 1: Diagnose Overfitting


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-1-diagnose-overfitting/lab-1-diagnose-overfitting.ipynb)

## Objective

Learn to identify and diagnose overfitting in neural networks by training an intentionally overfitting model on the Fashion-MNIST dataset and analyzing training curves.

## What You Will Learn

- What overfitting looks like in training vs. validation metrics
- How to build a model that is prone to overfitting (too many parameters, no regularization)
- How to read and interpret loss/accuracy curves
- How to identify the exact epoch where overfitting begins

## Prerequisites

- Python 3.13+
- Keras 3 with PyTorch backend
- Basic understanding of neural networks and classification

## Dataset

**Fashion-MNIST** -- 70,000 grayscale images (28x28) across 10 clothing categories:
T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot.

## Steps

### Step 1: Environment Setup

Install required packages (handled automatically in Google Colab) and configure Keras to use the PyTorch backend.

### Step 2: Load and Preprocess Data

- Load Fashion-MNIST via `keras.datasets`
- Normalize pixel values to [0, 1]
- Reshape for dense layers
- Split into train/validation/test sets

### Step 3: Build an Overfitting-Prone Model

Create a dense neural network that is intentionally too large for the task:
- Multiple hidden layers with many neurons (512, 512, 256, 256, 128)
- No dropout, no batch normalization, no regularization
- This creates a model with far more capacity than needed

### Step 4: Train for 30+ Epochs

- Train the model and capture the `History` object
- Use a validation split to track generalization performance
- Observe how training loss continues to decrease while validation loss increases

### Step 5: Plot Training Curves

- Plot training loss vs. validation loss
- Plot training accuracy vs. validation accuracy
- Identify the "overfitting onset point" -- the epoch where validation metrics start diverging from training metrics

### Step 6: Analyze the Gap

- Calculate the overfitting gap (train accuracy - val accuracy)
- Determine the best epoch based on validation loss
- Understand why the model overfits

### Step 7: Interactive Gradio Interface

Use a slider to select the number of training epochs and observe how overfitting develops over time.

## How to Run

1. Open `lab-1-diagnose-overfitting.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface at the end for interactive exploration

## Expected Results

- Training accuracy will approach ~99%+ after 30 epochs
- Validation accuracy will plateau around ~88-89%
- A clear divergence between training and validation curves will be visible
- The overfitting onset will typically occur around epoch 5-10
