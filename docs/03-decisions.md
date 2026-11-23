# 03: Architecture decision records

## ADR-001: Single system prompt instead of a multi-node workflow

**Status:** Accepted (February 2026)

**Context.** The first build used one GHL "AI message" node per question group, with If/Else branches between them (`agent/ghl-workflow-spec.md`). This gave fine control over where each answer was stored. But the bot had to follow the sequence exactly and not stray, grouped questions made messages long (against the "one question at a time" rule), and deploying the multi-node setup through GHL snapshots ran into difficulties. *(The details of the snapshot issue are not in the surviving notes.)*

**Decision.** Move the whole flow into one Conversation AI system prompt with explicit hard rules and a fixed sequence (`agent/system-prompt.md`).

**Consequences.**
- ➕ One place to edit; consistent tone; easy to clone per client via `{{ai.business_name}}`.
- ➕ The model holds context across the whole chat, so it handles "No, it's actually 14 Elm Road" naturally.
- ➖ Less structured storage. Answers land in the conversation rather than in separate fields, so a summary step (or later field extraction) is needed.
- ➖ Compliance depends on the model following instructions. That's why the `/evals` harness exists.

## ADR-002: Build inside GHL rather than an external agent service

**Status:** Accepted

**Context.** The client's leads, messaging channels and team already lived in GHL. An external agent (for example a custom API service) would need WhatsApp integration, contact sync and a second system to maintain.

**Decision.** Use GHL Conversation AI and native workflows.

**Consequences.** Faster to ship and maintainable by non-developers. In exchange, there's less control over model choice and logging, and testing has to happen outside GHL (hence the harness, which calls a model directly with the same prompt).

## ADR-003: Hard ban on valuations and booking

**Status:** Accepted

**Context.** A bot quoting a value creates a commercial expectation, and possibly a regulatory one. Booking needs a human to judge whether the lead is worth a call.

**Decision.** The prompt forbids valuations, value estimates, booking, and legal or financial advice. It hands off instead.

**Consequences.** Slightly less "complete" for the seller, but no liability from AI-generated numbers. The evaluation checks enforce this.

## ADR-004: Stable external IDs on contacts and properties

**Status:** Accepted (prepared, sync not live)

**Context.** The client planned to analyse deals in a separate app. Records had to be matchable in both directions without relying on names or addresses.

**Decision.** Add `lovable_contact_id` on contacts and `lovable_property_id` on the Property object now, before any sync exists. The inbound webhook workflow upserts on `lovable_property_id`.

**Consequences.** No rework when the sync is switched on. Until then the fields are empty.
