# Vibe Coding for AI: Machine Learning to AI Agents

A 2-day hands-on course covering deep learning with Keras 3 (PyTorch backend), from CNNs and RNNs to building AI Agents. All labs use a "vibe coding" workflow where you collaborate with AI assistants to build, debug, and iterate on ML code.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Basic Python programming knowledge
- Familiarity with NumPy and basic ML concepts

## Setup

### 1. Install uv (if not already installed)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and set up the project

```bash
git clone <repo-url>
cd TGS-2020503207-vibe-coding-ml
```

### 3. Install dependencies and create virtual environment

```bash
uv sync
```

This automatically creates a `.venv` with Python 3.13 and installs all dependencies (Keras 3, PyTorch, Gradio, HuggingFace, etc.).

### 4. Set up environment variables

Create a `.env` file in the project root with your HuggingFace API token:

```bash
HF_TOKEN=your_huggingface_token_here
```

### 5. Launch Jupyter

```bash
uv run jupyter notebook
```

Or open notebooks directly in VS Code with the Python extension (select the `.venv` kernel).

All notebooks use **Keras 3 with PyTorch backend**. The backend is configured automatically at the top of each notebook.

All notebooks are **Google Colab compatible** -- just upload and run.

### Notebook Variants

Each lab has two notebook versions:

| Variant | File Pattern | Description |
|---------|-------------|-------------|
| **Standard** | `lab-X-name.ipynb` | Core ML code without Gradio UI |
| **Gradio** | `lab-X-name-gradio.ipynb` | Includes interactive Gradio interface for testing |

Use the **standard** version if Gradio has issues in Colab. Use the **Gradio** version for interactive demos.

## Course Outline

### Topic 1: Vibe Coding CNNs and AI Agent Image Classifier
- Lab 1: Build a CNN from Scratch (MNIST)
- Lab 2: Image Preprocessing & Augmentation Layers (CIFAR-10)
- Lab 3: Train Image Recognition CNN with Vibe-Coding (CIFAR-10)
- Lab 4: Create an AI Agent Image Classifier

### Topic 2: Solving Overfitting Issues with Vibe Coding
- Lab 1: Diagnose Overfitting (Fashion-MNIST)
- Lab 2: Apply Overfitting Solutions
- Lab 3: Before/After Comparison Experiments

### Topic 3: Flexible ML Architectures with Vibe Coding
- Lab 1: Keras 3 Functional API Basics
- Lab 2: Multi-Input Model
- Lab 3: Skip Connections and Residual Blocks

### Topic 4: Fine Tuning with Vibe Coding
- Lab 1: Feature Extraction with Pre-trained Models
- Lab 2: Fine-Tuning Workflow
- Lab 3: High-Accuracy Transfer Learning Model
- Lab 4: Fine-Tuning with HuggingFace Models & Datasets

### Topic 5: Vibe Coding RNNs and AI Agent Chatbot
- Lab 1: TextVectorization and Embedding Layers (IMDB)
- Lab 2: Build RNN Models (LSTM, GRU, Bidirectional)
- Lab 3: Text Classification with RNN
- Lab 4: Create an AI Agent Chatbot
