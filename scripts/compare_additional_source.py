#!/usr/bin/env python3
"""Read-only comparison of the second book with the current selection.
Writes review artifacts under data/, never modifies live exercise CSVs.
"""
import csv,re
from pathlib import Path
from rank_verb_candidates import ROOT,read,lemma,paradigms

def compare():
    old_report={r['infinitive']:r for r in read('cleanup/archive/before-second-source/verb_candidate_comparison.csv')}
    current={r['infinitive']:r for r in read('saksa_epasaannolliset_verbit_ranked.csv')}
    data=read('cleanup/epasaannolliset_verbit_sivut_46-49.csv')
    source={}
    for row in data:
        name=row['Infinitiivi'].replace('/','').removeprefix('sich ').strip()
        if name not in source:source[name]=dict(row)
        # All perfect variants are useful; sum each distinct word once, not per sense.
        source[name].setdefault('perfect_variants',set())
        if row['Perfekti']:source[name]['perfect_variants'].add(row['Perfekti'])
    counts={}
    with (ROOT/'cleanup/deu_news_2025_1M/deu_news_2025_1M-words.txt').open(encoding='utf-8') as f:
        for line in f:
            _,word,n=line.rstrip('\n').split('\t');counts[word]=int(n)
    base_tables={t:{} for t in ['praesens','praeteritum']}
    for t in base_tables:
        for row in read('cleanup/archive/before-100/saksa_epasaannolliset_verbit_'+t+'.csv'):
            base_tables[t].setdefault(lemma(row['infinitive']),[row[p].strip() for p in ['ich','du','er','wir','ihr','sie']])
    for row in read('data/irregular_candidates.tsv','\t'):
        a,b=paradigms(row)
        base_tables['praesens'][row['infinitive']]=a;base_tables['praeteritum'][row['infinitive']]=b
    derived={
      'beschließen':('be','schließen'),'beschreiben':('be','schreiben'),
      'besitzen':('be','sitzen'),'ertragen':('er','tragen'),'gefallen':('ge','fallen'),
      'missverstehen':('miss','verstehen'),'verbinden':('ver','binden'),
      'verbringen':('ver','bringen'),'vergehen':('ver','gehen'),
      'vergleichen':('ver','gleichen'),'versprechen':('ver','sprechen'),
      'bewerben':('be','werben')}
    new=[]
    for inf,row in source.items():
        if inf in old_report:continue
        forms={inf}
        particle=row['Infinitiivi'].split('/')[0] if '/' in row['Infinitiivi'] else ''
        if particle:
            forms.add(particle+'zu'+inf[len(particle):]);method='separable: full prefixed forms only'
        else:
            prefix,base=derived[inf]
            for tense in base_tables:
                for cell in base_tables[tense][base]:
                    for value in cell.split('|'):
                        if value:forms.add(prefix+value)
            method='finite forms + infinitive + participle'
        for value in row['perfect_variants']:forms.add(value.split()[-1])
        if inf=='bewerben':forms.add('beworben')
        score=sum(counts.get(form,0) for form in forms)
        new.append(dict(infinitive=inf,score=score,method=method,source_meaning=row['Merkitys'],
                        counted_forms='; '.join(f'{form}:{counts[form]}' for form in sorted(forms) if counts.get(form))))
    combined={inf:int(r['score']) for inf,r in old_report.items()}
    combined.update({r['infinitive']:r['score'] for r in new})
    ranks={inf:i for i,(inf,score) in enumerate(sorted(combined.items(),key=lambda pair:(-pair[1],pair[0])),1)}
    for r in new:
        r['expanded_candidate_rank']=ranks[r['infinitive']]
        r['higher_than_current_entries']=sum(r['score']>int(old_report[inf]['score']) for inf in current)
        r['conservative_score'] = r['score'] - counts.get('gefallen',0) if r['infinitive']=='gefallen' else r['score']
        r['note']=''
        if r['infinitive']=='gefallen':r['note']='gefallen is also the participle of fallen; score is contaminated'
        elif r['infinitive']=='vergehen':r['note']='vergangen also has adjectival uses'
        elif r['infinitive']=='bewerben':r['note']='includes reflexive job applications and non-reflexive promotion'
    new.sort(key=lambda r:(-r['score'],r['infinitive']))
    fields=['expanded_candidate_rank','infinitive','score','higher_than_current_entries','method','source_meaning','conservative_score','note','counted_forms']
    with (ROOT/'cleanup/reviews/additional_book_comparison.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(new)
    print('Source rows:',len(data),'distinct infinitives:',len(source),'already considered:',len(set(source)&set(old_report)),'new candidates:',len(new),'combined pool:',len(combined))
    print('Currently included:',len(set(source)&set(current)))
    print('NEW CANDIDATES:')
    for r in new:print(r['expanded_candidate_rank'],r['infinitive'],r['score'],r['higher_than_current_entries'],r['note'])
    absent_known=[r for inf,r in old_report.items() if inf in source and inf not in current]
    print('PREVIOUSLY CONSIDERED:',[(r['infinitive'],r['score']) for r in sorted(absent_known,key=lambda r:-int(r['score']))[:12]])
    return new,ranks

if __name__=='__main__':compare()
