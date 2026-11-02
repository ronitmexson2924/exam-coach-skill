#!/usr/bin/env python3
"""Topic recurrence statistics from question-bank.csv.

Usage:
    python3 pyq_stats.py study-state/question-bank.csv [--out study-state/pyq-stats.csv]

Counting rules:
- topic_ids may hold several ids separated by ';' (multi-topic questions).
- Subparts of the same question (same paper_file + q_no) count as ONE
  appearance per topic, so a 3-part question on one topic is not triple-counted.
- Marks are summed per subpart, and only where the marks cell is a number.
  A subpart mapped to several topics splits its marks equally between them,
  so the per-topic totals add up to the marks actually on the papers.
- 'distinct_papers' counts different paper files containing the topic.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict


def year_of(value: str):
    m = re.search(r"(19|20)\d{2}", value or "")
    return int(m.group(0)) if m else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question_bank")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    appearances = defaultdict(set)   # topic -> {(paper, q_no)}
    papers = defaultdict(set)        # topic -> {paper}
    marks = defaultdict(float)
    marks_known = defaultdict(int)
    latest = {}
    types = defaultdict(lambda: defaultdict(int))
    all_papers = set()

    with open(args.question_bank, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            paper = (row.get("paper_file") or "").strip()
            if not paper:
                continue
            all_papers.add(paper)
            qno = (row.get("q_no") or "").strip()
            topics = [t.strip() for t in (row.get("topic_ids") or "").split(";") if t.strip()]
            yr = year_of(row.get("exam_session_year", ""))
            try:
                share = float(row.get("marks") or "") / len(topics) if topics else None
            except ValueError:
                share = None
            for t in topics:
                appearances[t].add((paper, qno))
                papers[t].add(paper)
                if share is not None:
                    marks[t] += share
                    marks_known[t] += 1
                if yr and (t not in latest or yr > latest[t]):
                    latest[t] = yr
                qtype = (row.get("type") or "").strip()
                if qtype:
                    types[t][qtype] += 1

    rows = []
    for t in sorted(appearances, key=lambda k: (-len(papers[k]), -len(appearances[k]), k)):
        common = sorted(types[t].items(), key=lambda kv: -kv[1])
        rows.append({
            "topic_id": t,
            "appearances": len(appearances[t]),
            "distinct_papers": len(papers[t]),
            "papers_total": len(all_papers),
            "total_marks": round(marks[t], 2) if marks_known[t] else "",
            "latest_year": latest.get(t, ""),
            "common_types": "; ".join(f"{k} x{v}" for k, v in common[:3]),
        })

    fields = ["topic_id", "appearances", "distinct_papers", "papers_total",
              "total_marks", "latest_year", "common_types"]
    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    w = csv.DictWriter(out, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
    if args.out:
        out.close()
        print(f"wrote {len(rows)} topics from {len(all_papers)} papers to {args.out}")
    if len(all_papers) <= 2:
        print(f"WARNING: only {len(all_papers)} paper(s) - small sample, avoid strong predictions.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
