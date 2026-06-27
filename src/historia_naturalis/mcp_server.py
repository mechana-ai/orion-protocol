from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings

from .models import AttemptStatus, Confidence, EntryKind, EntryScope, IdolType, SourceType
from .protocol import HISTORY_PASS_TEXT, ORION_PROTOCOL_TEXT
from .service import HistoriaNaturalis
from .storage import SQLiteLedgerStore


def _env_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


app = FastMCP(
    "historia-naturalis",
    instructions=(
        "Empirical debugging ledger. Use this server to separate observations from theories, "
        "record attempts and failed paths, run a History Pass, and activate ORION when a "
        "debugging session gets weird or repetitive."
    ),
    host=os.getenv("HISTORIA_HOST", "127.0.0.1"),
    port=int(os.getenv("HISTORIA_PORT", "8000")),
    streamable_http_path=os.getenv("HISTORIA_MCP_PATH", "/mcp"),
    transport_security=TransportSecuritySettings(
        allowed_hosts=_env_list(
            "HISTORIA_ALLOWED_HOSTS",
            ["127.0.0.1", "localhost"],
        ),
        allowed_origins=_env_list(
            "HISTORIA_ALLOWED_ORIGINS",
            ["http://127.0.0.1", "http://localhost"],
        ),
    ),
)
ledger = HistoriaNaturalis(
    SQLiteLedgerStore(os.getenv("HISTORIA_DB_PATH", "historia_naturalis.db"))
)


@app.resource(
    "orion://protocol",
    name="orion_protocol_doc",
    title="ORION Protocol",
    description="Concise protocol for empirical debugging, History Pass, and ORION activation.",
    mime_type="text/plain",
)
def orion_protocol_doc() -> str:
    return (
        "Historia Naturalis\n\n"
        "Use this MCP to run empirical debugging.\n\n"
        "Core sequence:\n"
        "1. Frame the problem clearly.\n"
        "2. Run a History Pass.\n"
        "3. Search history using both specific keywords and the broader incident pattern.\n"
        "4. Once the problem is framed and history is checked, do a fast web or vendor-doc search.\n"
        "5. Record observations separately from theories.\n"
        "6. Record attempts and failed paths.\n"
        "7. Activate ORION if the session gets weird, repetitive, or theory-heavy.\n\n"
        "History Pass:\n"
        f"{HISTORY_PASS_TEXT.strip()}\n\n"
        "ORION:\n"
        f"{ORION_PROTOCOL_TEXT.strip()}\n"
    )


@app.prompt(
    name="implement_orion_protocol",
    title="Implement ORION PROTOCOL",
    description="Returns the ORION invocation text for use in a debugging session.",
)
def implement_orion_protocol() -> str:
    return ORION_PROTOCOL_TEXT.strip()


@app.tool()
def observe(
    text: str,
    confidence: str,
    kind: str = "observation",
    session_id: str = "default",
    author: str = "ai:unknown",
    source_type: str = "ai_inference",
    issue_ref: str = "",
    scope: str = "field",
    parent_entry_id: str = "",
) -> dict:
    entry = ledger.observe(
        text=text,
        confidence=Confidence(confidence),
        kind=EntryKind(kind),
        session_id=session_id,
        author=author,
        source_type=SourceType(source_type),
        issue_ref=issue_ref or None,
        scope=EntryScope(scope),
        parent_entry_id=parent_entry_id or None,
    )
    return entry.to_dict()


@app.tool()
def suggest(action: str, expected: str, session_id: str = "default") -> dict:
    attempt = ledger.suggest(action=action, expected=expected, session_id=session_id)
    return attempt.to_dict()


@app.tool()
def result(attempt_id: str, status: str, actual: str) -> dict:
    ledger.result(attempt_id=attempt_id, status=AttemptStatus(status), actual=actual)
    return {"ok": True, "attempt_id": attempt_id, "status": status}


@app.tool()
def status(session_id: str = "default") -> dict:
    return ledger.status(session_id).to_dict()


@app.tool()
def observations(session_id: str = "default", issue_ref: str = "", include_archive: bool = True) -> dict:
    entries = ledger.observations(
        session_id=session_id,
        issue_ref=issue_ref or None,
        include_archive=include_archive,
    )
    return {"entries": [entry.to_dict() for entry in entries]}


@app.tool()
def lock(entry_id: str) -> dict:
    ledger.lock(entry_id)
    return {"ok": True, "entry_id": entry_id}


@app.tool()
def challenge(
    entry_id: str,
    text: str,
    session_id: str = "default",
    author: str = "ai:unknown",
    source_type: str = "ai_inference",
    issue_ref: str = "",
) -> dict:
    entry = ledger.challenge(
        entry_id=entry_id,
        text=text,
        session_id=session_id,
        author=author,
        source_type=SourceType(source_type),
        issue_ref=issue_ref or None,
    )
    return entry.to_dict()


@app.tool()
def name_idol(
    idol_type: str,
    claim: str,
    session_id: str = "default",
    author: str = "ai:unknown",
    issue_ref: str = "",
    evidence: str = "",
    linked_entry_ids: list[str] | None = None,
) -> dict:
    idol = ledger.name_idol(
        idol_type=IdolType(idol_type),
        claim=claim,
        session_id=session_id,
        author=author,
        issue_ref=issue_ref or None,
        evidence=evidence or None,
        linked_entry_ids=linked_entry_ids or [],
    )
    return idol.to_dict()


@app.tool()
def start_investigation(
    title: str,
    session_id: str = "default",
    issue_ref: str = "",
    author: str = "ai:unknown",
    summary: str = "",
) -> dict:
    investigation = ledger.start_investigation(
        title=title,
        session_id=session_id,
        issue_ref=issue_ref or None,
        author=author,
        summary=summary,
    )
    return investigation.to_dict()


@app.tool()
def idols(session_id: str = "default", issue_ref: str = "") -> dict:
    return {
        "idols": [idol.to_dict() for idol in ledger.idols(session_id=session_id, issue_ref=issue_ref or None)]
    }


@app.tool()
def smash_idol(idol_id: str, smashed_by_entry_id: str = "") -> dict:
    ledger.smash_idol(idol_id=idol_id, smashed_by_entry_id=smashed_by_entry_id or None)
    return {"ok": True, "idol_id": idol_id, "smashed_by_entry_id": smashed_by_entry_id or None}


@app.tool()
def orion_protocol(session_id: str = "default", issue_ref: str = "") -> dict:
    return ledger.orion_brief(session_id=session_id, issue_ref=issue_ref or None)


@app.tool()
def activate_orion(session_id: str = "default", issue_ref: str = "") -> dict:
    return ledger.orion_activation_prompt(session_id=session_id, issue_ref=issue_ref or None)


@app.tool()
def history_pass(session_id: str = "default", issue_ref: str = "") -> dict:
    return ledger.history_pass(session_id=session_id, issue_ref=issue_ref or None)


@app.tool()
def supersede(
    entry_id: str,
    text: str,
    confidence: str = "confirmed",
    session_id: str = "default",
    author: str = "ai:unknown",
    source_type: str = "runtime",
    issue_ref: str = "",
) -> dict:
    entry = ledger.supersede(
        entry_id=entry_id,
        text=text,
        confidence=Confidence(confidence),
        session_id=session_id,
        author=author,
        source_type=SourceType(source_type),
        issue_ref=issue_ref or None,
    )
    return entry.to_dict()


@app.tool()
def reframe_needed(session_id: str = "default", failure_threshold: int = 3) -> dict:
    return {
        "session_id": session_id,
        "reframe_needed": ledger.should_reframe(
            session_id=session_id,
            failure_threshold=failure_threshold,
        ),
    }


if __name__ == "__main__":
    app.run(transport="streamable-http")
