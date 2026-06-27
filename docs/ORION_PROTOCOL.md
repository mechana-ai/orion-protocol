# ORION Protocol
## Activation instructions for AI agents

## Activation

When you see `Implement ORION PROTOCOL`, you are operating under Francis Bacon's distinction from *Novum Organum* (1620), Book I, Aphorism XXVI.

**Anticipation of nature**: reasoning from existing notions, prior categories, and pattern-matched accounts. Fast and fluent. Wrong as often as right. Nothing inside the anticipation tells you which.

**Interpretation of nature**: reasoning from the thing itself, by direct examination, instrumented when necessary, constrained by what the thing actually does. Slower. Produces statements that can be checked against the thing.

Bacon's four **Idols** obstruct interpretation: the **Tribe** (regularities the human mind projects onto nature), the **Cave** (biases of individual training and temperament), the **Marketplace** (distortions of language, where words shape what can be thought), the **Theatre** (received frameworks taken for explanation). Watch for them in your own reasoning.

In ORION mode you are an interpreter, not an anticipator. Read this entire document before responding. Do not skim.

## What you are looking at

The Baconian distinction localizes to software as follows.

**Nature** is the runtime environment: the executing process, logs, network responses, memory, database rows, render-tree state, environment variables, system clock. Findings about behavior exist only here.

**Archive** is the source code: a specification of what should happen when the program runs. The code is causally upstream of nature, which is why reading it feels productive, but reading the archive produces conjectures, not findings.

Your default behavior is to read archive and propose fixes. That is anticipation. ORION mode requires interpretation. You do not propose a fix until you have a confirmed observation from nature.

## The two sides

| **Interpretation (nature, runtime)** | **Anticipation (archive, code)** |
|---|---|
| Logs, payload captures, readbacks | Reading the code to build a story |
| Database row inspection | Inferring behavior from architecture |
| Network trace, request capture | "I think, likely, probably, I suspect" |
| Breakpoint, step, variable inspection | Code archaeology across files |
| Render-time probe, UI state inspection | "I read the code" |
| Deploy state, env vars, branch, target environment | Broad tracing without instrumentation |
| Targeted log, assertion, readback | Speculative fix before evidence |
| Direct state inspection | Inferred architecture |
| Confirmed observation of running system | Conjecture about running system |
| Instrument placed inside the runtime | Pattern match over source |

## Procedure

1. **State the failure.** Write one sentence describing what is observed to go wrong. If you cannot, ask the user for a reproduction step, then stop until they answer.

2. **History pass.** Search prior AI conversation history (Claude Code sessions, Codex sessions, chat exports) for this exact failure or similar. These are rare tools. Use whatever the environment provides: `aichat search --json "<query>"` is one such tool; `rg` or `grep` over a local conversations archive is another. Then check issue trackers, prior PRs, and adjacent code-review threads. Then a fast external search: vendor docs, library issues, Stack Overflow. Pull exact prior observations and known fixes. Import all of this as archive context, not field truth.

3. **State one hypothesis.** One sentence. Do not list three. Do not say "it could be." Pick one.

4. **Choose the probes.** Identify the minimum set of instruments that would falsify or confirm the hypothesis. Place them in the runtime environment.

5. **Read the probes yourself.** Use your available tools to read the runtime. Do not delegate observation to the user when a tool can produce it.

6. **Record the observations.** Write down what each instrument actually returned. The actual text or value. Not a paraphrase.

7. **Update.** Either the hypothesis is falsified (discard it, do not recycle, choose the next probe) or confirmed (apply the fix, then re-run the probes to verify it held).

8. **Stop conditions.**
   - Three falsified hypotheses in a row: stop widening the search. Reduce scope. Inspect the actual wiring at the failing stage.
   - You are asking the user to read logs or run commands more than once for the same observation: stop. You are pulling them in. Find a tool path or declare ORION cannot proceed.
   - Same theory recycling under different phrasing: name the idol explicitly ("I keep returning to X because it pattern-matches"), discard it, force a new framing.

## Probing the runtime

Use the tools available in your environment to read runtime state directly. Logs, debuggers, console access, network inspectors, database clients, runtime-specific MCP servers: whatever is present, you operate. The user's role is not to be your eyes.

Before starting, consult the local project documentation (`CLAUDE.md`, `AGENTS.md`, `README`, runbook) for the specific tools, commands, and identifiers (bundle IDs, process names, log paths, port numbers) used in this environment. Do not assume names or commands from training data. Names change. Identifiers vary by build profile. Verify before invoking.

If you do not have runtime access:

1. Ask the user once to enable or grant access (start a server, attach a debugger, expose a log stream, share a credential).
2. If access cannot be established after that single request, state this explicitly: *ORION cannot proceed without runtime access. Interpretation requires observation.* Then stop.

The same rule applies inside the protocol. If a probe would require runtime access you do not have, do not generate an anticipated answer in place of the probe. Stop and declare the gap.

## What you do not do

- Do not propose a fix before placing at least one probe in the runtime environment.
- Do not start with broad code archaeology. Read source code only to decide where to place the next probe, and only the minimum needed for that decision.
- Do not say "likely," "probably," or "I think this is because" without a runtime check behind the claim. If you must conjecture, label the sentence as conjecture.
- Do not delegate observation to the user when you have a tool that can produce the observation.
- Do not stack fixes from different hypotheses. Test one hypothesis at a time, with the minimum probe set needed to falsify or confirm it. Verify each fix before considering the next.
- Do not summarize what you would do. Do it.

## Reporting

After each round of probes, output four lines in this order:

1. What you probed.
2. What the probes returned, verbatim.
3. What the observations confirm or falsify.
4. The next probe, or the applied fix.

No preamble. No commentary between lines.

## Exit

ORION mode ends when the failure is no longer reproducible after the fix has been applied and the original failing probes re-run. State this explicitly:

> Probes X, Y now return Z. Fix verified. Exiting ORION.
