"""
ViT Beans Trainer — Interactive Gradio Interface
=================================================
Fine-tune a Vision Transformer (ViT) on the Beans dataset using
HuggingFace Transformers and Datasets. Adjust hyperparameters via the
Gradio UI, then view evaluation metrics and sample predictions.
"""

# ── 1. Import Libraries ─────────────────────────────────────────────────────
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from datasets import load_dataset
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import gradio as gr

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ── 2. Load Beans Dataset from Hugging Face ──────────────────────────────────
dataset = load_dataset("beans")
CLASS_NAMES = dataset["train"].features["labels"].names
NUM_CLASSES = len(CLASS_NAMES)

print(f"Classes: {CLASS_NAMES}")
print(f"Train: {len(dataset['train'])}  Val: {len(dataset['validation'])}  Test: {len(dataset['test'])}")


# ── 3. Image Processor ──────────────────────────────────────────────────────
MODEL_NAME = "google/vit-base-patch16-224"
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)


def preprocess(examples):
    """Preprocess images using the ViT image processor."""
    images = [img.convert("RGB") for img in examples["image"]]
    inputs = image_processor(images=images, return_tensors="pt")
    inputs["labels"] = examples["labels"]
    return inputs


processed_dataset = dataset.with_transform(preprocess)


# ── 4. Collate and Metrics ───────────────────────────────────────────────────
def collate_fn(batch):
    """Custom collate function for the dataloader."""
    return {
        "pixel_values": torch.stack([x["pixel_values"] for x in batch]),
        "labels": torch.tensor([x["labels"] for x in batch]),
    }


def compute_metrics(eval_pred):
    """Compute accuracy for evaluation."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, predictions)}


# ── 5. Training Function ────────────────────────────────────────────────────
def train_and_evaluate(
    learning_rate, num_epochs, train_batch_size, eval_batch_size,
    warmup_ratio, weight_decay, progress=gr.Progress()
):
    """Fine-tune ViT on the Beans dataset and return evaluation results."""
    num_epochs = int(num_epochs)
    train_batch_size = int(train_batch_size)
    eval_batch_size = int(eval_batch_size)

    progress(0, desc="Loading pre-trained ViT model...")

    # Label mappings
    id2label = {i: label for i, label in enumerate(CLASS_NAMES)}
    label2id = {label: i for i, label in enumerate(CLASS_NAMES)}

    # Load model
    model = AutoModelForImageClassification.from_pretrained(
        MODEL_NAME,
        num_labels=NUM_CLASSES,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./vit-beans-finetuned",
        num_train_epochs=num_epochs,
        learning_rate=learning_rate,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        warmup_ratio=warmup_ratio,
        weight_decay=weight_decay,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=5,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        remove_unused_columns=False,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    progress(0.1, desc="Starting fine-tuning...")

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=processed_dataset["train"],
        eval_dataset=processed_dataset["validation"],
        compute_metrics=compute_metrics,
        data_collator=collate_fn,
    )

    # Train
    train_result = trainer.train()
    train_loss = train_result.metrics["train_loss"]

    progress(0.7, desc="Evaluating on test set...")

    # Evaluate on test set
    test_results = trainer.evaluate(processed_dataset["test"])
    test_acc = test_results["eval_accuracy"]
    test_loss = test_results["eval_loss"]

    # Get predictions
    predictions = trainer.predict(processed_dataset["test"])
    y_pred = np.argmax(predictions.predictions, axis=-1)
    y_true = predictions.label_ids
    probs = torch.nn.functional.softmax(
        torch.tensor(predictions.predictions), dim=-1
    ).numpy()

    progress(0.85, desc="Generating plots...")

    # ── 6. Training History Plot ─────────────────────────────────────────────
    log_history = trainer.state.log_history
    train_losses = [
        entry["loss"] for entry in log_history if "loss" in entry and "eval_loss" not in entry
    ]
    eval_entries = [entry for entry in log_history if "eval_loss" in entry]
    eval_losses = [entry["eval_loss"] for entry in eval_entries]
    eval_accs = [entry["eval_accuracy"] for entry in eval_entries]

    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    if eval_accs:
        ax1.plot(range(1, len(eval_accs) + 1), eval_accs, "b-o", label="Validation", linewidth=2)
        ax1.set_title("Validation Accuracy per Epoch", fontsize=14)
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Accuracy")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

    if train_losses:
        steps = range(1, len(train_losses) + 1)
        ax2.plot(steps, train_losses, "b-", alpha=0.6, label="Training", linewidth=1.5)
    if eval_losses:
        epoch_steps = np.linspace(1, len(train_losses), len(eval_losses)) if train_losses else range(1, len(eval_losses) + 1)
        ax2.plot(epoch_steps, eval_losses, "r-o", label="Validation", linewidth=2)
    ax2.set_title("Loss", fontsize=14)
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig1.suptitle(
        f"ViT Fine-Tuning on Beans | lr={learning_rate} | Test Acc: {test_acc:.4f}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()

    # ── 7. Confusion Matrix ──────────────────────────────────────────────────
    cm = confusion_matrix(y_true, y_pred)
    fig2, ax3 = plt.subplots(figsize=(7, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(ax=ax3, cmap="Blues", values_format="d", colorbar=False)
    ax3.set_title("Confusion Matrix on Test Set", fontsize=14)
    plt.tight_layout()

    # ── 8. Sample Predictions ────────────────────────────────────────────────
    test_raw = dataset["test"]
    np.random.seed(42)
    indices = np.random.choice(len(test_raw), 8, replace=False)

    fig3, axes = plt.subplots(2, 4, figsize=(16, 8))
    for i, ax in enumerate(axes.flat):
        idx = indices[i]
        sample = test_raw[idx]
        ax.imshow(sample["image"])
        pred_label = CLASS_NAMES[y_pred[idx]]
        true_label = CLASS_NAMES[y_true[idx]]
        confidence = probs[idx][y_pred[idx]]
        color = "green" if pred_label == true_label else "red"
        ax.set_title(
            f"Pred: {pred_label} ({confidence:.2f})\nTrue: {true_label}",
            color=color, fontsize=10,
        )
        ax.axis("off")
    fig3.suptitle("Sample Predictions on Test Set", fontsize=14)
    plt.tight_layout()

    progress(1.0, desc="Done!")

    # ── 9. Summary ───────────────────────────────────────────────────────────
    per_class_acc = cm.diagonal() / cm.sum(axis=1)
    per_class_lines = "\n".join(
        f"    {name:<25s} {acc:.4f}" for name, acc in zip(CLASS_NAMES, per_class_acc)
    )

    summary = (
        f"MODEL\n"
        f"{'─' * 40}\n"
        f"  Architecture:       Vision Transformer (ViT)\n"
        f"  Pre-trained:        {MODEL_NAME}\n"
        f"  Total Parameters:   {total_params:,}\n"
        f"  Trainable Params:   {trainable_params:,}\n"
        f"\n"
        f"CONFIGURATION\n"
        f"{'─' * 40}\n"
        f"  Learning Rate:      {learning_rate}\n"
        f"  Epochs:             {num_epochs}\n"
        f"  Train Batch Size:   {train_batch_size}\n"
        f"  Eval Batch Size:    {eval_batch_size}\n"
        f"  Warmup Ratio:       {warmup_ratio}\n"
        f"  Weight Decay:       {weight_decay}\n"
        f"  Device:             {DEVICE}\n"
        f"\n"
        f"RESULTS\n"
        f"{'─' * 40}\n"
        f"  Test Accuracy:      {test_acc:.4f} ({test_acc * 100:.2f}%)\n"
        f"  Test Loss:          {test_loss:.4f}\n"
        f"  Train Loss:         {train_loss:.4f}\n"
        f"\n"
        f"PER-CLASS ACCURACY\n"
        f"{'─' * 40}\n"
        f"{per_class_lines}\n"
    )

    return fig1, fig2, fig3, summary


# ── 10. Gradio Interface ────────────────────────────────────────────────────
demo = gr.Interface(
    fn=train_and_evaluate,
    inputs=[
        gr.Slider(
            minimum=1e-6, maximum=1e-3, value=2e-5, step=1e-6,
            label="Learning Rate",
        ),
        gr.Slider(
            minimum=1, maximum=10, value=3, step=1,
            label="Epochs",
        ),
        gr.Slider(
            minimum=4, maximum=32, value=16, step=4,
            label="Train Batch Size",
        ),
        gr.Slider(
            minimum=4, maximum=32, value=16, step=4,
            label="Eval Batch Size",
        ),
        gr.Slider(
            minimum=0.0, maximum=0.3, value=0.1, step=0.05,
            label="Warmup Ratio",
        ),
        gr.Slider(
            minimum=0.0, maximum=0.3, value=0.01, step=0.01,
            label="Weight Decay",
        ),
    ],
    outputs=[
        gr.Plot(label="Training Curves"),
        gr.Plot(label="Confusion Matrix"),
        gr.Plot(label="Sample Predictions"),
        gr.Textbox(label="Training Summary", lines=30),
    ],
    flagging_mode="never",
    title="ViT Beans Trainer — HuggingFace Fine-Tuning",
    description=(
        "Fine-tune a pre-trained Vision Transformer (google/vit-base-patch16-224) "
        "on the Beans leaf disease dataset from HuggingFace. Adjust learning rate, "
        "epochs, batch size, and regularization, then click Submit to train and evaluate."
    ),
)

if __name__ == "__main__":
    demo.launch()
