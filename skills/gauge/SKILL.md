---
name: gauge
description: >
  Print a one-time token usage snapshot for the current Claude Code session.
  Shows context %, cost, cache efficiency, degradation risk.
  Use when you want a quick token check without opening a second terminal.
  Triggers on: /gauge, "check tokens", "how much context", "token snapshot"
---

Run the context gauge in snapshot mode and print the result inline.

## Steps

1. Find the gauge script:
   - Check `tools/context-gauge/context_gauge.py` relative to current working directory
   - Check `~/cc-token-gauge/context_gauge.py`
   - If neither found: tell user to install from https://github.com/albatrossflyon/cc-token-gauge

2. Run it with --once flag:
```bash
python "tools/context-gauge/context_gauge.py" --once
```

3. Print the full dashboard output inline in the conversation.

4. Add one line of advice based on the output:
   - Context > 80%: "Run /compact now."
   - Messages > 30 + context > 50%: "Plan to /compact before next major task."
   - Cache efficiency < 30%: "Low cache reuse — /compact will rebuild cache and cut costs."
   - Otherwise: "Session healthy."

## If Python Not Found

Tell the user:
```
Python not found. Run this in a terminal instead:
python "C:/Users/<you>/Desktop/Universal Brain/tools/context-gauge/context_gauge.py" --once
```

## Notes
- --once flag prints once and exits. No loop, no refresh.
- Auto-finds the active session JSONL — no path needed.
- Works in CC terminal and CC Desktop.
