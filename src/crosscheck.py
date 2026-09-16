"""Challenge: recompute the largest issue counts in pandas, against the plain-Python audit."""
import re

import pandas as pd

from common import load_all

D = load_all()


def df(table):
    rows = []
    for r in D[table]:
        d = {"id": r["id"], "createdTime": r["createdTime"]}
        d.update(r["fields"])
        rows.append(d)
    return pd.DataFrame(rows)


apps, cands, offers, jobs = df("Applications"), df("Candidates"), df("Offers"), df("Job Openings")
people = df("People")
first = lambda s: s.apply(lambda v: v[0] if isinstance(v, list) and v else None)


def main():
    out = []

    # 1. applications submitted after the opening's Target Close
    j = jobs[["id", "Target Close", "Status", "Headcount"]].rename(
        columns={"id": "Opening_id", "Status": "job_status"})
    a = apps.copy()
    a["Opening_id"] = first(a["Opening"])
    m = a.merge(j, on="Opening_id", how="left")
    n1 = int((m["Applied On"] > m["Target Close"]).sum())
    out.append(("applications applied after Target Close", 251, n1))

    # 2. duplicate candidates on normalised name + phone
    c = cands.copy()
    c["key"] = (c["Full Name"].str.strip().str.lower() + "|"
                + c["Phone"].str.replace(r"\D", "", regex=True))
    n2 = int(c[c.duplicated("key", keep=False)].shape[0])
    out.append(("duplicate candidates (name+phone)", 12, n2))

    # 3. hiring manager outside the opening's department
    p = people[["id", "Department"]].copy()
    p["hm_dept"] = first(p["Department"])
    p = p[["id", "hm_dept"]].rename(columns={"id": "hm_id"})
    jj = jobs.copy()
    jj["hm_id"] = first(jj["Hiring Manager"])
    jj["job_dept"] = first(jj["Department"])
    mm = jj.merge(p, on="hm_id", how="left")
    n3 = int((mm["hm_dept"] != mm["job_dept"]).sum())
    out.append(("hiring manager outside the opening's department", 21, n3))

    # headline numbers too
    src = cands.set_index("id")["Source"]
    a2 = apps.copy()
    a2["cand"] = first(a2["Candidate"])
    a2["src"] = a2["cand"].map(src)
    hires = a2[a2["Stage"] == "Hired"]
    n4 = int((hires["src"] == "Job Board").sum())
    out.append(("C1 numerator: job-board hires", 7, n4))
    out.append(("C1 denominator: total hires", 26, int(hires.shape[0])))
    out.append(("C2 numerator: accepted offers", 26,
                int((offers["Status"] == "Accepted").sum())))
    out.append(("C2 denominator: all offers", 36, int(offers.shape[0])))

    print("| Check | plain Python | pandas | Agree? |")
    print("|---|---|---|---|")
    for name, py, pdv in out:
        print("| {} | {} | {} | {} |".format(
            name, py, pdv, "YES" if py == pdv else "**NO**"))


if __name__ == "__main__":
    main()
