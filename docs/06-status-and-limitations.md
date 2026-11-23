# 06: Status and limitations

## Status: configured prototype

| Item | Status |
|---|---|
| Qualification flow and rules (v1 script) | ✅ Written |
| Conversation AI workflow in GHL | ✅ Built (reported complete, Feb 2026) |
| Single-prompt version | ✅ Written |
| Property custom object, IDs, pipeline | ✅ Configured |
| Qualified / Nurture tagging, completion tag, review task | 🟡 Designed, not confirmed built |
| Webhook upsert from external app | 🟡 Shell prepared, untested |
| External app sync (Zapier) | ⬜ Not started (access pending) |
| Evaluation harness | ✅ Added Nov 2026 (portfolio work) |
| Production metrics | ⬜ Not published |

## Known limitations

- Answers are captured as conversation text and an AI summary, not yet as structured Property fields.
- Prompt compliance relies on the model. There is no hard state machine.
- WhatsApp templates and the 24-hour messaging window are handled by GHL settings outside this repo.

## What I'd do next

1. Add a structured-extraction step: an AI summary → JSON → Property fields, then create the Property automatically.
2. Score leads (hot / warm / nurture) from intent + timeline + price, and route them to pipeline stages.
3. Log every conversation to a dataset and run the harness on real (anonymised) transcripts.
4. Move to an external agent service only if model choice or observability becomes the limiting factor (see ADR-002).
