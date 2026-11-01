import csv
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SentenceDataTests(unittest.TestCase):
    def test_all_sets(self):
        for tense in ('praesens', 'praeteritum', 'perfekt'):
            with (ROOT / f'saksa_epasaannolliset_verbit_lauseharjoitus_{tense}.csv').open(encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual([int(r['rank']) for r in rows], list(range(1, 101)))
            for row in rows:
                self.assertTrue(row['sentence_fi'])
                self.assertTrue(row['answer_finite'])
                self.assertEqual(row['cloze_de'].count('{finite}'), 1)
                self.assertEqual(row['cloze_de'].count('{tail}'), int(tense == 'perfekt'))
                self.assertEqual(row['sentence_de'], row['cloze_de'].replace('{finite}', row['answer_finite'].split('|')[0]).replace('{tail}', row['answer_tail'].split('|')[0]))
            by_rank = {int(r['source_rank']): r for r in rows}
            self.assertEqual(len({r['infinitive'] for r in rows}), 100)
            if tense == 'perfekt':
                self.assertEqual(by_rank[3]['sentence_de'], 'Ich habe schwimmen können.')
                self.assertEqual(by_rank[15]['answer_finite'], 'hat')
                self.assertEqual(by_rank[28]['answer_finite'], 'habe')
                self.assertEqual(by_rank[7]['answer_finite'], 'bin')

            if tense == 'praeteritum':
                self.assertEqual(by_rank[116]['answer_finite'], 'wusch')

if __name__ == '__main__':
    unittest.main()
