# Vibe Coding for AI: Machine Learning to AI Agents

A 2-day hands-on WSQ course covering deep learning with Keras 3 (PyTorch backend), from CNNs to RAG AI Chatbots. All labs use a "vibe coding" workflow where you collaborate with AI assistants to build, debug, and iterate on ML code.

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

## Course Outline — Open in Colab

Click any badge below to open the notebook directly in Google Colab.

### Topic 1: Vibe Coding CNNs and AI Agent Image Classifier

**CNN MNIST Trainer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/cnn-mnist-trainer)

| Lab | Open in Colab |
|-----|---------------|
| Lab 1: Build a CNN from Scratch (MNIST) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-1-cnn-from-scratch/lab-1-cnn-from-scratch.ipynb) |
| Lab 2: Train CNN with Vibe-Coding (CIFAR-10) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-2-vibe-coding-cnn/lab-2-vibe-coding-cnn.ipynb) |
| Lab 3: AI Agent Image Classifier | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-1-cnn-image-classifier/lab-3-ai-agent-image-classifier/lab-3-ai-agent-image-classifier.ipynb) |

### Topic 2: Solving Overfitting Issues with Vibe Coding

**Overfitting Explorer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/overfitting-explorer)

| Lab | Open in Colab |
|-----|---------------|
| Lab 1: Diagnose Overfitting (Fashion-MNIST) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-1-diagnose-overfitting/lab-1-diagnose-overfitting.ipynb) |
| Lab 2: Apply Overfitting Solutions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-2-overfitting-solutions/lab-2-overfitting-solutions.ipynb) |
| Lab 3: Before/After Comparison | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-2-solving-overfitting/lab-3-before-after-comparison/lab-3-before-after-comparison.ipynb) |

### Topic 3: Residual Networks with Vibe Coding

**Residual Network Trainer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/residual-network-trainer)

| Lab | Open in Colab |
|-----|---------------|
| Lab 1: Skip Connections & Residual Blocks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-3-flexible-architectures/lab-1-skip-connections/lab-1-skip-connections.ipynb) |

### Topic 4: HuggingFace Fine Tuning with Vibe Coding

**ViT Beans Trainer (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/vit-beans-trainer)

**ViT Beans Classifier (Fine-Tuned Model):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/vit-beans-classifier)

| Lab | Open in Colab |
|-----|---------------|
| Lab 1: HuggingFace Fine-Tuning (ViT + Beans) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-4-fine-tuning/lab-1-huggingface-fine-tuning/lab-1-huggingface-fine-tuning.ipynb) |

### Topic 5: RAG AI Chatbot with Vibe Coding

**RAG AI Chatbot (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/rag-ai-chatbot)

**Pocket TTS Demo (Interactive Demo):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/alfredang/pocket-tts-demo)

| Lab | Open in Colab |
|-----|---------------|
| Lab 1: RAG AI Chatbot (ChromaDB + Qwen) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rag-ai-chatbot/lab-1-rag-ai-chatbot/lab-1-rag-ai-chatbot.ipynb) |
