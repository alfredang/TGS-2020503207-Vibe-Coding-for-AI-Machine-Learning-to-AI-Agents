# Lab 2: Image Preprocessing & Augmentation Layers


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-preprocessing-augmentation/lab-2-preprocessing-augmentation.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-preprocessing-augmentation/lab-2-preprocessing-augmentation-gradio.ipynb)

## Overview

In this lab, you will learn how to build preprocessing and data augmentation pipelines using Keras 3 built-in layers. You will work with the CIFAR-10 dataset and observe how augmentation improves model generalization. The backend is PyTorch.

## Learning Objectives

- Understand why preprocessing and augmentation are critical for image classification
- Use `keras.layers.Rescaling` and `keras.layers.Resizing` for preprocessing
- Apply augmentation layers (`RandomFlip`, `RandomRotation`, `RandomZoom`, `RandomBrightness`, `RandomContrast`)
- Integrate preprocessing and augmentation layers directly into a model
- Compare training results with and without augmentation
- Practice vibe-coding by prompting Claude to add advanced augmentation techniques

## Prerequisites

- Python 3.9+
- PyTorch installed
- Keras 3 installed (`pip install keras`)
- numpy, matplotlib
- Completion of Lab 1 (recommended)

## Steps

### Step 1: Load and Explore CIFAR-10

Load the CIFAR-10 dataset, which contains 60,000 32x32 color images across 10 classes (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck). Visualize sample images with their class names.

### Step 2: Build a Preprocessing Pipeline

Create a `keras.Sequential` pipeline with `Rescaling` and `Resizing` layers. Apply it to sample images and display before/after comparisons to verify the pipeline works correctly.

### Step 3: Build an Augmentation Pipeline

Create a `keras.Sequential` pipeline with random augmentation layers: horizontal flip, rotation, zoom, brightness, and contrast adjustments. Visualize multiple augmented versions of a single image to see the variety of transformations.

### Step 4: Integrate into a CNN Model

Combine the augmentation and preprocessing layers with Conv2D blocks into a single Sequential model. Train on CIFAR-10 for 10 epochs with augmentation applied on-the-fly during training.

### Step 5: Compare With and Without Augmentation

Train the same CNN architecture without augmentation layers and compare the learning curves side by side. Observe how augmentation affects overfitting and validation performance.

## Vibe-Coding Tips

Try these prompts with Claude to extend the lab:

- "Add RandAugment to the augmentation pipeline for stronger regularization."
- "Replace the simple CNN with a deeper architecture using residual connections."
- "Add CutMix or MixUp augmentation to the training loop."
- "Visualize what each augmentation layer does individually to a batch of images."
- "Export the preprocessing pipeline as a separate model for inference."

## How to Run

Open `lab-2-preprocessing-augmentation.ipynb` in Jupyter Notebook or JupyterLab and run the cells sequentially.
