"""Canonical offer-acceptance metric (D3). One definition, used by metrics.py and tests.

Every rule here is stated in docs/submission.md section D3. If the prose and this
module disagree, tests/test_acceptance.py decides.
"""
import re
from collections import defaultdict
from datetime import date

MIN_N = 30                 # below this, show counts not a rate
STALE_DAYS = 45            # an undecided offer older than this is stale, not open
TIMEZONE = "Asia/Kolkata"  # period boundaries; all Offers dates are date-only IST

ACCEPTED, DECLINED = "Accepted", "Declined"
# Forward-compatible: these statuses do not exist in Acme's base today.
NOT_ACCEPTED_STATUSES = {"Declined", "Withdrawn", "Expired"}
RESCINDED_STATUSES = {"Rescinded"}
TEST_TOKENS = {"test", "dummy", "sample", "asdf", "xxx", "foo"}


def _d(v):
    return date.fromisoformat(v[:10]) if isinstance(v, str) and v else None


def _first(rec, f):
    return (rec.get("fields", {}).get(f) or [None])[0]


def _is_test(rec):
    return any(isinstance(v, str) and v.strip().lower() in TEST_TOKENS
               for v in rec.get("fields", {}).values())


def classify(offer, app=None, as_of=None):
    """Classify ONE offer record. Returns (bucket, reason).

    bucket is one of: accepted, not_accepted, unresolved, excluded, open.
    """
    as_of = as_of or date.today()
    f = offer.get("fields", {})
    status = f.get("Status")
    sent, decided = _d(f.get("Offered On")), _d(f.get("Decision On"))

    if _is_test(offer) or (app is not None and _is_test(app)):
        return "excluded", "test record"
    if not f.get("Application"):
        return "excluded", "no linked application"
    if app is not None and not app.get("fields", {}).get("Candidate"):
        return "excluded", "no linked candidate"
    if sent is None:
        return "excluded", "no Offered On date"
    if decided is not None and decided < sent:
        return "excluded", "decision dated before the offer was sent"
    if status in RESCINDED_STATUSES:
        return "excluded", "rescinded by the company"
    if app is not None and status == ACCEPTED and \
            app.get("fields", {}).get("Stage") in ("Rejected", "Withdrawn"):
        return "excluded", "accepted offer on a rejected/withdrawn application"

    if status == ACCEPTED:
        return "accepted", ""
    if status in NOT_ACCEPTED_STATUSES:
        return "not_accepted", "candidate declined, withdrew, or the offer expired"
    if status == "Pending":
        if decided is not None:
            return "unresolved", "status Pending but a decision is dated"
        if (as_of - sent).days > STALE_DAYS:
            return "unresolved", "undecided for more than {} days".format(STALE_DAYS)
        return "open", "awaiting a decision, within the {}-day window".format(STALE_DAYS)
    return "excluded", "status outside the expected set"


def episodes(offers, apps_by_id):
    """Group offers into episodes (one candidate x one job opening) and pick the
    winning offer: latest Offered On, then latest Decision On, then highest Offer ID."""
    groups = defaultdict(list)
    for o in offers:
        app = apps_by_id.get(_first(o, "Application"))
        key = ((_first(app, "Candidate") if app else None),
               (_first(app, "Opening") if app else None),
               o["id"] if app is None else None)
        groups[key].append(o)
    out = []
    for key, os_ in groups.items():
        winner = sorted(os_, key=lambda o: (o["fields"].get("Offered On", ""),
                                            o["fields"].get("Decision On", ""),
                                            o["fields"].get("Offer ID", "")))[-1]
        out.append((key, winner, len(os_) - 1))
    return out


def acceptance(offers, apps_by_id, as_of=None, window=None):
    """The metric. Returns the full dashboard payload."""
    as_of = as_of or date.today()
    excluded = defaultdict(int)
    eps = episodes(offers, apps_by_id)

    superseded = sum(n for _, _, n in eps)
    if superseded:
        excluded["re-issued offer superseded by a later version"] = superseded

    if window:
        lo, hi = window
        kept = []
        for key, o, n in eps:
            sent = _d(o["fields"].get("Offered On"))
            if sent and lo <= sent <= hi:
                kept.append((key, o, n))
            else:
                excluded["outside the reporting window"] += 1
        eps = kept

    # candidate accepted on two different openings -> unresolvable conflict
    acc_reqs = defaultdict(set)
    for key, o, _ in eps:
        if o["fields"].get("Status") == ACCEPTED and key[0]:
            acc_reqs[key[0]].add(key[1])
    conflicted = {c for c, reqs in acc_reqs.items() if len(reqs) > 1}

    accepted = not_accepted = 0
    unresolved, open_now = [], []
    for key, o, _ in eps:
        if key[0] in conflicted:
            excluded["candidate accepted on two different openings"] += 1
            continue
        bucket, reason = classify(o, apps_by_id.get(_first(o, "Application")), as_of)
        if bucket == "accepted":
            accepted += 1
        elif bucket == "not_accepted":
            not_accepted += 1
        elif bucket == "unresolved":
            unresolved.append((o, reason))
        elif bucket == "open":
            open_now.append(o)
        else:
            excluded[reason] += 1

    n = accepted + not_accepted
    rate = 100.0 * accepted / n if n else None
    rng_d = n + len(unresolved)
    payload = {
        "accepted": accepted, "not_accepted": not_accepted, "n": n,
        "rate": rate,
        "display": ("{}/{} (n<{}, counts shown instead of a rate)".format(accepted, n, MIN_N)
                    if n < MIN_N else "{:.1f}%".format(rate)),
        "range_low": 100.0 * accepted / rng_d if rng_d else None,
        "range_high": 100.0 * (accepted + len(unresolved)) / rng_d if rng_d else None,
        "unresolved": len(unresolved),
        "unresolved_reasons": dict(sorted(
            {r: sum(1 for _, rr in unresolved if rr == r)
             for _, r in unresolved}.items())),
        "open": len(open_now),
        "provisional": bool(open_now),
        "excluded": dict(excluded),
        "guardrails": guardrails(offers, apps_by_id, as_of),
    }
    return payload


def guardrails(offers, apps_by_id, as_of=None):
    as_of = as_of or date.today()
    rescinded = sum(1 for o in offers
                    if o["fields"].get("Status") in RESCINDED_STATUSES)
    stale = [o for o in offers if o["fields"].get("Status") == "Pending"
             and not o["fields"].get("Decision On")
             and _d(o["fields"].get("Offered On"))
             and (as_of - _d(o["fields"].get("Offered On"))).days > STALE_DAYS]
    days = sorted((_d(o["fields"]["Decision On"]) - _d(o["fields"]["Offered On"])).days
                  for o in offers
                  if o["fields"].get("Decision On") and o["fields"].get("Offered On"))
    return {
        "rescind_rate": "{}/{}".format(rescinded, len(offers)) if offers else "0/0",
        "open_offers_older_than_{}_days".format(STALE_DAYS): len(stale),
        "median_days_to_decision": days[len(days) // 2] if days else None,
    }
