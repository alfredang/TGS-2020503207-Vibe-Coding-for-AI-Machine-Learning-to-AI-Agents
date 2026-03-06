# Lab 3: Text Classification with RNN


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-3-text-classification/lab-3-text-classification.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-3-text-classification/lab-3-text-classification-gradio.ipynb)

## Overview

This lab builds a complete, end-to-end text classification pipeline that accepts raw text strings as input. By embedding the `TextVectorization` layer directly inside the model, the final saved model can be deployed without any external preprocessing.

## Learning Objectives

- Build an end-to-end model with TextVectorization inside the Keras model
- Apply Bidirectional LSTM with Dropout for regularization
- Use EarlyStopping to prevent overfitting
- Plot and interpret learning curves (loss and accuracy)
- Evaluate model performance with sample predictions and confidence scores
- Save and reload the complete model for deployment

## Dataset

**IMDB Movie Reviews** (`keras.datasets.imdb`) -- 50,000 movie reviews for binary sentiment classification.

## Model Architecture

```
Input (raw text string)
    -> TextVectorization (max_tokens=10000, output_sequence_length=200)
    -> Embedding (10000, 128)
    -> Bidirectional(LSTM(64))
    -> Dropout(0.5)
    -> Dense(1, sigmoid)
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| End-to-end model | TextVectorization is part of the model graph, not a separate step |
| EarlyStopping | Halts training when validation loss stops improving |
| Dropout | Randomly zeroes neuron outputs during training to reduce overfitting |
| Confidence score | Sigmoid output interpreted as probability of positive sentiment |

## Requirements

- Python 3.13+
- Keras 3 (PyTorch backend)
- Gradio

## How to Run

1. Open `lab-3-text-classification.ipynb` in Jupyter or Google Colab.
2. Run all cells sequentially.
3. The model is saved to `imdb_sentiment_model.keras` for use in Lab 4.
4. The final section launches a Gradio interface for interactive testing with confidence visualization.

## References

- [Keras EarlyStopping Callback](https://keras.io/api/callbacks/early_stopping/)
- [Keras Save and Load Models](https://keras.io/guides/serialization_and_saving/)
