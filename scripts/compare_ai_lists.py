#!/usr/bin/env python3
"""Compare the two user-supplied AI drafts without changing the active selection."""
import csv,re
from collections import Counter
from pathlib import Path
from rank_verb_candidates import ROOT,read,PEOPLE

REGULAR={'hören','leben','passieren','gehören','aufwachen'}

def compare():
    a=[];b=[]
    for line in (ROOT/'cleanup/100 essential German irregular verbs_AI1.md').read_text().splitlines():
        if re.match(r'^\d+\t',line):a.append(line.split('\t')[1])
    for row in csv.reader((ROOT/'cleanup/irregular_verbs_AI2.md').read_text().splitlines()):
        if len(row)>1 and row[0].isdigit():b.append(row[1])
    corrected_b=[v.replace('ratan','raten') for v in b]
    sa=set(a)-REGULAR;sb=set(corrected_b)
    current={r['infinitive']:r for r in read('saksa_epasaannolliset_verbit_ranked.csv')}
    known={r['infinitive']:r for r in read('cleanup/reviews/verb_candidate_comparison.csv')}
    counts={}
    with (ROOT/'cleanup/deu_news_2025_1M/deu_news_2025_1M-words.txt').open() as f:
        for line in f:
            _,w,n=line.rstrip('\n').split('\t');counts[w]=int(n)
    bases={t:{} for t in ['praesens','praeteritum']}
    for t in bases:
        for row in read('cleanup/archive/before-100/saksa_epasaannolliset_verbit_'+t+'.csv'):
            bases[t].setdefault(row['infinitive'].split(' (')[0],[row[p] for p in PEOPLE])
    new={
      'beweisen':('be','weisen',False,'bewiesen'),
      'ausgehen':('aus','gehen',True,'ausgegangen'),
      'mitbringen':('mit','bringen',True,'mitgebracht'),
      'mitnehmen':('mit','nehmen',True,'mitgenommen'),
      'zurückkommen':('zurück','kommen',True,'zurückgekommen'),
      'zurückgeben':('zurück','geben',True,'zurückgegeben'),
      'aufgeben':('auf','geben',True,'aufgegeben'),
      'vorlesen':('vor','lesen',True,'vorgelesen'),
      'unterschreiben':('unter','schreiben',False,'unterschrieben')}
    extra_scores={}
    for inf,(prefix,stem,separable,part) in new.items():
        forms={inf,part}
        if separable:forms.add(prefix+'zu'+stem)
        else:
            for t in bases:
                for cell in bases[t][stem]:
                    for value in cell.split('|'):
                        if value:forms.add(prefix+value)
        extra_scores[inf]=sum(counts.get(w,0) for w in forms)
    rows=[]
    for inf in sorted(sa|sb|set(current)):
        rows.append(dict(infinitive=inf,AI1=inf in sa,AI2=inf in sb,current=inf in current,
                         score=int(known[inf]['score']) if inf in known else extra_scores.get(inf,''),
                         score_method='existing candidate comparison' if inf in known else 'new surface estimate'))
    with (ROOT/'cleanup/reviews/AI_LIST_COMPARISON.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('AI1:',len(a),'rows,',len(set(a)),'distinct, duplicates:',[v for v,n in Counter(a).items() if n>1])
    print('AI2:',len(b),'rows,',len(set(b)),'distinct, duplicates:',[v for v,n in Counter(b).items() if n>1])
    print('Valid distinct counts:',len(sa),len(sb),'shared:',len(sa&sb),'shared current:',len(sa&sb&set(current)))
    print('Missing in both AI lists:',sorted(sa&sb-set(current)))
    print('New beyond existing comparison:',extra_scores)
    print('Shared but missing scores:',[(inf,known[inf]['score']) for inf in sorted(sa&sb-set(current))])
    return rows
if __name__=='__main__':compare()
