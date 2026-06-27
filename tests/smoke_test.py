from pathlib import Path
from tempfile import TemporaryDirectory

from historia_naturalis.models import Confidence, EntryKind, EntryScope, IdolType, SourceType
from historia_naturalis.service import HistoriaNaturalis
from historia_naturalis.storage import SQLiteLedgerStore


def test_smoke_lifecycle() -> None:
    with TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "ledger.db"
        service = HistoriaNaturalis(SQLiteLedgerStore(db_path))
        investigation = service.start_investigation(
            title="Webhook stale deploy diagnosis",
            session_id="debug-1",
            issue_ref="#439",
            author="human:operator",
            summary="Telegram replies look stale after restart.",
        )

        obs = service.observe(
            text="Deploy log shows release sha abc123 on prod.",
            confidence=Confidence.CONFIRMED,
            kind=EntryKind.OBSERVATION,
            session_id="debug-1",
            issue_ref="#439",
            author="ai:analyst",
            source_type=SourceType.DEPLOYMENT,
            scope=EntryScope.FIELD,
        )
        theory = service.observe(
            text="The stale reply is probably caused by an undeployed webhook.",
            confidence=Confidence.HYPOTHESIS,
            kind=EntryKind.THEORY,
            session_id="debug-1",
            issue_ref="#439",
            author="ai:analyst",
            source_type=SourceType.AI_INFERENCE,
        )
        service.observe(
            text="Earlier session saw duplicate dispatchers causing ack-only Telegram replies.",
            confidence=Confidence.PROBABLE,
            kind=EntryKind.OBSERVATION,
            session_id="debug-1",
            issue_ref="#439",
            author="ai:archivist",
            source_type=SourceType.HISTORY,
            scope=EntryScope.ARCHIVE,
        )
        idol = service.name_idol(
            idol_type=IdolType.MODEL,
            claim="AI is treating stale deploy as fact without checking prod build state.",
            session_id="debug-1",
            issue_ref="#439",
            author="ai:analyst",
            linked_entry_ids=[theory.entry_id],
        )
        service.challenge(
            entry_id=theory.entry_id,
            text="Challenge: prod deploy timestamp is newer than the suspected stale webhook build.",
            session_id="debug-1",
            issue_ref="#439",
            author="ai:challenger",
            source_type=SourceType.DEPLOYMENT,
        )
        replacement = service.supersede(
            entry_id=obs.entry_id,
            text="Superseding observation: prod now shows sha def456 after forced redeploy.",
            confidence=Confidence.CONFIRMED,
            session_id="debug-1",
            issue_ref="#439",
            author="human:operator",
            source_type=SourceType.RUNTIME,
        )
        service.smash_idol(idol.idol_id, smashed_by_entry_id=replacement.entry_id)

        all_observations = service.observations("debug-1", issue_ref="#439")
        field_observations = service.observations("debug-1", issue_ref="#439", include_archive=False)
        assert len(all_observations) == 3
        assert len(field_observations) == 2
        assert any(entry.entry_id == replacement.entry_id for entry in field_observations)

        state = service.status("debug-1")
        assert len(state.investigations) == 1
        assert state.investigations[0].investigation_id == investigation.investigation_id
        assert len(state.entries) == 5
        assert len(state.idols) == 1
        assert any(entry.issue_ref == "#439" for entry in state.entries)
        assert any(entry.parent_entry_id == theory.entry_id for entry in state.entries)
        assert state.idols[0].smashed is True

        history = service.history_pass(session_id="debug-1", issue_ref="#439")
        assert "Run a History Pass before ORION." in history["history_prompt"]
        assert "duplicate dispatchers" in history["history_prompt"]
        assert "specific keywords and the broader incident pattern" in history["history_prompt"]
        assert "Once the problem is framed and history is checked, do a fast web or vendor-doc search." in history["history_prompt"]

        activation = service.orion_activation_prompt(session_id="debug-1", issue_ref="#439")
        assert "Implement ORION PROTOCOL." in activation["activation_prompt"]
        assert "Webhook stale deploy diagnosis" in activation["activation_prompt"]
        assert "#439" in activation["activation_prompt"]
        assert "stale deploy" in activation["activation_prompt"]


def main() -> None:
    test_smoke_lifecycle()


if __name__ == "__main__":
    main()
