"""
NPTEL Mock Exam — Flask Backend (V5)
Features: Google OAuth login, per-user SQLite history, cross-device resume, Gemini chat
Run locally: python app.py
Deployed:   gunicorn app:app
"""
import json
import os
import random
import requests as http_requests
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # loads .env for local dev; ignored on Render (env vars set in dashboard)

from flask import (
    Flask, render_template, session, redirect,
    url_for, request, jsonify,
)
from authlib.integrations.flask_client import OAuth

import database as db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "nptel-dev-secret-CHANGE-IN-PROD")

# ── Google OAuth ───────────────────────────────────────────────────────────────
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ── Constants ──────────────────────────────────────────────────────────────────
QUESTIONS_FILE  = os.path.join(os.path.dirname(__file__), "questions.json")
EXAM_DURATION   = 180 * 60   # seconds
SECTION_A_COUNT = 10
SECTION_B_COUNT = 15
SECTION_C_COUNT = 25

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta"
    "/models/gemini-2.0-flash:generateContent"
)

# ── Auth decorator ─────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ── Question helpers ───────────────────────────────────────────────────────────
def load_questions():
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def generate_test(test_id: int):
    """Reproducible 50-question set. Same test_id → same questions always."""
    all_q  = load_questions()
    sec_a  = [q for q in all_q if q["section"] == "A"]
    sec_b  = [q for q in all_q if q["section"] == "B"]
    sec_c  = [q for q in all_q if q["section"] == "C"]
    rng    = random.Random(test_id * 7919)
    test_qs = (
        rng.sample(sec_a, min(SECTION_A_COUNT, len(sec_a)))
        + rng.sample(sec_b, min(SECTION_B_COUNT, len(sec_b)))
        + rng.sample(sec_c, min(SECTION_C_COUNT, len(sec_c)))
    )
    rng.shuffle(test_qs)
    return test_qs


def get_test_questions():
    tid = session.get("test_id")
    return generate_test(tid) if tid else None


# ── Auth routes ────────────────────────────────────────────────────────────────
@app.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("index"))
    configured = bool(os.getenv("GOOGLE_CLIENT_ID"))
    return render_template("login.html", configured=configured)


@app.route("/auth/login")
def auth_login():
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/auth/callback")
def auth_callback():
    try:
        token    = google.authorize_access_token()
        userinfo = token.get("userinfo") or {}
        google_id = userinfo.get("sub")
        email     = userinfo.get("email", "")
        name      = userinfo.get("name", email)
        picture   = userinfo.get("picture", "")

        if not google_id:
            return redirect(url_for("login"))

        user_id = db.upsert_user(google_id, email, name, picture)
        session["user_id"]      = user_id
        session["user_name"]    = name
        session["user_picture"] = picture
        session["user_email"]   = email
        return redirect(url_for("index"))
    except Exception as e:
        print(f"[auth_callback] error: {e}")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ── Dashboard ──────────────────────────────────────────────────────────────────
@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    attempts_summary = db.get_all_attempts_summary(user_id)
    in_progress      = db.get_all_in_progress(user_id)
    return render_template(
        "index.html",
        attempts    = attempts_summary,
        in_progress = in_progress,
        user_name   = session.get("user_name", ""),
        user_picture= session.get("user_picture", ""),
    )


# ── Start / Resume ─────────────────────────────────────────────────────────────
@app.route("/start/<int:test_id>", methods=["POST"])
@login_required
def start(test_id):
    if test_id < 1 or test_id > 10:
        return redirect(url_for("index"))

    user_id = session["user_id"]
    action  = request.form.get("action", "new")

    # Preserve auth keys, clear exam state
    for key in ["test_id", "answers", "started_at",
                "result_saved", "resume_index", "resume_time"]:
        session.pop(key, None)

    if action == "resume":
        progress = db.get_exam_progress(user_id, test_id)
        if progress:
            session["test_id"]      = test_id
            session["answers"]      = json.loads(progress["answers_json"])
            session["started_at"]   = progress["started_at"]
            session["result_saved"] = False
            session["resume_index"] = progress["current_index"]
            session["resume_time"]  = progress["time_remaining"]
            return redirect(url_for("exam"))

    # Start fresh — delete any stale progress
    db.clear_exam_progress(user_id, test_id)
    now = datetime.now().isoformat()
    session["test_id"]      = test_id
    session["answers"]      = {}
    session["started_at"]   = now
    session["result_saved"] = False
    session["resume_index"] = 0
    session["resume_time"]  = EXAM_DURATION
    db.upsert_exam_progress(user_id, test_id, {}, 0, now, EXAM_DURATION)
    return redirect(url_for("exam"))


# ── Exam page ──────────────────────────────────────────────────────────────────
@app.route("/exam")
@login_required
def exam():
    if "test_id" not in session:
        return redirect(url_for("index"))
    questions     = get_test_questions()
    resume_index  = session.get("resume_index", 0)
    resume_time   = session.get("resume_time", EXAM_DURATION)
    saved_answers = json.dumps(session.get("answers", {}))
    return render_template(
        "exam.html",
        test_id      = session["test_id"],
        total        = len(questions),
        duration     = EXAM_DURATION,
        resume_index = resume_index,
        resume_time  = resume_time,
        saved_answers= saved_answers,
        user_name    = session.get("user_name", ""),
        user_picture = session.get("user_picture", ""),
    )


# ── API: question ──────────────────────────────────────────────────────────────
@app.route("/api/question/<int:n>")
@login_required
def get_question(n):
    questions = get_test_questions()
    if questions is None:
        return jsonify({"error": "no session"}), 403
    if n < 0 or n >= len(questions):
        return jsonify({"error": "out of range"}), 404
    q = questions[n]
    return jsonify({
        "index":    n,
        "total":    len(questions),
        "question": q["question"],
        "options":  q["options"],
        "week":     q["week"],
        "topic":    q["topic"],
        "section":  q["section"],
    })


# ── API: submit answer ─────────────────────────────────────────────────────────
@app.route("/api/submit", methods=["POST"])
@login_required
def submit_answer():
    questions = get_test_questions()
    if questions is None:
        return jsonify({"error": "no session"}), 403

    data   = request.get_json()
    n      = data.get("index")
    chosen = data.get("chosen")
    time_remaining = int(data.get("time_remaining", EXAM_DURATION))

    if n is None or n < 0 or n >= len(questions):
        return jsonify({"error": "invalid index"}), 400

    q           = questions[n]
    correct_idx = q["correct"]
    is_correct  = chosen == correct_idx

    answers          = session.get("answers", {})
    answers[str(n)]  = {"chosen": chosen, "correct": correct_idx, "is_correct": is_correct}
    session["answers"] = answers

    # Persist to DB for cross-device resume
    user_id    = session["user_id"]
    test_id    = session["test_id"]
    next_index = min(n + 1, len(questions) - 1)
    db.upsert_exam_progress(
        user_id, test_id, answers, next_index,
        session["started_at"], time_remaining,
    )

    return jsonify({
        "is_correct":    is_correct,
        "correct_index": correct_idx,
        "explanation":   q.get("explanation", ""),
    })


# ── Result page ────────────────────────────────────────────────────────────────
@app.route("/result")
@login_required
def result():
    questions = get_test_questions()
    if questions is None:
        return redirect(url_for("index"))

    answers  = session.get("answers", {})
    test_id  = session.get("test_id", 1)
    user_id  = session["user_id"]
    total    = len(questions)
    answered = len(answers)
    correct_count = sum(1 for v in answers.values() if v["is_correct"])
    score    = correct_count * 2

    sections   = {s: {"correct": 0, "total": 0} for s in ("A", "B", "C")}
    week_stats = {}
    for i, q in enumerate(questions):
        sec  = q["section"]
        week = q["week"]
        sections[sec]["total"] += 1
        week_stats.setdefault(week, {"correct": 0, "total": 0})
        week_stats[week]["total"] += 1
        ans = answers.get(str(i))
        if ans and ans["is_correct"]:
            sections[sec]["correct"] += 1
            week_stats[week]["correct"] += 1

    weak_weeks = sorted([
        w for w, s in week_stats.items()
        if s["total"] > 0 and s["correct"] / s["total"] < 0.5
    ])
    passed = score >= 40

    prev_attempts = db.get_attempts_for_test(user_id, test_id)
    if not session.get("result_saved"):
        attempt_num = db.record_attempt(
            user_id, test_id, score, correct_count, total,
            answered, passed, sections, week_stats,
        )
        session["result_saved"] = True
        db.clear_exam_progress(user_id, test_id)   # no longer in-progress
    else:
        attempt_num = len(prev_attempts)

    previous = prev_attempts[-1] if prev_attempts else None

    review = []
    for i, q in enumerate(questions):
        ans = answers.get(str(i))
        review.append({
            "num":         i + 1,
            "question":    q["question"],
            "options":     q["options"],
            "correct":     q["correct"],
            "chosen":      ans["chosen"] if ans else None,
            "is_correct":  ans["is_correct"] if ans else False,
            "explanation": q.get("explanation", ""),
            "week":        q["week"],
            "section":     q["section"],
            "topic":       q.get("topic", ""),
        })

    return render_template(
        "result.html",
        test_id       = test_id,
        score         = score,
        total         = total,
        answered      = answered,
        correct       = correct_count,
        passed        = passed,
        sections      = sections,
        weak_weeks    = weak_weeks,
        week_stats    = week_stats,
        review        = review,
        attempt_num   = attempt_num,
        previous      = previous,
        user_name     = session.get("user_name", ""),
        user_picture  = session.get("user_picture", ""),
        gemini_enabled= bool(GEMINI_API_KEY),
    )


# ── History page ───────────────────────────────────────────────────────────────
@app.route("/history/<int:test_id>")
@login_required
def history(test_id):
    if test_id < 1 or test_id > 10:
        return redirect(url_for("index"))
    user_id  = session["user_id"]
    attempts = db.get_attempts_for_test(user_id, test_id)
    return render_template(
        "history.html",
        test_id      = test_id,
        attempts     = attempts,
        user_name    = session.get("user_name", ""),
        user_picture = session.get("user_picture", ""),
    )


# ── Gemini API ─────────────────────────────────────────────────────────────────
@app.route("/api/gemini", methods=["POST"])
@login_required
def gemini_ask():
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini not configured on this server."}), 503

    data        = request.get_json()
    question    = data.get("question", "")
    options     = data.get("options", [])
    correct_idx = int(data.get("correct_idx", 0))
    user_idx    = data.get("user_idx")   # None if skipped
    is_correct  = bool(data.get("is_correct", False))
    explanation = data.get("explanation", "")
    week        = data.get("week", "")
    topic       = data.get("topic", "")

    labels        = ["A", "B", "C", "D"]
    correct_label = labels[correct_idx] if 0 <= correct_idx < 4 else "?"
    correct_text  = options[correct_idx] if 0 <= correct_idx < len(options) else ""
    options_block = "\n".join(
        f"  {labels[i]}) {opt}" for i, opt in enumerate(options)
    )

    if user_idx is not None:
        u_label = labels[user_idx] if 0 <= user_idx < 4 else "?"
        u_text  = options[user_idx] if 0 <= user_idx < len(options) else ""
        student_line = (
            f"Student answered: {u_label}) {u_text} "
            f"— {'CORRECT' if is_correct else 'INCORRECT'}"
        )
    else:
        student_line = "Student answered: (skipped / not answered)"

    prompt = f"""You are a friendly, concise tutor for the NPTEL "Joy of Computing Using Python" beginner course.

A student is reviewing their mock exam. Here is the question:

Week {week} | Topic: {topic}

QUESTION:
{question}

OPTIONS:
{options_block}

Correct answer: {correct_label}) {correct_text}
{student_line}
Standard explanation given: {explanation}

Please explain why the correct answer is right in simple, beginner-friendly language. If the student got it wrong, gently clarify their mistake. Keep the response to 4–6 sentences. Write plain paragraphs — no bullet points or markdown headers."""

    try:
        resp = http_requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        text   = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": text.strip()})
    except http_requests.Timeout:
        return jsonify({"error": "Gemini took too long. Please try again."}), 504
    except Exception as e:
        print(f"[gemini_ask] error: {e}")
        return jsonify({"error": "Gemini is unavailable right now. Try again shortly."}), 503


# ── Startup ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
