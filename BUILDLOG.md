# Build Log — claude-token-operator-kit

Open-source Claude Code OS. Reduces token consumption 50-75% for multi-step automations.
**Rule: Update this file every time a file is added, changed, or a feature ships.**

---

## What This Is

Full Claude Code operating system — config, guides, skills, and tools to run Claude Code efficiently. Public repo, portfolio piece, and productivity toolkit.

---

## File Map

| Folder | Purpose |
|--------|---------|
| `config/` | Claude Code configuration templates |
| `guides/` | Usage guides and documentation |
| `skills/` | Reusable skill definitions |
| `tools/` | CLI tools and utilities |
| `README.md` | Public-facing documentation |

---

## Status

- **Repo:** `github.com/albatrossflyon-coder/claude-token-operator-kit` (public)
- **Local:** `C:\Repos\claude-token-operator-kit`
- Last updated: 2026-07-01

---

## Tool Versions — Current (2026-07-01)

| Tool | Version | Location |
|------|---------|----------|
| jcodemunch-mcp | 1.108.90 | pip (user), MCP scope: user |
| jdatamunch-mcp | 1.16.0 | pip (user), MCP scope: user |
| jdocmunch-mcp | 1.92.0 | pip (user), MCP scope: user |
| jmunch-mcp | 0.2.1 | pip (user) |
| fff-mcp | 0.9.6 (nightly) | `C:\Users\albat\.local\bin\fff-mcp.exe`, MCP scope: user |
| RTK | installed | `C:\Users\albat\.cargo\bin\rtk.exe` |

All four MCP servers (fff, jcodemunch, jdatamunch, jdocmunch) registered in `~/.claude.json` at user scope — active in all Claude Code projects after restart.

fff has no stable release channel — only nightlies. Latest nightly (0.9.7-nightly.e0a9e08, Jun 30 2026) includes MCP server. Installed binary reports as 0.9.6.

## Pending

- [ ] Add recent skills (bash-scripting, multi-agent-patterns, etc.)
- [ ] Update README with latest token savings benchmarks
- [ ] Add RTK (Rust Token Killer) integration docs
- [ ] Update CLAUDE.md template to mention fff for file search
