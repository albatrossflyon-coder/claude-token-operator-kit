# Claude Code Configuration

## Accuracy Rules (Anthropic Research-Backed)
- **Only answer if confident** — if unsure, say so directly. Do not fabricate.
- **No sycophancy** — never reverse-engineer reasoning to agree with a suggestion. Check independently first.
- **Accept redirects** — if stopped mid-response, don't resist. Restart from the new direction.
- **Context at 50% = compact** — accuracy degrades at message 30+. Run /compact at 50% context to reset.

## Tool Priority (Token-Efficient Navigation)

### Four-Tier System
1. **Code files** (.py/.ts/.tsx) → jCodeMunch (`mcp__jcodemunch__*`)
2. **Doc files** (.md/.mdx/.rst) → jDocMunch (`mcp__jdocmunch__*`)
3. **Data files** (.json/.html, >100 lines) → jDataMunch
4. **File search by name** → fff (`mcp__fff__find_files`)
5. **File content search** → fff grep (`mcp__fff__grep`)

### Bash is ONLY allowed for:
- git commands (status, add, commit, diff, log)
- Package installs (npm install, pip install)
- CLI execution
- Build/test runners

### NEVER use Bash for:
- Reading files → Read tool or jCodeMunch/jDocMunch
- Searching file contents → fff grep
- Finding files → fff find_files
- Parsing JSON → jDataMunch
- Reading markdown → jDocMunch
- Reading code → jCodeMunch

## Output Rules
- Lead with the answer. No methodology preamble.
- No filler openers or closers.
- One qualifier per claim maximum.
- Return JSON with no indentation.
- Omit null/empty keys.

## Core Rules
- Ask before deleting anything
- Commit after every working feature
- Use /plan for any task over 5 minutes
- One task at a time — confirm before moving on
