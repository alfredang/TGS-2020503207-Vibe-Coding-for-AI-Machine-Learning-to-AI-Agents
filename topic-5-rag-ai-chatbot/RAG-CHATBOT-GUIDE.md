# Vibe Coding Guide: Build a RAG AI Chatbot with Gradio

This guide walks you through building an interactive RAG (Retrieval-Augmented Generation) chatbot using **vibe coding**. The chatbot uses ChromaDB for document storage and retrieval, and HuggingFace Qwen2.5-72B for generation. You will also learn how to deploy it to Hugging Face Spaces.

---

## Step 1: Set Up Your Project

Make sure you have the required dependencies installed:

```bash
pip install chromadb huggingface_hub gradio python-dotenv
```

Or if using `uv`:

```bash
uv pip install chromadb huggingface_hub gradio python-dotenv
```

Create a `.env` file with your HuggingFace token:

```
HF_TOKEN=your_huggingface_token_here
```

---

## Step 2: Vibe Code the RAG Chatbot

Open your AI assistant (Claude, ChatGPT, etc.) and use the following prompt:

### The Prompt

```
Create a single Python file for a RAG AI chatbot using ChromaDB and
HuggingFace Qwen2.5-72B-Instruct with a Gradio interface.

The app should have two tabs:

Tab 1 - Chat:
- A chatbot interface with multi-turn conversation history
- Each user question retrieves relevant chunks from ChromaDB
- Build a prompt with system message, retrieved context, and chat history
- Send to Qwen2.5-72B-Instruct via HuggingFace InferenceClient
- Display source documents used in the response
- Settings accordion with sliders for:
  - Number of context chunks to retrieve (1-10, default 3)
  - Temperature (0.0-1.0, default 0.7)
  - Max tokens (100-2000, default 500)
- Clear chat button

Tab 2 - Knowledge Base:
- File upload for .txt, .md, .csv files (multiple files)
- Chunk size slider (100-2000 characters, default 500)
- Chunk overlap slider (0-200 characters, default 50)
- Upload & Process button that:
  - Reads each file
  - Splits into overlapping chunks
  - Upserts into ChromaDB with source metadata
  - Shows status with chunk count
- Clear Knowledge Base button

Use:
- chromadb.Client() with DefaultEmbeddingFunction for vector storage
- HuggingFace InferenceClient for Qwen2.5-72B-Instruct API
- python-dotenv to load HF_TOKEN from .env
- gr.Blocks layout (not gr.Interface) for the tabbed UI
```

### What You Should Get

The AI will generate a Python file (e.g., `rag-chatbot.py`) with:

1. **ChromaDB setup** -- in-memory client with default embeddings for document storage
2. **Document processing** -- file reading, text chunking with overlap, metadata tracking
3. **RAG query pipeline** -- retrieve relevant chunks, build context prompt, call Qwen
4. **Multi-turn chat** -- conversation history passed to the model for context
5. **Source attribution** -- show which documents were used to answer
6. **Gradio Blocks UI** -- tabbed interface with Chat and Knowledge Base tabs
7. **Configurable settings** -- temperature, max tokens, chunk size, retrieval count

---

## Step 3: Iterate and Refine

Vibe coding is about iterating. Here are follow-up prompts you can use:

| What You Want | Prompt |
|---|---|
| Add PDF support | "Add PDF file upload support using PyMuPDF or pdfplumber" |
| Add web scraping | "Add a URL input that scrapes web pages and adds them to the knowledge base" |
| Show retrieved chunks | "Display the retrieved context chunks in an expandable section below the chat" |
| Add model selection | "Add a dropdown to switch between Qwen2.5-72B, Llama-3, and Mistral" |
| Add streaming | "Stream the model response token by token instead of waiting for the full response" |
| Persistent storage | "Use chromadb.PersistentClient to save the knowledge base to disk" |
| Add embedding model choice | "Add a dropdown to choose between default, sentence-transformers, and OpenAI embeddings" |
| Export chat | "Add a button to export the conversation as a markdown file" |

---

## Step 4: Test Locally

Run the file:

```bash
python rag-chatbot.py
```

Or with `uv`:

```bash
uv run rag-chatbot.py
```

Open `http://127.0.0.1:7860` in your browser. Try these experiments:

| Experiment | Steps | What to Observe |
|---|---|---|
| No-context chat | Ask a question without uploading documents | Model answers from general knowledge |
| Single document | Upload one .txt file, ask about its content | Model cites the source document |
| Multiple documents | Upload several files, ask cross-document questions | Model retrieves from multiple sources |
| Adjust retrieval | Change "chunks to retrieve" from 1 to 5 | More context = more detailed answers |
| Temperature test | Set temperature to 0.0 vs 1.0 | 0.0 = deterministic, 1.0 = creative |
| Large chunks | Set chunk size to 1000, overlap to 100 | Fewer but larger context windows |

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
    repo_id="YOUR_USERNAME/rag-ai-chatbot",
    repo_type="space",
    space_sdk="gradio",
    exist_ok=True,
)

# Upload app.py
api.upload_file(
    path_or_fileobj="rag-chatbot.py",
    path_in_repo="app.py",
    repo_id="YOUR_USERNAME/rag-ai-chatbot",
    repo_type="space",
)

# Upload requirements.txt
requirements = b"""chromadb
huggingface_hub
python-dotenv
"""

api.upload_file(
    path_or_fileobj=io.BytesIO(requirements),
    path_in_repo="requirements.txt",
    repo_id="YOUR_USERNAME/rag-ai-chatbot",
    repo_type="space",
)

print("Deployed! Visit: https://huggingface.co/spaces/YOUR_USERNAME/rag-ai-chatbot")
```

**Important:** Add your `HF_TOKEN` as a Space secret:
1. Go to your Space Settings
2. Under "Repository secrets", add `HF_TOKEN` with your token value

### 5.3 Wait for Build

After uploading, Hugging Face will:
1. Install dependencies from `requirements.txt`
2. Run `app.py`
3. Serve the Gradio interface

This takes 2-5 minutes. Visit your Space URL to see it live.

---

## Key Takeaways

1. **RAG = Retrieval + Generation** -- ChromaDB finds relevant documents, Qwen generates answers using that context
2. **Chunking matters** -- chunk size and overlap affect retrieval quality; too small loses context, too large dilutes relevance
3. **Embeddings are the backbone** -- ChromaDB's default embedding function converts text to vectors for similarity search
4. **Multi-turn context** -- passing conversation history to the model enables follow-up questions
5. **Source attribution builds trust** -- showing which documents were used helps users verify answers
6. **Vibe coding** lets you build sophisticated AI applications by describing what you want and iterating on the result
