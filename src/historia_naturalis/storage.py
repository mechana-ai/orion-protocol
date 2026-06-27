from __future__ import annotations

import json
import sqlite3
from pathlib import Path

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


class SQLiteLedgerStore:
    def __init__(self, db_path: str | Path = "historia_naturalis.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS ledger_entries (
              entry_id TEXT PRIMARY KEY,
              session_id TEXT NOT NULL,
              issue_ref TEXT,
              text TEXT NOT NULL,
              kind TEXT NOT NULL,
              scope TEXT NOT NULL,
              confidence TEXT NOT NULL,
              author TEXT NOT NULL,
              source_type TEXT NOT NULL,
              state TEXT NOT NULL,
              parent_entry_id TEXT,
              created_at TEXT NOT NULL,
              metadata TEXT NOT NULL,
              locked INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS attempts (
              attempt_id TEXT PRIMARY KEY,
              session_id TEXT NOT NULL,
              action TEXT NOT NULL,
              expected TEXT NOT NULL,
              status TEXT NOT NULL,
              actual TEXT,
              created_at TEXT NOT NULL,
              linked_entry_ids TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS idols (
              idol_id TEXT PRIMARY KEY,
              session_id TEXT NOT NULL,
              issue_ref TEXT,
              idol_type TEXT NOT NULL,
              claim TEXT NOT NULL,
              author TEXT NOT NULL,
              evidence TEXT,
              created_at TEXT NOT NULL,
              linked_entry_ids TEXT NOT NULL,
              smashed INTEGER NOT NULL DEFAULT 0,
              smashed_by_entry_id TEXT
            );

            CREATE TABLE IF NOT EXISTS investigations (
              investigation_id TEXT PRIMARY KEY,
              session_id TEXT NOT NULL,
              issue_ref TEXT,
              title TEXT NOT NULL,
              author TEXT NOT NULL,
              summary TEXT NOT NULL,
              status TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def add_entry(self, entry: LedgerEntry) -> LedgerEntry:
        self.conn.execute(
            """
            INSERT INTO ledger_entries (
              entry_id, session_id, issue_ref, text, kind, scope, confidence, author,
              source_type, state, parent_entry_id, created_at, metadata, locked
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.entry_id,
                entry.session_id,
                entry.issue_ref,
                entry.text,
                entry.kind.value,
                entry.scope.value,
                entry.confidence.value,
                entry.author,
                entry.source_type.value,
                entry.state.value,
                entry.parent_entry_id,
                entry.created_at,
                json.dumps(entry.metadata),
                int(entry.locked),
            ),
        )
        self.conn.commit()
        return entry

    def add_attempt(self, attempt: Attempt) -> Attempt:
        self.conn.execute(
            """
            INSERT INTO attempts (
              attempt_id, session_id, action, expected, status, actual, created_at, linked_entry_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt.attempt_id,
                attempt.session_id,
                attempt.action,
                attempt.expected,
                attempt.status.value,
                attempt.actual,
                attempt.created_at,
                json.dumps(attempt.linked_entry_ids),
            ),
        )
        self.conn.commit()
        return attempt

    def update_attempt(self, attempt_id: str, status: AttemptStatus, actual: str) -> None:
        self.conn.execute(
            "UPDATE attempts SET status = ?, actual = ? WHERE attempt_id = ?",
            (status.value, actual, attempt_id),
        )
        self.conn.commit()

    def add_idol(self, idol: Idol) -> Idol:
        self.conn.execute(
            """
            INSERT INTO idols (
              idol_id, session_id, issue_ref, idol_type, claim, author, evidence,
              created_at, linked_entry_ids, smashed, smashed_by_entry_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                idol.idol_id,
                idol.session_id,
                idol.issue_ref,
                idol.idol_type.value,
                idol.claim,
                idol.author,
                idol.evidence,
                idol.created_at,
                json.dumps(idol.linked_entry_ids),
                int(idol.smashed),
                idol.smashed_by_entry_id,
            ),
        )
        self.conn.commit()
        return idol

    def add_investigation(self, investigation: Investigation) -> Investigation:
        self.conn.execute(
            """
            INSERT INTO investigations (
              investigation_id, session_id, issue_ref, title, author, summary, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                investigation.investigation_id,
                investigation.session_id,
                investigation.issue_ref,
                investigation.title,
                investigation.author,
                investigation.summary,
                investigation.status,
                investigation.created_at,
            ),
        )
        self.conn.commit()
        return investigation

    def lock_entry(self, entry_id: str) -> None:
        self.conn.execute("UPDATE ledger_entries SET locked = 1 WHERE entry_id = ?", (entry_id,))
        self.conn.commit()

    def update_entry_state(self, entry_id: str, state: EntryState) -> None:
        self.conn.execute("UPDATE ledger_entries SET state = ? WHERE entry_id = ?", (state.value, entry_id))
        self.conn.commit()

    def smash_idol(self, idol_id: str, smashed_by_entry_id: str | None = None) -> None:
        self.conn.execute(
            "UPDATE idols SET smashed = 1, smashed_by_entry_id = ? WHERE idol_id = ?",
            (smashed_by_entry_id, idol_id),
        )
        self.conn.commit()

    def get_session(self, session_id: str) -> SessionState:
        entry_rows = self.conn.execute(
            "SELECT * FROM ledger_entries WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()
        attempt_rows = self.conn.execute(
            "SELECT * FROM attempts WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()
        idol_rows = self.conn.execute(
            "SELECT * FROM idols WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()
        investigation_rows = self.conn.execute(
            "SELECT * FROM investigations WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()

        investigations = [
            Investigation(
                investigation_id=row["investigation_id"],
                session_id=row["session_id"],
                issue_ref=row["issue_ref"],
                title=row["title"],
                author=row["author"],
                summary=row["summary"],
                status=row["status"],
                created_at=row["created_at"],
            )
            for row in investigation_rows
        ]
        entries = [
            LedgerEntry(
                entry_id=row["entry_id"],
                session_id=row["session_id"],
                issue_ref=row["issue_ref"],
                text=row["text"],
                kind=EntryKind(row["kind"]),
                scope=EntryScope(row["scope"]),
                confidence=Confidence(row["confidence"]),
                author=row["author"],
                source_type=SourceType(row["source_type"]),
                state=EntryState(row["state"]),
                parent_entry_id=row["parent_entry_id"],
                created_at=row["created_at"],
                metadata=json.loads(row["metadata"]),
                locked=bool(row["locked"]),
            )
            for row in entry_rows
        ]
        attempts = [
            Attempt(
                attempt_id=row["attempt_id"],
                session_id=row["session_id"],
                action=row["action"],
                expected=row["expected"],
                status=AttemptStatus(row["status"]),
                actual=row["actual"],
                created_at=row["created_at"],
                linked_entry_ids=json.loads(row["linked_entry_ids"]),
            )
            for row in attempt_rows
        ]
        idols = [
            Idol(
                idol_id=row["idol_id"],
                session_id=row["session_id"],
                issue_ref=row["issue_ref"],
                idol_type=IdolType(row["idol_type"]),
                claim=row["claim"],
                author=row["author"],
                evidence=row["evidence"],
                created_at=row["created_at"],
                linked_entry_ids=json.loads(row["linked_entry_ids"]),
                smashed=bool(row["smashed"]),
                smashed_by_entry_id=row["smashed_by_entry_id"],
            )
            for row in idol_rows
        ]
        return SessionState(
            session_id=session_id,
            investigations=investigations,
            entries=entries,
            attempts=attempts,
            idols=idols,
        )

    def get_observations(
        self,
        session_id: str,
        issue_ref: str | None = None,
        include_archive: bool = True,
    ) -> list[LedgerEntry]:
        state = self.get_session(session_id)
        observations = [entry for entry in state.entries if entry.kind == EntryKind.OBSERVATION]
        if issue_ref:
            observations = [entry for entry in observations if entry.issue_ref == issue_ref]
        if not include_archive:
            observations = [entry for entry in observations if entry.scope == EntryScope.FIELD]
        return observations

    def get_idols(self, session_id: str, issue_ref: str | None = None) -> list[Idol]:
        state = self.get_session(session_id)
        idols = state.idols
        if issue_ref:
            idols = [idol for idol in idols if idol.issue_ref == issue_ref]
        return idols
