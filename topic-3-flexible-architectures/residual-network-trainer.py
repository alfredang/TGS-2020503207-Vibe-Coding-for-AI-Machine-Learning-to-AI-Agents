"""
Residual Network Trainer — Interactive Gradio Interface
=======================================================
Train a mini-ResNet on CIFAR-10 using Keras with PyTorch backend.
Adjust depth, filters, learning rate, optimizer, and more via the Gradio UI.
"""

# ── 1. Import Libraries ─────────────────────────────────────────────────────
import os
os.environ["KERAS_BACKEND"] = "torch"

import keras
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import gradio as gr

print(f"Keras version: {keras.__version__}")
print(f"Backend: {keras.backend.backend()}")


# ── 2. Download and Prepare CIFAR-10 ──────────────────────────────────────
(x_train_raw, y_train_raw), (x_test_raw, y_test_raw) = keras.datasets.cifar10.load_data()

CLASS_NAMES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck",
]

# Normalize to [0, 1]
x_train_all = x_train_raw.astype("float32") / 255.0
x_test = x_test_raw.astype("float32") / 255.0

# Train/val split
x_train = x_train_all[:45000]
y_train = y_train_raw[:45000]
x_val = x_train_all[45000:]
y_val = y_train_raw[45000:]
y_test = y_test_raw

NUM_CLASSES = 10

print(f"Training set:   {x_train.shape}")
print(f"Validation set: {x_val.shape}")
print(f"Test set:       {x_test.shape}")


# ── 3. Gradio Progress Callback ──────────────────────────────────────────
class GradioProgressCallback(keras.callbacks.Callback):
    """Keras callback that updates a Gradio progress bar each epoch."""

    def __init__(self, progress, total_epochs):
        super().__init__()
        self.progress = progress
        self.total_epochs = total_epochs

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.progress(
            (epoch + 1) / self.total_epochs,
            desc=(
                f"Epoch {epoch + 1}/{self.total_epochs} — "
                f"loss: {logs.get('loss', 0):.4f} | "
                f"acc: {logs.get('accuracy', 0):.4f} | "
                f"val_loss: {logs.get('val_loss', 0):.4f} | "
                f"val_acc: {logs.get('val_accuracy', 0):.4f}"
            ),
        )


# ── 4. Residual Block Builder ─────────────────────────────────────────────
def residual_block(x, filters, stride=1):
    """Build a single residual block with two Conv2D layers and a skip connection."""
    shortcut = x

    # Main path
    out = keras.layers.Conv2D(filters, (3, 3), strides=stride, padding="same",
                               use_bias=False)(x)
    out = keras.layers.BatchNormalization()(out)
    out = keras.layers.ReLU()(out)

    out = keras.layers.Conv2D(filters, (3, 3), strides=1, padding="same",
                               use_bias=False)(out)
    out = keras.layers.BatchNormalization()(out)

    # Shortcut path — project if dimensions change
    if stride != 1 or x.shape[-1] != filters:
        shortcut = keras.layers.Conv2D(filters, (1, 1), strides=stride,
                                        padding="same", use_bias=False)(x)
        shortcut = keras.layers.BatchNormalization()(shortcut)

    out = keras.layers.Add()([out, shortcut])
    out = keras.layers.ReLU()(out)
    return out


# ── 5. Model Builder ──────────────────────────────────────────────────────
def build_resnet(num_blocks, base_filters, activation="relu"):
    """Build a mini-ResNet with configurable depth and width."""
    inputs = keras.layers.Input(shape=(32, 32, 3))

    # Initial convolution
    x = keras.layers.Conv2D(base_filters, (3, 3), padding="same", use_bias=False)(inputs)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)

    # Residual stages — each stage doubles the filters and halves spatial dims
    filters = base_filters
    for stage in range(3):
        for block in range(num_blocks):
            stride = 2 if (stage > 0 and block == 0) else 1
            x = residual_block(x, filters, stride=stride)
        filters *= 2

    # Classification head
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.3)(x)
    outputs = keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="mini_resnet")
    return model


# ── 6. Training Function ──────────────────────────────────────────────────
def train_and_evaluate(optimizer_name, learning_rate, num_blocks, base_filters,
                        epochs, batch_size, use_early_stopping,
                        progress=gr.Progress()):
    """Train ResNet with chosen hyperparameters and return evaluation plots."""
    epochs = int(epochs)
    batch_size = int(batch_size)
    num_blocks = int(num_blocks)
    base_filters = int(base_filters)

    # Setup optimizer
    optimizers = {
        "Adam": keras.optimizers.Adam,
        "SGD": keras.optimizers.SGD,
        "SGD + Momentum": lambda lr: keras.optimizers.SGD(learning_rate=lr, momentum=0.9),
        "RMSprop": keras.optimizers.RMSprop,
        "AdamW": keras.optimizers.AdamW,
    }

    if optimizer_name == "SGD + Momentum":
        optimizer = optimizers[optimizer_name](learning_rate)
    else:
        optimizer = optimizers.get(optimizer_name, keras.optimizers.Adam)(
            learning_rate=learning_rate
        )

    # Build and compile
    model = build_resnet(num_blocks, base_filters)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Count parameters
    total_params = model.count_params()

    # Callbacks
    progress(0, desc="Starting training...")
    callbacks = [GradioProgressCallback(progress, epochs)]

    if use_early_stopping:
        callbacks.append(keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=5,
            restore_best_weights=True, verbose=0,
        ))

    # Train
    history = model.fit(
        x_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        callbacks=callbacks,
        verbose=0,
    )

    # ── 7. Evaluate ──────────────────────────────────────────────────────
    progress(1.0, desc="Evaluating on test set...")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    h = history.history
    epochs_range = range(1, len(h["loss"]) + 1)

    # ── 8. Plot accuracy and loss curves ─────────────────────────────────
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.plot(epochs_range, h["accuracy"], "b-", label="Training", linewidth=2)
    ax1.plot(epochs_range, h["val_accuracy"], "r-", label="Validation", linewidth=2)
    ax1.set_title("Model Accuracy", fontsize=14)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(epochs_range, h["loss"], "b-", label="Training", linewidth=2)
    ax2.plot(epochs_range, h["val_loss"], "r-", label="Validation", linewidth=2)
    ax2.set_title("Model Loss", fontsize=14)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig1.suptitle(
        f"Mini-ResNet ({num_blocks} blocks, {base_filters} base filters) | "
        f"{optimizer_name} (lr={learning_rate}) | "
        f"Test Acc: {test_acc:.4f}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()

    # ── 9. Confusion matrix ──────────────────────────────────────────────
    y_pred = np.argmax(model.predict(x_test, verbose=0), axis=1)
    cm = confusion_matrix(y_test, y_pred)

    fig2, ax3 = plt.subplots(figsize=(8, 7))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(ax=ax3, cmap="Blues", values_format="d", colorbar=False)
    ax3.set_title("Confusion Matrix on Test Set", fontsize=14)
    plt.tight_layout()

    # ── 10. Architecture description ─────────────────────────────────────
    arch_lines = []
    arch_lines.append(f"Input (32x32x3)")
    arch_lines.append(f"  → Conv2D({base_filters}, 3x3) → BatchNorm → ReLU")
    filters = base_filters
    for stage in range(3):
        arch_lines.append(f"  → ResBlock({filters}) x {num_blocks}"
                         + (" [stride=2]" if stage > 0 else ""))
        filters *= 2
    arch_lines.append(f"  → GlobalAveragePooling2D → Dropout(0.3)")
    arch_lines.append(f"  → Dense(10, softmax)")
    arch_str = "\n".join(arch_lines)

    # Summary text
    summary = (
        f"ARCHITECTURE\n"
        f"{'─' * 40}\n"
        f"{arch_str}\n"
        f"\n"
        f"CONFIGURATION\n"
        f"{'─' * 40}\n"
        f"  Residual Blocks per Stage: {num_blocks}\n"
        f"  Base Filters:              {base_filters}\n"
        f"  Optimizer:                 {optimizer_name}\n"
        f"  Learning Rate:             {learning_rate}\n"
        f"  Epochs:                    {len(h['loss'])} (of {epochs} max)\n"
        f"  Batch Size:                {batch_size}\n"
        f"  Early Stopping:            {'Yes' if use_early_stopping else 'No'}\n"
        f"  Total Parameters:          {total_params:,}\n"
        f"\n"
        f"RESULTS\n"
        f"{'─' * 40}\n"
        f"  Test Accuracy:  {test_acc:.4f} ({test_acc * 100:.2f}%)\n"
        f"  Test Loss:      {test_loss:.4f}\n"
        f"  Train Accuracy: {h['accuracy'][-1]:.4f}\n"
        f"  Val Accuracy:   {h['val_accuracy'][-1]:.4f}\n"
        f"  Overfit Gap:    {h['accuracy'][-1] - h['val_accuracy'][-1]:.4f}\n"
    )

    return fig1, fig2, summary


# ── 11. Gradio Interface ─────────────────────────────────────────────────
demo = gr.Interface(
    fn=train_and_evaluate,
    inputs=[
        gr.Dropdown(
            choices=["Adam", "SGD", "SGD + Momentum", "RMSprop", "AdamW"],
            value="Adam",
            label="Optimizer",
        ),
        gr.Slider(
            minimum=0.0001, maximum=0.1, value=0.001, step=0.0001,
            label="Learning Rate",
        ),
        gr.Slider(
            minimum=1, maximum=4, value=2, step=1,
            label="Residual Blocks per Stage",
        ),
        gr.Slider(
            minimum=16, maximum=64, value=32, step=16,
            label="Base Filters",
        ),
        gr.Slider(
            minimum=5, maximum=50, value=20, step=5,
            label="Epochs",
        ),
        gr.Slider(
            minimum=32, maximum=256, value=128, step=32,
            label="Batch Size",
        ),
        gr.Checkbox(value=True, label="Early Stopping (patience=5)"),
    ],
    outputs=[
        gr.Plot(label="Accuracy & Loss Curves"),
        gr.Plot(label="Confusion Matrix"),
        gr.Textbox(label="Training Summary", lines=28),
    ],
    flagging_mode="never",
    title="Residual Network Trainer — CIFAR-10",
    description=(
        "Train a mini-ResNet on CIFAR-10 with skip connections and residual blocks. "
        "Adjust the number of residual blocks, base filters, optimizer, learning rate, "
        "and other hyperparameters, then click Submit to train and see the results."
    ),
)

if __name__ == "__main__":
    demo.launch()
