const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
for(const dir of ['_book','_book/en']){
 const html=fs.readFileSync(dir+'/teemamuodot.html','utf8');
 const rows=JSON.parse(html.match(/<script type="application\/json" id="verbs-heart-data">(.*?)<\/script>/s)[1]);
 const ctx={};ctx.window=ctx;vm.createContext(ctx);
 vm.runInContext(fs.readFileSync(dir+'/www/drill-common.js','utf8'),ctx);
 Object.assign(ctx.GermanDrill,{registerDrill(){},runOnPage(){}});
 let src=fs.readFileSync('www/drill-heart.js','utf8').replace('  function initDrill(root) {','  globalThis.checkCore = checkAnswer;\n  function initDrill(root) {');
 vm.runInContext(src,ctx);
 for(const row of rows){
  const combos=[row.infinitive,row.praesens,row.praeteritum,row.perfekt].reduce((a,v)=>a.flatMap(prefix=>v.split('|').map(x=>prefix.concat(x))),[[]]);
  for(const answers of combos){assert(ctx.checkCore(row,answers.join(' ')),row.infinitive);assert(ctx.checkCore(row,answers.join('\t')),row.infinitive);}
  assert(!ctx.checkCore(row,'incorrect'));
 }
}
console.log('All 100 principal-part answers and alternatives accepted in both languages, including separable prefixes.');
