# Changelog

All notable changes to **BriefScope CLOUD OpenAI** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-06-14

### Fixed

- Markdown written inside raw HTML wrappers (for example a multi-column layout
  `<div>`) is now parsed instead of leaking through as literal `###`/`-` text in
  generated documents. The Markdown engine enables the `md_in_html` and
  `attr_list` extensions, and the agent format guides document the required
  `markdown="1"` attribute.
- Chat state and any in-progress streamed reply are now preserved when switching
  between projects. A reply that arrives while you are viewing another project is
  kept, so returning no longer loses the message or requires a page reload.

### Changed

- Streaming responses no longer auto-scroll the chat on every token; the view
  scrolls only when a new message begins, letting you read at your own pace.

### Added

- Informative agent logs (agent start/finish, each tool entered with a safe
  argument summary, tool results, and sub-agent delegations) so advanced users
  can follow the agent's behavior.

## [1.1.0] - 2026-06-14

### Fixed

- Generated documents are now scoped per project: each deliverable is stored
  under a per-project folder (`generated/project_<id>`) and only appears in the
  project that created it. Previously all projects shared a single folder, so
  files generated in one project leaked into every other project.

### Added

- Per-document metadata sidecar (title, creation timestamp, format and owning
  project) saved next to each generated file and surfaced in the files panel.
- The file list in the UI now shows each document's title and creation date.

### Changed

- The `/files` list, download and delete endpoints now require a `project_id`
  and operate strictly within that project's folder.

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
