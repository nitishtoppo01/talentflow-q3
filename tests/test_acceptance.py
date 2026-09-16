"""One hand-built record per D3 edge case. If the prose and the code disagree, these win."""
import sys
from datetime import date

sys.path.insert(0, "src")

import pytest  # noqa: E402

from acceptance import acceptance, classify  # noqa: E402

AS_OF = date(2026, 9, 16)


def offer(oid="rec_o1", status="Accepted", sent="2026-06-01", decided="2026-06-10",
          app="rec_a1", **extra):
    f = {"Offer ID": oid, "Status": status, "Application": [app] if app else []}
    if sent:
        f["Offered On"] = sent
    if decided:
        f["Decision On"] = decided
    f.update(extra)
    return {"id": oid, "createdTime": "2026-08-27T00:00:00.000Z", "fields": f}


def app(aid="rec_a1", cand="rec_c1", opening="rec_j1", stage="Hired", **extra):
    f = {"Stage": stage}
    if cand:
        f["Candidate"] = [cand]
    if opening:
        f["Opening"] = [opening]
    f.update(extra)
    return {"id": aid, "createdTime": "2026-08-27T00:00:00.000Z", "fields": f}


APPS = {"rec_a1": app()}


# ---- one test per edge case named in the brief ----
@pytest.mark.parametrize("o,expected,label", [
    (offer(status="Accepted"), "accepted", "accepted counts in the numerator"),
    (offer(status="Declined"), "not_accepted", "declined counts in the denominator"),
    (offer(status="Pending", decided=None, sent="2026-09-01"), "open",
     "pending within 45 days is open: excluded from both point and range"),
    (offer(status="Pending", decided=None, sent="2026-01-01"), "unresolved",
     "pending and stale (>45 days) is unresolved: range only"),
    (offer(status="Pending", decided="2026-06-10"), "unresolved",
     "pending WITH a decision date is a status conflict: range only"),
    (offer(status="Expired"), "not_accepted",
     "expired counts as not accepted - the company let it lapse"),
    (offer(status="Withdrawn"), "not_accepted",
     "candidate withdrawal is a decline"),
    (offer(status="Rescinded"), "excluded",
     "rescinded by the company is not a candidate decision"),
    (offer(app=None), "excluded", "no linked application"),
    (offer(sent=None), "excluded", "no Offered On date"),
    (offer(sent="2026-06-10", decided="2026-06-01"), "excluded",
     "decision dated before the offer was sent"),
    (offer(**{"Offer ID": "test"}), "excluded", "test record, exact-value match"),
    (offer(status="Unknown Status"), "excluded", "status outside the expected set"),
])
def test_single_offer_classification(o, expected, label):
    bucket, _ = classify(o, APPS.get("rec_a1"), AS_OF)
    assert bucket == expected, label


def test_accepted_on_a_rejected_application_is_excluded():
    apps = {"rec_a1": app(stage="Rejected")}
    bucket, _ = classify(offer(status="Accepted"), apps["rec_a1"], AS_OF)
    assert bucket == "excluded"


def test_offer_with_no_linked_candidate_is_excluded():
    apps = {"rec_a1": app(cand=None)}
    bucket, _ = classify(offer(), apps["rec_a1"], AS_OF)
    assert bucket == "excluded"


def test_reissued_offer_counts_once_and_the_latest_version_wins():
    """Same candidate x opening, two offers: the later one is the episode's outcome."""
    apps = {"rec_a1": app(aid="rec_a1"), "rec_a2": app(aid="rec_a2")}
    offers = [offer("rec_o1", "Declined", "2026-02-01", "2026-02-10", app="rec_a1"),
              offer("rec_o2", "Accepted", "2026-07-01", "2026-07-10", app="rec_a2")]
    p = acceptance(offers, apps, AS_OF)
    assert p["n"] == 1 and p["accepted"] == 1
    assert p["excluded"]["re-issued offer superseded by a later version"] == 1


def test_exact_duplicate_records_count_once():
    apps = {"rec_a1": app()}
    offers = [offer("rec_o1"), offer("rec_o2")]   # same application, same everything
    p = acceptance(offers, apps, AS_OF)
    assert p["n"] == 1


def test_candidate_accepted_on_two_different_openings_is_excluded():
    apps = {"rec_a1": app(aid="rec_a1", opening="rec_j1"),
            "rec_a2": app(aid="rec_a2", opening="rec_j2")}
    offers = [offer("rec_o1", app="rec_a1"), offer("rec_o2", app="rec_a2")]
    p = acceptance(offers, apps, AS_OF)
    assert p["n"] == 0
    assert p["excluded"]["candidate accepted on two different openings"] == 2


def test_internal_candidate_is_included():
    """No field distinguishes internal candidates, so they are counted like any other."""
    apps = {"rec_a1": app(**{"Internal": True})}
    bucket, _ = classify(offer(), apps["rec_a1"], AS_OF)
    assert bucket == "accepted"


def test_accepted_then_reneged_stays_accepted():
    """Acme has no renege field; acceptance measures the decision when it was made."""
    bucket, _ = classify(offer(status="Accepted", **{"Reneged": True}), APPS["rec_a1"], AS_OF)
    assert bucket == "accepted"


def test_window_is_keyed_on_offered_on_not_decision_on():
    apps = {"rec_a1": app()}
    o = offer(sent="2026-03-31", decided="2026-04-02")
    inside = acceptance([o], apps, AS_OF, window=(date(2026, 1, 1), date(2026, 3, 31)))
    outside = acceptance([o], apps, AS_OF, window=(date(2026, 4, 1), date(2026, 6, 30)))
    assert inside["n"] == 1
    assert outside["n"] == 0


def test_below_min_n_shows_counts_not_a_rate():
    apps = {"rec_a1": app()}
    p = acceptance([offer()], apps, AS_OF)
    assert "%" not in p["display"] and "1/1" in p["display"]


def test_range_brackets_the_unresolved_records():
    apps = {"rec_a1": app(aid="rec_a1"), "rec_a2": app(aid="rec_a2", opening="rec_j2")}
    offers = [offer("rec_o1", "Accepted", app="rec_a1"),
              offer("rec_o2", "Pending", "2026-06-01", "2026-06-10", app="rec_a2")]
    p = acceptance(offers, apps, AS_OF)
    assert p["unresolved"] == 1
    assert p["range_low"] == pytest.approx(50.0)    # unresolved counts as declined
    assert p["range_high"] == pytest.approx(100.0)  # unresolved counts as accepted


def test_provisional_while_an_offer_is_still_open():
    apps = {"rec_a1": app()}
    p = acceptance([offer(status="Pending", decided=None, sent="2026-09-10")], apps, AS_OF)
    assert p["provisional"] is True


def test_guardrails_are_reported():
    apps = {"rec_a1": app()}
    p = acceptance([offer()], apps, AS_OF)
    g = p["guardrails"]
    assert "rescind_rate" in g
    assert "open_offers_older_than_45_days" in g
    assert g["median_days_to_decision"] == 9


def test_spec_reproduces_the_stage_4_cleaned_number():
    """The spec must give the same number as the Stage 4 waterfall: 23/28 = 82.1%."""
    from common import load
    offers = load("Offers")
    apps = {r["id"]: r for r in load("Applications")}
    p = acceptance(offers, apps, AS_OF)
    assert (p["accepted"], p["n"]) == (23, 28)
    assert round(p["rate"], 1) == 82.1
