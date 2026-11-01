import csv
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def read(path):
    with (ROOT/path).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
class SelectionTests(unittest.TestCase):
    def test_selection(self):
        rows=read('saksa_epasaannolliset_verbit_ranked.csv')
        self.assertEqual(len(rows),100)
        names={r['infinitive'] for r in rows};self.assertEqual(len(names),100)
        self.assertTrue({'sein','verstehen','bestehen','erhalten','entscheiden','anfangen','anbieten',
                         'essen','trinken','schlafen','vergessen','teilnehmen','waschen','versprechen','beschreiben','verbringen','annehmen',
                         'ankommen','anrufen','aufstehen','einsteigen','aussteigen','umsteigen'}<=names)
        self.assertFalse({'aufnehmen','angreifen','beschließen','besitzen','verbinden','schaffen'} & names)
        self.assertEqual(rows[0]['infinitive'],'sein')
        for suffix in ['praesens','fi_praesens','praeteritum','perfekt','lauseharjoitus_praesens','lauseharjoitus_praeteritum','lauseharjoitus_perfekt']:
            other=read(f'saksa_epasaannolliset_verbit_{suffix}.csv')
            self.assertEqual([(r['rank'],r['source_rank'],r['infinitive'],r['suomi']) for r in rows],[(r['rank'],r['source_rank'],r['infinitive'],r['suomi']) for r in other])
    @unittest.skipUnless((ROOT/'cleanup/reviews/verb_candidate_comparison.csv').exists(), 'Local corpus comparison is not included in public clones')
    def test_local_corpus_comparison(self):
        rows=read('saksa_epasaannolliset_verbit_ranked.csv')
        names={r['infinitive'] for r in rows}
        report=read('cleanup/reviews/verb_candidate_comparison.csv')
        self.assertEqual(len(report),205)
        self.assertEqual({r['infinitive'] for r in report if r['selected']=='True'},names)
        scores={r['infinitive']:int(r['score']) for r in report}
        self.assertEqual([scores[r['infinitive']] for r in rows],sorted([scores[r['infinitive']] for r in rows],reverse=True))
        for row in report:
            total=sum(int(item.rsplit(':',1)[1]) for item in row['counted_forms'].split('; ') if item)
            self.assertEqual(total,int(row['score']))
    def test_new_forms(self):
        for tense,verb,person,expected in [
            ('praesens','sein','ich','bin'),('praesens','verstehen','ihr','versteht'),
            ('praesens','anfangen','du','fängst an'),('praeteritum','verstehen','du','verstandest'),
            ('perfekt','entstehen','er','ist entstanden'),('perfekt','stattfinden','er','hat stattgefunden')]:
            rows={r['infinitive']:r for r in read(f'saksa_epasaannolliset_verbit_{tense}.csv')}
            self.assertEqual(rows[verb][person],expected)
        for tense in ['praesens','praeteritum','perfekt']:
            rows={r['infinitive']:r for r in read(f'saksa_epasaannolliset_verbit_{tense}.csv')}
            for verb in ['entstehen','stattfinden']:
                for person in ['ich','du','wir','ihr']:self.assertEqual(rows[verb][person],'')
if __name__=='__main__':unittest.main()
