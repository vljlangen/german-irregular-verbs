(function (global) {
  "use strict";

  const ENABLE_LOG_DOWNLOAD = false;

  // Ten groups of ten verbs in the current 100-verb selection.
  const HEART_RANGES = Array.from({ length: 10 }, (_, i) => {
    const min = i * 10 + 1;
    const max = min + 9;
    return { label: min + "–" + max, min, max };
  });
  const RANGES = HEART_RANGES;

  const LOG_HEADERS = [
    "date",
    "time",
    "drill_id",
    "drill_name",
    "rank_range",
    "duration_sec",
    "n_total",
    "n_correct",
    "pct_correct",
    "wrong_words",
  ];

  function norm(s) {
    return String(s || "")
      .trim()
      .replace(/\s+/g, " ")
      .toLowerCase();
  }

  // A pipe separates complete accepted answers inside one CSV cell.
  function answerVariants(value) {
    return String(value == null ? "" : value).split("|").map(s => s.trim()).filter(Boolean);
  }

  function acceptsAnswer(expected, actual) {
    return answerVariants(expected).some(variant => norm(variant) === norm(actual));
  }

  function displayAnswer(value) {
    return answerVariants(value).join(" / ");
  }

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function formatLocalDate(now) {
    return now.getFullYear() + "-" + pad2(now.getMonth() + 1) + "-" + pad2(now.getDate());
  }

  function formatLocalTime(now) {
    return pad2(now.getHours()) + ":" + pad2(now.getMinutes()) + ":" + pad2(now.getSeconds());
  }

  function sessionLogFilename(now) {
    return (
      "practice_log_" +
      formatLocalDate(now) +
      "_" +
      pad2(now.getHours()) +
      "-" +
      pad2(now.getMinutes()) +
      "-" +
      pad2(now.getSeconds()) +
      ".csv"
    );
  }

  function csvEscape(val) {
    const s = String(val == null ? "" : val);
    if (/[",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
    return s;
  }

  function rowToCsv(row, headers) {
    return headers.map((h) => csvEscape(row[h])).join(",");
  }

  function downloadCsv(filename, content) {
    const blob = new Blob(["\uFEFF" + content], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function downloadLogEntry(entry, filename) {
    if (!ENABLE_LOG_DOWNLOAD) return;
    const lines = [LOG_HEADERS.join(","), rowToCsv(entry, LOG_HEADERS)];
    downloadCsv(filename, lines.join("\n"));
    return filename;
  }

  function prepareSessionLog(entry, now) {
    if (!ENABLE_LOG_DOWNLOAD) return null;
    return { entry: entry, filename: sessionLogFilename(now) };
  }

  function attachLogDownload(root, getLastLog) {
    root.querySelectorAll(".drill-download-log, .drill-log-note").forEach(el => {
      el.hidden = !ENABLE_LOG_DOWNLOAD;
    });
    if (!ENABLE_LOG_DOWNLOAD) return;
    const btn = root.querySelector(".drill-download-log");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const saved = getLastLog();
      if (saved) downloadLogEntry(saved.entry, saved.filename);
    });
  }

  function finishSummaryHtml(opts) {
    const stopNote = opts.stoppedEarly ? " (keskeytetty)" : "";
    let html =
      "<p><strong>Valmis</strong>" +
      stopNote +
      "</p>" +
      "<p>Oikein: <strong>" +
      opts.nCorrect +
      "</strong> / " +
      opts.nTotal +
      " (" +
      opts.pct +
      " %)</p>";
    if (ENABLE_LOG_DOWNLOAD && opts.logFile) html +=
      '<p class="drill-log-saved"><small>Lataa loki painikkeesta (<code>' +
      opts.logFile +
      "</code>)</small></p>";
    if (opts.wrong.length) {
      html +=
        "<p>Väärät: " +
        opts.wrong
          .map(
            (w) =>
              "<br/><small>sija " +
              w.rank +
              " · " +
              w.label +
              " → " +
              w.expected +
              "</small>"
          )
          .join("") +
        "</p>";
    }
    return html;
  }

  const boots = [];

  function bootDrills() {
    boots.forEach((entry) => {
      document.querySelectorAll(entry.selector).forEach((root) => {
        if (root.getAttribute("data-drill-ready") === "1") return;
        root.setAttribute("data-drill-ready", "1");
        entry.init(root);
      });
    });
  }

  function runOnPage(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
    (function waitGitbook() {
      if (typeof gitbook !== "undefined" && gitbook.events && gitbook.events.bind) {
        gitbook.events.bind("page.change", fn);
        return;
      }
      setTimeout(waitGitbook, 50);
    })();
  }

  function registerDrill(selector, init) {
    boots.push({ selector: selector, init: init });
  }

  global.GermanDrill = {
    ENABLE_LOG_DOWNLOAD,
    RANGES,
    HEART_RANGES,
    norm,
    answerVariants,
    acceptsAnswer,
    displayAnswer,
    formatLocalDate,
    formatLocalTime,
    prepareSessionLog,
    downloadLogEntry,
    attachLogDownload,
    finishSummaryHtml,
    registerDrill: registerDrill,
    bootDrills: bootDrills,
    runOnPage: runOnPage,
  };

})(typeof window !== "undefined" ? window : globalThis);
