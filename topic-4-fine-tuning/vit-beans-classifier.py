"""
ViT Beans Classifier — Interactive Gradio Interface
====================================================
Classify bean leaf images using a fine-tuned Vision Transformer (ViT).
The model was fine-tuned on the Beans dataset (3 classes: angular_leaf_spot,
bean_rust, healthy) and achieves ~97% accuracy.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from datasets import load_dataset
from PIL import Image
import gradio as gr

# ── 1. Load Fine-Tuned Model ────────────────────────────────────────────────
MODEL_REPO = "tertiaryinfotech/vit-beans-finetuned"

print(f"Loading model from {MODEL_REPO}...")
image_processor = AutoImageProcessor.from_pretrained(MODEL_REPO)
model = AutoModelForImageClassification.from_pretrained(MODEL_REPO)
model.eval()

CLASS_NAMES = list(model.config.id2label.values())
print(f"Classes: {CLASS_NAMES}")
print("Model loaded successfully!")


# ── 2. Load Sample Images from Beans Dataset ────────────────────────────────
print("Loading sample images from Beans dataset...")
beans_dataset = load_dataset("beans", split="test")
SAMPLE_IMAGES = []
for class_idx, class_name in enumerate(CLASS_NAMES):
    for sample in beans_dataset:
        if sample["labels"] == class_idx:
            SAMPLE_IMAGES.append(sample["image"])
            break


# ── 3. Classification Function ──────────────────────────────────────────────
def classify_image(image):
    """Classify a bean leaf image and return predictions with visualization."""
    if image is None:
        return None, "Please upload an image."

    # Preprocess
    image = Image.fromarray(image) if not isinstance(image, Image.Image) else image
    image = image.convert("RGB")
    inputs = image_processor(images=image, return_tensors="pt")

    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

    # Sort by confidence
    sorted_indices = torch.argsort(probs, descending=True)

    # Create bar chart
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#2ecc71" if i == sorted_indices[0] else "#3498db" for i in range(len(CLASS_NAMES))]
    bars = ax.barh(CLASS_NAMES, probs.numpy(), color=colors)
    ax.set_xlabel("Confidence", fontsize=12)
    ax.set_title("Prediction Confidence", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.3)

    # Add percentage labels
    for bar, prob in zip(bars, probs.numpy()):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{prob * 100:.1f}%", va="center", fontsize=11)

    plt.tight_layout()

    # Summary text
    pred_class = CLASS_NAMES[sorted_indices[0]]
    pred_conf = probs[sorted_indices[0]].item()

    summary_lines = [
        f"PREDICTION",
        f"{'─' * 35}",
        f"  Class:      {pred_class}",
        f"  Confidence: {pred_conf:.4f} ({pred_conf * 100:.1f}%)",
        f"",
        f"ALL SCORES",
        f"{'─' * 35}",
    ]
    for idx in sorted_indices:
        name = CLASS_NAMES[idx]
        prob = probs[idx].item()
        marker = " ◀" if idx == sorted_indices[0] else ""
        summary_lines.append(f"  {name:<20s} {prob:.4f} ({prob * 100:.1f}%){marker}")

    summary_lines.extend([
        f"",
        f"MODEL",
        f"{'─' * 35}",
        f"  {MODEL_REPO}",
        f"  Fine-tuned ViT (google/vit-base-patch16-224)",
        f"  Test accuracy: ~97%",
    ])

    return fig, "\n".join(summary_lines)


# ── 4. Gradio Interface ─────────────────────────────────────────────────────
demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(label="Upload Bean Leaf Image"),
    outputs=[
        gr.Plot(label="Prediction Confidence"),
        gr.Textbox(label="Classification Result", lines=18),
    ],
    examples=[[img] for img in SAMPLE_IMAGES] if SAMPLE_IMAGES else None,
    flagging_mode="never",
    title="Bean Leaf Disease Classifier — Fine-Tuned ViT",
    description=(
        "Upload an image of a bean leaf to classify it as **angular leaf spot**, "
        "**bean rust**, or **healthy**. This model is a Vision Transformer (ViT) "
        "fine-tuned on the [Beans dataset](https://huggingface.co/datasets/beans) "
        "from HuggingFace, achieving ~97% test accuracy."
    ),
)

if __name__ == "__main__":
    demo.launch()
