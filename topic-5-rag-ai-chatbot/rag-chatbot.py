"""
RAG AI Chatbot — Interactive Gradio Interface
==============================================
A Retrieval-Augmented Generation chatbot using ChromaDB for document
storage and HuggingFace Qwen model for generation. Upload documents,
build a knowledge base, and chat with your data.
"""

import os
import tempfile
import chromadb
from chromadb.utils import embedding_functions
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import gradio as gr

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# ── 1. Configuration ────────────────────────────────────────────────────────
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Initialize HuggingFace Inference Client
client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

# Initialize ChromaDB with default embedding function
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="rag_documents",
    embedding_function=embedding_fn,
)

print(f"Model: {MODEL_NAME}")
print(f"ChromaDB collection: {collection.name}")
print(f"HF Token: {'configured' if HF_TOKEN else 'not set (add HF_TOKEN to .env)'}")


# ── 2. Document Processing ──────────────────────────────────────────────────
def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def upload_documents(files, chunk_size, chunk_overlap):
    """Process uploaded files and add to ChromaDB."""
    if not files:
        return "No files uploaded."

    chunk_size = int(chunk_size)
    chunk_overlap = int(chunk_overlap)
    total_chunks = 0

    for file in files:
        try:
            with open(file.name, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file.name, "r", encoding="latin-1") as f:
                text = f.read()

        filename = os.path.basename(file.name)
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap)

        if chunks:
            ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

            collection.upsert(
                documents=chunks,
                ids=ids,
                metadatas=metadatas,
            )
            total_chunks += len(chunks)

    doc_count = collection.count()
    return (
        f"Processed {len(files)} file(s), added {total_chunks} chunks.\n"
        f"Total documents in knowledge base: {doc_count}"
    )


def clear_knowledge_base():
    """Clear all documents from ChromaDB."""
    global collection
    chroma_client.delete_collection("rag_documents")
    collection = chroma_client.get_or_create_collection(
        name="rag_documents",
        embedding_function=embedding_fn,
    )
    return "Knowledge base cleared."


# ── 3. RAG Query ────────────────────────────────────────────────────────────
def query_rag(question, num_results, temperature, max_tokens, history):
    """Query the RAG system: retrieve context from ChromaDB, generate with Qwen."""
    incoming_history = history or []
    normalized_history = []

    # Convert any incoming format to list of dicts with role/content.
    for item in incoming_history:
        role = None
        content = None
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            # Legacy tuple format: (user, assistant)
            user_msg, assistant_msg = item
            if user_msg not in (None, ""):
                normalized_history.append({"role": "user", "content": str(user_msg)})
            if assistant_msg not in (None, ""):
                normalized_history.append({"role": "assistant", "content": str(assistant_msg)})
            continue
        elif hasattr(item, "role") and hasattr(item, "content"):
            role = getattr(item, "role", None)
            content = getattr(item, "content", None)

        if role in {"user", "assistant"} and content not in (None, ""):
            normalized_history.append({"role": role, "content": str(content)})

    if not question or not str(question).strip():
        return normalized_history, ""

    num_results = int(num_results)
    max_tokens = int(max_tokens)
    doc_count = collection.count()

    # Retrieve relevant documents
    context_text = ""
    sources = []
    if doc_count > 0:
        results = collection.query(
            query_texts=[question],
            n_results=min(num_results, doc_count),
        )

        if results["documents"] and results["documents"][0]:
            for i, (doc, meta) in enumerate(
                zip(results["documents"][0], results["metadatas"][0])
            ):
                context_text += f"\n[Source: {meta['source']}]\n{doc}\n"
                if meta["source"] not in sources:
                    sources.append(meta["source"])

    # Build prompt
    if context_text:
        system_prompt = (
            "You are a helpful AI assistant. Answer the user's question based on "
            "the provided context. If the context doesn't contain relevant information, "
            "say so and answer based on your general knowledge. Always cite which "
            "source document the information comes from."
        )
        user_message = (
            f"Context from knowledge base:\n{context_text}\n\n"
            f"Question: {question}"
        )
    else:
        system_prompt = (
            "You are a helpful AI assistant. The knowledge base is empty or has no "
            "relevant documents. Answer based on your general knowledge."
        )
        user_message = question

    # Build message history for multi-turn
    messages = [{"role": "system", "content": system_prompt}]
    for message in normalized_history:
        messages.append(message)
    messages.append({"role": "user", "content": user_message})

    # Generate response
    try:
        response = client.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            if hasattr(choice, "message"):
                answer = getattr(choice.message, "content", None) or ""
            elif isinstance(choice, dict):
                answer = choice.get("message", {}).get("content", "")
            else:
                answer = str(choice)
        elif isinstance(response, dict):
            answer = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            answer = str(response)
    except Exception as e:
        answer = f"Error calling model: {str(e)}"

    # Add source info
    if sources:
        answer += f"\n\n📄 Sources: {', '.join(sources)}"

    normalized_history.append({"role": "user", "content": question})
    normalized_history.append({"role": "assistant", "content": answer})
    return normalized_history, ""


# ── 4. Gradio Interface ─────────────────────────────────────────────────────
with gr.Blocks(title="RAG AI Chatbot — Qwen + ChromaDB") as demo:
    gr.Markdown(
        "# RAG AI Chatbot — Qwen + ChromaDB\n"
        "Upload documents to build a knowledge base, then chat with your data "
        "using Retrieval-Augmented Generation powered by Qwen2.5-72B and ChromaDB."
    )

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot(label="Conversation", height=450)
        with gr.Row():
            question_input = gr.Textbox(
                label="Ask a question",
                placeholder="Type your question here...",
                scale=4,
            )
            send_btn = gr.Button("Send", variant="primary", scale=1)

        with gr.Accordion("Settings", open=False):
            with gr.Row():
                num_results = gr.Slider(
                    minimum=1, maximum=10, value=3, step=1,
                    label="Number of context chunks to retrieve",
                )
                temperature = gr.Slider(
                    minimum=0.0, maximum=1.0, value=0.7, step=0.1,
                    label="Temperature",
                )
                max_tokens = gr.Slider(
                    minimum=100, maximum=2000, value=500, step=100,
                    label="Max Tokens",
                )

        clear_chat_btn = gr.Button("Clear Chat")

        send_btn.click(
            fn=query_rag,
            inputs=[question_input, num_results, temperature, max_tokens, chatbot],
            outputs=[chatbot, question_input],
        )
        question_input.submit(
            fn=query_rag,
            inputs=[question_input, num_results, temperature, max_tokens, chatbot],
            outputs=[chatbot, question_input],
        )
        clear_chat_btn.click(fn=lambda: ([], ""), outputs=[chatbot, question_input])

    with gr.Tab("Knowledge Base"):
        gr.Markdown("### Upload Documents\nUpload `.txt`, `.md`, or `.csv` files to build the knowledge base.")

        with gr.Row():
            file_upload = gr.File(
                label="Upload files",
                file_count="multiple",
                file_types=[".txt", ".md", ".csv"],
            )
            with gr.Column():
                chunk_size = gr.Slider(
                    minimum=100, maximum=2000, value=500, step=100,
                    label="Chunk Size (characters)",
                )
                chunk_overlap = gr.Slider(
                    minimum=0, maximum=200, value=50, step=10,
                    label="Chunk Overlap (characters)",
                )

        upload_btn = gr.Button("Upload & Process", variant="primary")
        upload_status = gr.Textbox(label="Status", interactive=False)

        upload_btn.click(
            fn=upload_documents,
            inputs=[file_upload, chunk_size, chunk_overlap],
            outputs=[upload_status],
        )

        gr.Markdown("---")
        clear_kb_btn = gr.Button("Clear Knowledge Base", variant="stop")
        clear_kb_status = gr.Textbox(label="Status", interactive=False)
        clear_kb_btn.click(fn=clear_knowledge_base, outputs=[clear_kb_status])

if __name__ == "__main__":
    demo.launch()
