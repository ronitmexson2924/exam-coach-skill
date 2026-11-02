#!/usr/bin/env python3
"""Create the study-state/ folder with empty, correctly-headed state files.

Usage:
    python3 init_state.py [PROJECT_DIR]

Safe to re-run: existing files are never overwritten.
"""
import sys
from pathlib import Path

CSV_HEADERS = {
    "question-bank.csv": "paper_file,exam_session_year,q_no,sub,marks,topic_ids,module,question_text,type,difficulty,mapping_confidence,choice_group",
    "topic-scores.csv": "topic_id,topic,module,frequency,marks,emphasis,recency,foundational,est_hours,expected_marks,verify",
    "progress.csv": "topic_id,topic,status,last_reviewed,next_review,interval_days,confidence,notes",
    "mistakes.csv": "date,topic_id,question,error_type,correction",
    "mock-results.csv": "date,paper,score,max_score,time_taken_min,weak_topics",
}

MD_FILES = {
    "exam-profile.md": None,  # copied from the template if present
    "file-inventory.md": "# File inventory\n\n| File | Type | Contents | Topics covered | Read status | Modified |\n|---|---|---|---|---|---|\n",
    "syllabus.md": "# Official syllabus checklist\n\n",
    "coverage.md": "# Resource coverage\n\n| Syllabus topic | Resource file | Pages/slides | PYQ evidence | Coverage |\n|---|---|---|---|---|\n",
    "study-plan.md": "# Study plan\n\n",
    "session-log.md": "# Session log\n\n",
}

# Keeps the student's progress out of git if their exam folder is a repo.
GITIGNORE = "# Created by exam-study-coach: keep study progress out of git\n*\n"


def main() -> None:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    state = project / "study-state"
    (state / "outputs").mkdir(parents=True, exist_ok=True)

    template = Path(__file__).resolve().parent.parent / "templates" / "exam-profile.md"
    created = []

    for name, header in CSV_HEADERS.items():
        path = state / name
        if not path.exists():
            path.write_text(header + "\n", encoding="utf-8")
            created.append(name)

    for name, body in MD_FILES.items():
        path = state / name
        if path.exists():
            continue
        if name == "exam-profile.md" and template.exists():
            body = template.read_text(encoding="utf-8")
        path.write_text(body or f"# {name}\n", encoding="utf-8")
        created.append(name)

    gitignore = state / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(GITIGNORE, encoding="utf-8")
        created.append(".gitignore")

    print(f"study-state ready at {state}")
    print("created: " + (", ".join(created) if created else "nothing (all files already existed)"))


if __name__ == "__main__":
    main()
