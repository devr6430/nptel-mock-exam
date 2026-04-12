/* NPTEL Mock Exam — exam.js
   Handles: question loading, answer submission, timer, navigation panel
*/
"use strict";

// ── State ────────────────────────────────────────────────────────────────────
const TOTAL = window.EXAM_TOTAL;
const DURATION = window.EXAM_DURATION;  // seconds
const TIMER_KEY = `exam_timer_${window.TEST_ID}`;

let currentIndex = 0;
let answered = {};   // { index: { chosen, correct, isCorrect } }
let timerInterval = null;

// ── DOM refs ─────────────────────────────────────────────────────────────────
const qText      = document.getElementById("q-text");
const qMeta      = document.getElementById("q-meta");
const qSectionTag = document.getElementById("q-section-tag");
const qWeekTag   = document.getElementById("q-week-tag");
const qTopicTag  = document.getElementById("q-topic-tag");
const optionsGrid = document.getElementById("options-grid");
const feedbackBox = document.getElementById("feedback-box");
const feedbackText = document.getElementById("feedback-text");
const explanationText = document.getElementById("explanation-text");
const btnNext    = document.getElementById("btn-next");
const btnFinish  = document.getElementById("btn-finish");
const qNumberBadge = document.getElementById("q-number-badge");
const timerEl    = document.getElementById("timer");
const progressBar = document.getElementById("progress-bar");
const qCurrent   = document.getElementById("q-current");
const navGrid    = document.getElementById("nav-grid");

// ── Timer ─────────────────────────────────────────────────────────────────────
function initTimer() {
  // Restore from localStorage (survives page refresh)
  let remaining = DURATION;
  const stored = localStorage.getItem(TIMER_KEY);
  if (stored) {
    remaining = parseInt(stored, 10);
    if (isNaN(remaining) || remaining < 0) remaining = DURATION;
  } else {
    localStorage.setItem(TIMER_KEY, DURATION);
  }
  renderTimer(remaining);
  timerInterval = setInterval(() => {
    remaining = Math.max(0, remaining - 1);
    localStorage.setItem(TIMER_KEY, remaining);
    renderTimer(remaining);
    if (remaining === 0) {
      clearInterval(timerInterval);
      alert("Time is up! Redirecting to results.");
      window.location.href = "/result";
    }
  }, 1000);
}

function renderTimer(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  timerEl.textContent =
    String(h).padStart(1, "0") + ":" +
    String(m).padStart(2, "0") + ":" +
    String(s).padStart(2, "0");
  timerEl.className = "font-mono font-bold text-base" +
    (seconds < 300 ? " timer-danger" : seconds < 600 ? " timer-warning" : "");
}

// ── Question Loading ──────────────────────────────────────────────────────────
async function loadQuestion(n) {
  currentIndex = n;
  qText.textContent = "Loading…";
  optionsGrid.innerHTML = "";
  feedbackBox.classList.add("hidden");
  btnNext.classList.add("hidden");
  btnFinish.classList.add("hidden");

  // Update top bar
  qCurrent.textContent = n + 1;
  progressBar.style.width = ((n / TOTAL) * 100) + "%";
  qNumberBadge.textContent = `Question ${n + 1} of ${TOTAL}`;

  // Update nav panel highlight
  document.querySelectorAll(".nav-dot").forEach((dot, i) => {
    dot.classList.remove("current");
    if (i in answered) {
      dot.classList.toggle("answered", answered[i].isCorrect);
      dot.classList.toggle("wrong-ans", !answered[i].isCorrect);
    } else {
      dot.classList.remove("answered", "wrong-ans");
    }
    if (i === n) dot.classList.add("current");
  });

  try {
    const res = await fetch(`/api/question/${n}`);
    if (!res.ok) throw new Error("fetch error");
    const data = await res.json();
    renderQuestion(data);
  } catch (e) {
    qText.textContent = "Error loading question. Please refresh.";
  }
}

const OPTION_LABELS = ["A", "B", "C", "D"];
const SECTION_COLORS = { A: "sec-A", B: "sec-B", C: "sec-C" };

function renderQuestion(data) {
  // Meta tags
  qSectionTag.textContent = "Section " + data.section;
  qSectionTag.className = "badge badge-sm font-bold " + (SECTION_COLORS[data.section] || "");
  qWeekTag.textContent = "Week " + data.week;
  qTopicTag.textContent = data.topic;

  qText.textContent = data.question;

  // Render options
  optionsGrid.innerHTML = "";
  data.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.innerHTML =
      `<span class="option-label">${OPTION_LABELS[i]}</span>` +
      `<span class="option-text">${escapeHtml(opt)}</span>`;

    // If already answered, restore state
    if (currentIndex in answered) {
      btn.disabled = true;
      const ans = answered[currentIndex];
      if (i === ans.correct) btn.classList.add("correct");
      if (i === ans.chosen && !ans.isCorrect) btn.classList.add("wrong");
    } else {
      btn.addEventListener("click", () => submitAnswer(i, data.options));
    }
    optionsGrid.appendChild(btn);
  });

  // Restore feedback if already answered
  if (currentIndex in answered) {
    showFeedback(answered[currentIndex]);
    showNavigationButtons();
  }
}

// ── Answer Submission ─────────────────────────────────────────────────────────
async function submitAnswer(chosen, options) {
  // Disable all buttons immediately
  document.querySelectorAll(".option-btn").forEach(b => { b.disabled = true; });

  try {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ index: currentIndex, chosen: chosen }),
    });
    const data = await res.json();

    const result = {
      chosen: chosen,
      correct: data.correct_index,
      isCorrect: data.is_correct,
      explanation: data.explanation,
    };
    answered[currentIndex] = result;

    // Highlight options
    document.querySelectorAll(".option-btn").forEach((btn, i) => {
      if (i === data.correct_index) btn.classList.add("correct");
      if (i === chosen && !data.is_correct) btn.classList.add("wrong");
    });

    showFeedback(result);
    updateNavDot(currentIndex, result.isCorrect);
    showNavigationButtons();
  } catch (e) {
    console.error("Submit error", e);
  }
}

function showFeedback(result) {
  feedbackBox.classList.remove("hidden");
  if (result.isCorrect) {
    feedbackBox.className = "alert alert-success mt-4";
    feedbackText.textContent = "✓ Correct!";
  } else {
    feedbackBox.className = "alert alert-error mt-4";
    feedbackText.textContent = "✗ Incorrect";
  }
  explanationText.textContent = result.explanation || "";
}

function updateNavDot(i, isCorrect) {
  const dot = document.getElementById(`nav-${i}`);
  if (!dot) return;
  dot.classList.remove("answered", "wrong-ans");
  dot.classList.add(isCorrect ? "answered" : "wrong-ans");
}

function showNavigationButtons() {
  const isLast = currentIndex === TOTAL - 1;
  btnNext.classList.toggle("hidden", isLast);
  btnFinish.classList.toggle("hidden", !isLast);
}

// ── Navigation ────────────────────────────────────────────────────────────────
function nextQuestion() {
  if (currentIndex < TOTAL - 1) {
    loadQuestion(currentIndex + 1);
  }
}

function jumpTo(n) {
  loadQuestion(n);
}

// ── Keyboard shortcuts ────────────────────────────────────────────────────────
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "Enter") {
    if (!btnNext.classList.contains("hidden")) nextQuestion();
  }
  const optMap = { "1": 0, "2": 1, "3": 2, "4": 3, "a": 0, "b": 1, "c": 2, "d": 3 };
  if (e.key in optMap && !(currentIndex in answered)) {
    const buttons = document.querySelectorAll(".option-btn:not(:disabled)");
    const idx = optMap[e.key];
    if (buttons[idx]) buttons[idx].click();
  }
});

// ── Utility ───────────────────────────────────────────────────────────────────
function escapeHtml(text) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

// ── Init ──────────────────────────────────────────────────────────────────────
initTimer();
loadQuestion(0);
