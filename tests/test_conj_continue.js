const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');

const siteDir = process.env.SITE_DIR || '_book';
const assetDir = process.env.SITE_DIR ? siteDir + '/www' : 'www';
const correctText = process.env.SITE_LANG === 'en' ? 'Correct!' : 'Oikein!';
const html = fs.readFileSync(siteDir + '/taivutus-preesens.html','utf8');
const json = html.match(/<script type="application\/json" id="verbs-conj-data">([\s\S]*?)<\/script>/)[1];
class Element {
  constructor() { this.events={};this.children=[];this.value='';this.classes=new Set();this.classList={add:c=>this.classes.add(c),remove:c=>this.classes.delete(c)}; }
  addEventListener(k,fn){this.events[k]=fn;}
  appendChild(el){this.children.push(el);}
  focus(){}
  click(){this.events.click();}
}
for(const correct of [false,true]) for(const tense of ['present','preterite','perfect']) {
 const els={};let init;const timers=[];
 const root={dataset:{tense},querySelector:s=>els[s] ||= new Element()};
 const ctx={document:{getElementById:()=>({textContent:json}),createElement:()=>new Element()},setTimeout:fn=>timers.push(fn)};
 ctx.window=ctx;vm.createContext(ctx);vm.runInContext(fs.readFileSync(assetDir + '/drill-common.js','utf8'),ctx);
 Object.assign(ctx.GermanDrill,{registerDrill:(selector,fn)=>init=fn,runOnPage(){},attachLogDownload(){}});
 vm.runInContext(fs.readFileSync(assetDir + '/drill-conj.js','utf8'),ctx);init(root);
 els['.drill-ranges'].children[0].click();
 for(let i=0;i<30;i++) {
  const before=els['.drill-progress'].textContent;
  const verbs = JSON.parse(json);
  const verb = verbs.find(v => {
    const cell = v[tense][Object.keys(v[tense]).find(pk => {
      const display = pk === 'sie' ? (tense === 'present' ? 'sie' : 'Sie') : pk;
      return display === els['.drill-cloze-person'].textContent;
    })];
    if (!cell) return false;
    const cue = tense === 'present' ? cell.fi : v.suomi;
    return cue === els['.drill-conj-lemma'].textContent;
  });
  if (correct) {
    const pk = Object.keys(verb[tense]).find(pk => (pk === 'sie' ? (tense === 'present' ? 'sie' : 'Sie') : pk) === els['.drill-cloze-person'].textContent);
    const cell = verb[tense][pk];
    els['.drill-answer'].value = (typeof cell === 'object' ? cell.answer : cell).split('|')[0];
  } else els['.drill-answer'].value='incorrect';
  els['.drill-submit'].click();
  assert.equal(timers.length,0,'wrong answer must not schedule advance');
  if (!correct) assert.match(els['.drill-feedback'].innerHTML,/<strong>.+<\/strong>/);
  else assert.equal(els['.drill-feedback'].textContent,correctText);
  assert.equal(els['.drill-progress'].textContent,before);
  assert(!els['.drill-continue-panel'].classes.has('drill-hidden'));
  assert(els['.drill-answer'].disabled);
  assert(els['.drill-submit'].classes.has('drill-hidden'));
  assert(!els['.drill-continue'].classes.has('drill-hidden'));
  els['.drill-submit'].click(); // Cannot count the answer twice.
  if(i%2===0) els['.drill-continue'].events.keydown({key:'Enter',repeat:false,preventDefault(){}});
  else els['.drill-continue'].click();
  if(i<29) {
   assert.match(els['.drill-progress'].textContent,new RegExp(`${i+2} / 30`));
   assert(!els['.drill-answer'].disabled);
   assert(!els['.drill-submit'].classes.has('drill-hidden'));
   assert(els['.drill-continue'].classes.has('drill-hidden'));
  }
 }
 assert(els['.drill-done'].classes.has('active'));
 assert.match(els['.drill-summary-text'].innerHTML,correct ? /30<\/strong> \/ 30/ : /0<\/strong> \/ 30/);
}
console.log('Passed all three tenses: bold answers, no automatic advance after errors, Enter/click continue, duplicate-submit protection and final-question feedback.');
