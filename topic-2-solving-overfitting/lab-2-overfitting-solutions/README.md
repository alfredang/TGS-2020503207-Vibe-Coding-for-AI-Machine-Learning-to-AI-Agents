# Lab 2: Apply Overfitting Solutions

## Objective

Learn to apply various regularization techniques to combat overfitting, testing each technique individually and then combining them into a fully regularized model.

## What You Will Learn

- How Dropout prevents co-adaptation of neurons
- How Batch Normalization stabilizes training
- How data augmentation increases effective dataset size
- How Early Stopping prevents training beyond the optimal point
- How L2 regularization penalizes large weights
- How to combine multiple techniques for best results

## Prerequisites

- Completion of Lab 1 (Diagnose Overfitting)
- Python 3.13+
- Keras 3 with PyTorch backend

## Dataset

**Fashion-MNIST** -- 70,000 grayscale images (28x28) across 10 clothing categories.

## Steps

### Step 1: Environment Setup

Install required packages and configure Keras with PyTorch backend.

### Step 2: Establish Baseline

Train the same overfitting-prone model from Lab 1 to serve as a comparison baseline.

### Step 3: Apply Dropout

- Add `Dropout(0.5)` layers between dense layers
- Train and compare curves against the baseline
- Observe how dropout reduces the gap between train and val metrics

### Step 4: Apply Batch Normalization

- Add `BatchNormalization()` layers before activations
- Train and compare curves
- Observe faster convergence and mild regularization effect

### Step 5: Apply Data Augmentation

- Use `RandomFlip("horizontal")` and `RandomRotation(0.1)` layers
- Reshape data for convolutional processing (required for augmentation)
- Train and compare curves
- Observe how augmentation helps the model generalize

### Step 6: Apply Early Stopping

- Use `EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)`
- Train and observe automatic stopping at optimal epoch
- Compare final performance

### Step 7: Apply L2 Regularization

- Add `kernel_regularizer=keras.regularizers.l2(1e-4)` to dense layers
- Train and compare curves
- Observe how weight penalty reduces overfitting

### Step 8: Combine All Techniques

Build a single model that uses Dropout + BatchNormalization + Data Augmentation + L2 Regularization, trained with Early Stopping.

### Step 9: Interactive Gradio Interface

Use checkboxes to select which regularization techniques to apply, then train and view the resulting curves.

## How to Run

1. Open `lab-2-overfitting-solutions.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface at the end for interactive exploration

## Expected Results

- Each technique individually reduces overfitting compared to baseline
- Dropout typically has the largest single impact
- Data augmentation improves generalization significantly
- The combined model achieves the best validation accuracy with minimal overfitting gap
- Early Stopping prevents unnecessary training epochs
