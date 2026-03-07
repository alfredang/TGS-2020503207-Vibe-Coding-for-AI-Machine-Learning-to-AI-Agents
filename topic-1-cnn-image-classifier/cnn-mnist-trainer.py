"""
CNN MNIST Classifier with Interactive Gradio Interface
======================================================
Train a CNN on MNIST handwritten digits using Keras with PyTorch backend.
Adjust optimizer, learning rate, epochs, and batch size via the Gradio UI.
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


# ── 2. Download and Prepare Dataset ─────────────────────────────────────────
(x_train_raw, y_train_raw), (x_test_raw, y_test_raw) = keras.datasets.mnist.load_data()

# Normalize pixel values to [0, 1]
x_train_all = x_train_raw.astype("float32") / 255.0
x_test = x_test_raw.astype("float32") / 255.0

# Add channel dimension: (28, 28) -> (28, 28, 1)
x_train_all = np.expand_dims(x_train_all, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Split validation set from training data
x_train = x_train_all[5000:]
y_train = y_train_raw[5000:]
x_val = x_train_all[:5000]
y_val = y_train_raw[:5000]
y_test = y_test_raw

NUM_CLASSES = 10
CLASS_NAMES = [str(i) for i in range(10)]

print(f"Training set:   {x_train.shape}")
print(f"Validation set: {x_val.shape}")
print(f"Test set:       {x_test.shape}")


# ── 3. Build Model ──────────────────────────────────────────────────────────
def build_cnn(activation="relu"):
    """Build a CNN model for MNIST classification."""
    model = keras.Sequential([
        keras.layers.Input(shape=(28, 28, 1)),
        keras.layers.Conv2D(32, (3, 3), activation=activation),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation=activation),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation=activation),
        keras.layers.Dense(NUM_CLASSES, activation="softmax"),
    ])
    return model


# ── 4. Gradio Progress Callback ──────────────────────────────────────────────
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


# ── 5. Training Function ────────────────────────────────────────────────────
def train_and_evaluate(optimizer_name, activation, learning_rate, epochs, batch_size, progress=gr.Progress()):
    """Train CNN with chosen hyperparameters and return evaluation plots."""
    epochs = int(epochs)
    batch_size = int(batch_size)

    # Setup optimizer
    if optimizer_name == "Adam":
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    elif optimizer_name == "SGD":
        optimizer = keras.optimizers.SGD(learning_rate=learning_rate)
    elif optimizer_name == "SGD + Momentum":
        optimizer = keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9)
    elif optimizer_name == "RMSprop":
        optimizer = keras.optimizers.RMSprop(learning_rate=learning_rate)
    elif optimizer_name == "AdamW":
        optimizer = keras.optimizers.AdamW(learning_rate=learning_rate)
    else:
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    # Build and compile
    model = build_cnn(activation=activation)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Train with progress bar
    progress(0, desc="Starting training...")
    progress_cb = GradioProgressCallback(progress, epochs)

    history = model.fit(
        x_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        callbacks=[progress_cb],
        verbose=0,
    )

    # ── 6. Evaluate ─────────────────────────────────────────────────────
    progress(1.0, desc="Evaluating on test set...")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    h = history.history
    epochs_range = range(1, len(h["loss"]) + 1)

    # ── 7. Plot accuracy and loss curves ────────────────────────────────
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
        f"{optimizer_name} | {activation} (lr={learning_rate}) | Test Acc: {test_acc:.4f} | Test Loss: {test_loss:.4f}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()

    # ── 8. Confusion matrix ─────────────────────────────────────────────
    y_pred = np.argmax(model.predict(x_test, verbose=0), axis=1)
    cm = confusion_matrix(y_test, y_pred)

    fig2, ax3 = plt.subplots(figsize=(8, 7))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(ax=ax3, cmap="Blues", values_format="d", colorbar=False)
    ax3.set_title("Confusion Matrix on Test Set", fontsize=14)
    plt.tight_layout()

    # Summary text
    summary = (
        f"Optimizer: {optimizer_name}\n"
        f"Activation: {activation}\n"
        f"Learning Rate: {learning_rate}\n"
        f"Epochs: {epochs}\n"
        f"Batch Size: {batch_size}\n"
        f"{'─' * 35}\n"
        f"Test Accuracy:  {test_acc:.4f} ({test_acc * 100:.2f}%)\n"
        f"Test Loss:      {test_loss:.4f}\n"
        f"{'─' * 35}\n"
        f"Train Accuracy: {h['accuracy'][-1]:.4f}\n"
        f"Val Accuracy:   {h['val_accuracy'][-1]:.4f}\n"
        f"Overfit Gap:    {h['accuracy'][-1] - h['val_accuracy'][-1]:.4f}\n"
    )

    return fig1, fig2, summary


# ── 9. Gradio Interface ─────────────────────────────────────────────────────
demo = gr.Interface(
    fn=train_and_evaluate,
    inputs=[
        gr.Dropdown(
            choices=["Adam", "SGD", "SGD + Momentum", "RMSprop", "AdamW"],
            value="Adam",
            label="Optimizer",
        ),
        gr.Dropdown(
            choices=["relu", "sigmoid", "tanh", "leaky_relu", "elu", "swish"],
            value="relu",
            label="Activation Function",
        ),
        gr.Slider(
            minimum=0.0001, maximum=0.1, value=0.001, step=0.0001,
            label="Learning Rate",
        ),
        gr.Slider(
            minimum=3, maximum=30, value=10, step=1,
            label="Epochs",
        ),
        gr.Slider(
            minimum=32, maximum=512, value=128, step=32,
            label="Batch Size",
        ),
    ],
    outputs=[
        gr.Plot(label="Accuracy & Loss Curves"),
        gr.Plot(label="Confusion Matrix"),
        gr.Textbox(label="Training Summary", lines=12),
    ],
    title="CNN MNIST Trainer",
    description=(
        "Train a Convolutional Neural Network on MNIST handwritten digits. "
        "Choose an optimizer, activation function, learning rate, epochs, and batch size, "
        "then click Submit to train and see the results."
    ),
)

if __name__ == "__main__":
    demo.launch()
