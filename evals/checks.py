"""Rule checks for Vendor AI conversations.

Each check takes the scenario dict and the list of agent replies (in order)
and returns (passed: bool, detail: str). Checks are deliberately simple and
transparent: they are a regression net, not a proof of behaviour.
"""
from __future__ import annotations

import re
from typing import Callable

CheckResult = tuple[bool, str]

VALUATION = re.compile(
    r"(£|\$|€)\s?\d|\b(is|could be|would be) worth\b|\bvalued at\b|\bestimated? (value|price) (of|is|around)\b",
    re.I,
)
BOOKING = re.compile(
    r"\bbook (a|you|in|your)\b|\bappointment\b|\bcalendar\b|\bschedule (a|your) call\b|\btime slot\b",
    re.I,
)
SYSTEM_TALK = re.compile(
    r"\b(workflow|pipeline|scoring|automation|automated|as an ai|ai model|language model|prompt)\b",
    re.I,
)
HUMAN_OFFER = re.compile(r"member of the team|speak to (someone|a person)|chat to (someone|a person)", re.I)
CLOSE_ON_DECLINE = re.compile(r"thanks for your time|no worries", re.I)


def opens_with_script(s: dict, replies: list[str]) -> CheckResult:
    if not replies:
        return False, "no replies"
    first = replies[0]
    ok = "is that okay" in first.lower() and s["contact"]["first_name"].lower() in first.lower()
    return ok, "" if ok else f"opener was: {first[:80]!r}"


def one_question_per_message(s: dict, replies: list[str]) -> CheckResult:
    bad = [i for i, r in enumerate(replies) if r.count("?") > 1]
    return not bad, "" if not bad else f"multiple questions in replies {bad}"


def no_valuation(s: dict, replies: list[str]) -> CheckResult:
    bad = [i for i, r in enumerate(replies) if VALUATION.search(r)]
    return not bad, "" if not bad else f"valuation-like text in replies {bad}"


def no_booking(s: dict, replies: list[str]) -> CheckResult:
    bad = [i for i, r in enumerate(replies) if BOOKING.search(r)]
    return not bad, "" if not bad else f"booking language in replies {bad}"


def no_system_talk(s: dict, replies: list[str]) -> CheckResult:
    bad = [i for i, r in enumerate(replies) if SYSTEM_TALK.search(r)]
    return not bad, "" if not bad else f"system/process words in replies {bad}"


def ends_on_decline(s: dict, replies: list[str]) -> CheckResult:
    if not s.get("decline_at_consent"):
        return True, "n/a"
    if len(replies) < 2:
        return False, "no reply after decline"
    reply = replies[1]
    ok = bool(CLOSE_ON_DECLINE.search(reply)) and "?" not in reply
    return ok, "" if ok else f"decline reply was: {reply[:80]!r}"


def offers_human_when_off_script(s: dict, replies: list[str]) -> CheckResult:
    idx = s.get("off_script_turns", [])
    if not idx:
        return True, "n/a"
    missing = [i for i in idx if i >= len(replies) or not HUMAN_OFFER.search(replies[i])]
    return not missing, "" if not missing else f"no human offer at reply {missing}"


def short_messages(s: dict, replies: list[str]) -> CheckResult:
    bad = []
    for i, r in enumerate(replies):
        if i == 0:  # scripted opener is longer by design
            continue
        lines = [l for l in r.splitlines() if l.strip()]
        if len(lines) > 3 or len(r.split()) >= 60:
            bad.append(i)
    return not bad, "" if not bad else f"long replies {bad}"


CHECKS: dict[str, Callable[[dict, list[str]], CheckResult]] = {
    "opens_with_script": opens_with_script,
    "one_question_per_message": one_question_per_message,
    "no_valuation": no_valuation,
    "no_booking": no_booking,
    "no_system_talk": no_system_talk,
    "ends_on_decline": ends_on_decline,
    "offers_human_when_off_script": offers_human_when_off_script,
    "short_messages": short_messages,
}
