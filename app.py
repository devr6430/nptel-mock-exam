"""
NPTEL Mock Exam — Flask Backend (V2)
Run: python app.py
Access on laptop: http://localhost:5000
Access on phone:  http://<your-laptop-LAN-IP>:5000
"""
import json
import os
import random
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, request, jsonify

app = Flask(__name__)
app.secret_key = "nptel-noc26-cs84-joc-2026-exam-prep"

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions.json")
ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "attempts.json")
EXAM_DURATION = 180 * 60  # 180 minutes in seconds
TOTAL_QUESTIONS = 50
SECTION_A_COUNT = 10
SECTION_B_COUNT = 15
SECTION_C_COUNT = 25


def load_questions():
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def generate_test(test_id: int):
    """
    Generate a reproducible 50-question test from the question bank.
    Samples 10 from Section A, 15 from Section B, 25 from Section C.
    Questions are then shuffled — NOT grouped by week.
    """
    all_q = load_questions()
    sec_a = [q for q in all_q if q["section"] == "A"]
    sec_b = [q for q in all_q if q["section"] == "B"]
    sec_c = [q for q in all_q if q["section"] == "C"]

    rng = random.Random(test_id * 7919)  # isolated RNG per test

    a_count = min(SECTION_A_COUNT, len(sec_a))
    b_count = min(SECTION_B_COUNT, len(sec_b))
    c_count = min(SECTION_C_COUNT, len(sec_c))

    test_qs = (
        rng.sample(sec_a, a_count)
        + rng.sample(sec_b, b_count)
        + rng.sample(sec_c, c_count)
    )
    rng.shuffle(test_qs)
    return test_qs


def get_test_questions():
    """Regenerate questions from session test_id (deterministic, avoids cookie bloat)."""
    test_id = session.get("test_id")
    if test_id is None:
        return None
    return generate_test(test_id)


# ── Attempt Persistence ───────────────────────────────────────────────────────

def load_attempts():
    if os.path.exists(ATTEMPTS_FILE):
        with open(ATTEMPTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_attempts(data):
    with open(ATTEMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def record_attempt(test_id, score, correct, total, answered, passed,
                   sections, week_stats):
    """Save a completed attempt to attempts.json."""
    all_attempts = load_attempts()
    key = str(test_id)
    if key not in all_attempts:
        all_attempts[key] = []

    attempt_num = len(all_attempts[key]) + 1
    all_attempts[key].append({
        "attempt": attempt_num,
        "score": score,
        "correct": correct,
        "total": total,
        "answered": answered,
        "passed": passed,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sections": sections,
        "week_stats": {str(k): v for k, v in week_stats.items()},
    })
    save_attempts(all_attempts)
    return attempt_num


def get_attempts_for_test(test_id):
    all_attempts = load_attempts()
    return all_attempts.get(str(test_id), [])


def get_all_attempts_summary():
    """Return a dict {test_id: {count, best_score, last_score, last_date}} for dashboard."""
    all_attempts = load_attempts()
    summary = {}
    for tid in range(1, 11):
        attempts = all_attempts.get(str(tid), [])
        if attempts:
            summary[tid] = {
                "count": len(attempts),
                "best_score": max(a["score"] for a in attempts),
                "last_score": attempts[-1]["score"],
                "last_passed": attempts[-1]["passed"],
                "last_date": attempts[-1]["date"],
            }
        else:
            summary[tid] = None
    return summary


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    attempts_summary = get_all_attempts_summary()
    return render_template("index.html", attempts=attempts_summary)


@app.route("/start/<int:test_id>", methods=["POST"])
def start(test_id):
    if test_id < 1 or test_id > 10:
        return redirect(url_for("index"))
    session.clear()
    session["test_id"] = test_id
    session["answers"] = {}
    session["started_at"] = datetime.now().isoformat()
    session["result_saved"] = False
    return redirect(url_for("exam"))


@app.route("/exam")
def exam():
    if "test_id" not in session:
        return redirect(url_for("index"))
    questions = get_test_questions()
    return render_template(
        "exam.html",
        test_id=session["test_id"],
        total=len(questions),
        duration=EXAM_DURATION,
    )


@app.route("/api/question/<int:n>")
def get_question(n):
    questions = get_test_questions()
    if questions is None:
        return jsonify({"error": "no session"}), 403
    if n < 0 or n >= len(questions):
        return jsonify({"error": "out of range"}), 404
    q = questions[n]
    return jsonify({
        "index": n,
        "total": len(questions),
        "question": q["question"],
        "options": q["options"],
        "week": q["week"],
        "topic": q["topic"],
        "section": q["section"],
    })


@app.route("/api/submit", methods=["POST"])
def submit_answer():
    questions = get_test_questions()
    if questions is None:
        return jsonify({"error": "no session"}), 403
    data = request.get_json()
    n = data.get("index")
    chosen = data.get("chosen")

    if n is None or n < 0 or n >= len(questions):
        return jsonify({"error": "invalid index"}), 400

    q = questions[n]
    correct_idx = q["correct"]
    is_correct = chosen == correct_idx

    answers = session.get("answers", {})
    answers[str(n)] = {
        "chosen": chosen,
        "correct": correct_idx,
        "is_correct": is_correct,
    }
    session["answers"] = answers

    return jsonify({
        "is_correct": is_correct,
        "correct_index": correct_idx,
        "explanation": q.get("explanation", ""),
    })


@app.route("/result")
def result():
    questions = get_test_questions()
    if questions is None:
        return redirect(url_for("index"))

    answers = session.get("answers", {})
    test_id = session.get("test_id", 1)

    # Score calculation
    total = len(questions)
    answered = len(answers)
    correct_count = sum(1 for v in answers.values() if v["is_correct"])
    score = correct_count * 2

    # Section breakdown
    sections = {"A": {"correct": 0, "total": 0}, "B": {"correct": 0, "total": 0}, "C": {"correct": 0, "total": 0}}
    week_stats = {}

    for i, q in enumerate(questions):
        sec = q["section"]
        week = q["week"]
        sections[sec]["total"] += 1
        if week not in week_stats:
            week_stats[week] = {"correct": 0, "total": 0}
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

    # Save attempt (only once per test session)
    prev_attempts = get_attempts_for_test(test_id)
    if not session.get("result_saved"):
        attempt_num = record_attempt(
            test_id, score, correct_count, total, answered, passed,
            sections, week_stats
        )
        session["result_saved"] = True
    else:
        attempt_num = len(prev_attempts)

    # Get the previous attempt for comparison (if exists)
    previous = prev_attempts[-1] if prev_attempts else None

    # Build review data
    review = []
    for i, q in enumerate(questions):
        ans = answers.get(str(i))
        review.append({
            "num": i + 1,
            "question": q["question"],
            "options": q["options"],
            "correct": q["correct"],
            "chosen": ans["chosen"] if ans else None,
            "is_correct": ans["is_correct"] if ans else False,
            "explanation": q.get("explanation", ""),
            "week": q["week"],
            "section": q["section"],
            "topic": q.get("topic", ""),
        })

    return render_template(
        "result.html",
        test_id=test_id,
        score=score,
        total=total,
        answered=answered,
        correct=correct_count,
        passed=passed,
        sections=sections,
        weak_weeks=weak_weeks,
        week_stats=week_stats,
        review=review,
        attempt_num=attempt_num,
        previous=previous,
    )


@app.route("/history/<int:test_id>")
def history(test_id):
    """Show all attempts for a specific test with comparison."""
    if test_id < 1 or test_id > 10:
        return redirect(url_for("index"))
    attempts = get_attempts_for_test(test_id)
    return render_template("history.html", test_id=test_id, attempts=attempts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
