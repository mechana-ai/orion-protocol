from __future__ import annotations

from .models import (
    Attempt,
    AttemptStatus,
    Confidence,
    EntryKind,
    EntryScope,
    EntryState,
    Idol,
    IdolType,
    Investigation,
    LedgerEntry,
    SessionState,
    SourceType,
)
from .protocol import HISTORY_PASS_TEXT, ORION_PROTOCOL_TEXT, render_history_pass, render_orion_activation
from .storage import SQLiteLedgerStore


class HistoriaNaturalis:
    def __init__(self, store: SQLiteLedgerStore | None = None) -> None:
        self.store = store or SQLiteLedgerStore()

    def observe(
        self,
        text: str,
        confidence: Confidence,
        kind: EntryKind = EntryKind.OBSERVATION,
        session_id: str = "default",
        author: str = "ai:unknown",
        source_type: SourceType = SourceType.AI_INFERENCE,
        issue_ref: str | None = None,
        scope: EntryScope = EntryScope.FIELD,
        parent_entry_id: str | None = None,
    ) -> LedgerEntry:
        entry = LedgerEntry(
            text=text,
            kind=kind,
            confidence=confidence,
            session_id=session_id,
            author=author,
            source_type=source_type,
            issue_ref=issue_ref,
            scope=scope,
            parent_entry_id=parent_entry_id,
        )
        return self.store.add_entry(entry)

    def suggest(
        self,
        action: str,
        expected: str,
        session_id: str = "default",
        linked_entry_ids: list[str] | None = None,
    ) -> Attempt:
        attempt = Attempt(
            action=action,
            expected=expected,
            session_id=session_id,
            linked_entry_ids=linked_entry_ids or [],
        )
        return self.store.add_attempt(attempt)

    def result(self, attempt_id: str, status: AttemptStatus, actual: str) -> None:
        self.store.update_attempt(attempt_id=attempt_id, status=status, actual=actual)

    def lock(self, entry_id: str) -> None:
        self.store.lock_entry(entry_id)

    def challenge(
        self,
        entry_id: str,
        text: str,
        session_id: str = "default",
        author: str = "ai:unknown",
        source_type: SourceType = SourceType.AI_INFERENCE,
        issue_ref: str | None = None,
    ) -> LedgerEntry:
        self.store.update_entry_state(entry_id, EntryState.CHALLENGED)
        return self.observe(
            text=text,
            confidence=Confidence.PROBABLE,
            kind=EntryKind.THEORY,
            session_id=session_id,
            author=author,
            source_type=source_type,
            issue_ref=issue_ref,
            scope=EntryScope.FIELD,
            parent_entry_id=entry_id,
        )

    def name_idol(
        self,
        idol_type: IdolType,
        claim: str,
        session_id: str = "default",
        author: str = "ai:unknown",
        issue_ref: str | None = None,
        evidence: str | None = None,
        linked_entry_ids: list[str] | None = None,
    ) -> Idol:
        idol = Idol(
            idol_type=idol_type,
            claim=claim,
            session_id=session_id,
            issue_ref=issue_ref,
            author=author,
            evidence=evidence,
            linked_entry_ids=linked_entry_ids or [],
        )
        return self.store.add_idol(idol)

    def start_investigation(
        self,
        title: str,
        session_id: str = "default",
        issue_ref: str | None = None,
        author: str = "ai:unknown",
        summary: str = "",
    ) -> Investigation:
        investigation = Investigation(
            title=title,
            session_id=session_id,
            issue_ref=issue_ref,
            author=author,
            summary=summary,
        )
        return self.store.add_investigation(investigation)

    def smash_idol(self, idol_id: str, smashed_by_entry_id: str | None = None) -> None:
        self.store.smash_idol(idol_id, smashed_by_entry_id=smashed_by_entry_id)

    def supersede(
        self,
        entry_id: str,
        text: str,
        confidence: Confidence,
        session_id: str = "default",
        author: str = "ai:unknown",
        source_type: SourceType = SourceType.RUNTIME,
        issue_ref: str | None = None,
    ) -> LedgerEntry:
        self.store.update_entry_state(entry_id, EntryState.SUPERSEDED)
        return self.observe(
            text=text,
            confidence=confidence,
            kind=EntryKind.OBSERVATION,
            session_id=session_id,
            author=author,
            source_type=source_type,
            issue_ref=issue_ref,
            scope=EntryScope.FIELD,
            parent_entry_id=entry_id,
        )

    def status(self, session_id: str = "default") -> SessionState:
        return self.store.get_session(session_id)

    def observations(
        self,
        session_id: str = "default",
        issue_ref: str | None = None,
        include_archive: bool = True,
    ) -> list[LedgerEntry]:
        return self.store.get_observations(
            session_id=session_id,
            issue_ref=issue_ref,
            include_archive=include_archive,
        )

    def idols(self, session_id: str = "default", issue_ref: str | None = None) -> list[Idol]:
        return self.store.get_idols(session_id=session_id, issue_ref=issue_ref)

    def orion_brief(self, session_id: str = "default", issue_ref: str | None = None) -> dict:
        state = self.status(session_id)
        failed_attempts = [attempt.to_dict() for attempt in state.attempts if attempt.status == AttemptStatus.FAILED]
        active_idols = [
            idol.to_dict()
            for idol in self.idols(session_id=session_id, issue_ref=issue_ref)
            if not idol.smashed
        ]
        field_observations = [
            entry.to_dict()
            for entry in self.observations(session_id=session_id, issue_ref=issue_ref, include_archive=False)
        ]
        archive_observations = [
            entry.to_dict()
            for entry in self.observations(session_id=session_id, issue_ref=issue_ref, include_archive=True)
            if entry.scope != EntryScope.FIELD
        ]

        return {
            "protocol": ORION_PROTOCOL_TEXT,
            "session_id": session_id,
            "issue_ref": issue_ref,
            "investigations": [inv.to_dict() for inv in state.investigations],
            "failed_attempts": failed_attempts[-5:],
            "active_idols": active_idols[-5:],
            "field_observations": field_observations[-10:],
            "archive_observations": archive_observations[-10:],
            "reframe_needed": self.should_reframe(session_id=session_id),
        }

    def history_pass(self, session_id: str = "default", issue_ref: str | None = None) -> dict:
        state = self.status(session_id)
        archive_observations = [
            entry.to_dict()
            for entry in self.observations(session_id=session_id, issue_ref=issue_ref, include_archive=True)
            if entry.scope == EntryScope.ARCHIVE
        ]
        failed_attempts = [
            attempt.to_dict()
            for attempt in state.attempts
            if attempt.status == AttemptStatus.FAILED
        ]
        return {
            "protocol": HISTORY_PASS_TEXT,
            "session_id": session_id,
            "issue_ref": issue_ref,
            "archive_observations": archive_observations[-10:],
            "failed_attempts": failed_attempts[-5:],
            "history_prompt": render_history_pass(
                issue_ref=issue_ref,
                archive_observations=archive_observations,
                failed_attempts=failed_attempts,
            ),
        }

    def orion_activation_prompt(self, session_id: str = "default", issue_ref: str | None = None) -> dict:
        brief = self.orion_brief(session_id=session_id, issue_ref=issue_ref)
        return {
            **brief,
            "activation_prompt": render_orion_activation(
                issue_ref=issue_ref,
                investigations=brief["investigations"],
                field_observations=brief["field_observations"],
                archive_observations=brief["archive_observations"],
                failed_attempts=brief["failed_attempts"],
                active_idols=brief["active_idols"],
                reframe_needed=brief["reframe_needed"],
            ),
        }

    def should_reframe(self, session_id: str = "default", failure_threshold: int = 3) -> bool:
        state = self.status(session_id)
        recent_attempts = state.attempts[-failure_threshold:]
        if len(recent_attempts) < failure_threshold:
            return False
        if not all(attempt.status == AttemptStatus.FAILED for attempt in recent_attempts):
            return False
        recent_entries = [entry for entry in state.entries if entry.scope == EntryScope.FIELD][-failure_threshold:]
        if any(
            entry.kind == EntryKind.OBSERVATION and entry.confidence == Confidence.CONFIRMED
            for entry in recent_entries
        ):
            return False
        return True
