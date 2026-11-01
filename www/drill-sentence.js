(function () {
  'use strict';
  const G = window.GermanDrill;
  const LABELS = {praesens: 'preesens', praeteritum: 'imperfekti', perfekt: 'perfekti'};
  function shuffle(rows) {
    const result = rows.slice();
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
  function isCorrect(row, finite, tail) {
    return G.acceptsAnswer(row.answer_finite, finite) &&
      (!row.answer_tail || G.acceptsAnswer(row.answer_tail, String(tail).trim().replace(/\.$/, '')));
  }
  function fullSentenceCorrect(row, value) {
    const normalize = text => String(text).normalize('NFC').trim().replace(/\s*\.\s*$/, '').replace(/\s+/g, ' ');
    // Expand the same accepted verb alternatives as the cloze exercise.
    return G.answerVariants(row.answer_finite).some(finite =>
      (row.answer_tail ? G.answerVariants(row.answer_tail) : ['']).some(tail =>
        G.acceptsAnswer(normalize(row.cloze_de.replace('{finite}', finite).replace('{tail}', tail)), normalize(value))));
  }
  function sentenceDiff(expected, actual) {
    const words = text => String(text).normalize('NFC').trim().replace(/\s*\.\s*$/, '').split(/\s+/).filter(Boolean);
    const a = words(expected), b = words(actual);
    const same = (x, y) => x.toLowerCase() === y.toLowerCase();
    const cost = Array.from({length: a.length + 1}, () => Array(b.length + 1).fill(0));
    for (let i = 0; i <= a.length; i++) cost[i][0] = i;
    for (let j = 0; j <= b.length; j++) cost[0][j] = j;
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        cost[i][j] = Math.min(cost[i - 1][j - 1] + (same(a[i - 1], b[j - 1]) ? 0 : 1),
          cost[i - 1][j] + 1, cost[i][j - 1] + 1);
      }
    }
    const changed = new Set(), extras = [];
    let i = a.length, j = b.length;
    while (i || j) {
      if (i && j && cost[i][j] === cost[i - 1][j - 1] + (same(a[i - 1], b[j - 1]) ? 0 : 1)) {
        if (!same(a[i - 1], b[j - 1])) changed.add(i - 1);
        i--; j--;
      } else if (i && cost[i][j] === cost[i - 1][j] + 1) {
        changed.add(--i);
      } else {
        extras.push(Math.min(i, a.length - 1)); j--;
      }
    }
    // An extra submitted word has no counterpart in the solution: mark its position.
    extras.forEach(index => { if (index >= 0) changed.add(index); });
    return {expected, changed, cost: cost[a.length][b.length]};
  }
  function appendFullCorrection(feedback, row, actual) {
    let best = null;
    G.answerVariants(row.answer_finite).forEach(finite => {
      (row.answer_tail ? G.answerVariants(row.answer_tail) : ['']).forEach(tail => {
        const expected = row.cloze_de.replace('{finite}', finite).replace('{tail}', tail);
        const diff = sentenceDiff(expected, actual);
        if (!best || diff.cost < best.cost) best = diff;
      });
    });
    let index = 0;
    best.expected.split(/(\s+)/).forEach(token => {
      if (!token) return;
      if (/^\s+$/.test(token)) feedback.appendChild(document.createTextNode(token));
      else {
        if (best.changed.has(index)) {
          const strong = document.createElement('strong');
          strong.textContent = token;
          feedback.appendChild(strong);
        } else feedback.appendChild(document.createTextNode(token));
        index++;
      }
    });
  }
  function init(root) {
    const data = document.getElementById('sentence-drill-data');
    if (!data) return;
    const tense = root.dataset.tense;
    const fullSentence = root.dataset.mode === 'full';
    const rows = JSON.parse(data.textContent).filter(row => row.tense === tense);
    const setup = root.querySelector('.sentence-setup');
    const run = root.querySelector('.sentence-run');
    const done = root.querySelector('.sentence-done');
    const prompt = root.querySelector('.sentence-fi');
    const sentence = root.querySelector('.sentence-cloze');
    const progress = root.querySelector('.sentence-progress');
    const feedback = root.querySelector('.sentence-feedback');
    const submit = root.querySelector('.sentence-submit');
    const next = root.querySelector('.sentence-next');
    const summary = root.querySelector('.sentence-summary');
    let state = null;
    let inputs = {};
    function show(panel) {
      [setup, run, done].forEach(el => { el.hidden = el !== panel; });
    }
    function question() {
      const row = state.queue[state.index];
      progress.textContent = `Lause ${state.index + 1} / ${state.queue.length} · ${LABELS[tense]}`;
      prompt.textContent = row.sentence_fi;
      if (fullSentence) {
        const hint = root.querySelector('.sentence-article-hint');
        hint.textContent = row.article_hint ? '(' + row.article_hint + ')' : '';
        hint.hidden = !row.article_hint;
      }
      sentence.replaceChildren();
      inputs = {};
      if (fullSentence) {
        const input = document.createElement('input');
        input.type = 'text'; input.autocomplete = 'off'; input.spellcheck = false;
        input.className = 'sentence-input sentence-full-input';
        input.setAttribute('aria-label', 'Koko saksankielinen lause');
        input.addEventListener('keydown', event => {
          if (event.key === 'Enter') { event.preventDefault(); check(); }
        });
        inputs.finite = input;
        sentence.appendChild(input);
      } else row.cloze_de.split(/(\{finite\}|\{tail\})/).forEach(part => {
        if (part === '{finite}' || part === '{tail}') {
          const key = part.slice(1, -1);
          const input = document.createElement('input');
          input.type = 'text'; input.autocomplete = 'off'; input.spellcheck = false;
          input.className = 'sentence-input';
          input.setAttribute('aria-label', key === 'finite' ? 'Persoonassa taipuva verbi tai apuverbi' : 'Lauseen loppuun tuleva verbiosa');
          input.addEventListener('keydown', event => {
            if (event.key === 'Enter') {
              event.preventDefault();
              if (key === 'finite' && inputs.tail) inputs.tail.focus();
              else check();
            }
          });
          inputs[key] = input; sentence.appendChild(input);
        } else sentence.appendChild(document.createTextNode(part));
      });
      feedback.textContent = '';
      feedback.className = 'sentence-feedback drill-feedback drill-hidden';
      submit.hidden = false; next.hidden = true;
      inputs.finite.focus();
    }
    function finish() {
      if (!state) return;
      summary.replaceChildren();
      const result = document.createElement('p');
      const count = state.index;
      result.textContent = `Oikein: ${state.correct} / ${count} (${count ? Math.round(100 * state.correct / count) : 0} %)`;
      summary.appendChild(result);
      state.wrong.forEach(row => {
        const item = document.createElement('p');
        item.textContent = row.sentence_fi + ' → ' + row.cloze_de
          .replace('{finite}', G.displayAnswer(row.answer_finite))
          .replace('{tail}', G.displayAnswer(row.answer_tail));
        summary.appendChild(item);
      });
      state = null; show(done);
    }
    function check() {
      if (!state || state.checked) return;
      const row = state.queue[state.index];
      const ok = fullSentence ? fullSentenceCorrect(row, inputs.finite.value) :
        isCorrect(row, inputs.finite.value, inputs.tail ? inputs.tail.value : '');
      if (ok) state.correct++;
      else state.wrong.push(row);
      feedback.replaceChildren();
      if (ok) feedback.textContent = 'Oikein!';
      else if (fullSentence) appendFullCorrection(feedback, row, inputs.finite.value);
      else {
        row.cloze_de.split(/(\{finite\}|\{tail\})/).forEach(part => {
          if (part === '{finite}' || part === '{tail}') {
            const answer = document.createElement('strong');
            answer.textContent = G.displayAnswer(part === '{finite}' ? row.answer_finite : row.answer_tail);
            feedback.appendChild(answer);
          } else feedback.appendChild(document.createTextNode(part));
        });
      }
      feedback.className = 'sentence-feedback drill-feedback ' + (ok ? 'ok' : 'err');
      Object.values(inputs).forEach(input => { input.disabled = true; });
      state.checked = true; state.index++;
      submit.hidden = true; next.hidden = false;
      next.textContent = state.index === state.queue.length ? 'Näytä tulos' : 'Seuraava lause';
      next.focus();
    }
    G.HEART_RANGES.forEach(range => {
      const button = document.createElement('button');
      button.type = 'button'; button.textContent = range.label;
      button.addEventListener('click', () => {
        const pool = rows.filter(row => row.rank >= range.min && row.rank <= range.max);
        if (!pool.length) return;
        state = {queue: shuffle(pool), index: 0, correct: 0, wrong: [], checked: false};
        show(run); question();
      });
      root.querySelector('.sentence-ranges').appendChild(button);
    });
    submit.addEventListener('click', check);
    next.addEventListener('click', () => {
      if (!state) return;
      if (state.index >= state.queue.length) finish();
      else { state.checked = false; question(); }
    });
    root.querySelector('.sentence-stop').addEventListener('click', finish);
    root.querySelector('.sentence-restart').addEventListener('click', () => show(setup));
    show(setup);
  }
  G.registerDrill('.drill-sentence', init);
  G.runOnPage(G.bootDrills);
})();
