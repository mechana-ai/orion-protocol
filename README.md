# ORION Protocol

`orion-protocol` is a suite of AI debugging tools. Or more simply, a prompt script.. the ORION Protocol for lighterweight debugging, and a MCP debugging ledger (historia-naturalis) for more stubborn or complex problems.

It is meant for bug investigations that are getting noisy, repetitive, or theory-heavy. The core idea is simple:

- record observations separately from theories
- record attempts and outcomes
- preserve archive context without confusing it for field truth
- run a History Pass before chasing a familiar failure again
- activate ORION when the session needs a hard reset into empirical debugging

This package can be used:

- as a Python library
- as an MCP server over `stdio` or HTTP

## Why this exists

Normal debugging with AI often fails by:

- not confirming runtime facts over guessing what code might do on execution
- making vague guesses based on pattern matching instead of research of the execution
- making repeated failed attempts that accumulates code like a thicket that is never cleaned out
- holding to stale frames after proving something wrong, AI will attempt that same fix again a few turns later
- AI occassionally resists outside research

ORION Protocol gives those different shapes so a debugging session can stay falsifiable instead of turning into narrative sludge.

For using ORION protocol, simply point your agent to the @ORION_PROTOCOL.md file and tell it 'Implement ORION PROTOCOL on [your bug description]'

Instructions for using the more robust MCP server are below:

## Requirements

- Python 3.11+
- `uv` recommended

## Quick start

### Run the smoke test

```bash
cd /Users/blairellis/GitHub/greater-instauration
uv run --extra dev pytest -q
```

### Run the MCP server over stdio

```bash
cd /Users/blairellis/GitHub/greater-instauration
uv run historia-naturalis
```

By default the SQLite ledger lives at `./historia_naturalis.db`.

### Override the database path

```bash
uv run historia-naturalis --db-path /tmp/historia_naturalis.db
```

### Run over streamable HTTP

```bash
uv run historia-naturalis \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8000 \
  --path /mcp \
  --db-path /tmp/historia_naturalis.db
```

### CLI help

```bash
uv run historia-naturalis --help
```

## Library example

```python
from historia_naturalis.models import Confidence, EntryKind, SourceType
from historia_naturalis.service import HistoriaNaturalis
from historia_naturalis.storage import SQLiteLedgerStore

service = HistoriaNaturalis(SQLiteLedgerStore("historia_naturalis.db"))

service.start_investigation(
    title="Search result mismatch",
    session_id="search-debug-1",
    issue_ref="BUG-123",
    author="human:operator",
    summary="Search results look incoherent after a recent refactor.",
)

obs = service.observe(
    text="Direct vector retrieval still returns plausible matches.",
    confidence=Confidence.CONFIRMED,
    kind=EntryKind.OBSERVATION,
    session_id="search-debug-1",
    issue_ref="BUG-123",
    author="human:operator",
    source_type=SourceType.RUNTIME,
)

attempt = service.suggest(
    action="Log the retrieval composition path",
    expected="See whether ranking or post-filtering is mutating the result set",
    session_id="search-debug-1",
    linked_entry_ids=[obs.entry_id],
)

service.result(
    attempt_id=attempt.attempt_id,
    status="failed",
    actual="The logs still do not expose the final ranking path",
)

print(service.history_pass(session_id="search-debug-1", issue_ref="BUG-123")["history_prompt"])
print(service.orion_activation_prompt(session_id="search-debug-1", issue_ref="BUG-123")["activation_prompt"])
```

## MCP surface

Main tools:

- `observe`
- `suggest`
- `result`
- `status`
- `observations`
- `lock`
- `challenge`
- `name_idol`
- `smash_idol`
- `start_investigation`
- `history_pass`
- `orion_protocol`
- `activate_orion`
- `supersede`
- `reframe_needed`

Resources/prompts:

- `orion://protocol`
- `implement_orion_protocol`

## What is ready

- core data model
- SQLite-backed ledger store
- ORION and History Pass prompt generation
- MCP server surface
- smoke test
- package build
- CLI entrypoint

## What is not ready

- no CI yet
- no release process yet
- no schema migration/versioning story yet
- no concurrency/process-locking guarantees for multi-client access
- no polished external docs beyond this README

## Privacy note

If you trial this against a private codebase or product, keep the actual investigation transcript private. The public package docs should stay generic; the real debugging ledger can remain local or private.

## Suggested release path

1. Commit the initial repo cleanly.
2. Add CI for `pytest` and `uv build`.
3. Trial the tool on one real bug investigation.
4. Tighten the MCP docs based on that real usage.
5. Tag `0.1.0`.
6. Decide whether distribution is GitHub-only, PyPI, or both.
