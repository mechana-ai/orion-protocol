Structural changes from your edits: dropped Sections III and IV per your cuts, folded V into II with the Idols brought in, cleaned up your Section I addition, filled in "xxx."

---

# ORION Protocol
## Investigation in the Runtime Environment

*Working draft. Accumulating.*

---

## I. The distinction

Francis Bacon, in *Novum Organum* (1620), Book I, Aphorism XXVI, separates two kinds of human reasoning about nature.

The first he calls the **anticipation of nature**: reasoning that proceeds from existing notions, prior categories, and received accounts of how the world should behave. Anticipations are rapid, fluent, and produce agreement readily, because they draw on what is already familiar. They are wrong as often as they are right, and no procedure inside an anticipation detects which it is.

The second he calls the **interpretation of nature**: reasoning that proceeds from the thing itself, by direct examination, instrumented when necessary, and constrained by what the thing actually does. Interpretations are slower, harder to produce, and harder to agree on. They produce knowledge that survives contact with the world.

Bacon was not making a casual stylistic recommendation. He was arguing that the dominant intellectual culture of his moment, organized around received accounts of nature, had to be displaced by direct empirical investigation. He named the standing obstacles to this displacement (the four Idols of Book I), described the procedures of interpretation (the Tables of Book II), and treated the work as a renewal of knowledge across the sciences.

AI all but ignores the second kind of reasoning during a debugging session. The source code is mistaken for nature. Because the code sits in an unusual third position, neither the running system nor a stale commentary on it, the activities of reviewing, simulating, and imagining what the code would do can be made to feel like investigation. They are not. They are code walk-through. The walk-through is sufficient for a narrow class of bugs: syntax errors, type mismatches, contract violations between functions, isolated logical errors where all inputs are specified in the visible code. It is insufficient for the larger class of bugs whose cause lives in the runtime environment rather than the text: concurrency, timing, stateful interactions, environment configuration, integration behavior, performance, and every failure that depends on how the code meets the world rather than what the code says. These are the bugs most worth finding, and they are the bugs an AI stuck in anticipation cannot find.

When the model attempts to find them by anticipation anyway, three consequences follow. The codebase accumulates fixes that did not address the failure. The code becomes harder to read and maintain as anticipations are layered on anticipations. The actual failure is obscured by the surrounding mutations rather than isolated.

The remedy is direct. Instruct the AI to investigate the runtime environment. Debugging then becomes safer, more efficient, and convergent.

---

## II. The runtime environment

The runtime environment is the live system in which code is executing. It includes the executing process, the values of environment variables, the state of memory and the filesystem at this moment, the network as it currently responds, the system clock, other processes running alongside, the hardware and its current state, and the inputs flowing through the system. It is what is in fact happening when the program runs.

The runtime environment is the observation space for software. Findings are produced here, and only here. Logs, payload captures, database inspection, network traces, breakpoints, variable inspection at a paused frame, render-time probes: these are the instruments of interpretation.

These observations have a property anticipation does not. They kill idols.

Bacon names four idols in *Novum Organum*, Book I. The **Tribe**: patterns the human mind projects onto nature because it is human. The **Cave**: biases each investigator brings from temperament and training. The **Marketplace**: distortions of language, where words shape what can be thought. The **Theatre**: inherited philosophical systems that determine in advance what counts as an explanation. Each idol is a structure that survives in the absence of contact with the thing itself, and dies when that contact is made.

The same structures appear in LLM debugging. The model projects the distribution of its training data onto the code in front of it (Tribe). It defaults to the framings and idioms most common in that distribution (Cave). It generates fluent text whose names do not correspond to what is actually in the runtime (Marketplace). It applies popular frameworks regardless of fit (Theatre). None of these dissolve under more reading. Only a reading taken from the runtime environment can falsify them.

Anticipation cannot kill its own idols. The model presents anticipations as conclusions reached by investigation. There is no internal procedure for distinguishing a pattern-match that is correct from one that is not. In agentic loops, each anticipated fix is applied to the code without verification. When the fix does not resolve the failure, a new fix is generated by the same process and applied the same way. The code mutates in response to anticipation rather than to observation. Over a long session, most additions to the codebase become responses to imagined bugs rather than demonstrated ones. The original failure remains uninvestigated. The idols are now embedded in the code, where they will guide the next round of anticipation.

A single confirmed observation, taken at the right place in the runtime environment, ends the cycle. The current candidate fix is either falsified, in which case the conjecture is discarded and the failing stage is isolated more sharply, or confirmed, in which case the fix can be applied with cause. Either outcome narrows the search space. Anticipation conducted without such observations does not narrow the search space. It produces additional code, generated by the same process that produced the candidate fixes, none of which has contacted the runtime environment.

---

## VI. The two sides, enumerated

| **Interpretation (runtime environment)** | **Anticipation (source code)** |
|---|---|
| Logs, payload captures, readbacks | Reading the code to build a story |
| Database row inspection | Inferring behavior from architecture |
| Network trace, request capture | "I think, likely, probably, I suspect" |
| Breakpoint, step, variable inspection | Code archaeology across files |
| Render-time probe | "I read the code" |
| Deploy state, env vars, branch, device | Broad tracing without instrumentation |
| Targeted log, assertion, readback | Speculative fix before evidence |
| Direct state inspection | Inferred architecture |
| Confirmed observation of running system | Conjecture about running system |
| Instrument placed inside the runtime | Pattern match over source |

The table is descriptive. The protocol does not forbid the activities on the right column. Reading code, building a story about it, and forming conjectures from its structure are necessary parts of debugging. The protocol requires that activities on the right column be classified as conjectures, and that the resolution of any conjecture be sought through activities on the left column.

---

*Continuing.*

---

Notes on what I did with your prose: kept your three consequences (cruft, unmaintainability, obscuring the real failure) but reworded for the register. Kept your bug-type distinction. Filled the "xxx" with "convergent" because that is the specific property anticipation fails to produce. Renumbered to I, II, VI so the section numbers stay stable for future inserts if you want III, IV, V to come back for something else (Popper, Zeller, activation phrase, operational rules).