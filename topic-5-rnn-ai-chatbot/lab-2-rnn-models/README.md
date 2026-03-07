# Lab 2: Build RNN Models (LSTM, GRU, Bidirectional)


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-2-rnn-models/lab-2-rnn-models.ipynb)

## Overview

This lab explores Recurrent Neural Network architectures for sequence modeling. You will build and compare four different RNN variants -- LSTM, GRU, Bidirectional LSTM, and Stacked LSTM -- on the IMDB sentiment classification task.

## Learning Objectives

- Understand RNN fundamentals and the vanishing gradient problem
- Learn how LSTM gates (forget, input, output) control information flow
- Compare GRU as a simplified alternative to LSTM
- Apply Bidirectional wrappers for capturing both forward and backward context
- Stack RNN layers using `return_sequences=True`
- Benchmark model accuracy and training time

## Dataset

**IMDB Movie Reviews** (`keras.datasets.imdb`) -- 50,000 movie reviews for binary sentiment classification.

## Models

| Model | Architecture | Description |
|-------|-------------|-------------|
| A | Embedding -> LSTM(64) -> Dense(1) | Standard LSTM |
| B | Embedding -> GRU(64) -> Dense(1) | GRU (fewer parameters) |
| C | Embedding -> Bidirectional(LSTM(64)) -> Dense(1) | Reads sequence in both directions |
| D | Embedding -> LSTM(64, return_sequences) -> LSTM(32) -> Dense(1) | Stacked (deep) LSTM |

## Key Concepts

| Concept | Description |
|---------|-------------|
| LSTM | Long Short-Term Memory -- uses gates to maintain long-range dependencies |
| GRU | Gated Recurrent Unit -- simplified LSTM with fewer parameters |
| Bidirectional | Processes the sequence forwards and backwards, concatenating outputs |
| Stacked RNN | Multiple RNN layers; intermediate layers must use `return_sequences=True` |

## Requirements

- Python 3.13+
- Keras 3 (PyTorch backend)
- Gradio

## How to Run

1. Open `lab-2-rnn-models.ipynb` in Jupyter or Google Colab.
2. Run all cells sequentially.
3. The final section launches a Gradio interface where you can select a model and test sentiment prediction.

## References

- [Understanding LSTM Networks (Colah's Blog)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Keras LSTM Layer](https://keras.io/api/layers/recurrent_layers/lstm/)
- [Keras GRU Layer](https://keras.io/api/layers/recurrent_layers/gru/)
