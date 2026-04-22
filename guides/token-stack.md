# The Token-Saving Stack

Three tools that work together to cut your Claude Code token usage by 60-90%.
Install all three once. They run automatically after that.

---

## 1. RTK — Rust Token Killer

Intercepts every Bash command before it hits your context window and compresses the output. Transparent — you run `git status`, RTK runs it and strips the noise.

**Install:**
```bash
# Mac/Linux
curl -fsSL https://rtk.ai/install.sh | sh

# Windows (PowerShell)
irm https://rtk.ai/install.ps1 | iex
```

**Wire into Claude Code:**
```bash
rtk init -g
```

**Verify:**
```bash
rtk init --show    # all items should show [ok]
rtk gain           # shows token savings analytics
```

---

## 2. jMunch Family — Smart File Reading

Replaces Bash cat/grep/find with token-optimized readers. Each tool understands its file type and returns only what Claude needs.

| Tool | For | Token savings |
|------|-----|--------------|
| jCodeMunch | .py .ts .tsx .js | 50,000+ tokens per call |
| jDocMunch | .md .mdx .rst | Sections only, not full files |
| jDataMunch | .json .html .csv | Schema + sample, not full dump |

**Install:**
```bash
# Via Claude Code MCP config (~/.claude/claude_desktop_config.json)
# Add the jcodemunch-mcp server — see: https://github.com/jmunch/jcodemunch-mcp
```

**Use in CLAUDE.md:**
```
## Tool Priority
1. Code files → jCodeMunch (mcp__jcodemunch__*)
2. Doc files → jDocMunch (mcp__jdocmunch__*)
3. Data files → jDataMunch (mcp__jdatamunch__*)
```

---

## 3. fff — Fast File Finder

Frecency-ranked file search (frequent + recent files first). Replaces `find` and `ls -r` with a single MCP call. Git-dirty files boosted to top.

**Install:**
```bash
# Download binary from: https://github.com/albatrossflyon-coder/ai-token-dashboard
# Add fff-mcp to your MCP config
```

**Use in CLAUDE.md:**
```
## File Search
- Find files by name → fff (mcp__fff__find_files)
- Search file contents → fff grep (mcp__fff__grep)
- NEVER use Bash grep or find
```

---

## Combined CLAUDE.md Block

Copy this into your project's CLAUDE.md to wire all three at once:

```markdown
## Token-Efficient Navigation

### Tool Priority
1. Code files (.py/.ts/.tsx) → jCodeMunch (`mcp__jcodemunch__*`)
2. Doc files (.md/.mdx/.rst) → jDocMunch (`mcp__jdocmunch__*`)
3. Data files (.json/.html) → jDataMunch (`mcp__jdatamunch__*`)
4. File search by name → fff (`mcp__fff__find_files`)
5. File content search → fff grep (`mcp__fff__grep`)

### Bash: allowed ONLY for
- git commands
- Package installs (npm install, pip install)
- CLI execution and build runners

### RTK hook active
All Bash output is compressed by RTK before hitting context.
Run `rtk gain` to see savings.
```

---

Built by [Albatross AI](https://github.com/albatrossflyon-coder) — tools for contractors and builders who don't want to burn money on tokens.
