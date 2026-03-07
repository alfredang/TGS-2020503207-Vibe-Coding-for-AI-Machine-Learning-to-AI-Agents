# Vibe Coding for AI: Machine Learning to AI Agents

A 2-day hands-on WSQ course covering deep learning with Keras 3 (PyTorch backend), from CNNs and RNNs to building AI Agents. All labs use a "vibe coding" workflow where you collaborate with AI assistants to build, debug, and iterate on ML code.

**Course Page:** [Tertiary Courses — WSQ Vibe Coding for AI: Machine Learning to AI Agents](https://www.tertiarycourses.com.sg/wsq-vibe-coding-for-ai-machine-learning-to-ai-agents.html)

**Apply via SkillsFuture:** [MySkillsFuture Course Directory (TGS-2020503207)](https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber=TGS-2020503207)

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

## Course Outline — Open in Colab

Click any badge below to open the notebook directly in Google Colab.

### Topic 1: Vibe Coding CNNs and AI Agent Image Classifier

**CNN MNIST Trainer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/tertiaryinfotech/cnn-mnist-trainer)

| Lab | Standard | Gradio |
|-----|----------|--------|
| Lab 1: Build a CNN from Scratch (MNIST) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-1-cnn-from-scratch/lab-1-cnn-from-scratch.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-1-cnn-from-scratch/lab-1-cnn-from-scratch-gradio.ipynb) |
| Lab 2: Train CNN with Vibe-Coding (CIFAR-10) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-vibe-coding-cnn/lab-2-vibe-coding-cnn.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-vibe-coding-cnn/lab-2-vibe-coding-cnn-gradio.ipynb) |
| Lab 3: AI Agent Image Classifier | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-3-ai-agent-image-classifier/lab-3-ai-agent-image-classifier.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-3-ai-agent-image-classifier/lab-3-ai-agent-image-classifier-gradio.ipynb) |

### Topic 2: Solving Overfitting Issues with Vibe Coding

**Overfitting Explorer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/tertiaryinfotech/overfitting-explorer)

| Lab | Standard | Gradio |
|-----|----------|--------|
| Lab 1: Diagnose Overfitting (Fashion-MNIST) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-1-diagnose-overfitting/lab-1-diagnose-overfitting.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-1-diagnose-overfitting/lab-1-diagnose-overfitting-gradio.ipynb) |
| Lab 2: Apply Overfitting Solutions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-2-overfitting-solutions/lab-2-overfitting-solutions.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-2-overfitting-solutions/lab-2-overfitting-solutions-gradio.ipynb) |
| Lab 3: Before/After Comparison | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-3-before-after-comparison/lab-3-before-after-comparison.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-3-before-after-comparison/lab-3-before-after-comparison-gradio.ipynb) |

### Topic 3: Residual Networks with Vibe Coding

| Lab | Standard | Gradio |
|-----|----------|--------|
| Lab 1: Skip Connections & Residual Blocks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-1-skip-connections/lab-1-skip-connections.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-1-skip-connections/lab-1-skip-connections-gradio.ipynb) |

### Topic 4: Fine Tuning with Vibe Coding

| Lab | Standard | Gradio |
|-----|----------|--------|
| Lab 1: Feature Extraction with Pre-trained Models | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-1-feature-extraction/lab-1-feature-extraction.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-1-feature-extraction/lab-1-feature-extraction-gradio.ipynb) |
| Lab 2: Fine-Tuning Workflow | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-2-fine-tuning-workflow/lab-2-fine-tuning-workflow.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-2-fine-tuning-workflow/lab-2-fine-tuning-workflow-gradio.ipynb) |
| Lab 3: High-Accuracy Transfer Learning | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-3-high-accuracy-transfer/lab-3-high-accuracy-transfer.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-3-high-accuracy-transfer/lab-3-high-accuracy-transfer-gradio.ipynb) |
| Lab 4: HuggingFace Fine-Tuning (ViT + Beans) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-4-huggingface-fine-tuning/lab-4-huggingface-fine-tuning.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-4-huggingface-fine-tuning/lab-4-huggingface-fine-tuning-gradio.ipynb) |

### Topic 5: Vibe Coding RNNs and AI Agent Chatbot

| Lab | Standard | Gradio |
|-----|----------|--------|
| Lab 1: TextVectorization & Embedding (IMDB) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-1-text-vectorization-embedding/lab-1-text-vectorization-embedding.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-1-text-vectorization-embedding/lab-1-text-vectorization-embedding-gradio.ipynb) |
| Lab 2: Build RNN Models (LSTM, GRU, Bidirectional) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-2-rnn-models/lab-2-rnn-models.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-2-rnn-models/lab-2-rnn-models-gradio.ipynb) |
| Lab 3: Text Classification with RNN | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-3-text-classification/lab-3-text-classification.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-3-text-classification/lab-3-text-classification-gradio.ipynb) |
| Lab 4: AI Agent Chatbot | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-4-ai-agent-chatbot/lab-4-ai-agent-chatbot.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-4-ai-agent-chatbot/lab-4-ai-agent-chatbot-gradio.ipynb) |
