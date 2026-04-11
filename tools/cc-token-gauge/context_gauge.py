#!/usr/bin/env python3
"""
context_gauge.py — Claude Code Token Dashboard
Watches the active session JSONL and displays a live token breakdown.
Run in a separate terminal pane: python context_gauge.py

Usage:
  python context_gauge.py              # auto-finds active session
  python context_gauge.py <path.jsonl> # watch a specific session
  python context_gauge.py --once       # print once and exit (no loop)
"""

import json
import os
import sys
import time
from pathlib import Path

# ── Model context limits ──────────────────────────────────────────────────────
MODEL_LIMITS = {
    "claude-sonnet-4-6": 200_000,
    "claude-opus-4-6":   200_000,
    "claude-haiku-4-5":  200_000,
}
DEFAULT_LIMIT = 200_000

# ── Pricing per million tokens (USD) ─────────────────────────────────────────
# Sonnet 4.6 / Opus 4.6 rates (update if Anthropic changes pricing)
PRICING = {
    "input":          3.00,   # fresh input
    "cache_creation": 3.75,   # writing to prompt cache
    "cache_read":     0.30,   # reading from prompt cache (10x cheaper)
    "output":        15.00,   # generated tokens
}

# ── ANSI colours ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

REFRESH_SECS = 5


# ─────────────────────────────────────────────────────────────────────────────
def find_active_session() -> Path | None:
    """Return the most-recently-modified *.jsonl under ~/.claude/projects/."""
    base = Path.home() / ".claude" / "projects"
    if not base.exists():
        return None
    files = list(base.rglob("*.jsonl"))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def parse_session(path: Path) -> dict:
    """
    Walk the JSONL once and collect:
      - latest usage snapshot (last assistant turn)
      - cumulative cost across all turns
      - message + tool-call counts
      - model name
    """
    latest_usage: dict = {}
    total_cost    = 0.0
    msg_count     = 0
    output_total  = 0
    tool_count    = 0
    model         = "claude-sonnet-4-6"
    compacted     = False

    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                # ── assistant message with usage ──────────────────────────
                msg = entry.get("message", {})
                if msg.get("role") == "assistant" and "usage" in msg:
                    u = msg["usage"]
                    latest_usage = u
                    model = msg.get("model", model)
                    msg_count += 1
                    output_total += u.get("output_tokens", 0)

                    # accumulate cost per turn
                    total_cost += (u.get("input_tokens", 0)                  / 1e6) * PRICING["input"]
                    total_cost += (u.get("cache_creation_input_tokens", 0)   / 1e6) * PRICING["cache_creation"]
                    total_cost += (u.get("cache_read_input_tokens", 0)       / 1e6) * PRICING["cache_read"]
                    total_cost += (u.get("output_tokens", 0)                 / 1e6) * PRICING["output"]

                # ── tool calls ────────────────────────────────────────────
                if entry.get("type") in ("tool_use", "create") or (
                    isinstance(msg.get("content"), list)
                    and any(c.get("type") == "tool_use" for c in msg.get("content", []))
                ):
                    tool_count += 1

                # ── detect /compact events ────────────────────────────────
                if entry.get("type") == "system" and "compact" in str(entry).lower():
                    compacted = True

    except (IOError, OSError):
        pass

    return {
        "usage":        latest_usage,
        "cost":         total_cost,
        "messages":     msg_count,
        "output_total": output_total,
        "tools":        tool_count,
        "model":        model,
        "compacted":    compacted,
        "session_file": path.name,
    }


# ─────────────────────────────────────────────────────────────────────────────
def bar(pct: float, width: int = 22) -> str:
    """Colour-coded block progress bar."""
    filled = round(pct / 100 * width)
    filled = max(0, min(filled, width))
    b = "█" * filled + "░" * (width - filled)
    if pct >= 80: colour = RED
    elif pct >= 50: colour = YELLOW
    else: colour = GREEN
    return f"{colour}{b}{RESET}"


def risk_label(messages: int, ctx_pct: float) -> tuple[str, str]:
    """(label, colour) based on Anthropic degradation research."""
    if ctx_pct >= 80 or messages >= 30:
        return "HIGH  ⚠", RED
    if ctx_pct >= 50 or messages >= 20:
        return "MEDIUM", YELLOW
    return "LOW   ✓", GREEN


def render(data: dict) -> str:
    u = data["usage"]
    inp   = u.get("input_tokens", 0)
    ccr   = u.get("cache_creation_input_tokens", 0)  # cache created
    crd   = u.get("cache_read_input_tokens", 0)       # cache read
    out   = u.get("output_tokens", 0)

    limit     = MODEL_LIMITS.get(data["model"], DEFAULT_LIMIT)
    ctx_total = inp + ccr + crd
    ctx_pct   = min(100.0, ctx_total / limit * 100)

    cost      = data["cost"]
    msgs      = data["messages"]
    velocity  = data["output_total"] / max(msgs, 1)

    # Cache efficiency — what % of cached tokens were reads (cheap) vs writes
    cached_all  = ccr + crd
    cache_eff   = (crd / cached_all * 100) if cached_all else 0.0

    risk, rc = risk_label(msgs, ctx_pct)

    # Context status tag
    if ctx_pct >= 80:   ctx_tag = f"{RED}⚠  RUN /compact NOW{RESET}"
    elif ctx_pct >= 50: ctx_tag = f"{YELLOW}⚡ compact soon{RESET}"
    else:               ctx_tag = f"{GREEN}✓  healthy{RESET}"

    W = 54  # inner width
    HL = "═" * W

    def row(label: str, gauge: str, detail: str) -> str:
        """Fixed-width dashboard row."""
        content = f"  {label:<10} {gauge}  {detail}"
        pad = W - len(_strip_ansi(content)) + 2
        return f"║{content}{' ' * max(pad, 0)}║"

    def info(text: str) -> str:
        pad = W - len(_strip_ansi(text)) + 2
        return f"║  {text}{' ' * max(pad - 2, 0)}║"

    def divider() -> str:
        return f"╠{HL}╣"

    lines = [
        f"╔{HL}╗",
        info(f"{BOLD}CC TOKEN DASHBOARD{RESET}  {DIM}{data['model']}{RESET}"),
        info(f"{DIM}session: {data['session_file'][:42]}{RESET}"),
        divider(),
        row("CONTEXT",  bar(ctx_pct),                    f"{ctx_pct:5.1f}%  {ctx_tag}"),
        row("COST",     bar(min(cost / 5.0 * 100, 100)), f"${cost:.4f}  {DIM}(est, $5=full bar){RESET}"),
        row("MESSAGES", bar(msgs / 50 * 100),            f"{msgs:3d}  {DIM}(30+ = degradation risk){RESET}"),
        row("VELOCITY", bar(velocity / 2000 * 100),      f"{velocity:,.0f} tok/msg"),
        divider(),
        info(f"{BOLD}TOKEN BREAKDOWN  (latest turn){RESET}"),
        info(f"  Input (fresh):   {inp:>10,}   {DIM}@ $3.00/M{RESET}"),
        info(f"  Cache READ:      {crd:>10,}   {DIM}@ $0.30/M  ← cheap{RESET}"),
        info(f"  Cache CREATED:   {ccr:>10,}   {DIM}@ $3.75/M{RESET}"),
        info(f"  Output:          {out:>10,}   {DIM}@ $15.00/M{RESET}"),
        info(f"  Total context:   {ctx_total:>10,}   {DIM}/ {limit:,}{RESET}"),
        divider(),
        info(f"  Cache efficiency : {cache_eff:5.1f}%   {DIM}(high = lower cost){RESET}"),
        info(f"  Tool calls       : {data['tools']:5d}   {DIM}this session{RESET}"),
        info(f"  Compacted        : {'YES' if data['compacted'] else 'no'}"),
        info(f"  Degradation risk : {rc}{risk}{RESET}   {DIM}(Anthropic research){RESET}"),
        divider(),
    ]

    # Advice
    if ctx_pct >= 80:
        advice = f"  {RED}→  /compact immediately — context degrading past 80%{RESET}"
    elif msgs >= 25 or ctx_pct >= 55:
        advice = f"  {YELLOW}→  plan to /compact before message 30 or 80% context{RESET}"
    elif cache_eff < 30:
        advice = f"  {YELLOW}→  low cache reuse — consider /compact to rebuild cache{RESET}"
    else:
        advice = f"  {GREEN}→  session healthy — keep going{RESET}"

    lines += [
        f"║{advice}{'':>{W - len(_strip_ansi(advice)) + 1}}║",
        f"╚{HL}╝",
        f"  {DIM}Refreshes every {REFRESH_SECS}s  •  Ctrl+C to exit{RESET}",
    ]

    return "\n".join(lines)


def _strip_ansi(s: str) -> str:
    """Remove ANSI escape codes for length calculation."""
    import re
    return re.sub(r"\033\[[0-9;]*m", "", s)


# ─────────────────────────────────────────────────────────────────────────────
def main():
    once = "--once" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        path = Path(args[0])
    else:
        path = find_active_session()

    if not path or not path.exists():
        print("No CC session found. Start Claude Code first, or pass a .jsonl path.")
        sys.exit(1)

    if once:
        data = parse_session(path)
        print(render(data))
        return

    print(f"Watching: {path}\n")
    time.sleep(1)

    try:
        while True:
            data = parse_session(path)
            os.system("cls" if os.name == "nt" else "clear")
            print(render(data))
            time.sleep(REFRESH_SECS)
    except KeyboardInterrupt:
        print("\nDashboard closed.")


if __name__ == "__main__":
    main()
