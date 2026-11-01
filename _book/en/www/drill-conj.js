(function () {
  "use strict";

  const G = window.GermanDrill;
  const SESSION_LENGTH = 30;

  const PERSON_KEYS = ["ich", "du", "er", "wir", "ihr", "sie"];

  const PERSON_DISPLAY = {
    ich: "ich",
    du: "du",
    er: "er",
    wir: "wir",
    ihr: "ihr",
    sie: "Sie",
  };

  /** Present (§2.3): 3. pers. mon. = sie; muissa luvuissa Sie = teitittely */
  function isThirdPersonVerb(verb) {
    return ["gelten", "gelingen", "geschehen", "entstehen", "stattfinden"].includes(verb.infinitive.trim());
  }

  function personDisplay(tense, personKey, verb) {
    if (verb && isThirdPersonVerb(verb)) return personKey === "er" ? "es" : "sie";
    if (personKey === "sie" && tense.key === "present") return "sie";
    return PERSON_DISPLAY[personKey];
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function tenseForm(verb, tenseKey, personKey) {
    const cell = verb[tenseKey][personKey];
    if (tenseKey === "present" && cell && typeof cell === "object" && cell.answer != null) {
      return cell.answer;
    }
    return cell;
  }

  function paradigmTableHtml(verb, tense) {
    const tenseKey = tense.key;
    const persons = PERSON_KEYS.filter(pk => G.answerVariants(tenseForm(verb, tenseKey, pk)).length > 0);
    const headerCells = persons.map(function (pk) {
      return (
        '<th scope="col">' + escapeHtml(personDisplay(tense, pk, verb)) + "</th>"
      );
    }).join("");
    const formCells = persons.map(function (pk) {
      return "<td>" + escapeHtml(G.displayAnswer(tenseForm(verb, tenseKey, pk))) + "</td>";
    }).join("");
    return (
      '<table class="drill-paradigm-table drill-paradigm-table--horizontal">' +
      "<thead><tr>" +
      headerCells +
      "</tr></thead><tbody><tr>" +
      formCells +
      "</tr></tbody></table>"
    );
  }

  function presentForm(verb, personKey) {
    const cell = verb.present[personKey];
    if (cell && typeof cell === "object" && cell.answer != null) return cell.answer;
    return cell;
  }

  function presentFiCue(verb, personKey) {
    const cell = verb.present[personKey];
    if (cell && typeof cell === "object" && cell.fi != null) return cell.fi;
    return verb.suomi;
  }

  const TENSES = {
    present: { key: "present", label: "present", drillId: "taivutus-praesens" },
    preterite: { key: "preterite", label: "simple past", drillId: "taivutus-imperfekti" },
    perfect: { key: "perfect", label: "perfect", drillId: "taivutus-perfekti" },
  };

  function loadVerbs() {
    const el = document.getElementById("verbs-conj-data");
    if (!el) return [];
    return JSON.parse(el.textContent);
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
    }
    return a;
  }

  /** n unique (verb × person) pairs from the range pool (≤10 verbs). */
  function buildQueue(verbs, n, tense) {
    const pairs = [];
    verbs.forEach((verb) => {
      PERSON_KEYS.forEach((personKey) => {
        if (G.answerVariants(tenseForm(verb, tense.key, personKey)).length) {
          pairs.push({ verb: verb, personKey: personKey });
        }
      });
    });
    return shuffle(pairs)
      .slice(0, Math.min(n, pairs.length))
      .map((p) => {
        const forms = p.verb[tense.key];
        const useFiPresent = tense.key === "present" && forms[p.personKey] &&
          typeof forms[p.personKey] === "object" && forms[p.personKey].fi != null;
        return {
          rank: p.verb.rank,
          infinitive: p.verb.infinitive,
          suomi: p.verb.suomi,
          fiCue: isThirdPersonVerb(p.verb) ? thirdPersonCue(p.verb, tense.key, p.personKey) : (useFiPresent ? presentFiCue(p.verb, p.personKey) : p.verb.suomi),
          tenseLabel: tense.label,
          personKey: p.personKey,
          personDisplay: personDisplay(tense, p.personKey, p.verb),
          taskLabel: personDisplay(tense, p.personKey, p.verb),
          verb: p.verb,
          expected: useFiPresent
            ? presentForm(p.verb, p.personKey)
            : forms[p.personKey],
        };
      });
  }

  function thirdPersonCue(verb, tense, person) {
    const cues = {
      entstehen: { present: ["it arises", "they arise"], preterite: ["it arose", "they arose"], perfect: ["it has arisen", "they have arisen"] },
      stattfinden: { present: ["it happens", "they happen"], preterite: ["it happened", "they happened"], perfect: ["it has happened", "they have happened"] },
      gelten: { present: ["it is valid", "they are valid"], preterite: ["it was valid", "they were valid"], perfect: ["it has been valid", "they have been valid"] },
      gelingen: { present: ["it succeeds", "they succeed"], preterite: ["it succeeded", "they succeeded"], perfect: ["it has succeeded", "they have succeeded"] },
      geschehen: { present: ["it happens", "they happen"], preterite: ["it happened", "they happened"], perfect: ["it has happened", "they have happened"] },
    };
    return cues[verb.infinitive.trim()][tense][person === "er" ? 0 : 1];
  }

  function initDrill(root) {
    const tenseKey = root.dataset.tense;
    const tense = TENSES[tenseKey];
    if (!tense) {
      console.error("drill-conj: unknown data-tense", tenseKey);
      return;
    }

    const drillName =
      "Irregular verbs – conjugation (" + tense.label + ")";
    const verbs = loadVerbs();
    const rangeBar = root.querySelector(".drill-ranges");
    const setupPanel = root.querySelector(".drill-setup");
    const runPanel = root.querySelector(".drill-run");
    const donePanel = root.querySelector(".drill-done");
    const lemmaEl = root.querySelector(".drill-conj-lemma");
    const personEl = root.querySelector(".drill-cloze-person");
    const progressEl = root.querySelector(".drill-progress");
    const inputEl = root.querySelector(".drill-answer");
    const feedbackEl = root.querySelector(".drill-feedback");
    const paradigmEl = root.querySelector(".drill-paradigm-sticky");
    const summaryEl = root.querySelector(".drill-summary-text");
    const continuePanel = root.querySelector(".drill-continue-panel");
    const continueBtn = root.querySelector(".drill-continue");
    const submitBtn = root.querySelector(".drill-submit");

    let state = null;
    let lastLog = null;

    function clearParadigm() {
      if (!paradigmEl) return;
      paradigmEl.innerHTML = "";
      paradigmEl.className = "drill-paradigm-sticky drill-hidden";
    }

    function showParadigm(html) {
      if (!paradigmEl) return;
      paradigmEl.innerHTML = html;
      paradigmEl.className = "drill-paradigm-sticky";
    }

    function show(panel) {
      [setupPanel, runPanel, donePanel].forEach((p) => p.classList.remove("active"));
      panel.classList.add("active");
    }

    function verbsInRange(min, max) {
      return verbs.filter((v) => v.rank >= min && v.rank <= max);
    }

    function startRange(min, max, label) {
      const pool = verbsInRange(min, max);
      if (!pool.length) {
        alert("No verbs in this group.");
        return;
      }
      state = {
        rangeLabel: label + " (" + tense.label + ")",
        queue: buildQueue(pool, SESSION_LENGTH, tense),
        index: 0,
        correct: 0,
        wrong: [],
        startedAt: Date.now(),
      };
      feedbackEl.className = "drill-feedback drill-hidden";
      feedbackEl.textContent = "";
      clearParadigm();
      inputEl.value = "";
      show(runPanel);
      nextQuestion();
    }

    function nextQuestion(clearFeedback) {
      if (!state || state.index >= state.queue.length) {
        finishSession(false);
        return;
      }
      state.submitted = false;
      state.awaitingContinue = false;
      continuePanel.classList.add("drill-hidden");
      continueBtn.classList.add("drill-hidden");
      submitBtn.classList.remove("drill-hidden");
      inputEl.disabled = false;
      submitBtn.disabled = false;
      clearParadigm();
      const q = state.queue[state.index];
      progressEl.textContent =
        "Question " + (state.index + 1) + " / " + state.queue.length;
      lemmaEl.textContent = q.fiCue;
      personEl.textContent = q.personDisplay;
      if (clearFeedback) {
        feedbackEl.className = "drill-feedback drill-hidden";
        feedbackEl.textContent = "";
      }
      inputEl.value = "";
      inputEl.focus();
    }

    function submitAnswer() {
      if (!state || state.submitted) return;
      state.submitted = true;
      inputEl.disabled = true;
      submitBtn.disabled = true;
      const q = state.queue[state.index];
      const ok = G.acceptsAnswer(q.expected, inputEl.value);
      if (ok) {
        state.correct += 1;
        clearParadigm();
        feedbackEl.className = "drill-feedback ok";
        feedbackEl.textContent = "Correct!";
      } else {
        state.wrong.push({
          rank: q.rank,
          label: q.fiCue + " · " + q.taskLabel,
          expected: G.displayAnswer(q.expected),
        });
        feedbackEl.className = "drill-feedback err";
        feedbackEl.innerHTML =
          "<p class=\"drill-feedback-msg\">Correct answer: " +
          "<strong>" + escapeHtml(G.displayAnswer(q.expected)) + "</strong>" +
          "</p>";
        if (tense.key === "present") {
          showParadigm(paradigmTableHtml(q.verb, tense));
        }
      }
      state.index += 1;
      state.awaitingContinue = true;
      continuePanel.classList.remove("drill-hidden");
      submitBtn.classList.add("drill-hidden");
      continueBtn.classList.remove("drill-hidden");
      continueBtn.focus();
    }

    function continueAfterFeedback() {
      if (!state || !state.awaitingContinue) return;
      state.awaitingContinue = false;
      continuePanel.classList.add("drill-hidden");
      if (state.index >= state.queue.length) finishSession(false);
      else nextQuestion(true);
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
        drill_id: tense.drillId,
        drill_name: drillName,
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

      clearParadigm();
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

    submitBtn.addEventListener("click", submitAnswer);
    continueBtn.addEventListener("click", continueAfterFeedback);
    continueBtn.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (!e.repeat) continueAfterFeedback();
      }
    });
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (e.repeat) return;
        if (state && state.awaitingContinue) continueAfterFeedback();
        else submitAnswer();
      }
    });
    root.querySelector(".drill-stop").addEventListener("click", () => {
      if (state) finishSession(true);
    });
    root.querySelector(".drill-restart").addEventListener("click", () => {
      show(setupPanel);
      feedbackEl.className = "drill-feedback drill-hidden";
      feedbackEl.textContent = "";
      clearParadigm();
    });
    G.attachLogDownload(root, () => lastLog);
    show(setupPanel);
  }

  G.registerDrill(".drill-conj", initDrill);
  G.runOnPage(G.bootDrills);
})();
