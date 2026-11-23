# Vendor AI evaluation harness

Runs scripted, synthetic seller conversations against `../agent/system-prompt.md` and checks every agent reply against the agent's hard rules. See `../docs/05-testing.md` for the check list.

```bash
pip install -r requirements.txt
python run_evals.py --dry-run     # no API key needed; validates the checks against sample replies
cp .env.example .env              # add ANTHROPIC_API_KEY
python run_evals.py               # live run
python run_evals.py --only t5_off_script_valuation
```

| File | Purpose |
|---|---|
| `scenarios/*.json` | One synthetic conversation each: seller turns, contact merge fields, expectations |
| `sample_replies.json` | Hand-written "good" agent replies used by `--dry-run` |
| `checks.py` | The rule checks |
| `run_evals.py` | Fills merge fields, runs the conversation, prints PASS/FAIL, writes `results.json` |

All names and addresses are fictional.
