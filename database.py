"""
database.py — SQLite helpers for NPTEL Mock Exam
Tables: users, attempts, exam_progress
"""
import sqlite3
import json
import os
from contextlib import contextmanager
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "exam.db")


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                google_id  TEXT UNIQUE NOT NULL,
                email      TEXT NOT NULL,
                name       TEXT NOT NULL,
                picture    TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS attempts (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                test_id         INTEGER NOT NULL,
                attempt_num     INTEGER NOT NULL,
                score           INTEGER NOT NULL,
                correct         INTEGER NOT NULL,
                total           INTEGER NOT NULL,
                answered        INTEGER NOT NULL,
                passed          INTEGER NOT NULL,
                date            TEXT NOT NULL,
                sections_json   TEXT NOT NULL,
                week_stats_json TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS exam_progress (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        INTEGER NOT NULL,
                test_id        INTEGER NOT NULL,
                answers_json   TEXT NOT NULL DEFAULT '{}',
                current_index  INTEGER NOT NULL DEFAULT 0,
                time_remaining INTEGER NOT NULL DEFAULT 10800,
                started_at     TEXT NOT NULL,
                last_updated   TEXT NOT NULL,
                UNIQUE(user_id, test_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


# ── Users ──────────────────────────────────────────────────────────────────────

def upsert_user(google_id, email, name, picture):
    """Insert or update a user; return their integer id."""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO users (google_id, email, name, picture, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(google_id) DO UPDATE SET
                email   = excluded.email,
                name    = excluded.name,
                picture = excluded.picture
        """, (google_id, email, name, picture, datetime.now().isoformat()))
        row = conn.execute(
            "SELECT id FROM users WHERE google_id = ?", (google_id,)
        ).fetchone()
        return row["id"]


def get_user_by_id(user_id):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


# ── Attempts ───────────────────────────────────────────────────────────────────

def record_attempt(user_id, test_id, score, correct, total,
                   answered, passed, sections, week_stats):
    """Append a completed attempt and return its attempt_num."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM attempts WHERE user_id=? AND test_id=?",
            (user_id, test_id),
        ).fetchone()
        attempt_num = row["c"] + 1
        conn.execute("""
            INSERT INTO attempts
              (user_id, test_id, attempt_num, score, correct, total,
               answered, passed, date, sections_json, week_stats_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, test_id, attempt_num,
            score, correct, total, answered,
            1 if passed else 0,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            json.dumps(sections),
            json.dumps({str(k): v for k, v in week_stats.items()}),
        ))
        return attempt_num


def get_attempts_for_test(user_id, test_id):
    """Return list of dicts (all attempts, oldest first)."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM attempts WHERE user_id=? AND test_id=? ORDER BY attempt_num",
            (user_id, test_id),
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["sections"]   = json.loads(d["sections_json"])
        d["week_stats"] = json.loads(d["week_stats_json"])
        d["passed"]     = bool(d["passed"])
        result.append(d)
    return result


def get_all_attempts_summary(user_id):
    """Return {1..10: {count, best_score, last_score, last_passed, last_date} or None}."""
    summary = {}
    with get_db() as conn:
        for tid in range(1, 11):
            rows = conn.execute(
                "SELECT score, passed, date FROM attempts "
                "WHERE user_id=? AND test_id=? ORDER BY attempt_num",
                (user_id, tid),
            ).fetchall()
            if rows:
                scores = [r["score"] for r in rows]
                last   = rows[-1]
                summary[tid] = {
                    "count":       len(rows),
                    "best_score":  max(scores),
                    "last_score":  last["score"],
                    "last_passed": bool(last["passed"]),
                    "last_date":   last["date"],
                }
            else:
                summary[tid] = None
    return summary


# ── Exam Progress ──────────────────────────────────────────────────────────────

def upsert_exam_progress(user_id, test_id, answers, current_index,
                         started_at, time_remaining):
    """Save (or update) in-progress exam state."""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO exam_progress
              (user_id, test_id, answers_json, current_index,
               time_remaining, started_at, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, test_id) DO UPDATE SET
                answers_json   = excluded.answers_json,
                current_index  = excluded.current_index,
                time_remaining = excluded.time_remaining,
                last_updated   = excluded.last_updated
        """, (
            user_id, test_id,
            json.dumps(answers),
            current_index,
            time_remaining,
            started_at,
            datetime.now().isoformat(),
        ))


def get_exam_progress(user_id, test_id):
    """Return progress dict or None."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM exam_progress WHERE user_id=? AND test_id=?",
            (user_id, test_id),
        ).fetchone()
    return dict(row) if row else None


def get_all_in_progress(user_id):
    """Return {test_id: {current_index, time_remaining, last_updated}} for all in-progress tests."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT test_id, current_index, time_remaining, last_updated "
            "FROM exam_progress WHERE user_id=?",
            (user_id,),
        ).fetchall()
    return {r["test_id"]: dict(r) for r in rows}


def clear_exam_progress(user_id, test_id):
    """Delete in-progress state (call when result is saved)."""
    with get_db() as conn:
        conn.execute(
            "DELETE FROM exam_progress WHERE user_id=? AND test_id=?",
            (user_id, test_id),
        )
