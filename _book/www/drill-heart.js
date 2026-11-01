(function () {
  "use strict";

  const G = window.GermanDrill;
  const DRILL_ID = "teemamuodot";
  const DRILL_NAME = "Epäsäännölliset verbit – teemamuotojen harjoittelu";

  function parseAnswer(raw) {
    const t = raw.trim();
    if (!t) return [];
    if (t.includes("\t")) return t.split("\t").map((x) => x.trim()).filter(Boolean);
    const parts = t.split(/\s+/);
    if (parts.length <= 4) return parts;
    const perfekt = parts.slice(-2).join(" ");
    return [parts[0], parts[1], parts[2], perfekt];
  }

  function expectedAnswer(v) {
    return [v.infinitive, v.praesens, v.praeteritum, v.perfekt];
  }

  function checkAnswer(v, raw) {
    const exp = expectedAnswer(v);
    if (raw.includes("\t")) {
      const got = parseAnswer(raw);
      return got.length === 4 && exp.every((e, i) => G.acceptsAnswer(e, got[i]));
    }
    // Whole-form combinations also support separable verbs: fängt an / fing an.
    const candidates = exp.reduce((answers, cell) => {
      return answers.flatMap(prefix => G.answerVariants(cell).map(form => (prefix + " " + form).trim()));
    }, [""]);
    return candidates.some(answer => G.norm(answer) === G.norm(raw));
  }

  function formatExpected(v) {
    return expectedAnswer(v).map(G.displayAnswer).join("\t");
  }

  function loadVerbs() {
    const el = document.getElementById("verbs-heart-data");
    if (!el) return [];
    return JSON.parse(el.textContent);
  }

  function initDrill(root) {
    const verbs = loadVerbs();
    const rangeBar = root.querySelector(".drill-ranges");
    const setupPanel = root.querySelector(".drill-setup");
    const runPanel = root.querySelector(".drill-run");
    const donePanel = root.querySelector(".drill-done");
    const promptEl = root.querySelector(".drill-prompt-text");
    const progressEl = root.querySelector(".drill-progress");
    const inputEl = root.querySelector(".drill-answer");
    const feedbackEl = root.querySelector(".drill-feedback");
    const summaryEl = root.querySelector(".drill-summary-text");

    let state = null;
    let lastLog = null;

    function show(panel) {
      [setupPanel, runPanel, donePanel].forEach((p) => p.classList.remove("active"));
      panel.classList.add("active");
    }

    function verbsInRange(min, max) {
      return verbs
        .filter((v) => v.rank >= min && v.rank <= max)
        .sort((a, b) => a.rank - b.rank);
    }

    function startRange(min, max, label) {
      const queue = verbsInRange(min, max);
      if (!queue.length) {
        alert("Ei verbejä tässä välissä.");
        return;
      }
      state = {
        rangeLabel: label,
        queue: queue.slice(),
        index: 0,
        correct: 0,
        wrong: [],
        startedAt: Date.now(),
      };
      feedbackEl.className = "drill-feedback drill-hidden";
      feedbackEl.textContent = "";
      inputEl.value = "";
      show(runPanel);
      nextQuestion();
    }

    function nextQuestion() {
      if (!state || state.index >= state.queue.length) {
        finishSession(false);
        return;
      }
      const v = state.queue[state.index];
      progressEl.textContent =
        "Sana " + (state.index + 1) + " / " + state.queue.length;
      promptEl.textContent = v.suomi;
      inputEl.value = "";
      inputEl.focus();
    }

    function submitAnswer() {
      if (!state) return;
      const v = state.queue[state.index];
      const ok = checkAnswer(v, inputEl.value);
      if (ok) {
        state.correct += 1;
        feedbackEl.className = "drill-feedback ok";
        feedbackEl.textContent = "Oikein!";
      } else {
        state.wrong.push({
          rank: v.rank,
          label: v.suomi,
          expected: formatExpected(v).replace(/\t/g, " "),
        });
        feedbackEl.className = "drill-feedback err";
        feedbackEl.textContent =
          "Oikea vastaus: " + expectedAnswer(v).map(G.displayAnswer).join("  ·  ");
      }
      state.index += 1;
      if (state.index >= state.queue.length) {
        setTimeout(() => finishSession(false), ok ? 400 : 1200);
      } else {
        setTimeout(nextQuestion, ok ? 400 : 1200);
      }
    }

    function finishSession(stoppedEarly) {
      if (!state) return;
      const durationSec = Math.round((Date.now() - state.startedAt) / 1000);
      const nTotal = stoppedEarly ? state.index : state.queue.length;
      const nCorrect = state.correct;
      const pct = nTotal ? Math.round((100 * nCorrect) / nTotal) : 0;
      const now = new Date();
      const wrongStr = state.wrong
        .map((w) => w.rank + ":" + w.label + " → " + w.expected)
        .join(" | ");

      const entry = {
        date: G.formatLocalDate(now),
        time: G.formatLocalTime(now),
        drill_id: DRILL_ID,
        drill_name: DRILL_NAME,
        rank_range: state.rangeLabel,
        duration_sec: durationSec,
        n_total: nTotal,
        n_correct: nCorrect,
        pct_correct: pct,
        wrong_words: wrongStr,
      };

      lastLog = G.prepareSessionLog(entry, now);
      const logFile = lastLog ? lastLog.filename : null;
      summaryEl.innerHTML = G.finishSummaryHtml({
        stoppedEarly,
        nCorrect,
        nTotal,
        pct,
        logFile,
        wrong: state.wrong,
      });

      show(donePanel);
      state = null;
    }

    G.HEART_RANGES.forEach((r) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = r.label;
      btn.addEventListener("click", () => startRange(r.min, r.max, r.label));
      rangeBar.appendChild(btn);
    });

    root.querySelector(".drill-submit").addEventListener("click", submitAnswer);
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitAnswer();
    });
    root.querySelector(".drill-stop").addEventListener("click", () => {
      if (state) finishSession(true);
    });
    root.querySelector(".drill-restart").addEventListener("click", () => {
      show(setupPanel);
      feedbackEl.className = "drill-feedback drill-hidden";
    });
    G.attachLogDownload(root, () => lastLog);
    show(setupPanel);
  }

  G.registerDrill(".drill-heart", initDrill);
  G.runOnPage(G.bootDrills);
})();
