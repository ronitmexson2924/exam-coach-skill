#!/usr/bin/env python3
"""Readiness snapshot from the state files.

Usage:
    python3 readiness.py study-state [--exam-date 2026-12-01] [--daily-hours 4] [--today 2026-11-02]

Reports coverage by priority, mock-score trend, overdue reviews, weak topics
from the mistake log, and whether the remaining estimated hours fit the time
left. It is an estimate from practice data, not a prediction of the paper.
"""
import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

READY = {"Practised", "Mastered"}


def read(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("state_dir")
    ap.add_argument("--exam-date")
    ap.add_argument("--daily-hours", type=float)
    ap.add_argument("--today")
    a = ap.parse_args()
    s = Path(a.state_dir)
    today = date.fromisoformat(a.today) if a.today else date.today()

    progress = {r["topic_id"]: r for r in read(s / "progress.csv")}
    priority = read(s / "priority.csv")
    mocks = read(s / "mock-results.csv")
    mistakes = read(s / "mistakes.csv")

    print(f"# Readiness snapshot ({today})\n")

    if priority:
        print("## Coverage by priority")
        remaining_hours = 0.0
        unestimated = []
        for label in ["P1", "P2", "P3", "P4", "P5"]:
            topics = [p for p in priority if p["label"] == label]
            if not topics:
                continue
            ready = [p for p in topics if progress.get(p["topic_id"], {}).get("status") in READY]
            mastered = [p for p in topics if progress.get(p["topic_id"], {}).get("status") == "Mastered"]
            print(f"- {label}: {len(ready)}/{len(topics)} practised or mastered "
                  f"({100*len(ready)/len(topics):.0f}%), {len(mastered)} mastered")
            for p in topics:
                if progress.get(p["topic_id"], {}).get("status") not in READY:
                    hours = num(p.get("est_hours"))
                    if hours is None:
                        unestimated.append(p["topic_id"])
                    else:
                        remaining_hours += hours
        print(f"\nEstimated hours still needed (topics not yet practised): {remaining_hours:g}")
        if unestimated:
            print(f"WARNING: {len(unestimated)} unfinished topic(s) have no est_hours and are not counted: "
                  + ", ".join(unestimated[:10]) + (" ..." if len(unestimated) > 10 else ""))
        if a.exam_date and a.daily_hours:
            days_left = (date.fromisoformat(a.exam_date) - today).days
            available = max(days_left, 0) * a.daily_hours
            verdict = "ON TRACK" if available >= remaining_hours * 1.15 else "BEHIND - replan by priority/ROI"
            if unestimated and verdict == "ON TRACK":
                verdict = "PROVISIONAL - estimate hours for the topics above before trusting this"
            print(f"Days to exam: {days_left}; hours available: {available:g} -> {verdict} "
                  f"(includes 15% buffer)")
        elif a.exam_date or a.daily_hours:
            print("Pass both --exam-date and --daily-hours for the on-track check.")
    else:
        print("No priority.csv yet - run priority.py first.")

    overdue = [r for r in progress.values()
               if r.get("next_review") and date.fromisoformat(r["next_review"]) < today]
    print(f"\n## Reviews\n- Overdue reviews: {len(overdue)}" +
          ("".join(f"\n  - {r['topic_id']}: {r.get('topic','')}" for r in overdue[:10])))

    if mocks:
        print("\n## Mock tests")
        pcts = []
        # ISO dates sort correctly as text; the stable sort keeps file order for ties
        for m in sorted(mocks, key=lambda m: (m.get("date") or "").strip()):
            sc, mx = num(m.get("score")), num(m.get("max_score"))
            if sc is not None and mx:
                pct = 100 * sc / mx
                pcts.append(pct)
                print(f"- {m.get('date','')} {m.get('paper','')}: {sc:g}/{mx:g} ({pct:.0f}%)"
                      + (f", {m['time_taken_min']} min" if m.get("time_taken_min") else ""))
        if len(pcts) >= 2:
            recent = pcts[-3:]
            lo, hi = min(recent), max(recent)
            print(f"Recent range: {lo:.0f}-{hi:.0f}%  (trend: {pcts[-1]-pcts[0]:+.0f} points since first mock)")
        elif pcts:
            print("Only one mock so far - take another before reading a trend.")

    if mistakes:
        print("\n## Mistake log")
        by_type = Counter(m.get("error_type", "unknown") for m in mistakes)
        by_topic = Counter(t.strip() for m in mistakes
                           for t in (m.get("topic_id") or "").split(";") if t.strip())
        print("- By error type: " + ", ".join(f"{k} {v}" for k, v in by_type.most_common()))
        print("- Weakest topics: " + ", ".join(f"{k} ({v})" for k, v in by_topic.most_common(5)))

    print("\nThis is an estimate from practice data, not a prediction of the actual paper.")


if __name__ == "__main__":
    main()
