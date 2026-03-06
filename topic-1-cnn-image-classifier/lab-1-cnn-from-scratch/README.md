# Lab 1: Build a CNN from Scratch

## Overview

In this lab, you will build your first Convolutional Neural Network (CNN) using the Keras 3 Sequential API with a PyTorch backend. You will train the model on the MNIST handwritten digit dataset and evaluate its performance. This lab introduces the vibe-coding approach -- using AI assistants like Claude to accelerate your ML workflow.

## Learning Objectives

- Understand the structure of a basic CNN (convolution, pooling, dense layers)
- Use the Keras 3 Sequential API to define a model
- Load, preprocess, and split image data for training
- Train a CNN and interpret training/validation metrics
- Visualize model predictions and learning curves
- Practice the vibe-coding mindset: describe intent, let AI generate code, then review and refine

## Prerequisites

- Python 3.9+
- PyTorch installed
- Keras 3 installed (`pip install keras`)
- numpy, matplotlib

## Steps

### Step 1: Load and Explore MNIST

Load the MNIST dataset using `keras.datasets.mnist`. Inspect the shapes of the training and test arrays and visualize a grid of 10 sample images to understand the data you are working with.

### Step 2: Preprocess Data

Normalize pixel values from [0, 255] to [0, 1]. Reshape images to include a channel dimension (28, 28, 1) for the convolution layers. One-hot encode the labels for categorical classification. Split a validation set from the training data.

### Step 3: Build the CNN Model

Construct a `keras.Sequential` model with:
- Two Conv2D + MaxPooling2D blocks (32 and 64 filters)
- A Flatten layer
- A Dense hidden layer with 64 units and ReLU activation
- A Dense output layer with 10 units and softmax activation

Print the model summary to review the architecture and parameter count.

### Step 4: Compile and Train

Compile the model with the Adam optimizer, categorical crossentropy loss, and accuracy metric. Train for 10 epochs with a validation split and store the training history.

### Step 5: Evaluate and Visualize

Plot training and validation accuracy/loss curves to check for overfitting. Evaluate the model on the held-out test set. Display 10 test images with their true and predicted labels.

## Vibe-Coding Tips

Try these prompts with Claude to extend or modify the lab:

- "Add dropout layers after each MaxPooling2D to reduce overfitting."
- "Replace the Sequential API with the Functional API and add a skip connection."
- "Add a confusion matrix visualization for the test set predictions."
- "Increase the model capacity and add batch normalization -- will it converge faster?"
- "Convert this model to use the JAX backend instead of PyTorch."

## How to Run

Open `lab-1-cnn-from-scratch.ipynb` in Jupyter Notebook or JupyterLab and run the cells sequentially.
