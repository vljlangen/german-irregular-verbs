#!/usr/bin/env python3
"""Build Finnish at _book/ and English at _book/en/ from shared German data.

Run: python3 scripts/build_site.py
English prompts: translations/en/data.py. Page/UI strings: translations/en/text.py.
The temporary English source is generated under .build/en; do not edit it.
"""
import csv
import importlib.util
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / '.build' / 'en'

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'translations' / 'en' / f'{name}.py')
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f); return reader.fieldnames, list(reader)

def write(path, fields, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n');writer.writeheader();writer.writerows(rows)

def build():
    data, text = module('data'), module('text')
    verbs = [line.split('|') for line in data.VERBS.splitlines()]
    assert len(verbs) == 140
    sentences = data.sentences()
    spec = importlib.util.spec_from_file_location('new_verbs', ROOT / 'data/new_verbs.py')
    additions = importlib.util.module_from_spec(spec); spec.loader.exec_module(additions)
    new_verbs = additions.entries()
    STAGE.mkdir(parents=True, exist_ok=True)
    (STAGE / 'scripts').mkdir(exist_ok=True)
    config = (ROOT / '_bookdown.yml').read_text()
    import re
    files = re.findall(r'^  - "(.*\.Rmd)"$', config, re.M)
    for name in files:
        translated = text.translate((ROOT / name).read_text())
        if name == 'index.Rmd':
            translated = translated.replace('href="en/index.html"', 'href="../index.html"').replace('lang="en" hreflang="en"', 'lang="fi" hreflang="fi"').replace('</i> English version</a>', '</i> Suomenkielinen versio</a>')
            language_prompt = '<p class="site-language-prompt" lang="fi">🇫🇮 Haluatko harjoitella suomeksi? <a href="../index.html" hreflang="fi">Siirry suomenkieliseen versioon.</a></p>'
            translated = translated.replace('```{r homepage-footer,', '<br>\n\n' + language_prompt + '\n\n```{r homepage-footer,', 1)
        (STAGE / name).write_text(translated)
    (STAGE / '_bookdown.yml').write_text(config.replace('Taulukko ', 'Table '))
    shutil.copy2(ROOT / 'scripts' / 'bookdown_helpers.R', STAGE / 'scripts' / 'bookdown_helpers.R')
    shutil.copytree(ROOT / 'www', STAGE / 'www', dirs_exist_ok=True)
    for path in (STAGE / 'www').iterdir():
        if path.suffix in {'.js','.html'}:path.write_text(text.translate(path.read_text()))
    # Translate all live German data copies; the Finnish sources stay untouched.
    live_files = ['ranked', 'fi_praesens', 'praesens', 'praeteritum', 'perfekt',
                  'lauseharjoitus_praesens', 'lauseharjoitus_praeteritum', 'lauseharjoitus_perfekt']
    for suffix in live_files:
        path = ROOT / f'saksa_epasaannolliset_verbit_{suffix}.csv'
        fields, rows = read(path)
        if 'rank' not in fields:continue
        for row in rows:
            rank = int(row.get('source_rank', row['rank']))
            if row['infinitive'] in new_verbs:
                entry = new_verbs[row['infinitive']]
                meaning, base = entry['english'], entry['english_base']
            else: meaning, base = verbs[rank - 1]
            row['suomi'] = meaning
            row['infinitive'] = row['infinitive'].replace('(transitiivinen)', '(transitive)').replace('(intransitiivinen)', '(intransitive)')
            if 'article_hint' in fields:
                row['article_hint'] = ''  # English prompts already express the article.
            if 'sentence_fi' in fields and 'lauseharjoitus_' in path.name:
                row['sentence_fi'] = (new_verbs[row['infinitive']]['example'][4][['praesens','praeteritum','perfekt'].index(row['tense'])]
                                      if row['infinitive'] in new_verbs else sentences[rank][row['tense']])
            if path.name.endswith('_fi_praesens.csv'):
                for de, fi, subject in zip(['ich','du','er','wir','ihr','sie'], ['minä','sinä','hän','me','te','he'], ['I','You','He','We','You','They']):
                    if row[de]:
                        if row['infinitive'] in {'gelten','gelingen','geschehen','entstehen','stattfinden'} and de == 'er':subject = 'It'
                        row[fi] = subject + ' ' + data.present(base,subject)
        write(STAGE / path.name, fields, rows)
    command = ['Rscript','-e','bookdown::render_book("index.Rmd", "bookdown::gitbook")']
    subprocess.run(command, cwd=ROOT, check=True)
    subprocess.run(command, cwd=STAGE, check=True)
    shutil.copytree(STAGE / '_book', ROOT / '_book' / 'en', dirs_exist_ok=True)
    print('Built Finnish: _book/index.html; English: _book/en/index.html')

if __name__ == '__main__':build()
