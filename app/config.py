"""
Persistent configuration for BriefScope CLOUD (OpenAI variant).

Source of truth: /data/config.json  (persists across container restarts)
Cloud API keys are never read from env vars — the user sets them via the frontend UI.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

# Paths
# App base dir = the package root (/code in the container). DATA_DIR and
# GENERATED_DIR default to paths RELATIVE to the app — not the FS root — so the
# plugin is self-contained. Both remain overridable via env vars.
BASE_DIR      = Path(__file__).resolve().parent.parent
DATA_DIR      = Path(os.getenv("DATA_DIR",      str(BASE_DIR / "data")))
GENERATED_DIR = Path(os.getenv("GENERATED_DIR", str(BASE_DIR / "generated")))
DB_PATH       = DATA_DIR / "briefscope.db"
# ChromaDB runs as a separate server reached over HTTP (HttpClient).
# Host/port are FIXED per variant — Chroma persists its own data in its container.
CHROMA_HOST   = "briefscope_chroma_openai"
CHROMA_PORT   = 8000
CONFIG_FILE   = DATA_DIR / "config.json"
# Intermediate research reports written by the researcher agent.
# Persistent (lives under DATA_DIR) but separate from user-facing deliverables
# in GENERATED_DIR, so it is never exposed through the /files download route.
RESEARCH_DIR  = DATA_DIR / "research"

DATA_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

# Embedding backend is FIXED to this variant's provider (OpenAI). The LLM provider
# is LOCKED to this same provider for this variant, so its API key is always required.
EMBEDDING_PROVIDER = "openai"
EMBEDDING_KEY = "openai_api_key"

_PROVIDER_KEY = {
    "anthropic": "anthropic_api_key",
    "openai":    "openai_api_key",
    "google":    "google_api_key",
}

# Allowed chat models per provider. The LLM is LOCKED to EMBEDDING_PROVIDER, so
# the chat model MUST belong to that same provider (the one used for embeddings).
_CLOUD_MODELS: dict[str, list[str]] = {
    "anthropic": [
        "claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001","claude-haiku-4-5",
        "claude-fable-5", "claude-opus-4-5", "claude-sonnet-4-5",
        "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022", "claude-3-opus-20240229",
    ],
    "openai": [
        "gpt-5.5", "gpt-5.4", "gpt-5.2", "gpt-5.1", "gpt-5.4-mini",
        "gpt-4.1", "gpt-4.1-mini", "gpt-4o", "gpt-4o-mini", "o4-mini",
    ],
    "google": [
        "gemini-3.5-flash", "gemini-3.1-flash-lite",
        "gemini-2.5-pro-preview-06-05", "gemini-2.5-flash-preview-05-20",
        "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro",
        "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-2.0-pro-exp",
    ],
}
# Only this variant's provider models are accepted (model fixed to the embedding provider).
ALLOWED_CLOUD_MODELS = _CLOUD_MODELS[EMBEDDING_PROVIDER]


def is_valid_cloud_model(model: str) -> bool:
    """True if ``model`` belongs to this variant's locked provider."""
    return model in ALLOWED_CLOUD_MODELS

# Defaults — cloud keys start empty, user fills them via the UI
_DEFAULTS: dict[str, Any] = {
    "llm_mode":              "cloud",
    # LLM provider is LOCKED to this variant's provider (OpenAI). See _load().
    "cloud_provider":        "openai",
    "cloud_model":           "gpt-4o-mini",
    "anthropic_api_key":     "",
    "openai_api_key":        "",
    "google_api_key":        "",
    # Embeddings — FIXED to this variant's provider (OpenAI). Model is editable.
    "embedding_model":       "text-embedding-3-small",
    "rag_threshold_tokens":  100_000,
    "rag_top_k":             15,
    "rag_chunk_size":        1200,
    "rag_chunk_overlap":     200,
    "history_compact_after": 6,
    # --- Multi-agent orchestration ---
    # "auto":     pick the flow from model capability (default). Cloud frontier
    #             models -> agentic; local/weak models -> pipeline.
    # "agentic":  orchestrator reasons with sub-agents-as-tools.
    # "pipeline": deterministic researcher -> creator fallback for weak models
    #             that handle nested tool-calling poorly (risk mitigation seccion 6).
    "orchestration_mode":    "auto",
    "max_delegations":       4,     # global cap on sub-agent calls per turn
    "agent_max_rounds":      8,     # max tool rounds inside a single agent
    "agent_max_depth":       2,     # orchestrator -> sub-agent nesting cap
}


def _load() -> dict[str, Any]:
    cfg = dict(_DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            stored = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            cfg = {**_DEFAULTS, **stored}
        except Exception:
            pass
    # Hard lock: the LLM provider always equals this variant's fixed provider,
    # even if a stale config.json stored a different one.
    cfg["cloud_provider"] = EMBEDDING_PROVIDER
    # Enforce: the chat model must belong to the locked provider. A stale or
    # foreign model (e.g. a Claude model in the OpenAI variant) resets to default.
    if cfg.get("cloud_model") not in ALLOWED_CLOUD_MODELS:
        cfg["cloud_model"] = _DEFAULTS["cloud_model"]
    return cfg


def _save(cfg: dict[str, Any]) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


# In-memory config — loaded once at import time
_cfg: dict[str, Any] = _load()


def get(key: str, default: Any = None) -> Any:
    return _cfg.get(key, default)


def all_settings() -> dict[str, Any]:
    return dict(_cfg)


def update(changes: dict[str, Any]) -> dict[str, Any]:
    """Apply partial update, persist to disk, return full config."""
    global _cfg
    _cfg.update({k: v for k, v in changes.items() if v is not None})
    # Re-assert the provider lock after any update.
    _cfg["cloud_provider"] = EMBEDDING_PROVIDER
    # Re-assert the model<->provider lock after any update.
    if _cfg.get("cloud_model") not in ALLOWED_CLOUD_MODELS:
        _cfg["cloud_model"] = _DEFAULTS["cloud_model"]
    _save(_cfg)
    return dict(_cfg)


def is_cloud_ready() -> bool:
    """True when both the chosen LLM and the (fixed) embedding provider have keys.

    The LLM provider is locked to EMBEDDING_PROVIDER for this variant, so its key
    is what matters; embeddings always use the same provider.
    """
    provider = get("cloud_provider", EMBEDDING_PROVIDER)
    llm_ok = bool(get(_PROVIDER_KEY.get(provider, ""), ""))
    embed_ok = bool(get(EMBEDDING_KEY, ""))
    return llm_ok and embed_ok
