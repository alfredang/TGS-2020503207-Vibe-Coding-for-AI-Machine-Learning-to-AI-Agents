# Vibe Coding Guide: Build an Overfitting Explorer with Gradio

This guide walks you through building an interactive overfitting before/after comparison tool using **vibe coding**. You will also learn how to deploy it to Hugging Face Spaces.

**Final Result:** [Overfitting Explorer on Hugging Face Spaces](https://huggingface.co/spaces/tertiaryinfotech/overfitting-explorer)

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install keras torch torchvision gradio matplotlib numpy
```

Or if using `uv`:

```bash
uv pip install keras torch torchvision gradio matplotlib numpy
```

---

## Step 2: Vibe Code the Overfitting Explorer

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for exploring overfitting solutions on Fashion-MNIST
using Keras with PyTorch backend and Gradio.

The app should:
- Use a Dense (fully connected) neural network as the baseline (784→512→512→256→256→128→10)
- Train TWO models side by side: a baseline (no regularization) and a regularized model
- The baseline always trains without any regularization so users can see the "before"
- Let users toggle these regularization techniques on/off via checkboxes:
  - Dropout (with adjustable dropout rate slider)
  - Batch Normalization
  - Data Augmentation (RandomFlip + RandomRotation — switches to CNN architecture)
  - L2 Regularization (with adjustable L2 factor slider)
  - Early Stopping
- Show a progress bar during training for both models
- Display two plots:
  1. Overlay comparison: baseline vs regularized accuracy and loss curves
  2. Side-by-side individual accuracy curves showing overfitting gap for each
- Show a text summary with:
  - The model architecture
  - Which techniques were applied
  - Baseline test accuracy, train/val accuracy, and overfitting gap
  - Regularized test accuracy, train/val accuracy, and overfitting gap
  - Improvement (test accuracy change and gap reduction)
- Add an epochs slider to control training length
- Remove the Gradio flag button
```

### What You Should Get

The AI will generate a Python file (e.g., `overfitting-explorer.py`) with:

1. **Keras backend setup** -- `os.environ["KERAS_BACKEND"] = "torch"` before importing Keras
2. **Fashion-MNIST data pipeline** -- download, normalize to [0,1], flat (784) and image (28x28x1) versions, train/val/test split
3. **Baseline model** -- large dense network (784→512→512→256→256→128→10) with no regularization
4. **Regularized model builder** -- dynamically adds Dropout, BatchNorm, L2, and Data Augmentation based on user selections. When augmentation is enabled, switches to a CNN architecture
5. **Side-by-side training** -- both models train and results are compared
6. **Visualization** -- overlay and individual accuracy/loss curves
7. **Gradio UI** -- checkboxes, sliders, plots, and summary text

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Add confusion matrix | "Add a confusion matrix comparison for baseline vs regularized models" |
| Add more techniques | "Add learning rate scheduling as a checkbox option" |
| Show model summary | "Display the model architecture summary for both models in the output" |
| Add per-class accuracy | "Show per-class accuracy comparison between baseline and regularized" |
| Change dataset | "Switch from Fashion-MNIST to CIFAR-10" |
| Add sample predictions | "Show 10 sample predictions from both models side by side" |

---

## Step 4: Test Locally

Run the file:

```bash
python overfitting-explorer.py
```

Or with `uv`:

```bash
uv run overfitting-explorer.py
```

Open `http://127.0.0.1:7860` in your browser. Try these experiments:

| Experiment | Settings | What to Observe |
|---|---|---|
| No regularization | All checkboxes OFF | Regularized = baseline, large gap |
| Dropout only | Dropout ON, rate=0.5 | Gap shrinks, training acc drops |
| BatchNorm only | BatchNorm ON | Faster convergence, slight regularization |
| Augmentation only | Augmentation ON | Switches to CNN, better generalization |
| L2 only | L2 ON, factor=0.001 | Weights stay small, mild gap reduction |
| Early Stopping only | Early Stopping ON | Training halts before overfitting worsens |
| All combined | Everything ON | Smallest gap, best generalization |

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
    repo_id="YOUR_USERNAME/overfitting-explorer",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py (your explorer file)
api.upload_file(
    path_or_fileobj="overfitting-explorer.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/overfitting-explorer",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""keras
torch
torchvision
matplotlib
numpy
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/overfitting-explorer",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/overfitting-explorer")
```

Replace `YOUR_USERNAME` and `hf_YOUR_TOKEN_HERE` with your actual values.

### 5.4 Or Use the CLI

```bash
# Login
huggingface-cli login --token hf_YOUR_TOKEN_HERE

# Create space
huggingface-cli repo create overfitting-explorer --type space --space-sdk gradio

# Clone, copy files, push
git clone https://huggingface.co/spaces/YOUR_USERNAME/overfitting-explorer
cp overfitting-explorer.py overfitting-explorer/app.py
echo -e "keras\ntorch\ntorchvision\nmatplotlib\nnumpy" > overfitting-explorer/requirements.txt
cd overfitting-explorer
git add . && git commit -m "Add overfitting explorer" && git push
```

### 5.5 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Run `app.py`
3. Serve the Gradio interface

This takes 2-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **Before/after comparison** is the best way to understand regularization -- seeing both models trained together makes the impact clear
2. **Each technique targets overfitting differently** -- Dropout prevents co-adaptation, BatchNorm stabilizes training, Data Augmentation increases effective training data, L2 penalizes large weights, Early Stopping halts before overfitting
4. **Combining techniques** usually gives the best results -- they complement each other
5. **The overfitting gap** (train accuracy - val accuracy) is the key metric to watch, not just accuracy
6. **Vibe coding** lets you build complex ML comparison tools by describing what you want and iterating
