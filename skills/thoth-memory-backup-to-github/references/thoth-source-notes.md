# Thoth source notes for memory backup design

These notes summarize source-of-truth details from the public Thoth repository that matter when designing a generalized backup workflow.

Sources reviewed:

- `https://github.com/siddsachar/Thoth`
- `https://raw.githubusercontent.com/siddsachar/Thoth/main/README.md`
- `https://raw.githubusercontent.com/siddsachar/Thoth/main/docs/ARCHITECTURE.md`
- `https://raw.githubusercontent.com/siddsachar/Thoth/main/memory.py`
- `https://raw.githubusercontent.com/siddsachar/Thoth/main/knowledge_graph.py`
- `https://raw.githubusercontent.com/siddsachar/Thoth/main/secret_store.py`

## Official storage assumptions

The public README describes Thoth as local-first. Durable data such as memories, documents, conversations, graph data, workflows, logs, and settings are stored locally under `~/.thoth` or platform-specific app data paths used by installers.

On Linux, the README specifically says user data is stored in `~/.thoth`.

The source supports overriding the data directory with `THOTH_DATA_DIR`. In `knowledge_graph.py`, the data directory is initialized as:

```python
_DATA_DIR = pathlib.Path(
    os.environ.get("THOTH_DATA_DIR", pathlib.Path.home() / ".thoth")
)
```

## Memory and knowledge graph paths

`memory.py` says the long-term memory database lives at:

```text
~/.thoth/memory.db
```

and the FAISS index lives at:

```text
~/.thoth/memory_vectors/
```

`knowledge_graph.py` implements the underlying entity/relation graph using SQLite, NetworkX, and FAISS. It sets:

```python
DB_PATH = str(_DATA_DIR / "memory.db")
_VECTOR_DIR = _DATA_DIR / "memory_vectors"
```

The SQLite database uses WAL mode. Live backups should therefore avoid blindly copying only the main database file while Thoth is running unless using SQLite's backup API or stopping Thoth first.

## Secrets and credentials

The README says provider keys and subscription tokens are stored in the OS credential store when available.

`secret_store.py` confirms Thoth has an OS keyring wrapper and intentionally does not fall back to plaintext from that module. It uses service names based on the active data directory and stores namespaced secrets through the platform keyring.

A generalized backup workflow should therefore avoid claiming that all secrets are simply in files under `~/.thoth`. Some metadata files may exist, but runnable credentials may be in the OS keyring or platform credential manager.

## Privacy implications

The README emphasizes:

- Thoth has no Thoth-hosted account system.
- Durable data stays local unless explicitly included in the current conversation or exposed through a tool result.
- Provider model use can send active conversation/tool context to external providers, but durable memory and documents remain local unless surfaced.

A GitHub backup workflow changes the privacy boundary. The skill should require:

- private GitHub repository
- encryption before commit/push
- explicit exclusions for secrets and volatile sessions
- restore validation before relying on the backup

## Generalization guidance

Do not hard-code paths from a single deployment. Always resolve:

1. `THOTH_DATA_DIR` if present
2. otherwise `~/.thoth`
3. platform-specific app data paths only if the user's installation/documentation says they apply

Do not assume Docker unless the user says Thoth is running in Docker.

Do not assume specific repository names, SSH aliases, passphrase paths, backup filenames, or retention settings.

## Maintenance note

Re-check these assumptions against the official Thoth repository before major Thoth version changes, installer/storage changes, or backup-script revisions. In particular, verify the active data-directory resolution, memory database path, vector index path, SQLite journaling mode, wiki/document storage locations, and secret-storage behavior before publishing deterministic backup scripts.
