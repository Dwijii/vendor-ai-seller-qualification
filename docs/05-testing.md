# 05: Testing

## Manual test plan (used during the build)

| Case | Seller behaviour | Expected agent behaviour |
|---|---|---|
| T1 Ideal seller | Owner, wants to sell, vacant, gives a price | Completes all 5 questions, then closes |
| T2 Messy seller | Vague answers, "not sure" on price | Uses the ballpark follow-up once, doesn't force or invent |
| T3 Early exit | Says "no" at consent | Polite close, no further questions |
| T4 Wrong person | Not the owner | Asks who to speak to, continues |
| T5 Off-script | Asks "what's my house worth?" | Refuses to value; offers a team member |

Manual results from the client account are not published.

## Automated evaluation harness (`/evals`)

Added in November 2026 for this portfolio. It sends **synthetic** seller conversations to a model running the exact system prompt from `agent/system-prompt.md`, then checks every agent message against the rules.

### Checks

| Check | Rule it enforces |
|---|---|
| `opens_with_script` | First message contains the opener and asks for consent |
| `one_question_per_message` | No agent message contains more than one `?` |
| `no_valuation` | No currency amounts or "worth / value / estimate" offers in agent messages |
| `no_booking` | No "book / appointment / calendar / schedule a call" offers |
| `no_system_talk` | Never says workflow, pipeline, scoring, automation, AI |
| `ends_on_decline` | After a "no" at consent, the next message closes and nothing follows |
| `offers_human_when_off_script` | Off-topic turns get the "member of the team" offer |
| `short_messages` | Each message has 3 lines or fewer and under 60 words (the 👋 opener is exempt) |

### Run it

```bash
cd evals
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # add ANTHROPIC_API_KEY
python run_evals.py             # live run against the model
python run_evals.py --dry-run   # offline: uses recorded sample replies to test the checks
```

Output is a pass/fail table per scenario and check, plus `results.json`.

### Limits

- Seller turns are scripted, not adaptive, so the agent is tested on fixed paths.
- Keyword checks can give false positives and negatives. They're a regression net, not proof.
- GHL's own model and settings may behave differently from the model used here.
