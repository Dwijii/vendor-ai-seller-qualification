# GHL workflow specification (multi-node version)

The first implementation, built in **Automation → Workflows → Conversation AI**. It is kept here because comparing it with the single-prompt version is the main design decision in this project.

## Trigger

| Setting | Value |
|---|---|
| Trigger type | Chat Initiated (Conversation AI) |
| Channels | WhatsApp, web chat |

## Nodes

| # | Node type | Purpose | Output stored to |
|---|---|---|---|
| 1 | AI Message | Intro and consent ("Is that okay?") | — |
| 2 | If / Else | Reply contains yes / ok / sure → continue; else → polite exit → END | — |
| 3 | AI Message | Seller identity and authority (owner or decision-maker) | Contact note / custom field `Vendor AI – Seller Profile` |
| 4 | AI Message | Motivation, timeline, flexibility | `Vendor AI – Motivation` |
| 5 | AI Message | Property basics (address, type, beds) | `Vendor AI – Property Basics` |
| 6 | AI Message | Condition, occupancy, issues | `Vendor AI – Condition` |
| 7 | AI Message | Price expectation, agent involvement, wrap-up | `Vendor AI – Pricing` |
| 8 | AI Message (internal) | Summarise the conversation as a call brief | Contact note `Vendor AI Summary` |
| 9 | If / Else (planned) | Owner AND timeline ≤ 6 months AND price given → tag `Vendor – Qualified`, stage *Call Ready*; else tag `Vendor – Nurture` | Tags, pipeline stage |
| 10 | Add Tag (planned) | `Vendor AI – Completed` to stop re-trigger loops | Tag |

## Hardening steps planned after the build

- Reply delay of 1.5–2 seconds per AI message, so WhatsApp replies don't feel instant and robotic.
- The decline branch must END the workflow and never fall through to later questions.
- A separate workflow: on tag `Vendor AI – Completed`, create a same-day task "Review Vendor AI Summary" for the team.

Nodes 9 and 10 and the review-task workflow were planned, not confirmed as built. See `docs/06-status-and-limitations.md`.
