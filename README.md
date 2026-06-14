# BriefScope — CLOUD OpenAI

**Document-analysis agent for the [QueAI](https://github.com/queai-project/QueAI)
kernel.** Upload your documents, ask questions about them, and let the agent
research, summarize and generate downloadable deliverables — powered by OpenAI
(GPT models + OpenAI embeddings).

> This is the **CLOUD OpenAI** variant. The embedding provider and the LLM are
> both fixed to OpenAI, so it requires an OpenAI API key and makes outbound
> requests to the OpenAI API. For offline, no-key alternatives see the
> [other variants](#other-variants).

---

## What it does

- **Projects** — group documents and conversations into isolated workspaces.
- **Document ingestion** — extract text from PDF, DOCX, XLSX, TXT, MD and more,
  with token counting per document.
- **Adaptive retrieval** — for a small corpus the agent reads the full context;
  once the corpus crosses a configurable token threshold it switches to **RAG**
  (vector search over ChromaDB) and retrieves the most relevant chunks.
- **Multi-agent orchestration** — an orchestrator delegates to a creator agent
  to research and produce deliverables.
- **File generation** — produces downloadable PDF, DOCX, PPTX, XLSX, MD and TXT
  files through two complementary engines (see [File generation](#file-generation)).
- **Streaming chat** — responses stream over Server-Sent Events; conversation
  history is kept and automatically compacted to save tokens.
- **Bilingual UI** — Spanish/English switch in the frontend.

## Architecture

```
client → Traefik (PathPrefix /api/briefscope_cloud_openai) → FastAPI app
                                                               ├── ChromaDB (vector store, bundled container)
                                                               └── OpenAI API (embeddings + chat)
```

- **Backend**: FastAPI (`app/`), SQLAlchemy for project/conversation metadata
  (SQLite under `data/`), served by uvicorn on port `8080`.
- **Vector store**: a bundled `chromadb/chroma` container
  (`briefscope_chroma_openai`), reached over HTTP on the shared
  `queai_network`. Data persists in its own Docker volume.
- **Frontend**: a React (Vite + TypeScript) single-page app served from
  `frontend_dist/` at `/ui`.
- **LLM layer**: LangChain unified layer targeting `langchain-openai`.

Key REST routes (all under the plugin root path `/api/briefscope_cloud_openai`):

| Route | Purpose |
|---|---|
| `/health` | Healthcheck used by the kernel |
| `/ui` | Single-page frontend |
| `/projects` | Create / list / delete projects |
| `/documents` | Upload and manage documents |
| `/chat` | Streaming chat (SSE) |
| `/config` | Read / update configuration (API key, RAG, history) |
| `/files` | Download generated deliverables |

## Requirements

- A running [QueAI](https://github.com/queai-project/QueAI) kernel (Docker +
  Docker Compose v2).
- An **OpenAI API key**.
- Outbound network access to the OpenAI API.

## Install

### As a QueAI plugin (recommended)

1. Make this plugin available to your kernel (clone it into the kernel's
   `plugins/` directory, or install it from the marketplace if registered).
2. Open the kernel hub at `http://localhost:8473/manager/`.
3. Find **BriefScope CLOUD OpenAI** in the catalog and install it.
4. Open the plugin UI and go to **Settings** to enter your OpenAI API key.

### Standalone (development)

```bash
docker compose up -d --build
```

This brings up the app and its bundled ChromaDB on the external
`queai_network`. The app expects that network to exist (the kernel creates it);
create it manually with `docker network create queai_network` if you run the
plugin on its own.

## Configuration

No secrets live in `.env`. The OpenAI API key and runtime parameters are entered
through the plugin **Settings** UI and persisted to `data/config.json` (which
survives container restarts via the plugin's Docker volume).

`docker-compose.yml` sets two environment variables automatically — do not
change them:

| Variable | Value | Meaning |
|---|---|---|
| `ROOT_PATH` | `/api/briefscope_cloud_openai` | Traefik path prefix / FastAPI `root_path` |
| `LLM_MODE` | `cloud` | Selects the cloud provider path |

Tunable from the Settings UI:

- **OpenAI API key** — required for the plugin to become "ready".
- **RAG token threshold** — corpus size above which RAG kicks in.
- **RAG top-K** — number of chunks retrieved per query.
- **History compaction** — number of turns after which old history is summarized.

## File generation

Two engines work together:

- **Rapid mode (Markdown-based)** — the agent writes Markdown, then converts:
  pandoc → DOCX, WeasyPrint → PDF (full Unicode + CSS), `markdown` → HTML.
- **Code mode (Python)** — the agent runs reportlab / python-docx /
  python-pptx / openpyxl to produce PDF, DOCX, PPTX and XLSX with precise
  layout.

Generated files are written under `generated/` and offered through the `/files`
download route in the UI.

## Building the frontend from source

The UI is built from the shared `briefscope-frontend` project:

```bash
cd ../briefscope-frontend
npm install
npm run build      # type-check + production build into dist/
```

Copy the `dist/` output into this plugin's `frontend_dist/` so it ships inside
the container image.

## Other variants

BriefScope ships in four interchangeable variants — same UI and features,
different LLM/embedding backend:

| Variant | LLM & embeddings | Keys / internet |
|---|---|---|
| **CLOUD OpenAI** (this one) | OpenAI GPT + OpenAI embeddings | OpenAI key, outbound |
| CLOUD Gemini | Google Gemini + Google embeddings | Google key, outbound |
| LOCAL CPU | Ollama + local sentence-transformers (CPU) | none, offline |
| LOCAL GPU | Ollama + local sentence-transformers (NVIDIA GPU) | none, offline |

## Documentation & policies

- [CHANGELOG.md](CHANGELOG.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- QueAI plugin contract: [PLUGIN_DEVELOPMENT.md](https://github.com/queai-project/QueAI/blob/main/docs/PLUGIN_DEVELOPMENT.md)

## License

MIT — see [LICENSE](LICENSE).
