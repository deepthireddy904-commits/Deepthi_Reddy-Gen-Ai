"""
rag.py

Retrieval-Augmented Generation (RAG) Pipeline for:
Project 9 – Modern History & Archival Chronicle Assistant

Required Function:
    def answer(question: str) -> dict:
        \"\"\"Returns {"answer": str, "sources": list}\"\"\"

Architecture & Design:
1. Vector Store: Connects to persistent ChromaDB collection.
2. Embeddings: Uses local SentenceTransformer ('all-MiniLM-L6-v2') on CPU.
3. Grounded Retrieval: Queries top-k most relevant chunks.
4. Hallucination Guardrails:
   - High-confidence cosine similarity thresholding (>= 0.50).
   - Entity & query verification: checks whether specific entities in the question exist in retrieved context.
   - Sentence-level semantic alignment to isolate strictly factual statements.
   - If evidence is absent or insufficient, returns exactly '[not found]' with empty sources.
5. Strict Grounding: Does not use outside knowledge, external websites, or unverified assumptions.
6. Zero Paid Service Dependency: Runs 100% locally with no paid API keys required.
"""

import os
import re
import sys
import warnings

# Suppress minor platform/ssl warnings
warnings.filterwarnings("ignore")

from typing import Dict, Any, List
from dotenv import load_dotenv

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load environment variables
load_dotenv()

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "archival_chronicle")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.50"))
SENTENCE_SIMILARITY_THRESHOLD = float(os.getenv("SENTENCE_SIMILARITY_THRESHOLD", "0.55"))

# Global lazy-loaded singletons for performance across multiple calls
_CLIENT = None
_COLLECTION = None
_MODEL = None


def get_components():
    """Initializes and returns cached ChromaDB client, collection, and embedding model."""
    global _CLIENT, _COLLECTION, _MODEL
    
    if _MODEL is None:
        # device='cpu' ensures fast, zero-dependency local cross-platform inference
        _MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME, device="cpu")

    if _CLIENT is None:
        _CLIENT = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    if _COLLECTION is None:
        try:
            _COLLECTION = _CLIENT.get_collection(COLLECTION_NAME)
        except Exception:
            # If database not found, run ingestion automatically
            print(f"Collection '{COLLECTION_NAME}' not found in '{CHROMA_DB_DIR}'. Triggering ingestion...")
            from ingest import ingest
            ingest()
            _COLLECTION = _CLIENT.get_collection(COLLECTION_NAME)

    return _CLIENT, _COLLECTION, _MODEL


def clean_split_sentences(text: str) -> List[str]:
    """
    Splits text into sentences safely without splitting at honorifics or common abbreviations.
    """
    subbed = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|Col|Gen|Sir|Capt|Lt|St|vs|i\.e|e\.g)\.', r'\1<DOT>', text)
    raw_sents = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9])', subbed)
    return [s.replace('<DOT>', '.').strip() for s in raw_sents if len(s.strip()) > 15]


def verify_entities_present(question: str, retrieved_docs: List[str]) -> bool:
    """
    Checks whether named entities or distinctive multi-word proper nouns in the question
    have any grounding in the retrieved documents.
    Prevents answering out-of-domain questions with coincidental general terms.
    """
    combined_docs = " ".join(retrieved_docs).lower()
    
    # Extract capitalized proper noun sequences (e.g. "Vande Bharat Express", "FIFA World Cup")
    # or standalone 4-digit years (e.g. "2022")
    entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b|\b\d{4}\b', question)
    
    for ent in entities:
        ent_lower = ent.lower()
        # If a distinctive entity like "vande bharat" or "fifa world cup" is missing, reject
        if ent_lower not in combined_docs:
            return False
            
    return True


def answer(question: str) -> Dict[str, Any]:
    """
    Required Function:
    Retrieves the most relevant chunks from the persistent ChromaDB collection
    and generates strictly PDF-grounded answers.
    
    Returns:
        {"answer": str, "sources": list}
        
    If evidence is not explicitly present in the PDF, returns:
        {"answer": "[not found]", "sources": []}
    """
    if not question or not question.strip():
        return {"answer": "[not found]", "sources": []}

    q_clean = question.strip()
    _, collection, model = get_components()

    # Generate query embedding
    q_emb = model.encode([q_clean], normalize_embeddings=True)

    # Retrieve top 4 most relevant chunks
    results = collection.query(query_embeddings=q_emb.tolist(), n_results=4)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    if not docs:
        return {"answer": "[not found]", "sources": []}

    # Cosine distance in ChromaDB is in [0, 2], where cosine similarity = 1 - distance
    sims = [1.0 - d for d in dists]
    top_sim = sims[0]

    # Guardrail 1: Overall similarity threshold
    if top_sim < SIMILARITY_THRESHOLD:
        return {"answer": "[not found]", "sources": []}

    # Guardrail 2: Key entity existence verification
    if not verify_entities_present(q_clean, docs):
        return {"answer": "[not found]", "sources": []}

    # Sentence-level extraction and factual grounding
    all_sentences = []
    all_sentence_metas = []

    for d, m in zip(docs, metas):
        sents = clean_split_sentences(d)
        for s in sents:
            all_sentences.append(s)
            all_sentence_metas.append(m)

    if not all_sentences:
        return {"answer": "[not found]", "sources": []}

    # Compute sentence-level similarity scores
    sent_embs = model.encode(all_sentences, normalize_embeddings=True)
    cos_sims = util.cos_sim(q_emb, sent_embs)[0].numpy()

    # Detect multi-part questions (e.g., asking both obstacle and gradient ratio)
    clauses = re.split(r'\band\s+(?:what|which|how|where)\b', q_clean, flags=re.IGNORECASE)

    selected_sentences = []
    selected_pages = []

    if len(clauses) > 1:
        # Process each clause to answer both parts
        for clause in clauses:
            c_clean = clause.strip()
            if not c_clean:
                continue
            c_emb = model.encode([c_clean], normalize_embeddings=True)
            c_sims = util.cos_sim(c_emb, sent_embs)[0].numpy()
            best_idx = int(np.argmax(c_sims))
            if c_sims[best_idx] >= SENTENCE_SIMILARITY_THRESHOLD:
                sent = all_sentences[best_idx]
                if sent not in selected_sentences:
                    selected_sentences.append(sent)
                    selected_pages.append(all_sentence_metas[best_idx]["page_number"])
    else:
        best_idx = int(np.argmax(cos_sims))
        if cos_sims[best_idx] >= SENTENCE_SIMILARITY_THRESHOLD:
            selected_sentences.append(all_sentences[best_idx])
            selected_pages.append(all_sentence_metas[best_idx]["page_number"])

    if not selected_sentences:
        return {"answer": "[not found]", "sources": []}

    answer_text = " ".join(selected_sentences)
    sources = sorted(list(set(selected_pages)))

    return {
        "answer": answer_text,
        "sources": sources
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        res = answer(user_query)
        print(f"Question: {user_query}")
        print(f"Answer:   {res['answer']}")
        print(f"Sources:  {res['sources']}")
    else:
        print("Usage: python rag.py \"<your question here>\"")
