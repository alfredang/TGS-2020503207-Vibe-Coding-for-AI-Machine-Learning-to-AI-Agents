# Lab 3: AI Agent Image Classifier


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-3-ai-agent-image-classifier/lab-3-ai-agent-image-classifier.ipynb)

## Overview

This lab demonstrates how to wrap a trained CNN inside an **AI agent** that can perceive images, reason about predictions, and take actions based on confidence thresholds. The notebook uses **Keras 3 with the PyTorch backend**.

## Prerequisites

- Python 3.9+
- Keras 3 with PyTorch backend installed
- NumPy, Matplotlib
- Completion of Lab 2 (or willingness to train a quick model in this notebook)

Install dependencies:

```bash
pip install keras torch numpy matplotlib
```

## Step-by-Step Guide

### Step 1: Understand AI Agents

Learn the **perception-reasoning-action** loop that defines an AI agent:
- **Perception:** The agent receives an image as input.
- **Reasoning:** The agent runs the image through a CNN and interprets the predictions.
- **Action:** The agent returns a natural language response with its classification.

### Step 2: Load the Trained Model

Load the model saved in Lab 2, or train a quick CIFAR-10 CNN from scratch within this notebook.

### Step 3: Build the classify_image Tool

Create a standalone function that:
- Preprocesses an input image.
- Runs inference through the CNN.
- Returns the top-3 predictions with confidence scores.

### Step 4: Build the Agent Class

Implement `ImageClassifierAgent` with:
- A tool registry mapping tool names to callable functions.
- A `process_request()` method that parses requests and dispatches to the correct tool.
- A `classify()` method that formats results into natural language.

### Step 5: Test the Agent

Run the agent on multiple CIFAR-10 test images and review its responses.

### Step 6: Add Confidence Thresholds

Enhance the agent to express uncertainty when the top prediction has low confidence (below 0.5). Add a `describe_prediction()` method that provides reasoning about the classification.

### Step 7: Vibe-Coding Challenge

Use the vibe-coding workflow to extend the agent with a second tool (e.g., a similarity search tool).

## Expected Outcome

By the end of this lab you will have a working AI agent that classifies CIFAR-10 images, explains its reasoning, and handles uncertainty gracefully.
