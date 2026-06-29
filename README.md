# ORION Protocol
<img width="257" height="400" alt="image" align="left" src="https://github.com/user-attachments/assets/400550dd-e6d5-44d1-be92-1a8d5046d902" />

orion-protocol includes two powerful AI debugging tools:

1. **`ORION_PROTOCOL.md`**: A lightweight prompt script. Copy it to a folder, point your AI to it, and tell it to use it. If you can point the AI to the logs, great. If not, tell it you will paste whatever logs it needs and to loop you in.
2. **`historia-naturalis`**: An MCP debugging ledger server for more stubborn or complex problems. 

Our friends were using it and seeing bugs resolved very fast, so they insisted we share it.

---

## Why This Exists

Agents will begin to loop in failing cycles of debugging and even return to past failed attempts. Add a fatigued developer or ‘viber’ that starts using curse words to try to goad the agent into success, and the only way out is generally a move to ‘touch grass’ and a `git restore`.

`ORION_PROTOCOL.md` was created to address this recurring problem.

### Epistemic Shifting vs. Identity Shifting
Telling an AI to debug instead of code review and pattern match to solve problems wasn't enough. Based on a hunch, we realized AI doesn’t use scientific methods of experimentation. We needed to shock the AI out of this reinforcement learning from human feedback (RLHF) space.

Instead of attempting to get results by Identity Shifting (*"You are a senior engineer"*), this method uses **Epistemic Shifting**—moving the LLM into a different theory of knowledge. Identity shifting acts like AI affirmations. Epistemic shifting reorients the LLM to enter a highly specific, sparsely populated cluster of its training data: early scientific philosophy using empirical methodology.

We pointed the agent to the work of Francis Bacon (1620, *[The Great Instauration](https://www.fbrt.org.uk/hermes/great-instauration/)*). By referencing Bacon, the LLM is **state-shocked** into an entirely new context of 400-year-old sense-making. The strong writing of Bacon overrides the maladaptation of LLMs to mistake passive code review for actual debugging. The trance breaks, the AI starts to debug, and you break out of running circles accumulating code-cruft.

### The Archive vs. Nature
This system maps Bacon’s terms perfectly onto modern software:
* **The Archive:** The corpus of ideas around a subject (the static source code sitting in a repo).
* **Nature:** The actual environment in question (the executable runtime environment).

Because these concepts map cleanly, agents are left with no room to return to low-effort semantic matching. They are forced to work through the empirical loop: Theory, observation, new theory. Loop as needed.

---

## 🛠️ ORION_PROTOCOL.md Prompt Script

Use ORION when debugging gets weird, repetitive, or theory-heavy.

### Definitions
* **ORION** means empirical debugging over theoretical debugging.
* **ORION** is a mode switch away from architectural speculation and toward runtime evidence.
* *Note: If you are still mainly reading code, narrating architecture, or proposing likely explanations, you are not doing ORION yet.*

### Invocation
> Implement ORION PROTOCOL

### Rules and Directives

#### 1. Core Rules
* **Separate observations from theories:** Record observations separately from theories. Treat only confirmed observations as ground truth.
* **Record attempts and outcomes:** Log failed attempts and do not recycle them.
* **The Golden Rule:** The archive suggests. The field decides. Do not confuse the archive (source code) with field truth (the executable environment).
* **Run a History Pass:** Search history using both specific keywords and the broader incident pattern before chasing a familiar failure again.
* **Name Idols:** Name idols when the session starts drifting.

#### 2. Empirical Mode vs. Theoretical Mode
* **Empirical means:** Install the smallest runtime instrumentation first. Prefer logs, readbacks, payload captures, DB row checks, network traces, and render-time probes over code archaeology. Do not spend multiple turns tracing source and narrating theories before adding debug output. Source inspection is allowed only to decide where to instrument, not as a substitute for instrumentation.
* **Theoretical means:** Reading files to build a story; inferring behavior from architecture alone; saying *"likely,"* *"probably,"* or *"I suspect"* without a runtime check; proposing fixes before identifying the failing stage with evidence.
* **The Priority Rule:** When ORION is invoked, empirical work wins over theoretical work. In any conflict between tracing code and installing probes, install probes. Theory may help choose the next probe, but theory does not count as progress.

#### 3. Execution Directives
* **History Pass Rule:** Search prior sessions, issues, and adjacent threads. Pull exact prior observations, failed attempts, and known fixes when possible. Import history as archive context, not field truth.
* **Observation Rule:** If you did not inspect the runtime state, logs, payload, deploy state, or code path directly, do not present the claim as fact. *"I read the code"* is not an observation about system behavior. Architectural storytelling is not evidence. A claim becomes field truth only after a runtime check or direct state inspection.
* **First-Move Rule:** On weird bugs, the first concrete action must be one of: add a targeted log, add a readback/assertion, or inspect the live payload/DB row/network response/rendered props. Do not begin with broad tracing across multiple files unless strictly necessary to place the probe.
* **Anti-Fantasy Rule:** Never patch based on inferred architecture alone. Never offer a speculative fix before showing the evidence that isolates the failing stage. If evidence is missing, say `missing evidence` and add instrumentation.
* **Reframe Rule:** If you stop getting new confirmed observations, reframe the investigation instead of repeating the same theory.

---

## 🖥️ The MCP Server: `historia-naturalis`

The MCP server takes a bit more effort, and you have to insist that the AI use it in our experience.

Instructions for using the MCP server are below:

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
