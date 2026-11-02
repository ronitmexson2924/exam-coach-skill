# Exam Study Coach

**Give Claude your syllabus, notes and old question papers. It tells you what's important, explains topics in simple words, finds good study resources and tests you until you're ready for the exam.**

It's a skill for Claude: a set of instructions that turns Claude into your personal exam coach.

---

## What it can do for you

**Understand your material**
- Reads the PDFs, notes, slides and syllabus you give it, including scanned pages
- Makes a list of every topic in your syllabus
- Looks at old question papers to see which topics come up most and for how many marks

**Tell you what to study**
- **Important topics:** ranks every topic from P1 (must study) to P5 (unclear)
- **Simple summaries:** explains your study material in easy words
- **Study resources:** tells you which file and page to read for each topic, plus good outside resources
- **YouTube videos:** suggests videos for each topic (links are checked, never made up)
- **Topic checklist:** a tick-box list of every topic so you can see your progress

After it reads your files, Claude **asks you which of these you want**, so you only get what's useful to you.

**Teach and test you**
- Teaches one topic at a time, from the basics up to exam level
- Makes a day-by-day study plan for your exam date, and updates it if you fall behind
- Quizzes you, reminds you to revise topics before you forget them, and keeps a list of your mistakes
- Gives you practice exams and marks your answers, even photos of handwritten ones
- Makes flashcards, formula sheets, cheat sheets and mind maps

**Remembers you**
- Saves your progress in a `study-state/` folder, so next time it carries on where you stopped

---

## Install it

Pick **one** option.

### Option 1: Claude app (easiest)

1. Download [`dist/exam-study-coach-skill.zip`](dist/exam-study-coach-skill.zip) from this repo.
2. In Claude, go to **Settings**, find **Skills** and upload the ZIP. Turn on code execution if Claude asks.
3. Start a chat, attach your syllabus, notes and papers, and say *"help me prepare for my exam"*.

### Option 2: Claude Code, from GitHub

In Claude Code, type:

```
/plugin marketplace add ronitmexson2924/exam-coach-skill
/plugin install exam-study-coach@exam-study-tools
```

Then restart Claude Code (or type `/reload-plugins`).

### Option 3: Claude Code, copy the folder

```bash
git clone https://github.com/ronitmexson2924/exam-coach-skill.git
mkdir -p ~/.claude/skills
cp -r exam-coach-skill/plugins/exam-study-coach/skills/exam-study-coach ~/.claude/skills/
```

---

## How to use it

**Step 1. Put your files in one folder.** Any names work; this layout just keeps things tidy:

```
my-exam/
├── syllabus/          your syllabus or course plan
├── question-papers/   old exam papers
├── notes/             class notes and slides
├── resources/         textbooks and handouts
└── answers/           (optional) photos of answers you want marked
```

**Step 2. Start the coach.** In Claude Code, open the folder (`cd my-exam`, then `claude`) and type `/exam-study-coach`, or just say *"help me prepare for my exam"*. In the Claude app, attach the files to the chat.

**Step 3. Read your exam report.** Claude reads everything and shows you the topics, how important each one is and what the exam looks like.

**Step 4. Choose the help you want.** Claude asks whether you'd like important topics, simple summaries, a resources list, YouTube videos, a topic checklist, or all of them.

**Step 5. Study a little every day.** Type `TODAY` to see what to do, learn the next topic, do your revision, and take a practice exam near the end.

---

## Things you can type

You can type these commands, or just ask in normal words.

| Type this | What you get |
|---|---|
| `ANALYZE MATERIALS` | Claude reads your files and gives you the exam report |
| `STUDY HELP` | Choose what kind of help you want |
| `IMPORTANT TOPICS` | The most important topics, in plain words |
| `SIMPLE SUMMARY: Chapter 3` | An easy-to-read summary of a file, topic or module |
| `RESOURCES: Module 2` | What to study from: your files, outside resources and videos |
| `VIDEOS: Paging` | YouTube videos for a topic |
| `TOPIC CHECKLIST` | A tick-box list of every topic |
| `MAKE STUDY PLAN` | A day-by-day timetable for your exam date |
| `TODAY` | What to study today |
| `START NEXT TOPIC` | Learn the next topic in your plan |
| `TEACH: Deadlocks` | Learn any topic you choose |
| `PRACTICE: Scheduling` | A quiz on a topic |
| `REVIEW TODAY` | Revise the topics that are due today |
| `MOCK TEST` | A timed practice exam |
| `EVALUATE MY ANSWER` | Get your answer marked, typed or as a photo |
| `FLASHCARDS: Module 1` | Flashcards you can use in Anki or Quizlet |
| `CHEAT SHEET: Module 4` | A one-page summary for last-minute revision |
| `READINESS` | How ready you are and whether you're on track |
| `REPLAN` | A new plan if you've fallen behind |

<details>
<summary>More commands</summary>

| Type this | What you get |
|---|---|
| `DIAGNOSTIC` | A short quiz to find your starting level |
| `SHOW PRIORITY LIST` | The full ranking, with scores and marks-per-hour |
| `EXAM PATTERN` | Marks, sections and choices in the exam |
| `SOCRATIC: <topic>` | Learn by answering Claude's questions |
| `TEACH BACK: <topic>` | You explain the topic and Claude finds the gaps |
| `VIVA: <topic>` | Practise for an oral exam |
| `15 MIN` | A quick session for busy days |
| `QUICK REVISION: <topic>` | Short revision notes |
| `SOLVE PYQ: <question>` | Step-by-step solution to an old exam question |
| `WEAK AREAS` / `MISTAKE REVIEW` | Practise your weak topics and past mistakes |
| `UPDATE PROGRESS` | What's done, what's left and whether you're on pace |
| `FORMULA SHEET` / `MIND MAP: <module>` | More study aids |
| `LAST-DAY REVISION` | A plan for the day before the exam |

</details>

---

## Good to know

**What P1 to P5 mean**

| Label | Meaning |
|---|---|
| **P1** | Must study: comes up a lot, carries many marks, or other topics need it |
| **P2** | High priority |
| **P3** | Medium priority |
| **P4** | Low priority, based on old papers |
| **P5** | Not sure yet: check with your teacher |

Rankings come from how often a topic appeared in old papers, how many marks it had, what your syllabus or teacher stressed, how recently it came up, and how many other topics depend on it.

- **Low priority doesn't mean skip it.** Any syllabus topic can come in the exam. Old papers are clues, not promises.
- **It doesn't make things up.** No invented topics, marks, page numbers or links. If it can't check a video link, it gives you a YouTube search instead.
- **Your files stay with you.** Everything is saved in your own folder. The `study-state/` folder is kept out of git automatically.
- **It's for learning.** Don't hand in what it writes as your own graded work.

**You need:** Python 3 for the helper scripts (already on most Macs and Linux computers). For scanned PDFs, OCR tools like `tesseract` help, but Claude can also read pages as images.

---

## What's in this repo

```
exam-coach-skill/
├── .claude-plugin/marketplace.json   lets Claude Code install the plugin
├── plugins/exam-study-coach/
│   ├── .claude-plugin/plugin.json    plugin details
│   └── skills/exam-study-coach/
│       ├── SKILL.md                  the instructions Claude follows
│       ├── scripts/                  small Python helpers that do the maths
│       └── templates/exam-profile.md form for your exam details
├── dist/exam-study-coach-skill.zip   ready-to-upload file for the Claude app
├── CHANGELOG.md                      what changed in each version
└── LICENSE
```

## License

MIT. See [LICENSE](LICENSE).
