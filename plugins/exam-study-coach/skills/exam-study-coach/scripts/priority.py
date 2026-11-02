#!/usr/bin/env python3
"""Compute weighted priority scores, P1-P5 labels and marks-per-hour (ROI).

Usage:
    python3 priority.py study-state/topic-scores.csv --out study-state/priority.csv
        [--weights frequency=30,marks=25,emphasis=20,recency=10,foundational=15]

Input columns (topic-scores.csv):
    topic_id, topic, module,
    frequency, marks, emphasis, recency, foundational   -> each scored 0-5, blank = N/A
    est_hours        -> estimated study hours (number)
    expected_marks   -> expected marks share for the topic (number, optional)
    verify           -> 'yes' if syllabus status is unclear (forces P5)

Rules:
- N/A dimensions are dropped and the remaining weights are rescaled to 100%.
- A topic with 3 or more N/A dimensions, or verify=yes, is labelled P5.
- Labels by weighted score (0-5): >=3.5 P1, >=2.75 P2, >=2.0 P3, else P4.
  Adjust the thresholds only with a stated reason.
- A low label never means "safe to skip".
"""
import argparse
import csv

DIMS = ["frequency", "marks", "emphasis", "recency", "foundational"]
DEFAULT_WEIGHTS = {"frequency": 30, "marks": 25, "emphasis": 20, "recency": 10, "foundational": 15}
THRESHOLDS = [(3.5, "P1"), (2.75, "P2"), (2.0, "P3")]


def num(value):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def parse_weights(text):
    if not text:
        return dict(DEFAULT_WEIGHTS)
    weights = {}
    for part in text.split(","):
        key, val = part.split("=")
        key = key.strip()
        if key not in DIMS:
            raise SystemExit(f"unknown dimension '{key}'; use {DIMS}")
        weights[key] = float(val)
    for d in DIMS:
        weights.setdefault(d, 0.0)
    return weights


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scores")
    ap.add_argument("--out", required=True)
    ap.add_argument("--weights", default=None)
    args = ap.parse_args()
    weights = parse_weights(args.weights)

    results = []
    with open(args.scores, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vals = {d: num(row.get(d)) for d in DIMS}
            for d, v in vals.items():
                if v is not None and not 0 <= v <= 5:
                    raise SystemExit(f"{row.get('topic_id')}: {d}={v} is outside 0-5")
            available = {d: v for d, v in vals.items() if v is not None and weights[d] > 0}
            na = [d for d in DIMS if vals[d] is None]
            wsum = sum(weights[d] for d in available)
            score = sum(v * weights[d] for d, v in available.items()) / wsum if wsum else 0.0

            if (row.get("verify") or "").strip().lower() in {"yes", "y", "true", "1"} or len(na) >= 3:
                label = "P5"
            else:
                label = next((lab for cut, lab in THRESHOLDS if score >= cut), "P4")

            confidence = "High" if not na else ("Medium" if len(na) == 1 else "Low")
            hours = num(row.get("est_hours"))
            exp_marks = num(row.get("expected_marks"))
            roi = round(exp_marks / hours, 2) if exp_marks is not None and hours else ""

            results.append({
                "topic_id": row.get("topic_id", ""),
                "topic": row.get("topic", ""),
                "module": row.get("module", ""),
                "score": round(score, 2),
                "label": label,
                "confidence": confidence,
                "na_dimensions": ";".join(na),
                "est_hours": "" if hours is None else hours,
                "expected_marks": "" if exp_marks is None else exp_marks,
                "marks_per_hour": roi,
            })

    order = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4}
    results.sort(key=lambda r: (order[r["label"]], -r["score"], r["topic_id"]))
    for i, r in enumerate(results, 1):
        r["rank"] = i

    fields = ["rank", "topic_id", "topic", "module", "score", "label", "confidence",
              "na_dimensions", "est_hours", "expected_marks", "marks_per_hour"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    counts = {lab: sum(r["label"] == lab for r in results) for lab in order}
    print(f"wrote {len(results)} topics to {args.out}  " +
          "  ".join(f"{k}:{v}" for k, v in counts.items()))
    print("weights used: " + ", ".join(f"{d}={weights[d]:g}" for d in DIMS))


if __name__ == "__main__":
    main()
