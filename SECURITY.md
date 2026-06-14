# Security Policy

Thanks for helping keep BriefScope safe for its users.

BriefScope is a plugin (module) for the [QueAI](https://github.com/queai-project/QueAI)
kernel. This policy covers the **BriefScope CLOUD OpenAI** plugin only. For
vulnerabilities in the kernel itself, report them to the QueAI project.

## Supported versions

| Version | Security support |
|---|---|
| `1.x` (`main` branch) | ✅ actively maintained |
| `< 1.0` (pre-releases) | no retroactive guarantee — please upgrade to the latest tag |

## How to report a vulnerability

**Do not open a public issue** for security vulnerabilities.

Use GitHub Private Vulnerability Reporting on this plugin's repository, or
contact the repository owner directly.

Please include at least:

- Plugin version (`manifest.json` → `version`) and kernel version.
- Reproduction steps.
- Observed or expected impact (unauthorized read/write, RCE, privilege
  escalation, secret disclosure, etc.).
- Your availability to coordinate disclosure.

## What to expect

- **Acknowledgement within 72 h** of submission.
- **Triage within 7 days**: we confirm whether it's an issue, its estimated
  severity and a target fix date.
- **Coordinated disclosure**: we work on a private fix and credit you when
  publishing the advisory and the patched version, unless you prefer to stay
  anonymous.

## In-scope

- Vulnerabilities in the plugin backend (`app/`) — RAG, agents, file
  generation, configuration and the REST API under `/api/briefscope_cloud_openai`.
- Improper handling of the user-supplied API key stored in `data/config.json`.
- Path traversal or unauthorized access through the document upload and the
  `/files` download route.

## Out-of-scope

- Vulnerabilities in the QueAI kernel (report to the kernel project).
- Vulnerabilities in third-party dependencies that have no exploit path through
  this plugin (report upstream; we will bump the pin once a fix is available).
- Issues requiring physical access to the host or valid kernel operator
  credentials.

## Notes specific to the CLOUD OpenAI variant

This variant **requires an OpenAI API key** and makes **outbound network
requests** to the OpenAI API for both embeddings and chat completions. This is
by design. Operators should be aware that:

- The API key is entered through the plugin UI and persisted to
  `data/config.json` inside the plugin's Docker volume. It is never read from,
  or written to, the kernel.
- Document content and prompts are sent to OpenAI for embedding and generation.
  Do not upload data you are not permitted to send to a third-party provider.

## Bug bounty

This project does not offer monetary rewards. It does offer public credit in
the changelog and the published advisory, unless you prefer to remain anonymous.
