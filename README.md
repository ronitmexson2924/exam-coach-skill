# Exam Study Coach

**A Claude skill that turns your own syllabus, notes, PDFs and previous question papers into an evidence-based exam preparation system.**

It reads your materials, ranks every syllabus topic by how much it matters, builds a timetable around your exam date, teaches you one topic at a time, tests you, marks your answers and remembers your progress between sessions.

> It won't just summarize your PDFs. It teaches you, tests you and tracks what you actually understand.

---

## Features

| Feature | What it does |
|---|---|
| **Syllabus analysis** | Extracts every module, topic and subtopic from the official syllabus, with sources |
| **Notes and PDF analysis** | Reads lecture notes, slides and textbooks, with OCR for scanned PDFs |
| **Question-paper analysis** | Builds a question bank from past papers and counts how often each topic appears |
| **Exam pattern detection** | Works out marks, sections and internal choice ("answer any 5 of 8") |
| **P1 to P5 priority ranking** | Scores topics on frequency, marks, faculty emphasis, recency and foundational value |
| **Marks-per-hour** | Shows which topics give the most marks for the study time they need |
| **Resource coverage map** | Shows which file and page covers each topic, and which topics have no material |
| **Diagnostic test** | A short adaptive quiz that finds your real starting level |
| **Study timetable** | A date-wise plan with buffers, revision cycles and mocks |
| **Auto re-planning** | `REPLAN` rebuilds the schedule when you fall behind |
| **Topic teaching** | Goes from beginner level to exam level with worked examples, past-paper links and answer formats |
| **Teaching modes** | Standard, Socratic, teach-back, ELI5, viva practice and 15-minute sprints |
| **Spaced repetition** | Reviews each topic after 1, 3, 7, 14 and 30 days, with all reviews done before the exam |
| **Mistake log** | Tags each error by type (concept, recall, calculation, misread, presentation, time) |
| **Mock tests** | Exam-style timed papers with a separate answer key |
| **Answer evaluation** | Marks typed answers or **photos of handwritten answers** and shows a model answer |
| **Readiness score** | Coverage by priority, mock trend, overdue reviews and an on-track check |
| **Study aids** | Anki/Quizlet flashcards, formula sheets, one-page cheat sheets and mind maps |
| **Progress across sessions** | Everything is saved in a `study-state/` folder, so you pick up where you left off |
| **Honest by design** | Never invents topics, marks or page numbers, and never says a topic is "sure to come" |

---

## Installation

### Option A: Claude Code via GitHub (recommended)

In Claude Code, run:

```
/plugin marketplace add ronitmexson2924/exam-coach-skill
/plugin install exam-study-coach@exam-study-tools
```

Restart Claude Code, or run `/reload-plugins`, and the skill is ready.

### Option B: Claude Code, manual copy

Download or clone this repo, then copy the skill folder into your personal skills folder:

```bash
git clone https://github.com/ronitmexson2924/exam-coach-skill.git
mkdir -p ~/.claude/skills
cp -r exam-coach-skill/plugins/exam-study-coach/skills/exam-study-coach ~/.claude/skills/
```

To use it in only one project, copy it to `<your-project>/.claude/skills/` instead.

### Option C: Claude app (claude.ai, desktop or web)

1. Download `dist/exam-study-coach-skill.zip` from this repo.
2. In Claude, open **Settings**, find the **Skills** section and upload the ZIP. Code execution must be turned on.
3. Attach your syllabus, notes and papers in a chat and say "analyze my exam materials".

---

## Quick start

**1. Set up your exam folder**

```
my-exam/
├── syllabus/          official syllabus or course plan
├── question-papers/   previous papers (CAT, FAT, mid-sem, end-sem, model papers)
├── notes/             lecture notes and slides
├── resources/         textbooks, handouts, reference PDFs
└── answers/           (optional) photos of your handwritten answers
```

**2. Open the folder in Claude Code and start the skill**

```
cd my-exam
claude
```

Then type `/exam-study-coach` (or `/exam-study-coach:exam-study-coach` if installed as a plugin), or just say *"help me prepare for my exam"*.

**3. Follow this order**

1. `ANALYZE MATERIALS`: Claude reads everything and gives you the exam report.
2. `DIAGNOSTIC`: a short quiz to find your starting level.
3. `MAKE STUDY PLAN`: give your exam date and daily hours.
4. `TODAY` / `START NEXT TOPIC`: learn one topic at a time.
5. `REVIEW TODAY`: do your spaced reviews every day.
6. `MOCK TEST`, then `EVALUATE MY ANSWER`: practise under exam conditions.
7. `READINESS` and `LAST-DAY REVISION`: final checks.

---

## Commands

You can type these exactly, or just ask in plain language.

| Command | What it does |
|---|---|
| `ANALYZE MATERIALS` | Reads all files (only new or changed ones on later runs) and writes the exam report |
| `DIAGNOSTIC` | Adaptive pre-test |
| `SHOW PRIORITY LIST` | Topics ranked P1 to P5, with evidence and marks-per-hour |
| `EXAM PATTERN` | Marks, sections and choice structure |
| `MAKE STUDY PLAN` | Date-wise timetable |
| `REPLAN` | Rebuilds the plan from your real progress |
| `TODAY` | Today's study blocks and due reviews |
| `START NEXT TOPIC` | Teaches the next topic in the plan |
| `TEACH: Paging` | Teaches a named topic |
| `SOCRATIC: Deadlocks` | Teaches by asking you questions |
| `TEACH BACK: Normalization` | You explain the topic and Claude finds the gaps |
| `VIVA: Transistors` | Oral-exam style questioning |
| `15 MIN` | A quick session for busy days |
| `QUICK REVISION: Module 3` | Short revision notes |
| `SOLVE PYQ: Q4 2024` | Step-by-step solution to a past question |
| `PRACTICE: Scheduling` | Topic quiz, with answers revealed after you try |
| `REVIEW TODAY` | Spaced-repetition review |
| `WEAK AREAS` / `MISTAKE REVIEW` | Drills on your weak topics and past mistakes |
| `MOCK TEST` | Timed exam simulation |
| `EVALUATE MY ANSWER` | Marks your typed or photographed answer |
| `UPDATE PROGRESS` | Shows what's done, what's left and whether you're on pace |
| `READINESS` | Readiness snapshot |
| `FLASHCARDS: Module 2` | Creates an Anki/Quizlet CSV |
| `FORMULA SHEET` / `CHEAT SHEET: Module 4` / `MIND MAP: Module 1` | Creates study aids |
| `LAST-DAY REVISION` | Final high-yield plan |

---

## How topics are prioritized

Each topic is scored 0 to 5 on five kinds of evidence, then weighted:

| Evidence | Weight |
|---|---:|
| Frequency across past papers | 30% |
| Marks / weightage | 25% |
| Official syllabus or faculty emphasis | 20% |
| Foundational importance | 15% |
| Recency | 10% |

| Label | Meaning |
|---|---|
| **P1** | Must study |
| **P2** | High priority |
| **P3** | Medium priority |
| **P4** | Low observed priority |
| **P5** | Verify: unclear syllabus status or too little evidence |

A low priority **never** means "safe to skip". Past papers are evidence, not a guarantee.

---

## What's in this repo

```
exam-coach-skill/
├── .claude-plugin/
│   └── marketplace.json            marketplace catalog (lets /plugin find the skill)
├── plugins/exam-study-coach/
│   ├── .claude-plugin/plugin.json  plugin manifest
│   └── skills/exam-study-coach/
│       ├── SKILL.md                the skill instructions
│       ├── scripts/                helper scripts (Python 3, no extra packages)
│       │   ├── init_state.py       creates the study-state/ folder
│       │   ├── pyq_stats.py        topic frequency from past papers
│       │   ├── score_from_pyq.py   fills frequency/marks/recency scores from the stats
│       │   ├── priority.py         P1 to P5 scores and marks-per-hour
│       │   ├── review_scheduler.py spaced-repetition schedule
│       │   └── readiness.py        readiness snapshot
│       └── templates/exam-profile.md
├── dist/exam-study-coach-skill.zip ready-to-upload ZIP for the Claude app
├── README.md
├── CHANGELOG.md
└── LICENSE
```

**Requirements:** Python 3 for the helper scripts (pre-installed on macOS and most Linux systems). For scanned PDFs, OCR tools such as `ocrmypdf` or `tesseract` help; Claude can also read scanned pages as images.

---

## Privacy

Your materials and progress stay in your own project folder. `init_state.py` puts a `.gitignore` inside `study-state/`, so your progress is never committed if your exam folder is also a git repo. If you also don't want to commit your notes and papers, add `syllabus/`, `question-papers/`, `notes/`, `resources/` and `answers/` to your exam folder's own `.gitignore`.

## Academic integrity

This skill is for learning and exam preparation. Follow your institution's rules, and don't submit work it generates as your own graded work.

## License

MIT. See [LICENSE](LICENSE).
