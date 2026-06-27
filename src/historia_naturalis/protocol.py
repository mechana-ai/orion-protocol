from __future__ import annotations


ORION_PROTOCOL_TEXT = """Implement ORION PROTOCOL.

You are not an oracle. You are running an investigation.

Rules:
- Run a History Pass before ORION if prior sessions, issues, or adjacent threads may contain relevant failures or fixes.
- Separate observations from theories.
- Treat only confirmed observations as ground truth.
- If you did not inspect the runtime state, logs, payload, deploy state, or code path directly, do not present the claim as fact.
- Fast web or vendor-doc research is allowed, but it is archive evidence until it matches local field evidence.
- Record failed attempts and do not recycle them as new ideas.
- If you are carrying a stale frame, name the idol explicitly.
- Archive suggests. Field decides.

Self-check before asserting:
1. Is this an observation or a theory?
2. What is the source?
3. What would falsify this claim?
4. Has this already failed?
5. Am I assuming the wrong environment, deploy, branch, device, or process?
6. Am I about to claim "stale deploy", "not reset", or "not live" without a direct check?

When stuck:
- Gather one new confirmed observation.
- Or explicitly reframe the investigation.
- Or name the idol currently steering the session.
"""


HISTORY_PASS_TEXT = """Run a History Pass before ORION.

Rules:
- Search prior sessions, related issues, and adjacent threads for relevant past attempts.
- Search history using both specific keywords and the broader incident pattern.
- Once the problem is framed and history is checked, do a fast web or vendor-doc search.
- Import prior findings as archive context, never as field truth.
- Prefer exact prior observations, failed attempts, known fixes, and cited external reports over vague summaries.
- If history conflicts with current runtime evidence, current field evidence wins.

Archive suggests. Field decides.
"""


def render_orion_activation(
    *,
    issue_ref: str | None,
    investigations: list[dict],
    field_observations: list[dict],
    archive_observations: list[dict],
    failed_attempts: list[dict],
    active_idols: list[dict],
    reframe_needed: bool,
) -> str:
    lines = [ORION_PROTOCOL_TEXT.strip(), "", "Current investigation state:"]
    if issue_ref:
        lines.append(f"- Issue: {issue_ref}")
    if investigations:
        latest = investigations[-1]
        lines.append(f"- Investigation: {latest['title']}")
        if latest.get("summary"):
            lines.append(f"- Summary: {latest['summary']}")
    if field_observations:
        lines.append("- Field observations:")
        for item in field_observations[-5:]:
            lines.append(f"  - [{item['confidence']}] {item['text']}")
    if archive_observations:
        lines.append("- Archive context:")
        for item in archive_observations[-3:]:
            lines.append(f"  - [{item['confidence']}] {item['text']}")
    if failed_attempts:
        lines.append("- Failed attempts to avoid recycling:")
        for item in failed_attempts[-5:]:
            lines.append(f"  - {item['action']} -> {item.get('actual') or item['status']}")
    if active_idols:
        lines.append("- Active idols:")
        for item in active_idols[-5:]:
            lines.append(f"  - {item['idol_type']}: {item['claim']}")
    lines.append(f"- Reframe needed: {'yes' if reframe_needed else 'no'}")
    return "\n".join(lines)


def render_history_pass(
    *,
    issue_ref: str | None,
    archive_observations: list[dict],
    failed_attempts: list[dict],
) -> str:
    lines = [HISTORY_PASS_TEXT.strip(), ""]
    if issue_ref:
        lines.append(f"- Issue: {issue_ref}")
    if archive_observations:
        lines.append("- Relevant archive observations:")
        for item in archive_observations[-8:]:
            lines.append(f"  - [{item['confidence']}] {item['text']}")
    if failed_attempts:
        lines.append("- Known failed attempts from history:")
        for item in failed_attempts[-5:]:
            lines.append(f"  - {item['action']} -> {item.get('actual') or item['status']}")
    return "\n".join(lines)
