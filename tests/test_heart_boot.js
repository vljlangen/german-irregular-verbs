const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const siteDir = process.env.SITE_DIR || '_book';
const assetDir = process.env.SITE_DIR ? siteDir + '/www' : 'www';
const correctText = process.env.SITE_LANG === 'en' ? 'Correct!' : 'Oikein!';
const html = fs.readFileSync(siteDir + '/teemamuodot.html', 'utf8');
const json = html.match(/<script type="application\/json" id="verbs-heart-data">([\s\S]*?)<\/script>/)[1];
class Element {
  constructor() { this.events = {}; this.children = []; this.attrs = {}; this.classList = {remove() {}, add() {}}; }
  querySelector(selector) { return this.childrenBySelector[selector]; }
  querySelectorAll() { return []; }
  getAttribute(k) { return this.attrs[k]; }
  setAttribute(k,v) { this.attrs[k] = v; }
  addEventListener(k,fn) { this.events[k] = fn; }
  appendChild(el) { this.children.push(el); }
  focus() {}
}
for (const readyState of ['loading','complete']) {
  const root = new Element(); root.childrenBySelector = {};
  for (const selector of ['.drill-ranges','.drill-setup','.drill-run','.drill-done','.drill-prompt-text','.drill-progress','.drill-answer','.drill-feedback','.drill-summary-text','.drill-submit','.drill-stop','.drill-restart']) root.childrenBySelector[selector] = new Element();
  const events = {}, nav = {};
  const ctx = {document: {readyState, getElementById: () => ({textContent: json}), querySelectorAll: selector => selector === '.drill-heart' ? [root] : [], createElement: () => new Element(), addEventListener: (k,fn) => { events[k] = fn; }}, gitbook: {events: {bind: (k,fn) => {nav[k] = fn;}}}, setTimeout: fn => fn()};
  ctx.window = ctx;
  vm.createContext(ctx);
  for (const file of [assetDir + '/drill-common.js', assetDir + '/drill-heart.js']) vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
  if (readyState === 'loading') events.DOMContentLoaded();
  const ranges = root.querySelector('.drill-ranges');
  assert.equal(ranges.children.length,10);
  nav['page.change']();
  assert.equal(ranges.children.length,10); // Navigation must not duplicate controls.
  ranges.children[0].events.click();
  assert(root.querySelector('.drill-prompt-text').textContent);
  assert.match(root.querySelector('.drill-progress').textContent,/1 \/ 10/);
}
console.log('Passed standalone core drill boot: DOM loading, direct load, GitBook navigation and range start.');
