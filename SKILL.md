# Skills & Capabilities Guide

> For AI agents and developers working on the NPTEL Mock Exam project.
> This file describes what skills are needed, how to use them, and what tools are available.

---

## 1. Question Engineering

### What You Need To Know
- NPTEL/SWAYAM exam format: 50 MCQs, 3 sections (A/B/C), 2 marks each, 180 minutes
- Section difficulty: A = factual recall, B = understanding, C = code tracing & scenarios
- All 12 weeks of "Joy of Computing Using Python" course syllabus

### How To Add Questions
```python
# In add_github_questions.py
add(week=5, section="B", topic="Dictionaries",
    question="Which method removes a key and returns its value?",
    options=["dict.remove()", "dict.del()", "dict.pop()", "dict.popitem()"],
    correct_idx=2,   # 0-indexed: option C
    explanation="dict.pop(key) removes the key and returns its value.")
```

### Rules
- Only include questions from **2025 and 2026** NPTEL sessions
- Skip image-dependent questions (code screenshots not renderable as text)
- Every question MUST have an `explanation` — this is the core learning feature
- `correct` is **0-indexed** (0=A, 1=B, 2=C, 3=D)
- Deduplicate: check first 50 chars of question text against existing bank
- After adding, run `python add_github_questions.py` to merge into questions.json

### Section Assignment Guidelines
| Section | Assign When | Examples |
|---------|------------|---------|
| A | Single-concept recall, definition, syntax | "What does .wav store?", "Which creates an empty list?" |
| B | Understanding, applying rules, moderate reasoning | "What does Monty Hall switching give?", "What is slicing [1:4]?" |
| C | Code tracing, multi-step, scenario-based | "After 3 passes of bubble sort...", "What is func(5) output?" |

### Question Sources
| Source | Type | How To Access |
|--------|------|--------------|
| `generate_all_weeks.py` | 2026 course assignments | Local file — parse `q_block()` calls |
| `progiez/nptel-assignment-answers` | 2024-2026 weekly quizzes | GitHub — `the-joy-of-computation-using-python/week-*.md` |
| `gxuxhxm/NPTEL-The-Joy-of-Computing-using-Python` | Quiz answers + exam papers | GitHub — `/Assignments/` directory |
| `kishanrajput23/NPTEL-The-Joy-of-Computing-using-Python` | Quiz answers + exam pattern | GitHub — Week folders with README.md |

---

## 2. Flask Backend Development

### Key Patterns
- **No database** — JSON files for persistence (questions.json, attempts.json)
- **Session-light** — only `test_id` + `answers` dict in cookie (avoid 4KB limit)
- **Deterministic tests** — `random.Random(test_id * 7919)` for reproducible generation
- **Attempt tracking** — `record_attempt()` appends to attempts.json on result page load

### Adding A New Route
```python
@app.route("/new-page")
def new_page():
    # Load any data needed
    data = load_something()
    return render_template("new_page.html", data=data)
```

### Template Rendering
- Uses Jinja2 (Flask default)
- All templates in `templates/` directory
- Static files (CSS, JS) in `static/` directory
- Access static: `{{ url_for('static', filename='style.css') }}`

### API Pattern (JSON endpoints)
```python
@app.route("/api/something", methods=["POST"])
def api_something():
    data = request.get_json()
    # Process...
    return jsonify({"result": value})
```

---

## 3. Frontend Development

### Design System
Ported from [tech1onegroup/design-system-template](https://github.com/tech1onegroup/design-system-template).

**Structure:** Samsung One UI base (1rem radius, spacious) + One Group brand overlay (warm reds, cream canvas).

### CSS Variables (use these, don't hardcode colors)
```css
var(--primary)       /* #762224 — buttons, header, active states */
var(--accent)        /* #c45a5c — hover states, secondary buttons */
var(--background)    /* #f5f3ed — page background */
var(--card)          /* #ffffff — all cards */
var(--foreground)    /* #141413 — primary text */
var(--muted-fg)      /* #5e5d59 — secondary text */
var(--correct)       /* #34C759 — correct answer green */
var(--wrong)         /* #FF3B30 — wrong answer red */
var(--border)        /* #f0eee6 — borders, dividers */
var(--radius)        /* 1rem — Samsung One UI rounded corners */
var(--radius-xl)     /* 1.4rem — cards and panels */
var(--shadow)        /* 0 2px 12px rgba(0,0,0,0.08) — card elevation */
```

### Adding A New Component
1. Create the HTML structure in the template
2. Style using existing CSS variables (never hardcode `#762224`, use `var(--primary)`)
3. Follow One UI patterns: large radius, spacious padding (16-26px), card-based layout
4. Mobile-first: test at 375px width minimum

### JavaScript (exam.js)
- Vanilla JS — no frameworks
- Fetch API for all server communication
- `localStorage` for timer persistence
- Keyboard shortcuts: `1-4`/`A-D` for options, `→`/`Enter` for next

---

## 4. Deployment

### Render.com
- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Auto-deploy:** connected to GitHub main branch
- **Free tier:** 750 hours/month, sleeps after 15 min inactivity

### Local Development
```bash
pip install flask
python app.py                    # http://localhost:5000
# Phone: http://<laptop-IP>:5000  (same WiFi)
```

### Environment
- Python 3.12+
- No environment variables required (app works with defaults)
- `attempts.json` auto-created on first test completion

---

## 5. Testing

### Manual Testing Checklist
- [ ] Homepage loads with 10 test cards
- [ ] "Start Test" creates session and redirects to exam
- [ ] Question loads with 4 options, section tag, week tag
- [ ] Clicking option shows green/red + explanation
- [ ] "Next" button appears after answering
- [ ] Timer counts down, survives page refresh
- [ ] After Q50, "View Results" shows score page
- [ ] Result page has: score circle, pass/fail, section table, week pills
- [ ] Q-by-Q review shows all 50 questions with correct answers
- [ ] Retaking test shows comparison with previous attempt
- [ ] Dashboard shows attempt count, best score, last score
- [ ] History page shows all attempts side-by-side
- [ ] Mobile responsive (test at 375px width)

### Automated Testing (Python)
```python
import requests
s = requests.Session()
s.post('http://localhost:5000/start/1', allow_redirects=True)
q = s.get('http://localhost:5000/api/question/0').json()
assert 'question' in q and len(q['options']) == 4
r = s.post('http://localhost:5000/api/submit', json={'index': 0, 'chosen': 0}).json()
assert 'is_correct' in r and 'explanation' in r
```

---

## 6. Common Tasks

| Task | Command / Action |
|------|-----------------|
| Add questions | Edit `add_github_questions.py` → run it → commit + push |
| Change colors | Edit CSS variables in `static/style.css` `:root` block |
| Add a new page | Create route in `app.py` + template in `templates/` |
| Update design | Modify `static/style.css` using design tokens |
| Check question count | `python -c "import json; print(len(json.load(open('questions.json',encoding='utf-8'))))"` |
| Reset attempts | Delete `attempts.json` (auto-recreated) |
| Deploy update | `git add . && git commit -m "..." && git push` → auto-deploys |
| Run locally | `python app.py` → http://localhost:5000 |
