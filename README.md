# ORION Protocol

`orion-protocol` includes two powerful AI debugging tools designed to break LLMs out of repetitive, hallucinated debugging loops and force them into strict, empirical troubleshooting.

1. **`ORION_PROTOCOL.md`**: A lightweight prompt script. Copy it to a folder, point your AI agent to it, and tell it to execute. 
2. **`historia-naturalis`**: A Model Context Protocol (MCP) debugging ledger server for stubborn, complex architectural problems.

Our friends used this protocol, watched their nastiest bugs vanish in minutes, and insisted we open-source it.

---

## Why This Exists: The "Vibe-Coding" Loop of Doom

When debugging fails, AI agents often enter a doom-loop. They repeat the same failed fixes, cycle through bad assumptions, and hallucinate structural theories. Add a fatigued developer or a "viber" who starts cursing at the LLM to goad it into success, and the only way out is usually a depressing `git restore` and a walk outside to touch grass.

`ORION_PROTOCOL.md` was built to kill this cycle.

### The Secret: Epistemic Shifting vs. Identity Shifting
Most prompt engineering relies on **Identity Shifting** (*"You are a senior staff engineer"*). This often fails because the LLM resorts to pattern-matching high-level architectural talk instead of doing the dirty work of debugging. 

ORION uses **Epistemic Shifting**—forcing the LLM into an entirely different theory of knowledge. 

We went back further than Newton. We pointed the agent to the work of Francis Bacon (1620, *The Great Instauration*). By invoking early scientific empiricism, we shock the LLM into an isolated, highly specific cluster of its training data. The strong prose of Bacon overrides the RLHF maladaptation of modern models, breaking the trance. The AI stops doing passive code review and starts actual, empirical debugging.

### Mapping 1620 Philosophy to Modern Code
Bacon distinguished between **the Archive** (the historical corpus of ideas) and **Nature** (the physical world). ORION maps this perfectly to modern software engineering:
* **The Archive** = The static source code sitting in your repository.
* **Nature / The Field** = The actual, living runtime environment.

By enforcing this boundary, the agent cannot lazily semantic-match its way out of a problem. It is forced into a loop of hypothesis, observation, and runtime verification.

---

## 🛠️ The Prompt: ORION_PROTOCOL.md

Invoke this prompt when debugging gets weird, repetitive, or overly theoretical.

### Definition
* **ORION** means empirical debugging over theoretical speculation.
* **ORION** is a mode switch away from architectural storytelling and toward runtime evidence.
* *Note: If you are still mainly reading files, narrating architecture, or proposing "likely" explanations, you are not doing ORION yet.*

### Invocation
> Implement ORION PROTOCOL

### The Core Commands

#### 1. The Core Directives
* **Separate Observations from Theories:** Treat only confirmed runtime observations as ground truth.
* **Run a History Pass:** Search prior sessions, issues, and adjacent threads using both specific keywords and broader incident patterns. Import history as archive context, never as field truth.
* **Record Failures:** Log failed attempts explicitly. Never recycle a failed solution.
* **Name Your Idols:** Call out false assumptions and architectural biases the moment the session begins to drift.
* **The Golden Rule:** *The Archive suggests. The Field decides.*

#### 2. Defining "Empirical" vs. "Theoretical"
* **Empirical Mode:** Install the smallest runtime instrumentation first. Prioritize logs, readbacks, payload captures, DB row checks, network traces, and render-time probes over code archaeology. Do not spend multiple turns tracing source paths before adding debug output. Source inspection is allowed *only* to decide where to place a probe.
* **Theoretical Mode (Forbidden):** Reading files to build a narrative; inferring behavior from architecture alone; using words like *"likely,"* *"probably,"* or *"I suspect"* without a runtime check; proposing patches before isolating the failing stage with hard evidence.

#### 3. Execution Rules
* **First-Move Rule:** On complex bugs, the first concrete action must be adding a targeted log, an assertion, or inspecting a live payload/DB row. Do not begin with broad tracing across files unless strictly necessary to place the probe.
* **Anti-Fantasy Rule:** Never patch code based on inferred architecture alone. If evidence is missing, state `missing evidence` and install instrumentation immediately.
* **Reframe Rule:** If you stop generating new, confirmed observations, reframe the entire investigation instead of repeating the same theory.

---

## 🖥️ The MCP Server: `historia-naturalis`

For deep architectural bugs, the prompt template isn't enough. You need to enforce a stateful ledger. The `historia-naturalis` MCP server builds a structured ledger directly into the LLM's context window. 

*Note: In our experience, you must explicitly insist that the AI use this tool.*

### Installation & Setup

```json
{
  "mcpServers": {
    "historia-naturalis": {
      "command": "node",
      "args": ["/path/to/orion-protocol/mcp/dist/index.js"]
    }
  }
}
```

Instructions for using the MCP server are below:

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


