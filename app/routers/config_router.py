"""
Config router — reads and writes DATA_DIR/config.json via the frontend UI.

Cloud variant: the LLM provider is LOCKED to this variant's fixed provider
(OpenAI or Google), so it is not exposed as an editable field. No Ollama fields.
"""
from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import config

router = APIRouter()


class ConfigOut(BaseModel):
    llm_mode:              str
    cloud_provider:        str
    cloud_model:           str
    anthropic_api_key_set: bool
    openai_api_key_set:    bool
    google_api_key_set:    bool
    cloud_ready:           bool
    embedding_provider:    str
    embedding_model:       str
    rag_threshold_tokens:  int
    rag_top_k:             int
    history_compact_after: int


class ConfigUpdate(BaseModel):
    # cloud_provider is intentionally absent — it is locked per variant.
    cloud_model:           Optional[str] = None
    anthropic_api_key:     Optional[str] = None
    openai_api_key:        Optional[str] = None
    google_api_key:        Optional[str] = None
    embedding_model:       Optional[str] = None
    rag_threshold_tokens:  Optional[int] = None
    rag_top_k:             Optional[int] = None
    history_compact_after: Optional[int] = None


@router.get("/", response_model=ConfigOut)
def get_config():
    cfg = config.all_settings()
    return ConfigOut(
        llm_mode              = "cloud",
        cloud_provider        = cfg["cloud_provider"],
        cloud_model           = cfg["cloud_model"],
        anthropic_api_key_set = bool(cfg.get("anthropic_api_key")),
        openai_api_key_set    = bool(cfg.get("openai_api_key")),
        google_api_key_set    = bool(cfg.get("google_api_key")),
        cloud_ready           = config.is_cloud_ready(),
        embedding_provider    = config.EMBEDDING_PROVIDER,
        embedding_model       = cfg["embedding_model"],
        rag_threshold_tokens  = cfg["rag_threshold_tokens"],
        rag_top_k             = cfg["rag_top_k"],
        history_compact_after = cfg["history_compact_after"],
    )


@router.post("/", response_model=ConfigOut)
def update_config(body: ConfigUpdate):
    changes: dict = {}
    raw = body.model_dump()

    # The chat model is FIXED to this variant's provider (same as embeddings).
    if raw.get("cloud_model") is not None and not config.is_valid_cloud_model(raw["cloud_model"]):
        raise HTTPException(
            status_code=400,
            detail=(f"El modelo '{raw['cloud_model']}' no pertenece al proveedor de esta "
                    f"versión ({config.EMBEDDING_PROVIDER}). Elige un modelo del mismo proveedor."),
        )

    # NOTE: "cloud_provider" is intentionally NOT updatable — the LLM provider is
    # locked to this variant's fixed provider (config enforces it on load).
    for field in ("cloud_model", "embedding_model",
                  "rag_threshold_tokens", "rag_top_k", "history_compact_after"):
        if raw[field] is not None:
            changes[field] = raw[field]

    for field in ("anthropic_api_key", "openai_api_key", "google_api_key"):
        if raw[field] is not None:
            changes[field] = raw[field]

    config.update(changes)
    return get_config()
