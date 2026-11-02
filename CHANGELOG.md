# Changelog

## 2.2.0 - 2026-11-02
- After the first analysis, Claude asks which kinds of help you want (`STUDY HELP`) and remembers the answer in `exam-profile.md`.
- New `IMPORTANT TOPICS`: the priority list in plain words.
- New `SIMPLE SUMMARY`: beginner-friendly summaries of your uploaded material, with file and page references.
- New `RESOURCES` and `VIDEOS`: what to study from for each topic, covering your own files, outside resources and YouTube links. Links are only given once they've been checked; otherwise you get a YouTube search link.
- New `TOPIC CHECKLIST`: a tick-box list of every syllabus topic.
- README rewritten in simpler language for students.

## 2.1.0 - 2026-11-02
- Added the missing `.claude-plugin/marketplace.json`, so `/plugin marketplace add` works.
- New `score_from_pyq.py` fills frequency, marks and recency scores from `pyq-stats.csv`.
- `init_state.py` adds a `.gitignore` inside `study-state/` so progress is never committed.
- `pyq_stats.py` splits a multi-topic question's marks between its topics instead of counting them in full for each.
- `readiness.py` warns about topics with no hour estimate instead of counting them as 0 hours, and orders mocks by date.
- `review_scheduler.py` no longer reschedules a review for the same day on the eve of the exam; `due --priority` lists P1 topics first.
- `priority.py` gives clear errors for malformed `--weights`.
- SKILL.md tells Claude to call scripts by the skill folder's full path.
- Filled in author and repository details; fixed install commands in the README.

## 2.0.0 - 2026-11-02
- Persistent `study-state/` folder so progress carries across sessions.
- Spaced repetition (1/3/7/14/30 days) with `REVIEW TODAY`.
- Adaptive `DIAGNOSTIC` pre-test.
- Exam blueprint analysis, including internal choice ("answer any 5 of 8").
- Marks-per-hour (ROI) per topic and `REPLAN` when you fall behind.
- Mistake log with error types, `WEAK AREAS` and `MISTAKE REVIEW`.
- Timed mocks, handwritten answer evaluation from photos, `READINESS` snapshot.
- Socratic, teach-back, viva and 15-minute sprint modes.
- Study aids: Anki/Quizlet flashcards, formula sheets, cheat sheets, mind maps.
- Bundled Python scripts for counting, scoring, scheduling and readiness.
- Packaged as a Claude Code plugin marketplace.

## 1.0.0
- Initial skill: syllabus and PYQ analysis, P1-P5 ranking, coverage matrix, timetable, topic teaching, mocks and evaluation.
