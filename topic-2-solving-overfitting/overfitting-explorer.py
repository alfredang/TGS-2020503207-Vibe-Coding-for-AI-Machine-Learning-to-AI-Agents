"""
Overfitting Explorer — Before/After Comparison with Gradio
==========================================================
Train a baseline (overfitting) model and a regularized model on Fashion-MNIST
side by side. Choose which regularization techniques to apply and see the
difference in accuracy/loss curves.
"""

# ── 1. Import Libraries ─────────────────────────────────────────────────────
import os
os.environ["KERAS_BACKEND"] = "torch"

import keras
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gradio as gr

print(f"Keras version: {keras.__version__}")
print(f"Backend: {keras.backend.backend()}")


# ── 2. Download and Prepare Fashion-MNIST ────────────────────────────────────
(x_train_raw, y_train_raw), (x_test_raw, y_test_raw) = keras.datasets.fashion_mnist.load_data()

CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
]

# Normalize to [0, 1]
x_train_all = x_train_raw.astype("float32") / 255.0
x_test = x_test_raw.astype("float32") / 255.0

# Train/val split
x_train = x_train_all[:50000]
x_val = x_train_all[50000:]
y_train = y_train_raw[:50000]
y_val = y_train_raw[50000:]
y_test = y_test_raw

# Flat versions for dense models
x_train_flat = x_train.reshape(-1, 784)
x_val_flat = x_val.reshape(-1, 784)
x_test_flat = x_test.reshape(-1, 784)

# Image versions for CNN models (with channel dim)
x_train_img = x_train.reshape(-1, 28, 28, 1)
x_val_img = x_val.reshape(-1, 28, 28, 1)
x_test_img = x_test.reshape(-1, 28, 28, 1)

print(f"Training set:   {x_train.shape}")
print(f"Validation set: {x_val.shape}")
print(f"Test set:       {x_test.shape}")


# ── 3. Gradio Progress Callback ─────────────────────────────────────────────
class ProgressCallback(keras.callbacks.Callback):
    """Keras callback that updates a Gradio progress bar."""

    def __init__(self, progress, total_epochs, label=""):
        super().__init__()
        self.progress = progress
        self.total_epochs = total_epochs
        self.label = label

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.progress(
            (epoch + 1) / self.total_epochs,
            desc=(
                f"{self.label} — Epoch {epoch + 1}/{self.total_epochs} | "
                f"loss: {logs.get('loss', 0):.4f} | "
                f"val_loss: {logs.get('val_loss', 0):.4f} | "
                f"val_acc: {logs.get('val_accuracy', 0):.4f}"
            ),
        )


# ── 4. Model Builders ───────────────────────────────────────────────────────
def build_baseline():
    """Large dense network with NO regularization — will overfit."""
    model = keras.Sequential([
        keras.layers.Input(shape=(784,)),
        keras.layers.Dense(512, activation="relu"),
        keras.layers.Dense(512, activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, x_train_flat, x_val_flat, x_test_flat


def build_regularized(use_dropout, use_batchnorm, use_augmentation,
                       use_l2, dropout_rate, l2_factor):
    """Build a model with selected regularization techniques."""
    needs_cnn = use_augmentation
    l2_reg = keras.regularizers.l2(l2_factor) if use_l2 else None

    if needs_cnn:
        # CNN model to support data augmentation
        layers = [keras.layers.Input(shape=(28, 28, 1))]

        # Data augmentation
        layers.append(keras.layers.RandomFlip("horizontal"))
        layers.append(keras.layers.RandomRotation(0.1))

        # Conv block 1
        layers.append(keras.layers.Conv2D(32, (3, 3), padding="same",
                                          kernel_regularizer=l2_reg))
        if use_batchnorm:
            layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Activation("relu"))
        layers.append(keras.layers.MaxPooling2D((2, 2)))
        if use_dropout:
            layers.append(keras.layers.Dropout(dropout_rate * 0.5))

        # Conv block 2
        layers.append(keras.layers.Conv2D(64, (3, 3), padding="same",
                                          kernel_regularizer=l2_reg))
        if use_batchnorm:
            layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Activation("relu"))
        layers.append(keras.layers.MaxPooling2D((2, 2)))
        if use_dropout:
            layers.append(keras.layers.Dropout(dropout_rate * 0.5))

        # Dense head
        layers.append(keras.layers.Flatten())
        layers.append(keras.layers.Dense(256, kernel_regularizer=l2_reg))
        if use_batchnorm:
            layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Activation("relu"))
        if use_dropout:
            layers.append(keras.layers.Dropout(dropout_rate))

        layers.append(keras.layers.Dense(128, kernel_regularizer=l2_reg))
        if use_batchnorm:
            layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Activation("relu"))
        if use_dropout:
            layers.append(keras.layers.Dropout(dropout_rate * 0.8))

        layers.append(keras.layers.Dense(10, activation="softmax"))

        model = keras.Sequential(layers)
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return model, x_train_img, x_val_img, x_test_img
    else:
        # Dense model (no augmentation)
        layers = [keras.layers.Input(shape=(784,))]

        for units in [512, 512, 256, 256, 128]:
            layers.append(keras.layers.Dense(units, kernel_regularizer=l2_reg))
            if use_batchnorm:
                layers.append(keras.layers.BatchNormalization())
            layers.append(keras.layers.Activation("relu"))
            if use_dropout:
                layers.append(keras.layers.Dropout(dropout_rate))

        layers.append(keras.layers.Dense(10, activation="softmax"))

        model = keras.Sequential(layers)
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return model, x_train_flat, x_val_flat, x_test_flat


# ── 5. Training and Comparison ──────────────────────────────────────────────
def train_and_compare(use_dropout, use_batchnorm, use_augmentation,
                       use_l2, use_early_stopping, dropout_rate, l2_factor,
                       epochs, progress=gr.Progress()):
    """Train baseline and regularized models, return comparison plots."""
    epochs = int(epochs)

    # ── Train baseline ──────────────────────────────────────────────────
    progress(0, desc="Training baseline model (no regularization)...")
    baseline_model, bx_train, bx_val, bx_test = build_baseline()
    baseline_cb = ProgressCallback(progress, epochs, label="Baseline")

    baseline_history = baseline_model.fit(
        bx_train, y_train,
        epochs=epochs, batch_size=128,
        validation_data=(bx_val, y_val),
        callbacks=[baseline_cb],
        verbose=0,
    )

    # ── Train regularized ───────────────────────────────────────────────
    progress(0, desc="Training regularized model...")
    reg_model, rx_train, rx_val, rx_test = build_regularized(
        use_dropout, use_batchnorm, use_augmentation,
        use_l2, dropout_rate, l2_factor,
    )

    reg_callbacks = [ProgressCallback(progress, epochs, label="Regularized")]
    reg_epochs = epochs

    if use_early_stopping:
        reg_callbacks.append(keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=5,
            restore_best_weights=True, verbose=0,
        ))
        reg_epochs = epochs + 20  # allow extra room for early stopping

    reg_history = reg_model.fit(
        rx_train, y_train,
        epochs=reg_epochs, batch_size=128,
        validation_data=(rx_val, y_val),
        callbacks=reg_callbacks,
        verbose=0,
    )

    # ── Evaluate on test set ────────────────────────────────────────────
    progress(1.0, desc="Evaluating on test set...")
    b_loss, b_acc = baseline_model.evaluate(bx_test, y_test, verbose=0)
    r_loss, r_acc = reg_model.evaluate(rx_test, y_test, verbose=0)

    bh = baseline_history.history
    rh = reg_history.history

    # ── Plot 1: Accuracy comparison ─────────────────────────────────────
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    b_ep = range(1, len(bh["loss"]) + 1)
    r_ep = range(1, len(rh["loss"]) + 1)

    ax1.plot(b_ep, bh["accuracy"], "b--", label="Baseline Train", linewidth=1.5)
    ax1.plot(b_ep, bh["val_accuracy"], "r--", label="Baseline Val", linewidth=1.5)
    ax1.plot(r_ep, rh["accuracy"], "b-", label="Regularized Train", linewidth=2)
    ax1.plot(r_ep, rh["val_accuracy"], "r-", label="Regularized Val", linewidth=2)
    ax1.set_title("Accuracy: Baseline vs Regularized", fontsize=13)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0.7, 1.0])

    ax2.plot(b_ep, bh["loss"], "b--", label="Baseline Train", linewidth=1.5)
    ax2.plot(b_ep, bh["val_loss"], "r--", label="Baseline Val", linewidth=1.5)
    ax2.plot(r_ep, rh["loss"], "b-", label="Regularized Train", linewidth=2)
    ax2.plot(r_ep, rh["val_loss"], "r-", label="Regularized Val", linewidth=2)
    ax2.set_title("Loss: Baseline vs Regularized", fontsize=13)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig1.suptitle("Before/After Overfitting Comparison", fontsize=15, fontweight="bold")
    plt.tight_layout()

    # ── Plot 2: Individual curves side by side ──────────────────────────
    fig2, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Baseline
    ax = axes[0]
    ax.plot(b_ep, bh["accuracy"], "b-", label="Train Acc", linewidth=2)
    ax.plot(b_ep, bh["val_accuracy"], "r-", label="Val Acc", linewidth=2)
    b_gap = bh["accuracy"][-1] - bh["val_accuracy"][-1]
    ax.set_title(f"Baseline (No Regularization)\nGap: {b_gap:.4f}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0.7, 1.0])

    # Regularized
    ax = axes[1]
    ax.plot(r_ep, rh["accuracy"], "b-", label="Train Acc", linewidth=2)
    ax.plot(r_ep, rh["val_accuracy"], "r-", label="Val Acc", linewidth=2)
    r_gap = rh["accuracy"][-1] - rh["val_accuracy"][-1]
    ax.set_title(f"Regularized\nGap: {r_gap:.4f}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0.7, 1.0])

    plt.tight_layout()

    # ── Build techniques list ───────────────────────────────────────────
    techniques = []
    if use_dropout:
        techniques.append(f"Dropout (rate={dropout_rate})")
    if use_batchnorm:
        techniques.append("Batch Normalization")
    if use_augmentation:
        techniques.append("Data Augmentation (RandomFlip + RandomRotation)")
    if use_l2:
        techniques.append(f"L2 Regularization (factor={l2_factor})")
    if use_early_stopping:
        techniques.append(f"Early Stopping (stopped at epoch {len(rh['loss'])})")

    if not techniques:
        techniques.append("None selected — regularized model is same as baseline")

    # ── Summary text ────────────────────────────────────────────────────
    summary = (
        f"TECHNIQUES APPLIED\n"
        f"{'─' * 45}\n"
        + "\n".join(f"  - {t}" for t in techniques) + "\n"
        f"\n"
        f"BASELINE (Before)\n"
        f"{'─' * 45}\n"
        f"  Test Accuracy:  {b_acc:.4f} ({b_acc * 100:.2f}%)\n"
        f"  Test Loss:      {b_loss:.4f}\n"
        f"  Train Accuracy: {bh['accuracy'][-1]:.4f}\n"
        f"  Val Accuracy:   {bh['val_accuracy'][-1]:.4f}\n"
        f"  Overfit Gap:    {b_gap:.4f}\n"
        f"\n"
        f"REGULARIZED (After)\n"
        f"{'─' * 45}\n"
        f"  Test Accuracy:  {r_acc:.4f} ({r_acc * 100:.2f}%)\n"
        f"  Test Loss:      {r_loss:.4f}\n"
        f"  Train Accuracy: {rh['accuracy'][-1]:.4f}\n"
        f"  Val Accuracy:   {rh['val_accuracy'][-1]:.4f}\n"
        f"  Overfit Gap:    {r_gap:.4f}\n"
        f"\n"
        f"IMPROVEMENT\n"
        f"{'─' * 45}\n"
        f"  Test Acc Change:   {(r_acc - b_acc) * 100:+.2f}%\n"
        f"  Gap Reduction:     {(b_gap - r_gap) * 100:+.2f}%\n"
    )

    return fig1, fig2, summary


# ── 6. Gradio Interface ─────────────────────────────────────────────────────
demo = gr.Interface(
    fn=train_and_compare,
    inputs=[
        gr.Checkbox(value=True, label="Dropout"),
        gr.Checkbox(value=True, label="Batch Normalization"),
        gr.Checkbox(value=True, label="Data Augmentation"),
        gr.Checkbox(value=True, label="L2 Regularization"),
        gr.Checkbox(value=True, label="Early Stopping"),
        gr.Slider(minimum=0.1, maximum=0.7, value=0.5, step=0.05,
                  label="Dropout Rate"),
        gr.Slider(minimum=0.00001, maximum=0.01, value=0.0001, step=0.00001,
                  label="L2 Factor"),
        gr.Slider(minimum=5, maximum=40, value=20, step=5,
                  label="Epochs (Baseline)"),
    ],
    outputs=[
        gr.Plot(label="Before/After Comparison"),
        gr.Plot(label="Individual Accuracy Curves"),
        gr.Textbox(label="Results Summary", lines=25),
    ],
    flagging_mode="never",
    title="Overfitting Explorer — Fashion-MNIST",
    description=(
        "Compare a baseline model (no regularization) with a regularized model "
        "on Fashion-MNIST. Toggle regularization techniques on/off to see how "
        "each one affects overfitting. The baseline always trains without any "
        "regularization so you can see the before/after difference."
    ),
)

if __name__ == "__main__":
    demo.launch()
