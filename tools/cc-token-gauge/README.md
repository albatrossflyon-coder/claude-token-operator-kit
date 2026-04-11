# cc-token-gauge

A live token dashboard for Claude Code. Runs in a second terminal pane alongside your session.

Zero dependencies. Pure Python. Works on Windows, Mac, Linux.

![CC Token Dashboard](screenshot.png)

```
╔══════════════════════════════════════════════════════╗
║  CC TOKEN DASHBOARD  claude-sonnet-4-6               ║
║  session: 46c62d90-0615-4d4f-b853-2c0edd0f0583.jsonl ║
╠══════════════════════════════════════════════════════╣
║  CONTEXT    ███████░░░░░░░░░░░░░░░   33.2%  ✓  healthy ║
║  COST       ██████████████████████  $11.55  (est)    ║
║  MESSAGES   ██████████████████████  237  (30+ = risk)║
║  VELOCITY   ███████░░░░░░░░░░░░░░░  624 tok/msg      ║
╠══════════════════════════════════════════════════════╣
║  TOKEN BREAKDOWN  (latest turn)                      ║
║    Input (fresh):            3   @ $3.00/M           ║
║    Cache READ:          66,051   @ $0.30/M  ← cheap  ║
║    Cache CREATED:          357   @ $3.75/M           ║
║    Output:                 137   @ $15.00/M          ║
║    Total context:       66,411   / 200,000           ║
╠══════════════════════════════════════════════════════╣
║    Cache efficiency :  99.5%   (high = lower cost)   ║
║    Tool calls       :   123   this session           ║
║    Compacted        : YES                            ║
║    Degradation risk : HIGH  ⚠   (Anthropic research) ║
╠══════════════════════════════════════════════════════╣
║  →  plan to /compact before message 30 or 80% context║
╚══════════════════════════════════════════════════════╝
```

## Why

Claude Code doesn't show you what's happening to your tokens. You're flying blind on:

- How close you are to context limits
- What your session is actually costing
- Whether your prompt cache is working
- When to run `/compact` before accuracy degrades

This script reads your active session JSONL directly — no API calls, no dependencies, no setup.

## Install

```bash
git clone https://github.com/YOUR_USERNAME/cc-token-gauge
```

That's it. Requires Python 3.10+.

## Usage

Open a second terminal pane while Claude Code is running:

```bash
python context_gauge.py              # auto-finds active session, refreshes every 5s
python context_gauge.py --once       # print once and exit
python context_gauge.py path/to/session.jsonl  # watch a specific file
```

`Ctrl+C` to exit.

## What Each Gauge Means

| Gauge | What it tracks |
|-------|---------------|
| CONTEXT | % of 200k context window used. Run `/compact` at 80%. |
| COST | Cumulative session cost in USD. Estimated from token counts × Anthropic pricing. |
| MESSAGES | Total assistant turns. Accuracy degrades at 30+ (Anthropic research). |
| VELOCITY | Average output tokens per message. High = longer responses. |
| Cache READ | Tokens served from prompt cache. These cost 10x less than fresh input. |
| Cache CREATED | New cache writes this turn. Slightly more expensive than fresh input. |
| Cache efficiency | `cache_read / (cache_read + cache_created)`. Higher = cheaper session. |
| Degradation risk | Based on message count + context %. Goes HIGH at 30+ messages or 80%+ context. |

## Pricing Used

Sonnet 4.6 / Opus 4.6 rates:

| Token type | Price per 1M |
|-----------|-------------|
| Input (fresh) | $3.00 |
| Cache creation | $3.75 |
| Cache read | $0.30 |
| Output | $15.00 |

Update `PRICING` in `context_gauge.py` if Anthropic changes rates.

## The Research Behind It

Anthropic's own research shows Claude's accuracy degrades in long sessions because:

1. The "I don't know" circuit gets overridden by competing signals
2. Reasoning becomes performative — right-looking but wrong
3. Sycophancy via reverse-engineered agreement
4. Internal momentum prevents mid-sentence self-correction
5. Context decay as earlier instructions fade

The degradation risk gauge is a practical implementation of this research. When it goes HIGH, run `/compact`.

## How It Works

Claude Code writes every session to a JSONL file at `~/.claude/projects/*/`. Each assistant turn includes a `usage` block with token counts. This script:

1. Finds the most recently modified JSONL (= your active session)
2. Walks every line, extracts usage from assistant turns
3. Calculates cumulative cost, cache efficiency, context %
4. Renders the dashboard with ANSI colors
5. Refreshes every 5 seconds

No API calls. No authentication. No packages to install.

## Customization

- `REFRESH_SECS` — change refresh rate (default: 5)
- `PRICING` — update token prices
- `MODEL_LIMITS` — add new models or update context windows

## License

MIT — use it, fork it, ship it.
