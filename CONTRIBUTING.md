# Contributing to BriefScope CLOUD OpenAI

Thanks for your interest in BriefScope! This guide covers what you need to know
to open an issue or send a patch.

BriefScope is a plugin (module) for the [QueAI](https://github.com/queai-project/QueAI)
kernel. If your change concerns the kernel rather than this plugin, please
contribute to the QueAI repository instead.

---

## Table of contents

- [Before you start](#before-you-start)
- [How to open an issue](#how-to-open-an-issue)
- [Local development](#local-development)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Code and commit style](#code-and-commit-style)
- [Pull requests](#pull-requests)
- [Reporting a vulnerability](#reporting-a-vulnerability)
- [Code of Conduct](#code-of-conduct)
- [License of your contributions](#license-of-your-contributions)

---

## Before you start

1. Read the [README](README.md) to understand the architecture (FastAPI
   backend + React frontend, ChromaDB vector store, OpenAI provider).
2. Search existing open and closed issues before creating a new one.

## How to open an issue

Describe what you expected, what happened, and how to reproduce it. Include the
plugin version (`manifest.json` → `version`), the kernel version, and relevant
container logs (`docker logs briefscope_cloud_openai_service`).

For security reports, **do not open a public issue** — see [SECURITY.md](SECURITY.md).

## Local development

You'll need Python 3.11+, Docker, Docker Compose v2, Node 18+ and git.

### Backend

```bash
# From the plugin directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run against a local ChromaDB (or point CHROMA_HOST at one)
export ROOT_PATH=/api/briefscope_cloud_openai
export LLM_MODE=cloud
uvicorn app.main:app --reload --port 8080
# Health: http://localhost:8080/api/briefscope_cloud_openai/health
```

The fastest way to run the whole stack (app + ChromaDB) the way the kernel does
is with Docker:

```bash
docker compose up -d --build
```

### Frontend

The UI lives in the shared `briefscope-frontend` project and is built into this
plugin's `frontend_dist/`. To work on it:

```bash
cd ../briefscope-frontend
npm install
npm run dev          # local dev server
npm run build        # type-check + production build
```

After a production build, copy the `dist/` output into the plugin's
`frontend_dist/` so it ships inside the container.

## Code and commit style

**Python**: type hints on public interfaces; keep functions small and focused.
**TypeScript/React**: `npm run build` must pass `tsc --noEmit` with no errors.

**Commits**: English, present-tense imperative (`fix: ...`, `feat: ...`,
`docs: ...`). Explain the *why* in the body, not just the *what*.

## Pull requests

1. Keep PRs focused — one logical change per PR.
2. If you change backend behavior, verify `python -m py_compile` on touched
   files and that the container still starts and reports healthy.
3. If you change the UI, run `npm run build` and rebuild `frontend_dist/`.
4. Update the [CHANGELOG](CHANGELOG.md) under an `Unreleased` heading.

## Reporting a vulnerability

See [SECURITY.md](SECURITY.md). **Please don't open a public issue** for
security problems.

## Code of Conduct

This project adopts the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md). By
participating you agree to follow it.

## License of your contributions

BriefScope is distributed under the MIT license. Any contribution you send is
incorporated under the same license. No CLA is required.
