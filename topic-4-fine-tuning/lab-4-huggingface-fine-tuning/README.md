# Lab 4: Fine-Tuning with HuggingFace Models & Datasets


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-4-huggingface-fine-tuning/lab-4-huggingface-fine-tuning.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-4-huggingface-fine-tuning/lab-4-huggingface-fine-tuning-gradio.ipynb)

## Overview

This lab introduces the HuggingFace ecosystem for fine-tuning pre-trained models. You will use the HuggingFace `datasets` library to load the Beans dataset, the `transformers` library to load a pre-trained Vision Transformer (ViT), and the `Trainer` API to fine-tune the model for bean leaf disease classification. This lab uses PyTorch directly via transformers (not Keras).

## Learning Objectives

- Load and explore datasets from the HuggingFace Hub
- Use AutoImageProcessor for preprocessing images to match model requirements
- Load a pre-trained Vision Transformer (ViT) for image classification
- Configure TrainingArguments for fine-tuning
- Fine-tune using the HuggingFace Trainer API
- Evaluate with accuracy and confusion matrix
- Optionally push the fine-tuned model to the HuggingFace Hub
- Build a Gradio interface for bean leaf disease classification

## Key Concepts

- **HuggingFace Hub**: A repository of pre-trained models and datasets
- **Vision Transformer (ViT)**: A transformer-based architecture for image classification
- **AutoImageProcessor**: Automatically selects the correct preprocessing for a given model
- **Trainer API**: A high-level API for training and evaluating transformers models
- **TrainingArguments**: Configuration for the training loop (epochs, learning rate, etc.)

## Dataset

- **Beans Dataset**: 3 classes of bean leaf images
  - Angular leaf spot
  - Bean rust
  - Healthy
- Small dataset (~1,000 images), free to download from HuggingFace Hub

## Model

- **google/vit-base-patch16-224**: Vision Transformer pre-trained on ImageNet-21k, fine-tuned on ImageNet-1k
- Input size: 224x224 pixels
- Patches: 16x16 pixels

## Requirements

- Python 3.13+
- PyTorch
- transformers
- datasets
- huggingface_hub
- python-dotenv
- scikit-learn
- Gradio
- NumPy, Matplotlib

## Setup

1. Create a `.env` file with your HuggingFace token:
   ```
   HF_TOKEN=hf_your_token_here
   ```
2. The token is optional for downloading public datasets/models but required for pushing to the Hub

## How to Run

1. Open `lab-4-huggingface-fine-tuning.ipynb` in Google Colab or locally
2. Run all cells sequentially
3. The final section launches a Gradio interface for interactive testing

## Expected Results

- Fine-tuned ViT should achieve ~95%+ accuracy on the Beans test set
- The model can distinguish between healthy and diseased bean leaves
- Confusion matrix shows per-class performance

## Video Tutorial Reference

This lab's workflow is based on the approach shown in:
- **[Fine-Tune an Open Source LLM with Claude Code (Hugging Face Model Trainer Skill)](https://www.youtube.com/watch?v=HGPTUc7tEq4)** by Alejandro AO
- **[We Got Claude to Fine-Tune an Open Source LLM (HuggingFace Blog)](https://huggingface.co/blog/hf-skills-training)**

The video demonstrates the HuggingFace Skills workflow where you can instruct Claude Code to fine-tune models on cloud GPUs using natural language. While this lab focuses on local fine-tuning with the Trainer API, the same concepts apply:

1. Select a pre-trained model from the HuggingFace Hub
2. Load and preprocess a dataset from HuggingFace Datasets
3. Configure training arguments (epochs, learning rate, hardware)
4. Fine-tune using the Trainer API
5. Evaluate and push the fine-tuned model to the Hub

### Bonus: HuggingFace Skills (Cloud Fine-Tuning)

For larger models or cloud-based training, you can use HuggingFace Skills with Claude Code:

```bash
# Install the skill in Claude Code
claude mcp add --transport http hf-skills https://huggingface.co/mcp?bouquet=skills --header "Authorization: Bearer $HF_TOKEN"

# Then simply ask Claude:
# "Fine-tune Qwen3-0.6B on open-r1/codeforces-cots for instruction following"
```

This supports SFT, DPO, and GRPO training methods on models from 0.5B to 70B parameters.
