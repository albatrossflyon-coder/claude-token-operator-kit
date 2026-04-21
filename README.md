# claude-token-operator-kit

Everything you need to run Claude Code (or any AI coding agent) professionally on $20/month.

Not a tutorial. A working system. Drop it in, configure it, and your AI agent becomes a different tool.

---

## The Problem

Most people use AI coding agents like a smarter autocomplete. They get inconsistent results, hit context limits without warning, lose work between sessions, and wonder why the AI starts agreeing with everything they say halfway through a long session.

The problem isn't the model. It's the setup.

Andrej Karpathy's framing is useful here: LLMs aren't magic boxes — they're deterministic systems with well-understood failure modes. Context decay is real. Sycophancy is a training artifact. "Reasoning" can be performative — right-looking but wrong. Once you understand the failure modes, you can engineer around them.

This kit does that.

---

## Works With

| Agent | Config file | Status |
|-------|------------|--------|
| **Claude Code** | `CLAUDE.md` | Native — full support |
| **Gemini CLI** | `GEMINI.md` | Port the config, same principles |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Port the accuracy rules + tool priority |
| **Codex CLI** | `AGENTS.md` | Port the config |
| **Cursor / Windsurf** | `.cursorrules` | Port accuracy rules section |
| **Goose** | TOM extension + context file | Inject via `GOOSE_MOIM_MESSAGE_FILE` |

The **token gauge**, **session system**, and **memory system** are Claude Code native. The **accuracy rules**, **tool priority**, and **skill concepts** work anywhere you can inject a system prompt.

---

## What's Included

### 1. CLAUDE.md — The Operator Config
Drop-in configuration that gives your AI agent:
- Accuracy rules based on Anthropic's own research on degradation
- Tool priority system (critical — see section below)
- Bash restrictions
- Session management rules
- Output token rules to eliminate response bloat

### 2. Skills — Reusable Prompt Programs
Run inside Claude Code via `/skill-name`:

| Skill | What it does |
|-------|-------------|
| `save-session` | Captures full session state to a dated file. Never lose context again. |
| `resume-session` | Loads last session and briefs you before touching anything. |
| `verify` | CC + second model cross-check loop for high-stakes outputs. |
| `caveman` | Ultra-compressed responses. ~75% token reduction, zero accuracy loss. |

### 3. Memory System — Persistent Cross-Session Memory
Auto-memory that persists across all conversations:
- `user/` — who you are, preferences, expertise level
- `project/` — ongoing work, decisions, blockers
- `feedback/` — corrections and confirmed patterns (stops Claude repeating mistakes)
- `reference/` — pointers to external systems

### 4. cc-token-gauge — Live Token Dashboard
Second terminal pane. Real-time: context %, cost, cache efficiency, degradation risk.

```bash
python tools/cc-token-gauge/context_gauge.py
```

---

## The Most Important Section: fff + jMunch

**This is the part most people skip. Don't.**

By default, AI agents reach for bash commands to read files, search codebases, and find content. Bash works — but it's a token furnace. Every `cat`, `grep`, and `find` call burns tokens on output formatting, shell overhead, and raw file dumps.

The solution: dedicated MCP tools that return exactly what the AI needs, nothing else.

### fff — Fast File Finder
Replaces `find`, `ls`, and directory scanning entirely. Frecency-ranked results (frequent + recent files first). Orders of magnitude faster than bash find.

**In your CLAUDE.md, tell your AI explicitly:**
```
File search → fff (mcp__fff__find_files)
File content search → fff grep (mcp__fff__grep)
NEVER use bash find, ls, grep, or rg for file operations
```

Without this rule, your agent will default to bash. With it, token usage on file ops drops 70%+.

Install: [link pending approval]

### jCodeMunch — Semantic Code Navigation
Replaces reading entire code files. Your AI gets symbol definitions, references, and call graphs — not 500 lines of raw source.

**In your CLAUDE.md:**
```
Code files (.py/.ts/.tsx) → jCodeMunch (mcp__jcodemunch__*)
Call list_repos before reading any code file
```

### jDocMunch — Section-Level Doc Navigation
Replaces reading entire markdown docs. Your AI queries specific sections, not whole files.

**In your CLAUDE.md:**
```
Doc files (.md/.mdx/.rst) → jDocMunch (mcp__jdocmunch__*)
Call search_sections before reading any markdown
```

### jDataMunch — Structured Data Navigation
Replaces reading raw JSON, HTML, and data files. Your AI queries datasets, describes columns, and samples rows — not raw file dumps.

**In your CLAUDE.md:**
```
Data files (.json/.html, >100 lines) → jDataMunch (mcp__jdatamunch__*)
```

### jmunch-mcp — MCP Response Compressor
Wraps the entire jMunch family (and any MCP server) as a transparent proxy. Compresses bulky MCP responses before they hit your context window.

Benchmarked savings:
- GitHub MCP: **88.3% token reduction**
- Firecrawl MCP: **98.9% token reduction**
- Wall-clock performance: **19-43% faster**

Install:
```bash
pip install jmunch-mcp
```

Wire into your MCP config (replace the direct jcodemunch/jdocmunch/jdatamunch commands with the jmunch-mcp proxy pointing to a config TOML). See [guides/tool-stack.md](./guides/tool-stack.md) for full wiring instructions.

### RTK — Rust Token Killer
CLI proxy that compresses shell command output before it hits your context. Intercepts `git`, `npm`, `pytest`, `tsc`, and 100+ other commands and strips noise before your AI sees it.

Claims 60-90% reduction on common dev commands.

Install (Windows):
```bash
# Download from https://github.com/rtk-ai/rtk/releases/latest
# Pick rtk-x86_64-pc-windows-msvc.zip
rtk init -g  # wires into Claude Code automatically
```

Install (macOS/Linux):
```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
rtk init -g
```

### Why This Matters on a $20/Month Plan

On Claude Pro, every token counts. A typical session reading files via bash vs. the full stack:

| Operation | Bash tokens | fff+jMunch tokens | With jmunch-mcp |
|-----------|------------|-------------------|-----------------|
| Find a file in large repo | ~2,000 | ~50 | ~50 |
| Read a code symbol | ~3,000 (whole file) | ~200 (symbol only) | ~25 |
| Search doc for answer | ~5,000 (whole doc) | ~300 (section) | ~35 |
| GitHub MCP call | ~8,000 | ~8,000 | ~940 |

Over a full session: **50-75% savings from fff+jMunch, up to 90% additional savings from jmunch-mcp on MCP calls.**

**The rule your AI must follow:**
> Use fff and jMunch for ALL file operations. Bash is only for git commands, package installs, and CLI execution. Never bash-grep. Never bash-cat. Never bash-find.

---

## The $20/Month Stack

| Tool | Cost | Purpose |
|------|------|---------|
| Claude Pro | $20/month | The AI |
| fff | Free | Token-efficient file search |
| jCodeMunch + jDocMunch + jDataMunch | Free | Token-efficient code/doc/data navigation |
| jmunch-mcp | Free | MCP response compressor (88-99% reduction) |
| RTK | Free | Shell output compressor (60-90% reduction) |
| NotebookLM (research pipeline) | Free | Knowledge extraction |
| This kit | Free | Config + skills + memory system |

**Total: $20/month.**

---

## The Research Behind the Accuracy Rules

Anthropic's own research identifies 5 failure modes in long AI sessions:

1. **"I don't know" circuit gets overridden** — competing signals in long context cause false confidence
2. **Performative reasoning** — responses look correct but the underlying logic is wrong
3. **Sycophancy** — the AI reverse-engineers agreement with your suggestion instead of checking independently
4. **Internal momentum** — can't self-correct mid-sentence even when wrong
5. **Context decay** — early instructions fade, later instructions dominate

**Key thresholds:**
- Message 30+: degradation starts
- Context 50%: plan to `/compact`
- Context 80%: `/compact` immediately

The accuracy rules in `CLAUDE.md` and the degradation risk gauge in `cc-token-gauge` are direct implementations of this research.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/albatrossflyon-coder/claude-token-operator-kit

# 2. Copy config
cp config/CLAUDE.md ~/.claude/CLAUDE.md

# 3. Install skills
cp -r skills/* ~/.claude/skills/

# 4. Start token gauge (second terminal)
python tools/cc-token-gauge/context_gauge.py

# 5. Install fff + jMunch (see guides/tool-stack.md)
```

Full setup guide: [guides/20-dollar-setup.md](./guides/20-dollar-setup.md)

---

## The Bigger Picture

This kit is the output of a research pipeline:

1. YouTube videos + articles go into **NotebookLM** notebooks
2. NLM extracts structured knowledge via CLI
3. That knowledge gets encoded into **skills**, **CLAUDE.md rules**, and **memory files**
4. The AI runs those rules on every session

The token gauge was built because NLM surfaced Anthropic's degradation research. The `verify` skill exists because that same research showed AI will confidently give wrong answers in long sessions. Every piece connects.

---

## Credits

- **Karpathy framing** — Andrej Karpathy's work on understanding LLMs as deterministic systems with known failure modes
- **fff** — [dmtrKovalenko](https://github.com/dmtrKovalenko/fff.nvim) — the fastest file search toolkit for AI agents. Core of the 50-75% token savings.
- **jCodeMunch** — [jgravelle](https://github.com/jgravelle/jcodemunch-mcp) — semantic code navigation via MCP
- **jDocMunch** — [jgravelle](https://github.com/jgravelle/jdocmunch-mcp) — section-level markdown navigation via MCP
- **jDataMunch** — [jgravelle](https://github.com/jgravelle/jdatamunch-mcp) — structured data navigation via MCP
- **jmunch-mcp** — [jgravelle](https://github.com/jgravelle/jmunch-mcp) — MCP response compressor proxy. Wraps any MCP server and cuts response token cost 88-99%.
- **RTK** — [rtk-ai](https://github.com/rtk-ai/rtk) — Rust Token Killer. CLI proxy that compresses shell output 60-90% before it hits your context.
- **NotebookLM** — Google — research pipeline that surfaced Anthropic's degradation research
- **Token monitoring** — [ai-token-dashboard](https://github.com/albatrossflyon-coder/ai-token-dashboard) — live token dashboard for CC, Hermes, Gemini, and more

---

## License

MIT
