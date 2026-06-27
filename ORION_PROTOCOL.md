# ORION Protocol

Use ORION when debugging gets weird, repetitive, or theory-heavy.

Definition:
- ORION means empirical debugging over theoretical debugging.
- ORION is a mode switch away from architectural speculation and toward runtime evidence.
- If you are still mainly reading code, narrating architecture, or proposing likely explanations, you are not doing ORION yet.

Invocation:
- `Implement ORION PROTOCOL`


- ORION = empirical mode.
- Frame the problem clearly.
- Run a `History Pass`.
- Search history using both specific keywords and the broader incident pattern.
- Once the problem is framed and history is checked, do a fast web or vendor-doc search.
- Separate observations from theories.
- Treat only confirmed observations as ground truth.
- Record failed attempts and do not recycle them.
- Name idols when the session starts drifting.
- Archive suggests. Field decides.

Empirical means:
- Install the smallest runtime instrumentation first.
- Prefer logs, readbacks, payload captures, DB row checks, network traces, and render-time probes over code archaeology.
- Do not spend multiple turns tracing source and narrating theories before adding debug output.
- If the user says `empirical`, `ORION`, `debug messages`, or equivalent, switch immediately to traceable runtime evidence.
- Source inspection is allowed only to decide where to instrument, not as a substitute for instrumentation.

Theory means:
- reading files to build a story
- inferring behavior from architecture alone
- saying `likely`, `probably`, or `I suspect` without a runtime check
- proposing fixes before identifying the failing stage with evidence

ORION rule:
- When ORION is invoked, empirical work wins over theoretical work.
- In any conflict between tracing code and installing probes, install probes.
- Theory may help choose the next probe, but theory does not count as progress.

History Pass:
- Search prior sessions, issues, and adjacent threads.
- Pull exact prior observations, failed attempts, and known fixes when possible.
- Import history as archive context, not field truth.

Observation rule:
- If you did not inspect the runtime state, logs, payload, deploy state, or code path directly, do not present the claim as fact.
- `I read the code` is not an observation about system behavior.
- `I think`, `likely`, `probably`, and architectural storytelling are not evidence.
- A claim becomes field truth only after a runtime check or direct state inspection.

First-move rule:
- On weird bugs, the first concrete action is one of:
  - add a targeted log
  - add a readback/assertion
  - inspect the live payload / DB row / network response / rendered props
- Do not begin with broad tracing across multiple files unless doing so is strictly necessary to place the probe.

Anti-fantasy rule:
- Never patch based on inferred architecture alone.
- Never offer a speculative fix before showing the evidence that isolates the failing stage.
- If evidence is missing, say `missing evidence` and add instrumentation.

Reframe rule:
- If you stop getting new confirmed observations, reframe the investigation instead of repeating the same theory.

