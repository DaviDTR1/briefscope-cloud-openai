# Changelog

All notable changes to **BriefScope CLOUD OpenAI** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-06-14

First public release as a QueAI plugin.

### Added

- Document-analysis agent over user-uploaded documents (PDF, DOCX, XLSX, TXT,
  MD and more), organized into projects.
- Retrieval strategy that adapts to corpus size: full-context for small
  corpora, RAG (ChromaDB vector search) above a configurable token threshold.
- Multi-agent orchestration (orchestrator + creator) for research and
  deliverable generation.
- Downloadable file generation in two engines:
  - **Rapid mode** (Markdown → DOCX via pandoc, → PDF via WeasyPrint, → HTML).
  - **Code mode** (Python: reportlab / python-docx / python-pptx / openpyxl)
    for PDF, DOCX, PPTX and XLSX with precise layout.
- Streaming chat responses (SSE) with conversation history and automatic
  history compaction to save tokens.
- React frontend with a Spanish/English language switcher.
- Settings UI to enter the OpenAI API key and tune RAG / history parameters;
  configuration persists to `data/config.json`.
- QueAI integration: `manifest.json`, Traefik `PathPrefix` routing, healthcheck
  endpoint and bundled ChromaDB service via `docker-compose.yml`.

### Notes

- This variant fixes both the embedding provider and the LLM to **OpenAI** and
  requires an OpenAI API key. It makes outbound requests to the OpenAI API.

[Unreleased]: https://github.com/queai-project/QueAI
[1.0.0]: https://github.com/queai-project/QueAI
