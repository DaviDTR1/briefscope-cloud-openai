"""
Embedding provider for the CLOUD-OPENAI variant.

The embedding backend is FIXED to OpenAI for this plugin variant, regardless of
which LLM the user selects in Ajustes (the LLM is provider-agnostic; embeddings
are not, because the vector store must use one consistent embedding space).

Returns a LangChain ``Embeddings`` object, so RAG code stays provider-neutral.
"""
from __future__ import annotations

from typing import Any

from app import config

# Fixed embedding provider for this variant. The API key is shared with the
# OpenAI LLM option, but it is required here even if another LLM is chosen.
EMBEDDING_PROVIDER = "openai"
EMBEDDING_KEY = "openai_api_key"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def build_embeddings() -> Any:
    api_key = config.get(EMBEDDING_KEY, "")
    if not api_key:
        raise ValueError(
            "[Error: API key de OpenAI no configurada (necesaria para los "
            "embeddings de esta variante). Ve a Ajustes.]"
        )
    from langchain_openai import OpenAIEmbeddings

    model = config.get("embedding_model", "") or DEFAULT_EMBEDDING_MODEL
    return OpenAIEmbeddings(model=model, api_key=api_key)
