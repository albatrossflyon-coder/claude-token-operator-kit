# The $20/Month Setup Guide

Everything configured and running in under 30 minutes.

## Prerequisites

- Claude Pro ($20/month) — claude.ai/upgrade
- Python 3.10+
- Git

## Step 1 — Drop In the Config (5 min)

```bash
cp config/CLAUDE.md ~/.claude/CLAUDE.md
```

This installs the accuracy rules and tool priority system. Takes effect immediately on next session.

## Step 2 — Install Skills (5 min)

```bash
cp -r skills/* ~/.claude/skills/
```

Skills available after install:
- `/save-session` — save full session state before context runs out
- `/resume-session` — load last session and get briefed before touching anything
- `/verify` — cross-check high-stakes outputs with a second model
- `/caveman` — compress responses ~75% when you need to conserve tokens

## Step 3 — Start the Token Gauge (2 min)

Open a second terminal pane alongside Claude Code:

```bash
python tools/cc-token-gauge/context_gauge.py
```

Leave it running. Refresh every 5 seconds. Watch the CONTEXT % and MESSAGES gauges.

**When to act:**
- Messages hits 30 → plan to `/compact`
- Context hits 50% → `/compact` soon
- Context hits 80% → `/compact` NOW

## Step 4 — Install fff + jMunch (10 min)

These are the tools that make the CLAUDE.md config actually work.

Without them, Claude Code falls back to bash for file operations — slow and token-hungry.
With them, file navigation uses 50-75% fewer tokens on any real project.

**fff (Fast File Finder):**
```bash
# Install via the fff MCP server
curl -fsSL https://raw.githubusercontent.com/dmtrKovalenko/fff.nvim/main/install-mcp.sh | bash
```
Repo: https://github.com/dmtrKovalenko/fff.nvim

**jCodeMunch + jDocMunch:**
```bash
# Install via npm (runs as MCP server)
npx -y @jgravelle/jcodemunch-mcp
npx -y @jgravelle/jdocmunch-mcp
```
Repos: https://github.com/jgravelle/jcodemunch-mcp | https://github.com/jgravelle/jdocmunch-mcp

Add both to your Claude Code MCP config (`~/.claude/mcp_servers.json`) after installing.

## Step 5 — Set Up Memory (5 min)

Create your memory directory:

```bash
mkdir -p ~/.claude/projects/$(basename $(pwd))/memory
```

Add a `MEMORY.md` index file — Claude will auto-read this at session start and write to it when it learns something worth keeping.

See `guides/memory-system.md` for the full setup.

## That's It

Total cost: $20/month (Claude Pro).
Everything else is free.

---

## What to Expect

**First session:** Claude Code will follow the accuracy rules immediately. It'll push back more, ask for clarification, and refuse to fabricate — that's the system working.

**After a few sessions:** The memory system starts filling in. Claude remembers your project context, your preferences, what didn't work last time.

**After a week:** You stop repeating yourself. Session saves mean you can pick up exactly where you left off. The token gauge becomes second nature — you'll know when to compact before it even tells you.
