# Lab 1: Functional API Basics


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-1-functional-api-basics/lab-1-functional-api-basics.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-1-functional-api-basics/lab-1-functional-api-basics-gradio.ipynb)

## Overview

This lab introduces the Keras Functional API as a flexible alternative to the Sequential API. You will learn how to build complex model architectures that go beyond simple layer stacking, including models with branching and merging paths.

## Learning Objectives

- Understand the limitations of the Sequential API
- Build models using `keras.Input` and `keras.Model` with the Functional API
- Visualize model architectures using `keras.utils.plot_model()`
- Create branching architectures with parallel convolutional paths merged via `Concatenate`

## Dataset

- **CIFAR-10**: 60,000 32x32 color images across 10 classes (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)

## Key Concepts

1. **Sequential API** - Linear stack of layers; simple but limited to single-input, single-output models
2. **Functional API** - Graph-based model construction allowing arbitrary topologies
3. **Branching architectures** - Multiple parallel processing paths that merge results

## Prerequisites

- Python 3.13+
- Keras 3 with PyTorch backend
- Basic understanding of CNNs (Topic 2)

## How to Run

1. Open `lab-1-functional-api-basics.ipynb` in Google Colab or Jupyter
2. Run all cells sequentially
3. Use the Gradio interface in the final section to classify CIFAR-10 images interactively

## File Structure

```
lab-1-functional-api-basics/
├── README.md
└── lab-1-functional-api-basics.ipynb
```
