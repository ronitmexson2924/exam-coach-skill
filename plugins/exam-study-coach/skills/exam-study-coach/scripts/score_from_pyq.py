#!/usr/bin/env python3
"""Fill the frequency, marks and recency scores in topic-scores.csv from pyq-stats.csv.

Usage:
    python3 score_from_pyq.py study-state/pyq-stats.csv study-state/topic-scores.csv [--overwrite]

Scores (0-5, rounded to 2 decimals):
- frequency = 5 x distinct_papers / papers_total
- marks     = 5 x total_marks / the highest total_marks of any topic
- recency   = 5 for the newest paper year, minus 1 per year older, never below 1
A syllabus topic that never appears in the papers scores 0 on all three (no
appearance is evidence, not missing data). A dimension stays blank when the
stats cannot support it (e.g. no marks or years were read reliably).

Only blank cells are filled unless --overwrite is given, so scores you set by
hand are kept. emphasis, foundational, est_hours and expected_marks are left
for you to fill from the syllabus and resources.
"""
import argparse
import csv


def num(value):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def fmt(value):
    return f"{round(value, 2):g}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pyq_stats")
    ap.add_argument("topic_scores")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    with open(args.pyq_stats, newline="", encoding="utf-8") as f:
        stats = {r["topic_id"]: r for r in csv.DictReader(f)}
    with open(args.topic_scores, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    papers_total = max((num(s.get("papers_total")) or 0 for s in stats.values()), default=0)
    if not papers_total:
        raise SystemExit("pyq-stats has no papers; run pyq_stats.py on a filled question bank first")
    max_marks = max((num(s.get("total_marks")) or 0 for s in stats.values()), default=0)
    years = [num(s.get("latest_year")) for s in stats.values() if num(s.get("latest_year"))]
    newest = max(years) if years else None

    filled = 0
    for r in rows:
        s = stats.get(r.get("topic_id", "").strip())
        scores = {}
        if s is None:
            scores = {"frequency": 0.0, "marks": 0.0 if max_marks else None,
                      "recency": 0.0 if newest else None}
        else:
            scores["frequency"] = 5 * (num(s.get("distinct_papers")) or 0) / papers_total
            m = num(s.get("total_marks"))
            scores["marks"] = 5 * m / max_marks if m is not None and max_marks else None
            y = num(s.get("latest_year"))
            scores["recency"] = max(1.0, 5 - (newest - y)) if y and newest else None
        for dim, value in scores.items():
            if value is None:
                continue
            if args.overwrite or not (r.get(dim) or "").strip():
                r[dim] = fmt(value)
                filled += 1

    with open(args.topic_scores, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"filled {filled} score cell(s) in {args.topic_scores} "
          f"from {int(papers_total)} paper(s)")
    unknown = sorted(set(stats) - {r.get("topic_id", "").strip() for r in rows})
    if unknown:
        print("WARNING: topic ids in the question bank but not in topic-scores.csv "
              "(fix the mapping or add them as verify=yes): " + ", ".join(unknown))


if __name__ == "__main__":
    main()
