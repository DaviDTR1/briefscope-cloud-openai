# BriefScope — CLOUD OpenAI

**Document-analysis agent.** Upload your documents, ask questions about them, and
let the agent research, summarize and generate downloadable deliverables —
powered by OpenAI (GPT models + OpenAI embeddings).

> Runs **two ways**: as a plugin inside the
> [QueAI](https://github.com/queai-project/QueAI) kernel, or fully
> **standalone** with nothing but Docker — see
> [Run standalone (without QueAI)](#run-standalone-without-queai).

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

- **Docker + Docker Compose v2** — that's all you need to run it.
- An **OpenAI API key** (entered later through the Settings UI).
- Outbound network access to the OpenAI API.

QueAI is **optional**: it's only needed if you want to run BriefScope as a
managed plugin alongside other plugins. To run it on its own, skip straight to
[Run standalone (without QueAI)](#run-standalone-without-queai).

## Run standalone (without QueAI)

BriefScope is a self-contained FastAPI app plus a bundled ChromaDB container. It
does not need the kernel, Traefik or any other plugin to run — only Docker.

```bash
# Build and start everything (app + ChromaDB)
docker compose -f docker-compose.standalone.yml up -d --build

# Then open the UI
#    http://localhost:8080/ui/
```

Then open **Settings** in the UI and paste your OpenAI API key. That's it — the
key is saved to `data/config.json` (a Docker volume) and survives restarts.

`docker-compose.standalone.yml` is **self-contained**: it defines every service,
its own private network and volumes, publishes the app on host port `8080`, and
blanks `ROOT_PATH` so the UI, REST API and interactive docs (`/docs`) all live at
the host root instead of behind the kernel's `/api/...` path prefix. You do
**not** need the base `docker-compose.yml`, a second `-f` flag, or a manually
created network. Want a different port? Edit the `8080:8080` mapping in that
file. To stop and remove everything:

```bash
docker compose -f docker-compose.standalone.yml down
```

## Install as a QueAI plugin

If you do run the [QueAI](https://github.com/queai-project/QueAI) kernel, install
BriefScope as a plugin instead:

1. Make this plugin available to your kernel (clone it into the kernel's
   `plugins/` directory, or install it from the marketplace if registered).
2. Open the kernel hub at `http://localhost:8473/manager/`.
3. Find **BriefScope CLOUD OpenAI** in the catalog and install it.
4. Open the plugin UI and go to **Settings** to enter your OpenAI API key.

In this mode the kernel provides the `queai_network` and Traefik routes the app
at `/api/briefscope_cloud_openai`; the base `docker-compose.yml` is used as-is
(no standalone override).

## Configuration

No secrets live in `.env`. The OpenAI API key and runtime parameters are entered
through the plugin **Settings** UI and persisted to `data/config.json` (which
survives container restarts via the plugin's Docker volume).

`docker-compose.yml` sets two environment variables automatically:

| Variable | Value | Meaning |
|---|---|---|
| `ROOT_PATH` | `/api/briefscope_cloud_openai` | FastAPI `root_path` / kernel path prefix. Blanked to `""` in `docker-compose.standalone.yml` so everything serves at the host root. |
| `LLM_MODE` | `cloud` | Selects the cloud provider path. Leave as-is. |

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
