"""
extract_all_assignments.py
Parse all 36 downloaded HTML files and build a new questions.json
with all single-answer MCQ questions from 2024–2026 assignments.

Section assignment (mirrors NPTEL final exam difficulty curve):
  Weeks 1–4  → Section A  (easy)
  Weeks 5–8  → Section B  (medium)
  Weeks 9–12 → Section C  (hard)
"""

import base64
import json
import os
import re
import sys
from bs4 import BeautifulSoup, NavigableString

HTML_DIR  = os.path.join(os.path.dirname(__file__), "static", "html")
OUT_FILE  = os.path.join(os.path.dirname(__file__), "questions.json")

YEARS = [2024, 2025, 2026]

def week_to_section(week):
    if week <= 4:  return "A"
    if week <= 8:  return "B"
    return "C"


def inner_text(tag):
    """Return visible text of a tag, collapsing whitespace."""
    if tag is None:
        return ""
    return re.sub(r"\s+", " ", tag.get_text(separator=" ")).strip()


def extract_image_url(tag):
    """Return first <img> src found inside tag, or empty string."""
    if tag is None:
        return ""
    img = tag.find("img")
    return img["src"] if img and img.get("src") else ""


def parse_html_file(path, year, week):
    """Return list of question dicts from one HTML assignment file."""
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # ── Step 1: Decode every atob() payload that describes a single question ──
    # Use a two-pass approach: first find all qids from div IDs, then
    # search for each qid's questionData assignment and decode the base64.
    q_payloads = {}   # qid -> decoded dict

    # Pattern: questionData["<qid>"] = JSON.parse( ... window.atob( "<b64>" ...
    # Use a greedy match from questionData[ up to the base64 string
    all_b64_pat = re.compile(
        r'questionData\[.+?window\.atob\(\s*"([A-Za-z0-9+/=\s]+?)"',
        re.DOTALL,
    )
    all_qid_pat = re.compile(r'questionData\["([^"]+)"\]')

    # Collect all (qid, position) pairs
    qid_positions = [(m.group(1), m.start()) for m in all_qid_pat.finditer(html)]

    for qid, pos in qid_positions:
        # Find the base64 string that follows this questionData assignment
        chunk = html[pos:pos + 2000]
        b64_m = re.search(r'window\.atob\(\s*"([A-Za-z0-9+/=\s]+?)"', chunk, re.DOTALL)
        if not b64_m:
            continue
        b64 = re.sub(r"\s+", "", b64_m.group(1))
        try:
            data = json.loads(base64.b64decode(b64).decode("utf-8"))
        except Exception:
            continue
        if "choices" in data:
            q_payloads[qid] = data

    if not q_payloads:
        return []

    # ── Step 2: Parse HTML to get question text, options, feedback ────────────
    soup = BeautifulSoup(html, "html.parser")
    questions = []

    for qid, payload in q_payloads.items():
        # Skip MSQ (multiple correct answers)
        if payload.get("multipleCorrectAnswer", False):
            continue

        choices = payload.get("choices", [])
        if len(choices) < 2:
            continue

        # Find the correct answer index (score == 1.0 or max score)
        max_score = max(c.get("score", 0) for c in choices)
        correct_idx = next(
            (i for i, c in enumerate(choices) if c.get("score", 0) == max_score),
            0,
        )

        # Options from the decoded payload (most reliable — avoids HTML encoding)
        options = [c.get("text", "").strip() for c in choices]
        if any(not o for o in options):
            options = None   # fall back to HTML parsing

        # Find the DOM element for this question
        mc_div = soup.find(id=qid)
        if mc_div is None:
            continue

        # Question text
        qt_div = mc_div.find(class_="qt-question")
        q_text = inner_text(qt_div) if qt_div else ""

        # If options couldn't come from payload, read from HTML labels
        if options is None:
            choice_divs = mc_div.find_all(class_="gcb-mcq-choice")
            options = [inner_text(d.find("label")) for d in choice_divs]

        # Skip if we still don't have 4 options
        if len(options) != 4:
            continue

        # Group introduction — provides context shared across multiple questions
        group = mc_div.find_parent(class_="qt-question-group")
        intro_text = ""
        if group:
            intro_div = group.find(class_="qt-introduction")
            if intro_div:
                intro_text = inner_text(intro_div)
                # Flag if the intro references an image we can't embed
                if intro_div.find("img"):
                    img_url = extract_image_url(intro_div)
                    intro_text += f" [Image: {img_url}]" if img_url else " [Image]"

        # Combine intro + question (only if intro adds meaningful context)
        full_question = q_text
        if intro_text and intro_text not in q_text:
            full_question = intro_text + " — " + q_text

        # Infer topic from the question text (simple heuristic)
        topic = infer_topic(q_text, week)

        # Unique ID
        qid_clean = f"y{year}w{week}_{qid[:8]}"

        questions.append({
            "id":          qid_clean,
            "week":        week,
            "year":        year,
            "section":     week_to_section(week),
            "topic":       topic,
            "question":    full_question,
            "options":     options,
            "correct":     correct_idx,
            "explanation": "",
        })

    return questions


TOPIC_KEYWORDS = {
    "scratch": "Scratch",
    "sprite": "Scratch",
    "loop":   "Loops",
    "repeat": "Loops",
    "palindrome": "Palindrome",
    "fibonacci": "Fibonacci",
    "sort": "Sorting",
    "bubble": "Bubble Sort",
    "binary search": "Binary Search",
    "search": "Searching",
    "dict": "Dictionaries",
    "list": "Lists",
    "string": "Strings",
    "caesar": "Caesar Cipher",
    "cipher": "Caesar Cipher",
    "recursion": "Recursion",
    "recursive": "Recursion",
    "turtle": "Turtle Graphics",
    "graph": "Graphs",
    "networkx": "Graphs",
    "pagerank": "PageRank",
    "collatz": "Collatz",
    "sentiment": "Sentiment Analysis",
    "nltk": "NLTK",
    "magic square": "Magic Square",
    "monty hall": "Monty Hall",
    "birthday": "Birthday Paradox",
    "selenium": "Selenium",
    "calendar": "Calendar",
    "leap year": "Leap Year",
    "numpy": "NumPy",
    "image": "Image Processing",
    "csv": "CSV",
    "file": "File Handling",
    "variable": "Variables",
    "function": "Functions",
    "armstrong": "Armstrong Numbers",
    "prime": "Prime Numbers",
    "factorial": "Factorial",
    "fizzbuzz": "FizzBuzz",
    "random": "Randomness",
}

def infer_topic(text, week):
    lower = text.lower()
    for kw, topic in TOPIC_KEYWORDS.items():
        if kw in lower:
            return topic
    return f"Week {week}"


def main():
    all_questions = []
    stats = {}

    for year in YEARS:
        year_dir = os.path.join(HTML_DIR, str(year))
        if not os.path.isdir(year_dir):
            print(f"  SKIP  {year}/ (not found)")
            continue
        for week in range(1, 13):
            path = os.path.join(year_dir, f"week{week}.html")
            if not os.path.exists(path):
                print(f"  SKIP  {year}/week{week}.html")
                continue
            qs = parse_html_file(path, year, week)
            all_questions.extend(qs)
            key = f"{year}/w{week}"
            stats[key] = len(qs)
            print(f"  OK    {year}/week{week}.html  -> {len(qs)} questions")

    # Deduplicate: only remove exact matches (same text + same options + same correct)
    seen = set()
    unique = []
    for q in all_questions:
        key = (
            q["question"].strip().lower(),
            tuple(o.strip().lower() for o in q["options"]),
            q["correct"],
        )
        if key not in seen:
            seen.add(key)
            unique.append(q)

    print(f"\nTotal extracted : {len(all_questions)}")
    print(f"After deduplicate: {len(unique)}")

    # Section distribution
    for sec in ("A", "B", "C"):
        n = sum(1 for q in unique if q["section"] == sec)
        print(f"  Section {sec}: {n}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"\nSaved -> {OUT_FILE}")
    return unique


if __name__ == "__main__":
    main()
