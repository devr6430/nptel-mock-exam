# NPTEL Mock Exam — Joy of Computing Using Python

> **Course:** noc26_cs84 | **Session:** Jan–Apr 2026 | **Proctored Exam:** April 18, 2026
> **Live URL:** Deployed on Render.com

---

## 1. WORKFLOW — How the App Works End-to-End

### 1.1 User Journey

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  Dashboard   │────▶│  Start Test   │────▶│  Take Exam    │────▶│   Results     │
│  (10 tests)  │     │  POST /start  │     │  50 questions │     │  Score +      │
│  + attempts  │     │  /1 to /10    │     │  one-at-a-time│     │  Comparison + │
│  + scores    │     └──────────────┘     │  + timer      │     │  Q-by-Q Review│
└─────────────┘                           └───────────────┘     └──────┬───────┘
       ▲                                                               │
       │                                                               ▼
       │                                                        ┌──────────────┐
       └────────────────────────────────────────────────────────│  History Page │
                                                                │  All attempts │
                                                                │  compared     │
                                                                └──────────────┘
```

### 1.2 Exam Flow (Inside a Test)

1. **User clicks "Start Test"** → `POST /start/<test_id>` → session created with test_id
2. **Exam page loads** → JavaScript calls `GET /api/question/0`
3. **Question rendered**: question text + 4 option buttons + progress bar + timer
4. **User clicks an option** → `POST /api/submit` with `{index, chosen}`
5. **Server responds**: `{is_correct, correct_index, explanation}`
6. **JS highlights**: green (correct) or red (wrong), correct answer always shown green
7. **"Next →" button appears** → fetch question n+1
8. **After question 50** → "View Results" button → `GET /result`
9. **Result page**: score/100, pass/fail, section breakdown, week-wise, comparison with previous attempt, full Q-by-Q review with explanations
10. **Attempt saved** to `attempts.json` for tracking

### 1.3 Question Generation (Deterministic)

```python
def generate_test(test_id):
    rng = random.Random(test_id * 7919)   # seeded RNG — same test_id = same questions
    sec_a = [q for q in all_q if q["section"] == "A"]   # 31 questions
    sec_b = [q for q in all_q if q["section"] == "B"]   # 51 questions
    sec_c = [q for q in all_q if q["section"] == "C"]   # 47 questions
    test = rng.sample(sec_a, 10) + rng.sample(sec_b, 15) + rng.sample(sec_c, 25)
    rng.shuffle(test)   # random order across all weeks
    return test          # 50 questions total
```

**Why seeded?** Same test_id always produces the exact same 50 questions in the exact same order. This allows:
- Retaking the same test to measure improvement
- Comparing attempt 1 vs attempt 2 fairly (same questions)

### 1.4 Attempt Tracking System

```
User takes Test 1 → score saved to attempts.json
User retakes Test 1 → new attempt appended
Dashboard shows: attempt count, best score, last score
Result page shows: score delta vs previous attempt (▲+12 or ▼-4)
History page: side-by-side table of ALL attempts
```

**Data flow:**
- `attempts.json` is created automatically on first test completion
- Each attempt stores: score, correct count, sections breakdown, week stats, date
- Dashboard reads this on every page load to show badges
- Result page compares current vs previous attempt

### 1.5 Exam Format (Exact NPTEL Replica)

| Section | Questions | Marks Each | Total Marks | Difficulty |
|---------|-----------|------------|-------------|------------|
| A       | 10        | 2          | 20          | Easy — factual recall |
| B       | 15        | 2          | 30          | Medium — understanding |
| C       | 25        | 2          | 50          | Hard — code tracing, scenarios |
| **Total** | **50**  | —          | **100**     | **Pass: 40/100** |

- Duration: **180 minutes** (3 hours)
- No negative marking
- Questions randomly shuffled from ALL 12 weeks (not grouped by week)

---

## 2. AGENT — Architecture, Files, and Data

### 2.1 File Structure

```
mock_exam/
├── app.py                     ← Flask backend: routes, test generation, attempt persistence
├── questions.json             ← Question bank: 129 MCQs with explanations
├── attempts.json              ← Auto-generated: all test attempt history (gitignored)
├── requirements.txt           ← Python dependencies (flask, gunicorn)
├── render.yaml                ← Render.com deployment config
├── CLAUDE.md                  ← This file — complete project documentation
├── SCHEDULE.md                ← 7-day exam prep schedule
├── .gitignore                 ← Excludes __pycache__, attempts.json, versions/
│
├── extract_questions.py       ← Script: extracts 97 base questions from generate_all_weeks.py
├── add_github_questions.py    ← Script: adds 32 questions from 2025/2026 GitHub repos
│
├── templates/
│   ├── index.html             ← Dashboard: 10 test cards, attempt badges, retake buttons
│   ├── exam.html              ← Exam UI: question card, options, timer, nav panel
│   ├── result.html            ← Results: score circle, sections, comparison, Q-by-Q review
│   └── history.html           ← History: score progression chart, attempt comparison table
│
├── static/
│   ├── style.css              ← Complete design system (Samsung One UI + One Group tokens)
│   └── exam.js                ← Client-side: question loading, answer submission, timer, keyboard
│
└── versions/                  ← Version snapshots (gitignored, local only)
    ├── v1/                    ← 97 questions, basic flow
    ├── v2/                    ← 129 questions, Q-by-Q review
    └── v3/                    ← Attempt tracking, comparison, One UI design
```

### 2.2 Backend Routes (app.py)

| Route | Method | What It Does | Returns |
|-------|--------|-------------|---------|
| `/` | GET | Load dashboard with attempt summary for all 10 tests | `index.html` with `attempts` dict |
| `/start/<id>` | POST | Clear session, set test_id, redirect to exam | Redirect → `/exam` |
| `/exam` | GET | Render exam shell (JS takes over) | `exam.html` with test_id, total, duration |
| `/api/question/<n>` | GET | Return question n (0-indexed) without correct answer | JSON: `{question, options, week, topic, section}` |
| `/api/submit` | POST | Check answer, save to session, return feedback | JSON: `{is_correct, correct_index, explanation}` |
| `/result` | GET | Calculate score, save attempt, build review, compare to previous | `result.html` with full data |
| `/history/<id>` | GET | Load all attempts for test_id | `history.html` with attempts list |

### 2.3 Question Bank (questions.json)

**129 questions** — 2025 and 2026 sessions only (no older content).

Each question object:
```json
{
  "id": "w1_q1",
  "week": 1,
  "section": "A",
  "topic": "Scratch loops",
  "question": "What is the final value of counter?",
  "options": ["8", "5", "3", "10"],
  "correct": 0,
  "explanation": "Loop 1 runs 5 times, Loop 2 runs 3 times. Total = 8."
}
```

**Distribution:**
| Week | Count | Topics |
|------|-------|--------|
| 1 | 15 | Scratch: loops, variables, repeat-until |
| 2 | 23 | Nested loops, palindromes, discount logic, Armstrong numbers |
| 3 | 13 | Lists, slicing, FizzBuzz, file handling, combinatorics |
| 4 | 9 | Magic squares, birthday paradox, random module, Dobble |
| 5 | 11 | Dictionaries, Monty Hall, binary search, bubble sort |
| 6 | 10 | Caesar cipher, recursion, min-max, tic-tac-toe |
| 7 | 9 | Turtle graphics, PIL, CSV, Google Maps, Snakes & Ladders |
| 8 | 8 | Tuples, NLTK, sentiment analysis, image processing |
| 9 | 8 | Stylometry, NetworkX, graphs, string immutability |
| 10 | 3 | FLAMES, string methods, NumPy |
| 11 | 11 | Selenium, datetime, calendar, leap years |
| 12 | 9 | PageRank, Collatz conjecture, directed graphs |

**Sources:**
- `generate_all_weeks.py` — 97 questions from the Jan-Apr 2026 course assignments
- `progiez/nptel-assignment-answers` GitHub — 32 additional questions from Jul-Dec 2025 and Jan-Apr 2025 sessions

### 2.4 Attempt Storage (attempts.json)

Auto-created on first test completion. Not committed to git.

```json
{
  "1": [
    {
      "attempt": 1,
      "score": 64,
      "correct": 32,
      "total": 50,
      "answered": 48,
      "passed": true,
      "date": "2026-04-13 10:30",
      "sections": {"A": {"correct": 8, "total": 10}, "B": {...}, "C": {...}},
      "week_stats": {"1": {"correct": 3, "total": 4}, ...}
    }
  ]
}
```

### 2.5 Design System (style.css)

Ported from [tech1onegroup/design-system-template](https://github.com/tech1onegroup/design-system-template):

**Layer 1 — Samsung One UI structure:**
- Border radius: `1rem` (large, rounded — Samsung signature)
- Spacious padding throughout
- Card-based layout
- Mobile-first responsive

**Layer 2 — One Group brand overlay:**
| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#762224` | Buttons, header border, nav active |
| `--accent` | `#c45a5c` | Hover states, retake button |
| `--background` | `#f5f3ed` | Page background (warm canvas) |
| `--card` | `#ffffff` | All cards and panels |
| `--foreground` | `#141413` | Primary text |
| `--muted-fg` | `#5e5d59` | Secondary text |
| `--correct` | `#34C759` | Correct answer highlight |
| `--wrong` | `#FF3B30` | Wrong answer highlight |
| `--border` | `#f0eee6` | Card borders, dividers |

**Typography:**
- Body: Inter (Google Fonts CDN)
- Headings: Georgia (system serif)
- Code/Timer: JetBrains Mono (monospace)

### 2.6 Frontend (exam.js)

Client-side JavaScript handles:
- **Question loading**: `fetch(/api/question/n)` → render question + options
- **Answer submission**: `fetch(/api/submit)` → highlight correct/wrong → show explanation
- **Timer**: Countdown from 10800s, stored in `localStorage` (survives page refresh)
- **Navigation panel**: Color-coded dots (cyan=current, green=correct, red=wrong)
- **Keyboard shortcuts**: `1-4` or `A-D` to select option, `→`/`Enter` for next

---

## 3. TOOL — Development, Deployment, and Maintenance

### 3.1 Local Development

```bash
# First time setup
cd mock_exam
pip install flask
python app.py
# Open http://localhost:5000

# Phone access (same WiFi network)
# Find laptop IP: ipconfig → IPv4 Address (e.g., 192.168.1.15)
# Open http://192.168.1.15:5000 on phone
```

### 3.2 Deployment (Render.com)

**One-time setup:**
1. Push code to GitHub
2. Go to render.com → New Web Service → Connect GitHub repo
3. Render auto-detects `render.yaml` and deploys

**Auto-deploy:** Every `git push` to main triggers a new deployment.

**render.yaml config:**
```yaml
services:
  - type: web
    name: nptel-mock-exam
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 3.3 Adding More Questions

1. Edit `add_github_questions.py` — add new `add()` calls with question data
2. Run: `python add_github_questions.py`
3. Verify: `python -c "import json; print(len(json.load(open('questions.json',encoding='utf-8'))))"`
4. Commit and push → auto-deploys to Render

**Question format:**
```python
add(week=5, section="B", topic="Dictionaries",
    question="Which method removes a key and returns its value?",
    options=["dict.remove()", "dict.del()", "dict.pop()", "dict.popitem()"],
    correct_idx=2,
    explanation="dict.pop(key) removes the key and returns its value.")
```

### 3.4 Versioning

Versions are saved in `mock_exam/versions/` (gitignored — local snapshots only):

| Version | Date | Questions | Key Changes |
|---------|------|-----------|-------------|
| V1 | 2026-04-12 | 97 | Initial app — exam flow, timer, Testbook UI |
| V2 | 2026-04-12 | 129 | +32 questions (2025/2026), Q-by-Q review |
| V3 | 2026-04-12 | 129 | Attempt tracking, comparison, history, One UI design |

### 3.5 Key Decisions and Why

| Decision | Why |
|----------|-----|
| Questions in JSON, not database | Simple, portable, no setup needed. 129 questions fits easily in memory. |
| Seeded random for test generation | Same test_id = same questions = fair comparison between attempts. |
| Attempts in JSON file, not DB | Local app — no need for SQLite complexity. File persists across restarts. |
| Session stores only test_id + answers | Avoids 4KB cookie limit. Questions regenerated on-the-fly (deterministic). |
| One UI design tokens, not the full React library | Flask uses Jinja2 templates, not React. CSS variables port the visual language. |
| gunicorn for production | Flask's dev server isn't production-safe. gunicorn handles concurrent requests. |
| 2025/2026 questions only | User explicitly requested — older questions may not match current syllabus. |

### 3.6 Known Limitations

- **No user accounts** — attempt history is per-server (shared on Render, local on laptop)
- **No negative marking** — NPTEL has not confirmed negative marking for this course
- **Some questions reference NPTEL portal images** — these were excluded (text-only questions included)
- **Week 10 has only 3 questions** — limited self-contained content available for that week
- **Timer uses localStorage** — different browsers/devices have separate timers
