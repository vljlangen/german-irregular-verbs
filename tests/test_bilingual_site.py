"""Checks the built Finnish and English sites, not the temporary sources."""
import json
from pathlib import Path
import re
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1] / '_book'
PAGES = ['index', 'verbiluettelo', 'modaaliverbit', 'sein', 'teemamuodot',
         'taivutus-preesens', 'taivutus-imperfekti', 'taivutus-perfekti',
         'lauseet-preesens', 'lauseet-imperfekti', 'lauseet-perfekti',
         'kokonaiset-lauseet-preesens', 'kokonaiset-lauseet-imperfekti', 'kokonaiset-lauseet-perfekti']

def dataset(language, page, identifier):
    directory = ROOT / 'en' if language == 'en' else ROOT
    html = (directory / f'{page}.html').read_text()
    match = re.search(r'<script type="application/json" id="' + identifier + r'">(.*?)</script>', html, re.S)
    return json.loads(match.group(1))

class Visible(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip -= 1
    def handle_data(self, text):
        if not self.skip: self.parts.append(text)

class BilingualTests(unittest.TestCase):
    def test_pages_and_language_links(self):
        for language in ('fi', 'en'):
            directory = ROOT / 'en' if language == 'en' else ROOT
            for page in PAGES:
                html = (directory / f'{page}.html').read_text()
                self.assertIn(f'lang="{language}"', html)
                link = re.search(r'<a class="site-language-link".*?</a>', html).group()
                self.assertIn('Suomenkielinen versio' if language == 'en' else 'English version', link)
                target = '../index.html' if language == 'en' else 'en/index.html'
                self.assertIn(f'href="{target}"', link)
                self.assertTrue((directory / target).exists())
                for href in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', html):
                    if '://' not in href:
                        self.assertTrue((directory / href).exists(), (language, page, href))
                if language == 'en':
                    # The English homepage intentionally includes a Finnish language-switch prompt.
                    language_prompt = re.search(r'<p class="site-language-prompt" lang="fi">.*?</p>', html, re.S)
                    if page == 'index':
                        self.assertIsNotNone(language_prompt)
                        self.assertIn('href="../index.html"', language_prompt.group())
                        self.assertIn('🇫🇮', language_prompt.group())
                    parser = Visible(); parser.feed(re.sub(r'<p class="site-language-prompt" lang="fi">.*?</p>', '', html, flags=re.S))
                    visible = ' '.join(parser.parts).lower().replace('suomenkielinen versio', '')
                    for word in ['kirjoita', 'yleisyysjärjest', 'harjoitukset', 'valitse', 'oikein', 'suomenkielinen']:
                        self.assertNotIn(word, visible, (page, word))

    def test_shared_german_answers(self):
        fi = dataset('fi','teemamuodot','verbs-heart-data')
        en = dataset('en','teemamuodot','verbs-heart-data')
        self.assertEqual(len(fi),100)
        self.assertEqual(len(en),100)
        for a,b in zip(fi,en):
            for key in ['rank','praesens','praeteritum','perfekt']:
                self.assertEqual(a[key],b[key])
            self.assertNotEqual(a['suomi'],b['suomi'])
        fi = dataset('fi','taivutus-preesens','verbs-conj-data')
        en = dataset('en','taivutus-preesens','verbs-conj-data')
        for a,b in zip(fi,en):
            for tense in ['preterite','perfect']:
                self.assertEqual(a[tense],b[tense])
            for person in ['ich','du','er','wir','ihr','sie']:
                self.assertEqual(a['present'][person]['answer'],b['present'][person]['answer'])
                if a['present'][person]['answer']:
                    self.assertNotEqual(a['present'][person]['fi'],b['present'][person]['fi'])
        fi = dataset('fi','lauseet-preesens','sentence-drill-data')
        en = dataset('en','lauseet-preesens','sentence-drill-data')
        self.assertEqual(len(en),300)
        for a,b in zip(fi,en):
            for key in ['rank','tense','person','sentence_de','cloze_de','answer_finite','answer_tail']:
                self.assertEqual(a[key],b[key])
            self.assertNotEqual(a['sentence_fi'],b['sentence_fi'])

if __name__ == '__main__': unittest.main()
