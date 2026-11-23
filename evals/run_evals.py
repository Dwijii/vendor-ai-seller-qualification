"""Run synthetic seller conversations against the Vendor AI system prompt.

Usage:
    python run_evals.py              # live: calls the Anthropic API
    python run_evals.py --dry-run    # offline: uses sample_replies.json
    python run_evals.py --only t5_off_script_valuation
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from checks import CHECKS  # noqa: E402
PROMPT_FILE = ROOT.parent / "agent" / "system-prompt.md"
SCENARIO_DIR = ROOT / "scenarios"
SAMPLE_REPLIES = ROOT / "sample_replies.json"


def load_prompt() -> str:
    text = PROMPT_FILE.read_text(encoding="utf-8")
    m = re.search(r"<!-- PROMPT-START -->\s*```text\n(.*?)```\s*<!-- PROMPT-END -->", text, re.S)
    if not m:
        sys.exit(f"Could not find the prompt block in {PROMPT_FILE}")
    return m.group(1).strip()


def fill_merge_fields(prompt: str, scenario: dict) -> str:
    values = {
        "ai.business_name": scenario.get("business_name", "Example Homebuyers"),
        "contact.first_name": scenario["contact"]["first_name"],
        "contact.address": scenario["contact"]["address"],
    }
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", lambda m: values.get(m.group(1), m.group(0)), prompt)


def load_scenarios(only: str | None) -> list[dict]:
    scenarios = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(SCENARIO_DIR.glob("*.json"))]
    return [s for s in scenarios if not only or s["id"] == only]


def run_live(system: str, seller_turns: list[str], model: str) -> list[str]:
    from anthropic import Anthropic  # imported here so --dry-run needs no SDK

    client = Anthropic()
    messages: list[dict] = []
    replies: list[str] = []
    for turn in seller_turns:
        messages.append({"role": "user", "content": turn})
        resp = client.messages.create(model=model, max_tokens=300, system=system, messages=messages)
        reply = "".join(b.text for b in resp.content if b.type == "text").strip()
        messages.append({"role": "assistant", "content": reply})
        replies.append(reply)
    return replies


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="use sample_replies.json instead of the API")
    ap.add_argument("--only", help="run a single scenario id")
    args = ap.parse_args()

    if not args.dry_run:
        try:
            from dotenv import load_dotenv

            load_dotenv(ROOT / ".env")
        except ImportError:
            pass
        if not os.getenv("ANTHROPIC_API_KEY"):
            sys.exit("ANTHROPIC_API_KEY is not set (copy .env.example to .env), or use --dry-run")
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

    prompt = load_prompt()
    samples = json.loads(SAMPLE_REPLIES.read_text(encoding="utf-8")) if args.dry_run else {}
    results = []
    failures = 0

    for s in load_scenarios(args.only):
        system = fill_merge_fields(prompt, s)
        replies = samples.get(s["id"], []) if args.dry_run else run_live(system, s["seller_turns"], model)
        checks = {}
        for name, fn in CHECKS.items():
            passed, detail = fn(s, replies)
            checks[name] = {"passed": passed, "detail": detail}
            failures += 0 if passed else 1
        results.append({"id": s["id"], "description": s["description"], "replies": replies, "checks": checks})

    width = max(len(n) for n in CHECKS)
    for r in results:
        print(f"\n{r['id']}: {r['description']}")
        for name, c in r["checks"].items():
            mark = "PASS" if c["passed"] else "FAIL"
            extra = f"  ({c['detail']})" if c["detail"] and c["detail"] != "n/a" else ""
            print(f"  {name:<{width}}  {mark}{extra}")

    out = ROOT / "results.json"
    out.write_text(json.dumps({"mode": "dry-run" if args.dry_run else model, "results": results}, indent=2))
    print(f"\n{len(results)} scenarios, {failures} failed checks. Details in {out.name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
