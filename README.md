
# ORION Protocol

<img width="444" height="691" alt="image" src="https://github.com/user-attachments/assets/db6b5b94-0d12-4e45-9f3e-4a8fc5d2eee5" />

`orion-protocol` includes two powerful AI debugging tools:

**A prompt script:** the [ORION_PROTOCOL.md](ORION_PROTOCOL.md) is enough for most debugging sessions.

  You can just copy the script to a folder and point AI to it and tell it to use it.  Thats it. 
  If you can point AI to the logs great. if not, tell it you will paste whatever logs it needs and to loop you in.

  Our friends were using it and seeing bugs resolved very fast so they insisted we share it.  

**An MCP debugging ledger** (historia-naturalis) for more stubborn or complex problems.

## Why this exists

Agents will begin to loop in failing cycles of debugging and even return to past failed attempts.  Add a fatigued developer or ‘viber’ that starts using curse words to try to goad the agent into success and the only way out is generally a move to ‘touch grass’ and a git restore.

[ORION_PROTOCOL.md](ORION_PROTOCOL.md) was created to address this recurring problem.

Maybe AI it needed an education.  Based on a hunch, we realized, AI doesn’t use scientific methods.  We went back further than Newton.  We needed to slap AI  into some new awareness, get it on other neural networks, old ones, to shock it out of this horrible RLHF hellspace.  

That did the trick.

We pointed my agent to the work of Francis Bacon. 1620.  [The Great Instuartion](https://www.fbrt.org.uk/hermes/great-instauration/).  Instauration means restoration. Bacon believed humanity needed to restore its connection with nature and regain the mastery over creation. 

**Good Plan.**

Telling AI to debug instead of code review and pattern match to solve problems wasnt enough.

But by invoking Bacon, we managed to put AI into a totally different **‘attention head’**. Reorienting the LLM to enter to a highly specific, sparsely populated cluster of its training data—early scientific philosophy using empirical methodology lit something up.

The trance broke.  AI started to debug, and we broke out of those running circles accumulating code creft.  

Another reason this worked: Instead of attempting to get results by **Identity Shifting**  “You are a senior engineer”, this method uses **Epistemic Shifting**. Moving the LLM into a different theory of knowledge.  I’ve always been suspicious of those ‘pretend you are a super genius' prompts.  Sounds like AI affirmations.

Another reason it worked:  Clear distinctions between ‘**the archive**’ (bacon’s term for the corpus of ideas around a subject, and ‘**nature**’ the actual environment in question), mapped very well on to ‘**source code**’ and ‘**run-time environment**'.  Agents were left with no room to return to its low effort semantic matching and has to work to debug in this system. Theory, oberservation, new theory. Loop as needed.

[ORION_PROTOCOL.md](ORION_PROTOCOL.md)

By referencing the work of Francis Bacon, the LLM is sort of '**state-shocked**' into an entirely new context. Sense-making from 400 years ago. That seems to be enough to slap the models out of the annoying habit of mistaking code review for actual debugging. _The strong work and writing of Bacon overrides the mal-adaptation of LLM's to misunderstand code review of static code for actual debugging._

The core direction is simple:

- record observations separately from theories
- record attempts and outcomes
- Dont confuse archive (just the code sitting in a repo) with field truth (the executable environment).
- run a History Pass before chasing a familiar failure again

The MCP server takes a bit more effort and you have to insist that the AI use it in our experience. 

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


