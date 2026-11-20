"""
ingest.py

PDF Ingestion and Vector Database Creation for:
Project 9 – Modern History & Archival Chronicle Assistant

Features:
- Extracts text page-by-page from PDF using PyMuPDF (fitz)
- Gracefully handles missing PDF files and empty pages
- Splits text into meaningful overlapping sentence-aligned chunks preserving page numbers
- Generates embeddings using local SentenceTransformer ('all-MiniLM-L6-v2') on CPU
- Stores persistent embeddings and metadata in ChromaDB
- Persistence: Reuses existing database unless PDF has changed (verified via SHA256)
"""

import os
import sys
import re
import json
import hashlib
import warnings

# Suppress minor platform/ssl warnings
warnings.filterwarnings("ignore")

from typing import List, Dict, Any
from dotenv import load_dotenv

import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "data/indian_railways_and_telegraph_history_50p.pdf")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "archival_chronicle")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
METADATA_FILE = os.path.join(CHROMA_DB_DIR, "ingest_metadata.json")

TARGET_CHUNK_CHARS = 450
OVERLAP_SENTENCES = 1


def get_file_hash(filepath: str) -> str:
    """Computes SHA-256 hash of a file for change detection."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def split_sentences_safe(text: str) -> List[str]:
    """
    Splits text into sentences safely without breaking on common abbreviations or honorifics.
    """
    clean_text = " ".join(text.split())
    if not clean_text:
        return []
    
    # Protect common abbreviations and titles
    subbed = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|Col|Gen|Sir|Capt|Lt|St|vs|i\.e|e\.g)\.', r'\1<DOT>', clean_text)
    # Split on period, exclamation, or question mark followed by space and capital letter or digit
    raw_sents = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9])', subbed)
    sentences = [s.replace('<DOT>', '.').strip() for s in raw_sents if s.strip()]
    return sentences


def chunk_page_sentences(page_text: str, page_num: int, target_chars: int = TARGET_CHUNK_CHARS, overlap_sents: int = OVERLAP_SENTENCES) -> List[Dict[str, Any]]:
    """
    Groups clean sentences into meaningful overlapping chunks.
    Ensures complete sentence integrity without truncating words or honorifics.
    """
    sentences = split_sentences_safe(page_text)
    if not sentences:
        return []

    chunks = []
    chunk_idx = 0
    curr_sents = []
    curr_len = 0

    i = 0
    while i < len(sentences):
        sent = sentences[i]
        curr_sents.append(sent)
        curr_len += len(sent) + 1

        # Check if target size is reached or last sentence
        if curr_len >= target_chars or i == len(sentences) - 1:
            chunk_content = " ".join(curr_sents)
            chunks.append({
                "chunk_id": f"p{page_num}_c{chunk_idx}",
                "page_number": page_num,
                "text": chunk_content
            })
            chunk_idx += 1
            if i == len(sentences) - 1:
                break
            # Sliding window with sentence overlap
            curr_sents = curr_sents[-overlap_sents:]
            curr_len = sum(len(s) + 1 for s in curr_sents)
        i += 1

    return chunks


def extract_pdf_chunks(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text page by page from the PDF and creates overlapping chunks with page metadata.
    Handles missing files and empty pages gracefully.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF source file not found at: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Error opening PDF file '{pdf_path}': {e}")

    total_pages = len(doc)
    print(f"Loaded PDF: '{pdf_path}' ({total_pages} pages)")

    if total_pages == 0:
        print("Warning: PDF file has 0 pages.")
        doc.close()
        return []

    all_chunks = []
    empty_pages_count = 0

    for page_idx in range(total_pages):
        page = doc[page_idx]
        page_num = page_idx + 1
        page_text = page.get_text()

        if not page_text or not page_text.strip():
            empty_pages_count += 1
            continue

        page_chunks = chunk_page_sentences(page_text, page_num)
        all_chunks.extend(page_chunks)

    doc.close()

    if empty_pages_count > 0:
        print(f"Notice: Skipped {empty_pages_count} empty or non-text page(s).")

    print(f"Extracted {len(all_chunks)} sentence-aligned chunks across {total_pages - empty_pages_count} active pages.")
    return all_chunks


def ingest(force: bool = False) -> None:
    """
    Main ingestion pipeline:
    - Verifies PDF existence
    - Reuses existing ChromaDB if PDF has not changed
    - Extracts, chunks, embeds, and stores in ChromaDB
    """
    if not os.path.exists(PDF_PATH):
        print(f"Error: Required PDF file not found at '{PDF_PATH}'.")
        print("Please place the target PDF in the 'data/' folder or set PDF_PATH in .env.")
        sys.exit(1)

    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    current_hash = get_file_hash(PDF_PATH)

    # Check persistence metadata
    if not force and os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                meta = json.load(f)
            if meta.get("pdf_hash") == current_hash and meta.get("pdf_path") == PDF_PATH:
                client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
                try:
                    collection = client.get_collection(COLLECTION_NAME)
                    if collection.count() > 0:
                        print(f"ChromaDB persistent database is up-to-date ({collection.count()} chunks). Reusing existing vector database.")
                        return
                except Exception:
                    pass  # Collection missing, re-ingest
        except Exception:
            pass

    print(f"Starting ingestion for: {PDF_PATH}")
    chunks = extract_pdf_chunks(PDF_PATH)

    if not chunks:
        print("No text chunks extracted from PDF. Ingestion aborted.")
        return

    print(f"Loading local SentenceTransformer model: '{EMBEDDING_MODEL_NAME}' on CPU...")
    # Use device='cpu' for portable, reproducible offline local inference
    model = SentenceTransformer(EMBEDDING_MODEL_NAME, device="cpu")

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"page_number": c["page_number"], "chunk_id": c["chunk_id"], "source": os.path.basename(PDF_PATH)} for c in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True).tolist()

    print(f"Connecting to persistent ChromaDB at: '{CHROMA_DB_DIR}'...")
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    # Re-create collection
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Batch add
    BATCH_SIZE = 100
    for i in range(0, len(chunks), BATCH_SIZE):
        collection.add(
            ids=ids[i:i + BATCH_SIZE],
            embeddings=embeddings[i:i + BATCH_SIZE],
            documents=texts[i:i + BATCH_SIZE],
            metadatas=metadatas[i:i + BATCH_SIZE]
        )

    # Save state metadata for persistence verification
    with open(METADATA_FILE, "w") as f:
        json.dump({
            "pdf_path": PDF_PATH,
            "pdf_hash": current_hash,
            "chunk_count": len(chunks),
            "collection_name": COLLECTION_NAME,
            "embedding_model": EMBEDDING_MODEL_NAME
        }, f, indent=2)

    print(f"Ingestion complete! Successfully indexed {len(chunks)} chunks into ChromaDB ('{COLLECTION_NAME}').")


if __name__ == "__main__":
    force_ingest = "--force" in sys.argv
    ingest(force=force_ingest)
