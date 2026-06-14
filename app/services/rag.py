"""
RAG service using ChromaDB with provider embeddings.

Embeddings are computed via the variant's fixed cloud provider (OpenAI or
Gemini) — see ``app.services.embeddings.build_embeddings``. Vectors are passed
to ChromaDB explicitly, so Chroma never needs its own (sentence-transformers)
embedding function. The provider/model is consistent within a deployment, so
index-time and query-time embeddings always match.
"""
from __future__ import annotations

from typing import List

import chromadb

from app.config import CHROMA_HOST, CHROMA_PORT
from app import config as _cfg
from app.services.embeddings import build_embeddings

_client: chromadb.ClientAPI | None = None


def _get_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return _client


def _embed_documents(texts: List[str]) -> List[List[float]]:
    return build_embeddings().embed_documents(texts)


def _embed_query(text: str) -> List[float]:
    return build_embeddings().embed_query(text)


def _collection_name(project_id: int) -> str:
    return f"project_{project_id}"


def _chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> List[str]:
    chunk_size = chunk_size or _cfg.get("rag_chunk_size", 1200)
    overlap    = overlap    or _cfg.get("rag_chunk_overlap", 200)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def index_document(project_id: int, document_id: int, filename: str, text: str) -> None:
    client = _get_client()
    col = client.get_or_create_collection(name=_collection_name(project_id))
    chunks = _chunk_text(text)
    if not chunks:
        return
    ids = [f"doc{document_id}_chunk{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": document_id, "filename": filename, "chunk": i}
                 for i in range(len(chunks))]
    embeddings = _embed_documents(chunks)
    col.upsert(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)


def delete_document(project_id: int, document_id: int) -> None:
    client = _get_client()
    try:
        col = client.get_collection(name=_collection_name(project_id))
        col.delete(where={"document_id": document_id})
    except Exception:
        pass


def delete_project(project_id: int) -> None:
    client = _get_client()
    try:
        client.delete_collection(_collection_name(project_id))
    except Exception:
        pass


def retrieve(project_id: int, query: str, top_k: int | None = None) -> List[dict]:
    top_k = top_k or _cfg.get("rag_top_k", 15)
    client = _get_client()
    try:
        col = client.get_collection(name=_collection_name(project_id))
    except Exception:
        return []
    count = col.count()
    if not count:
        return []
    query_vec = _embed_query(query)
    results = col.query(query_embeddings=[query_vec], n_results=min(top_k, count))
    if not results or not results["documents"]:
        return []
    items = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        items.append({
            "filename": meta.get("filename", ""),
            "chunk":    meta.get("chunk", 0),
            "text":     doc,
        })
    return items


def format_rag_context(chunks: List[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        header = '  <fragmento id="' + str(i) + '" archivo="' + c["filename"] + '" chunk="' 