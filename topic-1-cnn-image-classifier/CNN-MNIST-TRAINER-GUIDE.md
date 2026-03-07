# Vibe Coding Guide: Build a CNN MNIST Trainer with Gradio

This guide walks you through building an interactive CNN MNIST classifier using **vibe coding** -- describing your intent to an AI assistant (Claude) and iterating on the result. You will also learn how to deploy it to Hugging Face Spaces.

**Final Result:** [CNN MNIST Trainer on Hugging Face Spaces](https://huggingface.co/spaces/tertiaryinfotech/cnn-mnist-trainer)

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install keras torch torchvision scikit-learn gradio matplotlib numpy
```

Or if using `uv`:

```bash
uv pip install keras torch torchvision scikit-learn gradio matplotlib numpy
```

---

## Step 2: Vibe Code the CNN Trainer

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for CNN training on MNIST classification using Keras with PyTorch backend.

Include the following:
- Import libraries
- Download dataset
- Prepare the data (normalize, add channel dimension, train/val/test split)
- Setup the CNN model
- Setup optimizer and metrics
- Train the model
- Evaluate the model -- show accuracy, loss curves and confusion matrix
- Gradio interface that allows the user to:
  - Choose different optimizers (Adam, SGD, SGD + Momentum, RMSprop, AdamW)
  - Choose activation functions (relu, sigmoid, tanh, leaky_relu, elu, swish)
  - Adjust learning rate with a slider
  - Adjust epochs and batch size
  - Show a progress bar during training
  - Display accuracy/loss plots, confusion matrix, and a training summary
```

### What You Should Get

The AI will generate a Python file (e.g., `cnn-mnist-trainer.py`) with:

1. **Keras backend setup** -- `os.environ["KERAS_BACKEND"] = "torch"` before importing Keras
2. **Data pipeline** -- MNIST download, normalization to [0,1], channel dimension, train/val/test split
3. **CNN architecture** -- Conv2D + MaxPooling layers, Dense classifier head
4. **Configurable training** -- optimizer and activation as parameters
5. **Evaluation** -- accuracy/loss curves + confusion matrix using sklearn
6. **Gradio UI** -- dropdowns, sliders, plots, and text output

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Add activation selection | "Add an activation function dropdown with relu, sigmoid, tanh, leaky_relu, elu, swish" |
| Add progress bar | "Show the training progress bar in Gradio with epoch-by-epoch metrics" |
| Remove flag button | "Remove the Flag button from the Gradio interface" |
| Add more optimizers | "Add AdaGrad and Nadam to the optimizer choices" |
| Add dropout controls | "Add a slider for dropout rate and add Dropout layers to the model" |
| Change dataset | "Switch from MNIST to Fashion-MNIST" |

---

## Step 4: Test Locally

Run the file:

```bash
python cnn-mnist-trainer.py
```

Or with `uv`:

```bash
uv run cnn-mnist-trainer.py
```

Open `http://127.0.0.1:7860` in your browser. Try different combinations:

- **Adam + relu + lr=0.001** -- fast convergence, good baseline
- **SGD + relu + lr=0.01** -- slower but steady
- **SGD + sigmoid + lr=0.01** -- observe vanishing gradient effects
- **AdamW + swish + lr=0.001** -- modern combination

---

## Step 5: Deploy to Hugging Face Spaces

### 5.1 Get a Hugging Face Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token with **Write** permissions
3. Copy the token (starts with `hf_`)

### 5.2 Install Hugging Face Hub

```bash
pip install huggingface_hub
```

### 5.3 Create and Upload to a Space

You can do this with a simple Python script:

```python
from huggingface_hub import HfApi
import io

api = HfApi(token="hf_YOUR_TOKEN_HERE")

# Create the Space
api.create_repo(
    repo_id="YOUR_USERNAME/cnn-mnist-trainer",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py (your trainer file)
api.upload_file(
    path_or_fileobj="cnn-mnist-trainer.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/cnn-mnist-trainer",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""keras
torch
torchvision
scikit-learn
matplotlib
numpy
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/cnn-mnist-trainer",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/cnn-mnist-trainer")
```

Replace `YOUR_USERNAME` and `hf_YOUR_TOKEN_HERE` with your actual values.

### 5.4 Or Use the CLI

```bash
# Login
huggingface-cli login --token hf_YOUR_TOKEN_HERE

# Create space
huggingface-cli repo create cnn-mnist-trainer --type space --space-sdk gradio

# Clone, copy files, push
git clone https://huggingface.co/spaces/YOUR_USERNAME/cnn-mnist-trainer
cp cnn-mnist-trainer.py cnn-mnist-trainer/app.py
echo -e "keras\ntorch\ntorchvision\nscikit-learn\nmatplotlib\nnumpy" > cnn-mnist-trainer/requirements.txt
cd cnn-mnist-trainer
git add . && git commit -m "Add CNN MNIST trainer" && git push
```

### 5.5 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Run `app.py`
3. Serve the Gradio interface

This takes 2-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **Vibe coding** lets you describe what you want and iterate -- you don't need to memorize Keras APIs
2. **Start simple** -- get a working model first, then add features (activation selector, progress bar, etc.)
3. **Gradio** makes any ML script interactive with minimal code
4. **Hugging Face Spaces** gives you free hosting for Gradio apps -- just upload `app.py` and `requirements.txt`
5. **Experiment freely** -- try different optimizers, activations, and learning rates to build intuition
