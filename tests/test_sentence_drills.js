const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const siteDir = process.env.SITE_DIR || '_book';
const assetDir = process.env.SITE_DIR ? siteDir + '/www' : 'www';
const fullMode = process.env.SENTENCE_MODE === 'full';
const correctText = process.env.SITE_LANG === 'en' ? 'Correct!' : 'Oikein!';
class Element {
  constructor() { this.children = []; this.events = {}; this.hidden = false; this.value = ''; this.textContent = ''; }
  appendChild(el) { this.children.push(el); }
  replaceChildren() { this.children = []; }
  addEventListener(event, fn) { this.events[event] = fn; }
  setAttribute() {}
  focus() {}
  click() { this.events.click(); }
}
const html = fs.readdirSync(siteDir).filter(n => n.endsWith('.html')).map(n => fs.readFileSync(siteDir + '/' + n, 'utf8')).find(s => s.includes('id="sentence-drill-data"'));
assert(html);
const json = html.match(/<script type="application\/json" id="sentence-drill-data">([\s\S]*?)<\/script>/)[1];
const rows = JSON.parse(json);
assert.equal(rows.length, 300);
let init;
const context = { document: {getElementById: () => ({textContent: json}), createElement: () => new Element(), createTextNode: text => ({textContent: text})} };
vm.createContext(context);
vm.runInContext(fs.readFileSync(assetDir + '/drill-common.js', 'utf8'), context);
context.window = {GermanDrill: {...context.GermanDrill, registerDrill: (selector, fn) => { init = fn; }, runOnPage() {}}};
vm.runInContext(fs.readFileSync(assetDir + '/drill-sentence.js', 'utf8'), context);
for (const tense of ['praesens', 'praeteritum', 'perfekt']) {
  const elements = {};
  const root = {dataset: {tense, mode: fullMode ? 'full' : ''}, querySelector: selector => elements[selector] ||= new Element()};
  init(root);
  assert.equal(elements['.sentence-ranges'].children.length, 10);
  for (let group = 0; group < (fullMode ? 10 : 1); group++) {
  elements['.sentence-ranges'].children[group].click();
  assert(!elements['.sentence-run'].hidden);
  for (let i = 0; i < 10; i++) {
    assert.match(elements['.sentence-feedback'].className, /drill-hidden/);
    const row = rows.find(row => row.tense === tense && row.sentence_fi === elements['.sentence-fi'].textContent && row.rank > group * 10 && row.rank <= (group + 1) * 10);
    assert(row);
    if (fullMode) {
      const hint = elements['.sentence-article-hint'];
      assert.equal(hint.hidden, !row.article_hint);
      assert.equal(hint.textContent, row.article_hint ? '(' + row.article_hint + ')' : '');
      if (process.env.SITE_LANG === 'en') assert(!row.article_hint);
    }
    const inputs = elements['.sentence-cloze'].children.filter(el => el instanceof Element);
    assert.equal(inputs.length, !fullMode && tense === 'perfekt' ? 2 : 1);
    inputs[0].value = fullMode ? '  ' + row.cloze_de.replace('{finite}', row.answer_finite.split('|').at(-1)).replace('{tail}', row.answer_tail.split('|').at(-1)).replace(/\.$/, i % 2 ? '' : '.').replace(/ /g, '  ') + '  ' : row.answer_finite.split('|').at(-1);
    if (inputs[1]) inputs[1].value = row.answer_tail.split('|').at(-1) + (i % 2 === 0 ? '. ' : '');
    if (fullMode) {
      let prevented = false;
      inputs[0].events.keydown({key: 'Enter', preventDefault() { prevented = true; }});
      assert(prevented);
    } else elements['.sentence-submit'].click();
    elements['.sentence-submit'].click(); // Double submission must not count twice.
    assert.equal(elements['.sentence-feedback'].textContent, correctText);
    assert(!elements['.sentence-feedback'].className.includes('drill-hidden'));
    elements['.sentence-next'].click();
  }
  assert(!elements['.sentence-done'].hidden);
  assert.match(elements['.sentence-summary'].children[0].textContent, /10 \/ 10 \(100 %\)/);
  elements['.sentence-restart'].click();
  elements['.sentence-ranges'].children[9].click();
  const inputs = elements['.sentence-cloze'].children.filter(el => el instanceof Element);
  inputs[0].value = 'incorrect';
  elements['.sentence-submit'].click();
  assert(!elements['.sentence-feedback'].children.some(el => el.textContent.includes('Oikea vastaus:')));
  assert.match(elements['.sentence-feedback'].className, /err/);
  if (fullMode) assert(elements['.sentence-feedback'].children.some(el => el instanceof Element));
  else assert.equal(elements['.sentence-feedback'].children.filter(el => el instanceof Element).length, tense === 'perfekt' ? 2 : 1);
  elements['.sentence-stop'].click();
  assert.match(elements['.sentence-summary'].children[0].textContent, /0 \/ 1 \(0 %\)/);
  assert.equal(elements['.sentence-summary'].children.length, 2);
  elements['.sentence-restart'].click();
  elements['.sentence-ranges'].children[0].click();
  elements['.sentence-stop'].click();
  assert.match(elements['.sentence-summary'].children[0].textContent, /0 \/ 0 \(0 %\)/);
  }
}
console.log('Passed all three sentence drills: rendered data, 10 ranges, complete sessions, double submission, wrong feedback, stop, restart and zero-answer summaries.');

if (fullMode) {
  // Exercise all rendered answers, including every verb alternative.
  const source = fs.readFileSync(assetDir + '/drill-sentence.js', 'utf8')
    .replace('  G.registerDrill(', '  window.testFullSentenceCorrect = fullSentenceCorrect; window.testAppendFullCorrection = appendFullCorrection;\n  G.registerDrill(');
  vm.runInContext(source, context);
  for (const row of rows) {
    for (const finite of row.answer_finite.split('|')) {
      for (const tail of row.answer_tail.split('|')) {
        const answer = row.cloze_de.replace('{finite}', finite).replace('{tail}', tail);
        assert(context.window.testFullSentenceCorrect(row, answer));
        assert(context.window.testFullSentenceCorrect(row, answer.replace(/\.$/, '')));
        assert(!context.window.testFullSentenceCorrect(row, ''));
        assert(!context.window.testFullSentenceCorrect(row, finite));
        assert(!context.window.testFullSentenceCorrect(row, answer + ' falsch'));
      }
    }
  }
  console.log('Passed all 300 complete sentences: full answers, alternatives, optional period and rejection of missing/extra words.');
}

if (fullMode) {
  const row = {cloze_de: 'Ich {finite} ein Buch.', answer_finite: 'lese', answer_tail: ''};
  function bold(actual) {
    const feedback = new Element();
    context.window.testAppendFullCorrection(feedback, row, actual);
    assert.equal(feedback.children.map(el => el.textContent).join(''), 'Ich lese ein Buch.');
    return feedback.children.filter(el => el instanceof Element).map(el => el.textContent);
  }
  assert.deepEqual(bold('Ich lese das Heft.'), ['ein', 'Buch.']);
  assert.deepEqual(bold('Ich lese Buch.'), ['ein']);
  assert.deepEqual(bold('Ich liest ein Buch.'), ['lese']);
  assert.deepEqual(bold('Ich lese ein Buch'), []);
  assert.deepEqual(bold('Ich lese jetzt ein Buch.'), ['ein']);
  assert.deepEqual(bold(''), ['Ich', 'lese', 'ein', 'Buch.']);
  console.log('Passed correction highlighting: articles, nouns, verbs, missing/extra words and optional period.');
}
