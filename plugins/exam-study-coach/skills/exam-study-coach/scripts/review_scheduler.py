#!/usr/bin/env python3
"""Spaced-repetition scheduler for study-state/progress.csv.

Usage:
    # list topics due for review today (or on --today)
    python3 review_scheduler.py due study-state/progress.csv [--today 2026-11-02]

    # record a review or check result and schedule the next one
    python3 review_scheduler.py update study-state/progress.csv TOPIC_ID --result pass|fail
        [--today 2026-11-02] [--exam-date 2026-12-01] [--status Practised]

Intervals: 1, 3, 7, 14, 30 days. A pass moves to the next interval; a fail resets
to 1 day and sets status to 'Revision due'. If --exam-date is given, the next
review is moved earlier so it lands no later than the day before the exam.
"""
import argparse
import csv
from datetime import date, timedelta

INTERVALS = [1, 3, 7, 14, 30]
FIELDS = ["topic_id", "topic", "status", "last_reviewed", "next_review",
          "interval_days", "confidence", "notes"]


def parse_day(text):
    return date.fromisoformat(text) if text else date.today()


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def next_interval(current, passed):
    if not passed:
        return INTERVALS[0]
    try:
        cur = int(current)
    except (TypeError, ValueError):
        return INTERVALS[0]
    bigger = [i for i in INTERVALS if i > cur]
    return bigger[0] if bigger else INTERVALS[-1]


def cmd_due(args):
    today = parse_day(args.today)
    due = []
    for r in load(args.progress):
        nr = r.get("next_review", "").strip()
        if nr and date.fromisoformat(nr) <= today:
            due.append((date.fromisoformat(nr), r))
    due.sort(key=lambda x: x[0])
    if not due:
        print(f"No reviews due on {today}.")
        return
    print(f"{len(due)} review(s) due on {today}:")
    for d, r in due:
        overdue = (today - d).days
        tag = f" (overdue {overdue}d)" if overdue else ""
        print(f"- {r['topic_id']}: {r.get('topic','')} [{r.get('status','')}]{tag}")


def cmd_update(args):
    today = parse_day(args.today)
    rows = load(args.progress)
    match = [r for r in rows if r.get("topic_id") == args.topic_id]
    if not match:
        raise SystemExit(f"topic_id '{args.topic_id}' not found in {args.progress}")
    r = match[0]
    passed = args.result == "pass"
    interval = next_interval(r.get("interval_days"), passed)
    nxt = today + timedelta(days=interval)
    if args.exam_date:
        last_ok = date.fromisoformat(args.exam_date) - timedelta(days=1)
        if nxt > last_ok:
            nxt = max(today + timedelta(days=1), last_ok) if last_ok > today else today
            interval = (nxt - today).days
    r["last_reviewed"] = today.isoformat()
    r["next_review"] = nxt.isoformat()
    r["interval_days"] = str(interval)
    if args.status:
        r["status"] = args.status
    elif not passed:
        r["status"] = "Revision due"
    save(args.progress, rows)
    print(f"{args.topic_id}: {args.result} -> next review {nxt} (interval {interval}d), status {r['status']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("due")
    d.add_argument("progress")
    d.add_argument("--today")
    u = sub.add_parser("update")
    u.add_argument("progress")
    u.add_argument("topic_id")
    u.add_argument("--result", choices=["pass", "fail"], required=True)
    u.add_argument("--today")
    u.add_argument("--exam-date")
    u.add_argument("--status")
    args = ap.parse_args()
    cmd_due(args) if args.cmd == "due" else cmd_update(args)


if __name__ == "__main__":
    main()
