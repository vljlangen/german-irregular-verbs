# Build and publish

Run from the project root:

```sh
python3 scripts/build_site.py
```

This builds all 14 pages in Finnish at `_book/index.html` and English at
`_book/en/index.html`. Commit `_book/` together with the sources. For Netlify,
use the repository root as the base directory, an empty build command and
`_book` as the publish directory.

## Editable files

- `index.Rmd`, the numbered Rmd pages and `_bookdown.yml`: Finnish pages and navigation.
- `www/`: shared drill engines, widgets and styles.
- `translations/en/`: English prompts and interface text.
- Eight root CSV files: the current 100 verbs, conjugations and sentence exercises.
- `data/new_verbs.py`: additional authored bilingual content.
- `data/meaning_overrides.json`: durable Finnish meaning changes.
- `data/selection_policy.json`: author-selected inclusions and exclusions.
- `data/sentence_article_hints_fi.json`: article hints for complete-sentence exercises.

`rank` is the current exercise order. `source_rank` is a stable translation/template
identifier; do not renumber it when reordering verbs.

## Local cleanup archive

`cleanup/` contains historical sources, corpus files, previous versions, research
comparisons and the copied earlier project. `.gitignore` excludes this directory,
`.build/`, Python caches and local editor/runtime files. `_book/` is intentionally
not ignored. No source PDFs belong in the published `_book/` directory.

The ordinary bilingual build and tests work without `cleanup/`. Historical
selection research and sentence regeneration still require local inputs there:

```sh
python3 scripts/apply_verb_selection.py
python3 scripts/build_sentence_drills.py
python3 scripts/build_site.py
```

The detailed corpus comparison is stored at
`cleanup/reviews/verb_candidate_comparison.csv`. Its test runs when that local
file is available and is skipped in public clones. Only the eight root
practice CSVs are included in the public repository.

Those first two maintenance commands cannot be reproduced from a public clone
without the local archive and corpus. The checked-in CSVs contain all the data
needed to build the current site. `cleanup/MOVED_FILES.json` records the moves.

## Checks

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/test_core_answers.js
node tests/test_heart_boot.js
node tests/test_conj_continue.js
node tests/test_sentence_drills.js
SENTENCE_MODE=full node tests/test_sentence_drills.js
SITE_DIR=_book/en SITE_LANG=en node tests/test_heart_boot.js
SITE_DIR=_book/en SITE_LANG=en node tests/test_conj_continue.js
SITE_DIR=_book/en SITE_LANG=en node tests/test_sentence_drills.js
SITE_DIR=_book/en SITE_LANG=en SENTENCE_MODE=full node tests/test_sentence_drills.js
```
