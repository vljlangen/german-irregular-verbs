#!/usr/bin/env python3
"""Reproducible surface-form frequency estimate; no POS tagging or lemmatisation.

Compare all earlier distinct verbs plus independently researched candidates.
Shared bare stems of separable verbs are excluded to avoid crediting e.g. bieten
occurrences to anbieten. Thus separable-verb counts are conservative lower bounds.
"""
import csv
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PEOPLE = ['ich','du','er','wir','ihr','sie']

def read(path, delimiter=','):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def lemma(value): return re.sub(r' \(.*', '', value)

def paradigms(row):
    spec = importlib.util.spec_from_file_location('conjugation', ROOT/'scripts/generate_conjugation_csvs.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    inf = row['infinitive']
    present = module.conjugate(inf, row['praesens'], 'praesens')
    past = module.conjugate(inf, row['praeteritum'], 'praeteritum')
    # Explicit forms where generic stem heuristics are insufficient.
    fixes = {
      'bergen': (['berge','birgst','birgt','bergen','bergt','bergen'], ['barg','bargst','barg','bargen','bargt','bargen']),
      'sein': (['bin','bist','ist','sind','seid','sind'], ['war','warst','war','waren','wart','waren']),
      'entscheiden': (['entscheide','entscheidest','entscheidet','entscheiden','entscheidet','entscheiden'], ['entschied','entschiedest','entschied','entschieden','entschiedet','entschieden']),
      'geraten': (['gerate','gerätst','gerät','geraten','geratet','geraten'], ['geriet','gerietst','geriet','gerieten','gerietet','gerieten']),
      'empfinden': (['empfinde','empfindest','empfindet','empfinden','empfindet','empfinden'], ['empfand','empfandest','empfand','empfanden','empfandet','empfanden']),
      'scheiden': (['scheide','scheidest','scheidet','scheiden','scheidet','scheiden'], ['schied','schiedest','schied','schieden','schiedet','schieden']),
      'entstehen': (['entstehe','entstehst','entsteht','entstehen','entsteht','entstehen'], ['entstand','entstandest','entstand','entstanden','entstandet','entstanden']),
      'bestehen': (['bestehe','bestehst','besteht','bestehen','besteht','bestehen'], ['bestand','bestandest','bestand','bestanden','bestandet','bestanden']),
      'verstehen': (['verstehe','verstehst','versteht','verstehen','versteht','verstehen'], ['verstand','verstandest','verstand','verstanden','verstandet','verstanden']),
      'erhalten': (['erhalte','erhältst','erhält','erhalten','erhaltet','erhalten'], ['erhielt','erhieltst','erhielt','erhielten','erhieltet','erhielten']),
    }
    if inf in fixes: return fixes[inf]
    compounds = {
      'beschließen': ('be','schließen',False), 'beschreiben': ('be','schreiben',False),
      'besitzen': ('be','sitzen',False), 'ertragen': ('er','tragen',False),
      'gefallen': ('ge','fallen',False), 'missverstehen': ('miss','verstehen',False),
      'verbinden': ('ver','binden',False), 'verbringen': ('ver','bringen',False),
      'vergehen': ('ver','gehen',False), 'vergleichen': ('ver','gleichen',False),
      'versprechen': ('ver','sprechen',False), 'bewerben': ('be','werben',False),
      'abbiegen': ('ab','biegen',True), 'nachdenken': ('nach','denken',True),
      'abfahren': ('ab','fahren',True), 'abfliegen': ('ab','fliegen',True),
      'angreifen': ('an','greifen',True), 'ankommen': ('an','kommen',True),
      'auskommen': ('aus','kommen',True), 'abnehmen': ('ab','nehmen',True),
      'annehmen': ('an','nehmen',True), 'aufnehmen': ('auf','nehmen',True),
      'zunehmen': ('zu','nehmen',True), 'anrufen': ('an','rufen',True),
      'ausschlafen': ('aus','schlafen',True), 'einschlafen': ('ein','schlafen',True),
      'vorschlagen': ('vor','schlagen',True), 'aufschreiben': ('auf','schreiben',True),
      'umschreiben': ('um','schreiben',True), 'ansehen': ('an','sehen',True),
      'fernsehen': ('fern','sehen',True), 'aussprechen': ('aus','sprechen',True),
      'aufstehen': ('auf','stehen',True), 'aussteigen': ('aus','steigen',True),
      'einsteigen': ('ein','steigen',True), 'umsteigen': ('um','steigen',True),
      'beitreten': ('bei','treten',True), 'abwaschen': ('ab','waschen',True),
      'anziehen': ('an','ziehen',True), 'ausziehen': ('aus','ziehen',True),
      'umziehen': ('um','ziehen',True), 'einziehen': ('ein','ziehen',True),
      'bekommen': ('be','kommen',False), 'verlassen': ('ver','lassen',False),
      'erfahren': ('er','fahren',False), 'empfangen': ('emp','fangen',False),
      'anbieten': ('an','bieten',True), 'anfangen': ('an','fangen',True),
      'teilnehmen': ('teil','nehmen',True), 'stattfinden': ('statt','finden',True),
      'aussehen': ('aus','sehen',True), 'unternehmen': ('unter','nehmen',False),
    }
    if inf in compounds:
        prefix,base,separable=compounds[inf]
        result=[]
        for tense in ['praesens','praeteritum']:
            rows=read('cleanup/archive/before-100/saksa_epasaannolliset_verbit_'+tense+'.csv')
            source=next((r for r in rows if lemma(r['infinitive'])==base),None)
            if source:
                forms=[source[p].strip() for p in PEOPLE]
            else:
                candidates=read('data/irregular_candidates.tsv','\t')
                base_row=next(r for r in candidates if r['infinitive']==base)
                forms=paradigms(base_row)[0 if tense=='praesens' else 1]
            result.append([form+' '+prefix if separable else prefix+form for form in forms])
        return result
    return present, past

def comparison():
    base = {}
    archive = 'cleanup/archive/before-100/'
    oldtables = {t:{r['rank']:r for r in read(archive+f'saksa_epasaannolliset_verbit_{t}.csv')} for t in ['praesens','praeteritum']}
    for row in read(archive+'saksa_epasaannolliset_verbit_ranked.csv'):
        inf = lemma(row['infinitive'])
        if inf not in base:
            copy = dict(row, infinitive=inf)
            copy['paradigms'] = [[oldtables[t][row['rank']][p].strip() for p in PEOPLE] for t in ['praesens','praeteritum']]
            base[inf] = copy
    # Preserve the latest meanings and forms for current verbs.
    current = {r['infinitive']:r for r in read('cleanup/archive/before-corpus-selection/saksa_epasaannolliset_verbit_ranked.csv')}
    for inf,row in current.items(): base[inf].update(row)
    extra = read('data/irregular_candidates.tsv', '\t')
    for row in extra:
        base[row['infinitive']] = dict(row, paradigms=paradigms(row))
    counts = {}
    with (ROOT/'cleanup/deu_news_2025_1M/deu_news_2025_1M-words.txt').open(encoding='utf-8') as f:
        for line in f:
            _,word,count = line.rstrip('\n').split('\t');counts[word] = int(count)
    for inf,row in base.items():
        forms = {inf}
        for paradigm in row['paradigms']:
            for cell in paradigm:
                for form in cell.split('|'):
                    # Pronoun-free, unambiguous complete tokens only.
                    if form and ' ' not in form: forms.add(form)
        for variant in row['perfekt'].split('|'): forms.add(variant.split()[-1])
        if ' ' in row['praesens']:
            particle = row['praesens'].split()[-1]
            forms.add(particle+'zu'+inf[len(particle):])
            row['method'] = 'separable: full prefixed forms only'
        else: row['method'] = 'finite forms + infinitive + participle'
        if inf == 'gefallen': forms.discard('gefallen') # Also the participle of fallen.
        if inf == 'sein': forms.discard('sein') # Also a very common possessive determiner.
        forms.discard('')
        row['score'] = sum(counts.get(f,0) for f in forms)
        row['counted_forms'] = '; '.join(f'{f}:{counts.get(f,0)}' for f in sorted(forms) if counts.get(f,0))
    ordered = sorted(base.values(),key=lambda r:(-r['score'],r['infinitive']))
    required = {r['infinitive'] for r in extra if r['group'] in {'required','additional_corpus','pedagogical'}}
    import json
    policy = json.loads((ROOT / 'data/selection_policy.json').read_text())
    excluded = set(policy['exclude'])
    required = (required | set(policy['include'])) - excluded
    eligible = [r for r in ordered if r['infinitive'] not in excluded]
    chosen = [r for r in eligible if r['infinitive'] in required]
    chosen += [r for r in eligible if r['infinitive'] not in required][:100-len(chosen)]
    chosen.sort(key=lambda r:(-r['score'],r['infinitive']))
    selected = {r['infinitive'] for r in chosen}
    fields = ['candidate_rank','infinitive','score','selected','required','previously_selected','method','counted_forms']
    with (ROOT/'cleanup/reviews/verb_candidate_comparison.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for i,r in enumerate(ordered,1):
            w.writerow(dict(candidate_rank=i,infinitive=r['infinitive'],score=r['score'],selected=r['infinitive'] in selected,required=r['infinitive'] in required,previously_selected=r['infinitive'] in current,method=r['method'],counted_forms=r['counted_forms']))
    return chosen, current

if __name__=='__main__':
    chosen,current=comparison()
    print('Candidates:',len(read('cleanup/reviews/verb_candidate_comparison.csv')))
    print('Added:',[(r['infinitive'],r['score']) for r in chosen if r['infinitive'] not in current])
    print('Removed:',sorted(set(current)-{r['infinitive'] for r in chosen}))
