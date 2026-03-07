# Lab 2: Fine-Tuning Workflow


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-2-fine-tuning-workflow/lab-2-fine-tuning-workflow.ipynb)

## Overview

This lab extends the feature extraction approach from Lab 1 by introducing a complete fine-tuning workflow. After training a classification head on frozen features, you will selectively unfreeze top layers of the base model and continue training with a very low learning rate. This allows the pre-trained features to adapt to your specific dataset while avoiding catastrophic forgetting.

## Learning Objectives

- Implement a multi-phase fine-tuning workflow
- Understand why we train the head first before unfreezing layers
- Use a reduced learning rate for fine-tuning to avoid destroying pre-trained features
- Apply EarlyStopping and ReduceLROnPlateau callbacks
- Visualize and compare learning curves across training phases
- Experiment with unfreezing different numbers of layers

## Key Concepts

- **Fine-Tuning**: Unfreezing some or all layers of a pre-trained model and retraining with a low learning rate
- **Catastrophic Forgetting**: When fine-tuning destroys previously learned representations
- **Learning Rate Scheduling**: Reducing the learning rate during training to find better optima
- **EarlyStopping**: Halting training when validation performance stops improving
- **ReduceLROnPlateau**: Automatically reducing learning rate when metrics plateau

## Training Phases

1. **Phase 1 - Feature Extraction**: Freeze base model, train only the classification head (5 epochs)
2. **Phase 2 - Fine-Tuning**: Unfreeze top layers, recompile with Adam(lr=1e-5), train (10 epochs)
3. **Phase 3 - Fine-Tuning with Callbacks**: Continue training with EarlyStopping and ReduceLROnPlateau

## Dataset

- **CIFAR-10** (subset): Airplane (class 0) vs Automobile (class 1)
- Same binary classification task as Lab 1

## Requirements

- Python 3.13+
- Keras 3 with PyTorch backend
- torchvision
- Gradio
- NumPy, Matplotlib

## How to Run

1. Open `lab-2-fine-tuning-workflow.ipynb` in Google Colab or locally
2. Run all cells sequentially
3. The final section launches a Gradio interface for interactive testing

## Expected Results

- Phase 1 (feature extraction) establishes a strong baseline
- Phase 2 (fine-tuning) further improves accuracy by 1-3%
- Fine-tuning with callbacks prevents overfitting and finds optimal stopping point
