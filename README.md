# ORION Protocol
<img width="257" height="400" alt="image" align="left" src="https://github.com/user-attachments/assets/400550dd-e6d5-44d1-be92-1a8d5046d902" />

orion-protocol includes two powerful AI debugging tools:

1. **`ORION_PROTOCOL.md`**: A lightweight prompt script. Copy it to a folder, point your AI to it, and tell it to use it. If you can point the AI to the logs, great. If not, tell it you will paste whatever logs it needs and to loop you in.
2. **`historia-naturalis`**: An MCP debugging ledger server for more stubborn or complex problems. 

Our colleagues were using it and seeing bugs resolved very fast, so they insisted we share it.

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

Use ORION when debugging gets weird, repetitive, or theory-heavy. Copy [`ORION_PROTOCOL.md`](ORION_PROTOCOL.md) into your project, point your AI to it, and tell it:

> Implement ORION PROTOCOL

---

## 🖥️ The MCP Server: `historia-naturalis`

The MCP server takes a bit more effort, and you have to insist that the AI use it in our experience.

Instructions for using the MCP server are below:

### Install

```bash
pip install git+https://github.com/mechana-ai/orion-protocol.git
```

### Configure Your MCP Client

```json
{
  "mcpServers": {
    "historia-naturalis": {
      "command": "historia-naturalis"
    }
  }
}
```

The database is created automatically on first run.

---

## Support the Project

Free for individuals and students. Commercial teams (5+) require a license — see [LICENSE](LICENSE) for details.

☕ [Buy Us a Coffee](https://buy.polar.sh/polar_cl_3dtTjfHjcJvCwlFVjfruyptIeEBwkcwTdQ6wd0SLFuG) · 🏢 [Commercial Team License](https://buy.polar.sh/polar_cl_PJQKNTc2nfN8pbVL9sxXs5E3IGIEKPfbcy8KC36eRgP)
