# Vibe Coding Guide: Build a Pocket TTS Demo with Gradio

This guide walks you through building a text-to-speech demo using **vibe coding**. The app uses Kyutai's Pocket TTS model (100M parameters, CPU-optimized) with a Gradio interface. You will also learn how to deploy it to Hugging Face Spaces.

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install pocket-tts scipy gradio
```

Or if using `uv`:

```bash
uv pip install pocket-tts scipy gradio
```

No API keys or tokens needed -- Pocket TTS runs locally on CPU.

---

## Step 2: Vibe Code the Pocket TTS Demo

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for a text-to-speech demo using Kyutai's
Pocket TTS (pocket_tts package) with a Gradio interface.

The app should:
- Load the Pocket TTS model using TTSModel.load_model()
- Offer 8 pre-built voices: alba, marius, javert, jean, fantine,
  cosette, eponine, azelma
- Cache all voice states at startup for faster generation
- Allow users to upload a custom audio file for voice cloning
- Generate speech from text input and return a .wav file
- Use scipy.io.wavfile to save the audio output

UI layout (use gr.Blocks, not gr.Interface):
- Text input box (multiline, 4 lines) with a default sample sentence
- Voice dropdown to select from pre-built voices
- Audio upload for optional custom voice cloning
- Generate Speech button (primary variant)
- Audio output player for the generated speech
- Use a two-column layout: inputs on the left (scale=2),
  output on the right (scale=1)

Use:
- pocket_tts.TTSModel for model loading and audio generation
- tts_model.get_state_for_audio_prompt() for voice state loading
- tts_model.generate_audio() for speech synthesis
- scipy.io.wavfile.write() to save audio to a temp .wav file
- tempfile.NamedTemporaryFile for temporary audio files
```

### What You Should Get

The AI will generate a Python file (e.g., `pocket-tts-demo.py`) with:

1. **Model loading** -- Pocket TTS model loaded at startup (~100M parameters)
2. **Voice caching** -- all 8 pre-built voices pre-loaded as voice states for instant switching
3. **Voice cloning** -- upload any audio file to clone that voice
4. **Speech generation** -- text-to-speech synthesis with ~200ms latency to first chunk
5. **Audio output** -- generated speech saved as .wav and played in the browser
6. **Gradio Blocks UI** -- clean two-column layout with inputs and output

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Add streaming audio | "Stream audio chunks in real-time instead of waiting for full generation" |
| Add speed control | "Add a slider to control speech speed/rate" |
| Add batch generation | "Allow generating speech for multiple sentences at once" |
| Save voice presets | "Add a button to save custom voice clones as .safetensors presets" |
| Add language detection | "Show a warning if non-English text is entered since Pocket TTS only supports English" |
| Add waveform display | "Display the audio waveform visualization below the audio player" |
| Compare voices | "Generate the same text with all 8 voices and display them side by side" |
| Add download button | "Add a download button to save the generated .wav file" |

---

## Step 4: Test Locally

Run the file:

```bash
python pocket-tts-demo.py
```

Or with `uv`:

```bash
uv run pocket-tts-demo.py
```

Open `http://127.0.0.1:7860` in your browser. Try these experiments:

| Experiment | Steps | What to Observe |
|---|---|---|
| Basic generation | Type a sentence, click Generate | Audio plays in ~1 second |
| Voice comparison | Try each of the 8 voices with the same text | Each voice has distinct character |
| Voice cloning | Upload a .wav file, generate speech | Output mimics the uploaded voice |
| Long text | Enter a paragraph of text | Model handles longer inputs smoothly |
| Short text | Enter just "Hello" | Fast generation for short inputs |
| Special characters | Try text with numbers, abbreviations | How the model handles non-standard text |

---

## Step 5: Deploy to Hugging Face Spaces

### 5.1 Get a Hugging Face Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token with **Write** permissions
3. Copy the token (starts with `hf_`)

### 5.2 Create and Upload to a Space

```python
from huggingface_hub import HfApi
import io

api = HfApi(token="hf_YOUR_TOKEN_HERE")

# Create the Space
api.create_repo(
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py
api.upload_file(
    path_or_fileobj="pocket-tts-demo.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""pocket-tts
scipy
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/pocket-tts-demo",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/pocket-tts-demo")
```

### 5.3 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Download the Pocket TTS model (~100M parameters)
3. Cache all 8 voice states
4. Serve the Gradio interface

This takes 3-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **Pocket TTS is CPU-friendly** -- 100M parameters means no GPU needed, runs on any machine
2. **Voice cloning is simple** -- just provide an audio sample and the model adapts
3. **Caching voice states speeds up generation** -- pre-loading voices avoids repeated computation
4. **Gradio makes deployment easy** -- from local demo to public URL in minutes
5. **Vibe coding** lets you build sophisticated AI demos by describing what you want and iterating on the result
