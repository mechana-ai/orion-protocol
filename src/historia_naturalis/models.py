from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Confidence(StrEnum):
    CONFIRMED = "confirmed"
    PROBABLE = "probable"
    HYPOTHESIS = "hypothesis"


class EntryKind(StrEnum):
    OBSERVATION = "observation"
    THEORY = "theory"


class EntryScope(StrEnum):
    FIELD = "field"
    ARCHIVE = "archive"


class SourceType(StrEnum):
    HUMAN_REPORT = "human_report"
    LOG = "log"
    RUNTIME = "runtime"
    CODE_INSPECTION = "code_inspection"
    DEPLOYMENT = "deployment"
    NETWORK = "network"
    DATABASE = "database"
    HISTORY = "history"
    WEB_RESEARCH = "web_research"
    AI_INFERENCE = "ai_inference"


class EntryState(StrEnum):
    ACTIVE = "active"
    CHALLENGED = "challenged"
    SUPERSEDED = "superseded"


class IdolType(StrEnum):
    REPORT = "report"
    MODEL = "model"
    ENVIRONMENT = "environment"
    ARCHIVE = "archive"
    RECENCY = "recency"
    REPETITION = "repetition"
    INTERFACE = "interface"
    AGREEMENT = "agreement"


class AttemptStatus(StrEnum):
    PROPOSED = "proposed"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    INCONCLUSIVE = "inconclusive"


@dataclass(slots=True)
class LedgerEntry:
    text: str
    kind: EntryKind
    confidence: Confidence
    author: str = "ai:unknown"
    source_type: SourceType = SourceType.AI_INFERENCE
    session_id: str = "default"
    issue_ref: str | None = None
    scope: EntryScope = EntryScope.FIELD
    state: EntryState = EntryState.ACTIVE
    parent_entry_id: str | None = None
    entry_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)
    locked: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Attempt:
    action: str
    expected: str
    session_id: str = "default"
    attempt_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    status: AttemptStatus = AttemptStatus.PROPOSED
    actual: str | None = None
    linked_entry_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Idol:
    idol_type: IdolType
    claim: str
    session_id: str = "default"
    issue_ref: str | None = None
    author: str = "ai:unknown"
    evidence: str | None = None
    idol_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)
    linked_entry_ids: list[str] = field(default_factory=list)
    smashed: bool = False
    smashed_by_entry_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Investigation:
    title: str
    session_id: str = "default"
    issue_ref: str | None = None
    author: str = "ai:unknown"
    summary: str = ""
    status: str = "active"
    investigation_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SessionState:
    session_id: str
    investigations: list[Investigation] = field(default_factory=list)
    entries: list[LedgerEntry] = field(default_factory=list)
    attempts: list[Attempt] = field(default_factory=list)
    idols: list[Idol] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "investigations": [investigation.to_dict() for investigation in self.investigations],
            "entries": [entry.to_dict() for entry in self.entries],
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "idols": [idol.to_dict() for idol in self.idols],
        }
