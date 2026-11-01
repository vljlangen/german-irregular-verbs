#!/usr/bin/env python3
"""Apply the reproducible corpus selection, keeping previous datasets in archive."""
import importlib.util
from pathlib import Path
import shutil
from rank_verb_candidates import ROOT, PEOPLE, read, comparison
import csv

def write(path,fields,rows):
    with (ROOT/path).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

def apply():
    backup=ROOT/'cleanup/archive/before-corpus-selection'
    if not backup.exists():
        backup.mkdir()
        for p in ROOT.glob('saksa_epasaannolliset_verbit*.csv'):shutil.copy2(p,backup/p.name)
    spec=importlib.util.spec_from_file_location('new',ROOT/'data/new_verbs.py');new=importlib.util.module_from_spec(spec);spec.loader.exec_module(new);extra=new.entries()
    chosen,current=comparison()
    sets={t:{} for t in ['ranked','fi_praesens','praesens','praeteritum','perfekt']}
    for folder in ['cleanup/archive/before-100','cleanup/archive/before-corpus-selection']:
        for kind in sets:
            for r in read(folder+'/saksa_epasaannolliset_verbit_'+kind+'.csv'):
                inf=r['infinitive'].split(' (')[0]
                # First semantic variant from the earlier list; current values win.
                if folder.endswith('before-100') and inf in sets[kind]:continue
                sets[kind][inf]=r
    output={kind:[] for kind in sets}
    for rank,candidate in enumerate(chosen,1):
        inf=candidate['infinitive']
        if inf in extra:
            info=extra[inf];pr,pt=candidate['paradigms']
            aux=candidate['perfekt'].split()[0];part=candidate['perfekt'].split()[-1]
            auxiliaries=['bin','bist','ist','sind','seid','sind'] if aux=='ist' else ['habe','hast','hat','haben','habt','haben']
            pf=[a+' '+part for a in auxiliaries]
            restricted=inf in {'entstehen','stattfinden'}
            meta=dict(rank=str(rank),source_rank=info['source_rank'],infinitive=inf,suomi=info['suomi'])
            output['ranked'].append(dict(meta,praesens=candidate['praesens'],praeteritum=candidate['praeteritum'],perfekt=candidate['perfekt']))
            for kind,forms in [('praesens',pr),('praeteritum',pt),('perfekt',pf)]:
                output[kind].append(dict(meta,**{p:f if not restricted or p in {'er','sie'} else '' for p,f in zip(PEOPLE,forms)}))
            fi=dict(meta)
            for p,label,form,hint in zip(PEOPLE,['minä','sinä','hän','me','te','he'],pr,info['fi_forms']):
                active=not restricted or p in {'er','sie'}
                fi[p]=( ('es' if restricted and p=='er' else p)+' '+form) if active else ''
                fi[label]=(('se' if p=='er' else 'ne') if restricted else label)+' '+hint if active else ''
            output['fi_praesens'].append(fi)
        else:
            for kind in sets:
                r=dict(sets[kind][inf]);r['source_rank']=r.get('source_rank',r['rank']);r['rank']=str(rank);r['infinitive']=inf;output[kind].append(r)
    import json
    overrides_path = ROOT / 'data/meaning_overrides.json'
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    for kind,rows in output.items():
        for row in rows:
            if row['infinitive'] in overrides:
                row['suomi'] = overrides[row['infinitive']]
        fields=['rank','source_rank','infinitive']
        if kind=='ranked':fields+=['praesens','praeteritum','perfekt','suomi']
        elif kind=='fi_praesens':fields+=['suomi']+[col for p,fi in zip(PEOPLE,['minä','sinä','hän','me','te','he']) for col in [p,fi]]
        else:fields+=['suomi']+PEOPLE
        write(Path('saksa_epasaannolliset_verbit_'+kind+'.csv'),fields,rows)
    print('Added:',[r['infinitive'] for r in chosen if r['infinitive'] not in current])
    print('Removed:',sorted(set(current)-{r['infinitive'] for r in chosen}))

if __name__=='__main__':apply()
