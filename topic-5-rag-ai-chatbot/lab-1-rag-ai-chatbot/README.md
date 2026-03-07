# Lab 1: RAG AI Chatbot with ChromaDB and Qwen


## Open in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rag-ai-chatbot/lab-1-rag-ai-chatbot/lab-1-rag-ai-chatbot.ipynb)

## Overview

This lab introduces Retrieval-Augmented Generation (RAG) by building a chatbot that answers questions using your own documents. You will use ChromaDB as a vector database for document storage and retrieval, and HuggingFace's Qwen2.5-72B-Instruct model for generating responses.

## Learning Objectives

- Understand the RAG (Retrieval-Augmented Generation) pattern
- Use ChromaDB for vector storage and similarity search
- Split documents into overlapping chunks for retrieval
- Build prompts that combine retrieved context with user questions
- Use HuggingFace InferenceClient to call large language models
- Implement multi-turn conversation with context

## Key Concepts

- **RAG**: Retrieval-Augmented Generation -- retrieve relevant documents, then generate answers using that context
- **ChromaDB**: An open-source vector database for storing and querying embeddings
- **Embeddings**: Dense vector representations of text used for similarity search
- **Chunking**: Splitting documents into smaller pieces with overlap for better retrieval
- **InferenceClient**: HuggingFace's API client for calling hosted models

## Architecture

```
User Question
     |
     v
[ChromaDB] --> Retrieve relevant chunks
     |
     v
[Build Prompt] = System message + Context + Chat history + Question
     |
     v
[Qwen2.5-72B-Instruct] --> Generate answer
     |
     v
Response with source attribution
```

## Requirements

- Python 3.13+
- chromadb
- huggingface_hub
- python-dotenv

## Setup

1. Create a `.env` file with your HuggingFace token:
   ```
   HF_TOKEN=hf_your_token_here
   ```
2. The token is required for calling the Qwen model via HuggingFace Inference API

## How to Run

1. Open `lab-1-rag-ai-chatbot.ipynb` in Google Colab or locally
2. Run all cells sequentially
3. Upload documents and ask questions about them

## Expected Results

- The chatbot retrieves relevant document chunks for each question
- Responses cite which source documents were used
- Multi-turn conversation maintains context across questions
- Without documents, the model answers from general knowledge
