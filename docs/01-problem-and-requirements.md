# 01: Problem and requirements

## Context

A UK property-investment business buys homes directly from owners (often motivated sellers dealing with probate, relocation or a stalled sale). Paid social ads drive seller enquiries into GoHighLevel. Enquiries arrive at any hour, mostly by WhatsApp.

## Users

| User | Need |
|---|---|
| **Seller (lead)** | A quick, respectful reply; no pressure; to know someone will call |
| **Acquisitions team member** | Only call real sellers; know the address, intent, occupancy and price before dialling |
| **Agency (system owner)** | A repeatable setup that can be cloned for each property client |

## Functional requirements

| ID | Requirement |
|---|---|
| F1 | Reply to a new chat within seconds, 24/7 |
| F2 | Ask for consent before asking questions; exit cleanly on "no" |
| F3 | Confirm the person is the owner or a decision-maker |
| F4 | Confirm or capture the property address |
| F5 | Capture selling intent, occupancy status and price expectation |
| F6 | Offer a human whenever the conversation leaves the script |
| F7 | Store answers on the contact record for the caller |
| F8 | Never give valuations, book appointments, or give legal or financial advice |

## Non-functional requirements

- **Tone:** short, human, British English, one question per message.
- **Safety:** no claims about value; no mention of automation or scoring.
- **Maintainability:** non-developers must be able to edit the wording inside GHL.
- **Portability:** the same agent must work for several clients through merge fields (`{{ai.business_name}}`).

## Success criteria (how I would measure it)

| Metric | Why it matters |
|---|---|
| Time to first reply | The speed-to-lead problem this solves |
| % of chats completing all five questions | Measures conversation friction |
| % of completed chats tagged *qualified* | Filter effectiveness |
| Caller-rated brief usefulness (1–5) | Whether the handoff actually helps |

These metrics were defined for this write-up. Live figures from the client account are not published.
