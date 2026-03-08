"""
Pocket TTS Demo — Text-to-Speech with Gradio
=============================================
A lightweight text-to-speech demo using Kyutai's Pocket TTS model.
CPU-optimized, 100M parameters, ~200ms latency to first audio chunk.
"""

import tempfile
import os
import numpy as np
from pocket_tts import TTSModel
import gradio as gr

# ── 1. Load Model ──────────────────────────────────────────────────────────
print("Loading Pocket TTS model...")
tts_model = TTSModel.load_model()
print("Model loaded!")

# Pre-built voices
VOICES = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]

# Cache voice states for faster generation
voice_states = {}
for voice in VOICES:
    voice_states[voice] = tts_model.get_state_for_audio_prompt(voice)
    print(f"  Cached voice: {voice}")


# ── 2. TTS Generation ─────────────────────────────────────────────────────
def generate_speech(text, voice, custom_audio):
    """Generate speech from text using selected voice or custom audio."""
    if not text or not text.strip():
        return None

    # Use custom voice if provided, otherwise use pre-built voice
    if custom_audio is not None:
        voice_state = tts_model.get_state_for_audio_prompt(custom_audio)
    else:
        voice_state = voice_states.get(voice)
        if voice_state is None:
            voice_state = tts_model.get_state_for_audio_prompt(voice)

    audio = tts_model.generate_audio(voice_state, text)
    audio_np = audio.numpy()

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    import scipy.io.wavfile
    scipy.io.wavfile.write(tmp.name, tts_model.sample_rate, audio_np)

    return tmp.name


# ── 3. Gradio Interface ───────────────────────────────────────────────────
with gr.Blocks(title="Pocket TTS Demo") as demo:
    gr.Markdown(
        "# Pocket TTS Demo\n"
        "Lightweight text-to-speech powered by [Kyutai Pocket TTS](https://github.com/kyutai-labs/pocket-tts). "
        "100M parameters, CPU-optimized, ~200ms latency."
    )

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Text to speak",
                placeholder="Enter text here...",
                lines=4,
                value="Hello! Welcome to the Pocket TTS demo. This is a lightweight text to speech model that runs on CPU.",
            )
            voice_dropdown = gr.Dropdown(
                choices=VOICES,
                value="alba",
                label="Voice",
            )
            custom_audio = gr.Audio(
                label="Custom voice (optional — upload audio to clone)",
                type="filepath",
            )
            generate_btn = gr.Button("Generate Speech", variant="primary")

        with gr.Column(scale=1):
            audio_output = gr.Audio(label="Generated Speech", type="filepath")

    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, voice_dropdown, custom_audio],
        outputs=[audio_output],
    )

if __name__ == "__main__":
    demo.launch()
