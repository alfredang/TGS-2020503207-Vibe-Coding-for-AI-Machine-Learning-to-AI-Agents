# Vibe Coding Guide: Build a ViT Fine-Tuning Trainer with Gradio

This guide walks you through building an interactive Vision Transformer (ViT) fine-tuning trainer using **vibe coding**. You will also learn how to deploy it to Hugging Face Spaces.

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install torch torchvision transformers datasets scikit-learn gradio matplotlib numpy
```

Or if using `uv`:

```bash
uv pip install torch torchvision transformers datasets scikit-learn gradio matplotlib numpy
```

---

## Step 2: Vibe Code the ViT Beans Trainer

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for fine-tuning a pre-trained Vision Transformer
(ViT) on the Beans leaf disease dataset using HuggingFace Transformers,
Datasets, and Gradio.

The app should:
- Load the "beans" dataset from HuggingFace Hub
- Use google/vit-base-patch16-224 as the pre-trained model
- Use AutoImageProcessor for preprocessing
- Use the HuggingFace Trainer API for fine-tuning
- Let users adjust via Gradio:
  - Learning rate slider
  - Number of epochs slider
  - Train batch size slider
  - Eval batch size slider
  - Warmup ratio slider
  - Weight decay slider
- Show a progress bar during training
- Display training curves (accuracy and loss), confusion matrix,
  and sample predictions with confidence scores
- Show a training summary with model info, configuration, test accuracy,
  and per-class accuracy
- Remove the Gradio flag button
```

### What You Should Get

The AI will generate a Python file (e.g., `vit-beans-trainer.py`) with:

1. **HuggingFace dataset loading** -- `load_dataset("beans")` for train/val/test splits
2. **Image preprocessing** -- `AutoImageProcessor` matched to the ViT model
3. **Pre-trained ViT model** -- loaded with `AutoModelForImageClassification`
4. **HuggingFace Trainer API** -- `TrainingArguments` + `Trainer` for fine-tuning
5. **Evaluation** -- accuracy, confusion matrix, sample predictions with confidence
6. **Gradio UI** -- sliders for hyperparameters, plots and text output

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Freeze backbone | "Add a checkbox to freeze the ViT backbone and only train the classification head" |
| Add data augmentation | "Add random horizontal flip and color jitter to the training data" |
| Show attention maps | "Visualize the attention maps from the last transformer layer" |
| Change model | "Add a dropdown to choose between vit-base, vit-small, and deit-small" |
| Add learning rate scheduler | "Add a cosine learning rate scheduler and show the lr curve" |
| Change dataset | "Add a dropdown to switch between beans, food101, and cifar10" |
| Show training time | "Add training time per epoch and total training time to the summary" |
| Export model | "Add a button to save the fine-tuned model as a .safetensors file" |

---

## Step 4: Test Locally

Run the file:

```bash
python vit-beans-trainer.py
```

Or with `uv`:

```bash
uv run vit-beans-trainer.py
```

Open `http://127.0.0.1:7860` in your browser. Try these experiments:

| Experiment | Settings | What to Observe |
|---|---|---|
| Quick test | 1 epoch, lr=2e-5, batch=16 | Fast training, decent accuracy |
| Standard | 3 epochs, lr=2e-5, batch=16 | Good accuracy (~95%+) |
| Higher LR | 3 epochs, lr=1e-4, batch=16 | May overshoot or converge faster |
| Small batch | 3 epochs, lr=2e-5, batch=4 | Slower, more gradient noise |
| More regularization | 3 epochs, lr=2e-5, decay=0.1, warmup=0.2 | More stable training |

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
    repo_id="YOUR_USERNAME/vit-beans-trainer",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py (your trainer file)
api.upload_file(
    path_or_fileobj="vit-beans-trainer.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/vit-beans-trainer",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""torch
torchvision
transformers
datasets
scikit-learn
matplotlib
numpy
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/vit-beans-trainer",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/vit-beans-trainer")
```

Replace `YOUR_USERNAME` and `hf_YOUR_TOKEN_HERE` with your actual values.

### 5.4 Or Use the CLI

```bash
# Login
huggingface-cli login --token hf_YOUR_TOKEN_HERE

# Create space
huggingface-cli repo create vit-beans-trainer --type space --space-sdk gradio

# Clone, copy files, push
git clone https://huggingface.co/spaces/YOUR_USERNAME/vit-beans-trainer
cp vit-beans-trainer.py vit-beans-trainer/app.py
echo -e "torch\ntorchvision\ntransformers\ndatasets\nscikit-learn\nmatplotlib\nnumpy" > vit-beans-trainer/requirements.txt
cd vit-beans-trainer
git add . && git commit -m "Add ViT beans trainer" && git push
```

### 5.5 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Run `app.py`
3. Serve the Gradio interface

This takes 3-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **Transfer learning is powerful** -- a pre-trained ViT achieves 95%+ accuracy on Beans with just 3 epochs of fine-tuning
2. **HuggingFace Trainer simplifies training** -- handles the training loop, evaluation, checkpointing, and mixed precision automatically
3. **AutoImageProcessor ensures correct preprocessing** -- each model expects specific image sizes, normalization values, and transforms
4. **Small datasets benefit most from fine-tuning** -- the Beans dataset has only ~1,000 images, but pre-trained features make it work
5. **Vibe coding** lets you build sophisticated fine-tuning pipelines by describing what you want and iterating on the result
