# Vibe Coding Guide: Build a Residual Network Trainer with Gradio

This guide walks you through building an interactive mini-ResNet trainer for **Fashion-MNIST** using **vibe coding**. This follows on from Topic 2 (Solving Overfitting), applying residual architectures to the same Fashion-MNIST dataset. You will also learn how to deploy it to Hugging Face Spaces.

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install keras torch torchvision scikit-learn gradio matplotlib numpy datasets
```

Or if using `uv`:

```bash
uv pip install keras torch torchvision scikit-learn gradio matplotlib numpy datasets
```

---

## Step 2: Vibe Code the Residual Network Trainer

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for training a mini-ResNet on Fashion-MNIST using
Keras with PyTorch backend and Gradio. Load the dataset from HuggingFace with
load_dataset("fashion_mnist").

Dataset:
- Fashion-MNIST: 28x28 grayscale images, 10 classes
- Normalize to [0,1] and reshape to (28, 28, 1)
- Split training set into 50,000 train / 10,000 validation

Model Architecture:
- Input layer for 28x28x1 images
- Initial Conv2D layer with 32 filters (3x3), BatchNorm, ReLU
- 3 stages of residual blocks, doubling filters each stage (32 → 64 → 128)
- Each residual block: Conv2D → BatchNorm → ReLU → Conv2D → BatchNorm → Add(shortcut) → ReLU
- Use 1x1 convolution to project the shortcut when dimensions change
- Use stride=2 at the start of stages 2 and 3 to downsample
- GlobalAveragePooling2D → Dropout(0.3) → Dense(10, softmax)

Let users adjust via Gradio:
  - Optimizer (Adam, SGD, SGD + Momentum, RMSprop, AdamW)
  - Learning rate slider
  - Number of residual blocks per stage (1-4)
  - Base filters (16, 32, 48, 64)
  - Epochs slider (default 10)
  - Batch size slider (default 128)
  - Early stopping checkbox

- Show a progress bar during training
- Display accuracy/loss plots, confusion matrix, and a training summary
- The summary should show the architecture, configuration, test accuracy, and overfit gap
- Remove the Gradio flag button
```

### What You Should Get

The AI will generate a Python file (e.g., `residual-network-trainer.py`) with:

1. **Keras backend setup** -- `os.environ["KERAS_BACKEND"] = "torch"` before importing Keras
2. **Fashion-MNIST data pipeline** -- load from HuggingFace, normalize to [0,1], reshape to (28,28,1), train/val/test split
3. **Residual block function** -- reusable `residual_block(x, filters, stride)` using Functional API
4. **Mini-ResNet builder** -- 3 stages of configurable residual blocks for 28x28 grayscale input
5. **Configurable training** -- optimizer, learning rate, depth, width as parameters
6. **Evaluation** -- accuracy/loss curves + confusion matrix using sklearn
7. **Gradio UI** -- dropdowns, sliders, checkbox, plots, and text output

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Add activation selection | "Add an activation function dropdown with relu, swish, gelu" |
| Add learning rate scheduler | "Add ReduceLROnPlateau and show the learning rate changes in the plot" |
| Show model architecture | "Display the model summary and a plot_model diagram in the output" |
| Compare with plain network | "Add a checkbox to train a plain network (no skip connections) for comparison" |
| Compare with Topic 2 | "Add a simple CNN baseline (no skip connections) to show the improvement from residual blocks" |
| Add data augmentation | "Add RandomFlip and RandomRotation augmentation layers from Topic 2" |
| Add per-class accuracy | "Show per-class accuracy for all 10 Fashion-MNIST classes in the summary" |

---

## Step 4: Test Locally

Run the file:

```bash
python residual-network-trainer.py
```

Or with `uv`:

```bash
uv run residual-network-trainer.py
```

Open `http://127.0.0.1:7860` in your browser. Try these experiments:

| Experiment | Settings | What to Observe |
|---|---|---|
| Quick baseline | 2 blocks, 32 filters, Adam, 10 epochs | Good accuracy on Fashion-MNIST |
| Shallow ResNet | 1 block, 32 filters, Adam | Fast training, moderate accuracy |
| Deep ResNet | 4 blocks, 32 filters, Adam | Better accuracy, slower training |
| Wide ResNet | 2 blocks, 64 filters, Adam | More parameters, potentially better |
| SGD + Momentum | 2 blocks, 32 filters, SGD+Mom lr=0.01 | Classic training setup |
| Small + Early Stop | 2 blocks, 16 filters, Early Stop ON | Efficient, stops before overfitting |

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

```python
from huggingface_hub import HfApi
import io

api = HfApi(token="hf_YOUR_TOKEN_HERE")

# Create the Space
api.create_repo(
    repo_id="YOUR_USERNAME/residual-network-trainer",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py (your trainer file)
api.upload_file(
    path_or_fileobj="residual-network-trainer.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/residual-network-trainer",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""keras
torch
torchvision
scikit-learn
matplotlib
numpy
datasets
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/residual-network-trainer",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/residual-network-trainer")
```

Replace `YOUR_USERNAME` and `hf_YOUR_TOKEN_HERE` with your actual values.

### 5.4 Or Use the CLI

```bash
# Login
huggingface-cli login --token hf_YOUR_TOKEN_HERE

# Create space
huggingface-cli repo create residual-network-trainer --type space --space-sdk gradio

# Clone, copy files, push
git clone https://huggingface.co/spaces/YOUR_USERNAME/residual-network-trainer
cp residual-network-trainer.py residual-network-trainer/app.py
echo -e "keras\ntorch\ntorchvision\nscikit-learn\nmatplotlib\nnumpy\ndatasets" > residual-network-trainer/requirements.txt
cd residual-network-trainer
git add . && git commit -m "Add residual network trainer" && git push
```

### 5.5 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Run `app.py`
3. Serve the Gradio interface

This takes 2-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **Residual blocks solve vanishing gradients** -- skip connections allow gradients to flow directly through the network, enabling much deeper architectures
2. **Continuity from Topic 2** -- using the same Fashion-MNIST dataset lets you directly compare ResNet performance against the plain CNNs from Topic 2 (overfitting labs)
3. **Deeper is not always better** -- more blocks increase capacity but also training time; find the sweet spot for your dataset
4. **Width matters too** -- increasing base filters adds parameters and capacity without adding depth
5. **The Functional API is essential for skip connections** -- you cannot build residual blocks with Sequential because Add layers need two inputs
6. **Vibe coding** lets you build complex architectures by describing what you want and iterating on the result
