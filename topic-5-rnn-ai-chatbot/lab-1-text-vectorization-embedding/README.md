# Lab 1: TextVectorization and Embedding Layers

## Overview

This lab introduces two fundamental NLP building blocks in Keras: **TextVectorization** and **Embedding** layers. You will learn how raw text is converted into numerical sequences and then mapped to dense vector representations that neural networks can process.

## Learning Objectives

- Understand how `TextVectorization` converts raw text into integer sequences
- Configure vocabulary size and sequence length parameters
- Visualize the mapping from words to integers and back
- Build an `Embedding` layer that learns dense word representations
- Train a simple sentiment classification model on IMDB reviews

## Dataset

**IMDB Movie Reviews** (`keras.datasets.imdb`) -- 50,000 movie reviews labeled as positive or negative sentiment. We use 25,000 for training and 25,000 for testing.

## Model Architecture

```
TextVectorization (max_tokens=10000, output_sequence_length=200)
    -> Embedding (10000, 128)
    -> GlobalAveragePooling1D
    -> Dense(1, sigmoid)
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| TextVectorization | Converts raw strings to integer token sequences |
| Vocabulary | Fixed-size mapping from words to integer indices |
| Embedding | Learns a dense vector for each token in the vocabulary |
| GlobalAveragePooling1D | Averages embeddings across the sequence dimension |

## Requirements

- Python 3.13+
- Keras 3 (PyTorch backend)
- Gradio

## How to Run

1. Open `lab-1-text-vectorization-embedding.ipynb` in Jupyter or Google Colab.
2. Run all cells sequentially.
3. The final section launches a Gradio interface for interactive sentiment prediction.

## References

- [Keras TextVectorization](https://keras.io/api/layers/preprocessing_layers/text/text_vectorization/)
- [Keras Embedding Layer](https://keras.io/api/layers/core_layers/embedding/)
