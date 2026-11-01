#!/usr/bin/env python3
"""Build three curated sentence cloze sets from the active verb selection. Original 840 examples stay intact.

Finnish past translations below are authored explicitly, not mechanically inflected.
German finite forms come from the maintained paradigm CSVs. Each blank represents
one verb slot; a slot can contain several words (modal perfect double infinitive).
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

# One Finnish imperfekti / perfekti pair for each rank, in unchanged rank order.
PAST_FI = '''Minusta tuli väsynyt.|Minusta on tullut väsynyt.
Minulla oli aikaa.|Minulla on ollut aikaa.
Kykenin uimaan.|Olen kyennyt uimaan.
Annoin sinulle vettä.|Olen antanut sinulle vettä.
Minun piti opiskella.|Minun on pitänyt opiskella.
Minun täytyi työskennellä.|Minun on täytynyt työskennellä.
Tulin ajoissa.|Olen tullut ajoissa.
Menin kotiin.|Olen mennyt kotiin.
Halusin nukkua.|Olen halunnut nukkua.
Seisoin täällä.|Olen seissyt täällä.
Näin auton.|Olen nähnyt auton.
Jäin kotiin.|Olen jäänyt kotiin.
Jätin ikkunan auki.|Olen jättänyt ikkunan auki.
Löysin avaimen.|Olen löytänyt avaimen.
Kirja oli täällä.|Kirja on ollut täällä.
Toin leipää.|Olen tuonut leipää.
Otin bussin.|Olen ottanut bussin.
Puhuin saksaa.|Olen puhunut saksaa.
Tapasin ystäväni.|Olen tavannut ystäväni.
Pidin ovea.|Olen pitänyt ovea.
Nimeni oli Anna.|Nimeni on ollut Anna.
Lippu oli voimassa.|Lippu on ollut voimassa.
Tein paljon.|Olen tehnyt paljon.
Tiesin sen.|Olen tiennyt sen.
Sain mennä.|Olen saanut mennä.
Tarjosimme apua.|Olemme tarjonneet apua.
Kirjoitin sähköpostin.|Olen kirjoittanut sähköpostin.
Vedin pöytää.|Olen vetänyt pöytää.
Muutin Berliiniin.|Olen muuttanut Berliiniin.
Juoksin puistossa.|Olen juossut puistossa.
Matkustin Turkuun.|Olen matkustanut Turkuun.
Ajoin autoa.|Olen ajanut autoa.
Lasi putosi maahan.|Lasi on pudonnut maahan.
Aloitin työn.|Olen aloittanut työn.
Kadotin puhelimeni.|Olen kadottanut puhelimeni.
Voitin pelin.|Olen voittanut pelin.
Nousin portaita.|Olen noussut portaita.
Autoin äitiäni.|Olen auttanut äitiäni.
Loin uuden teoksen.|Olen luonut uuden teoksen.
Suljin oven.|Olen sulkenut oven.
Kannoin laukkua.|Olen kantanut laukkua.
Kutsuin häntä Maxiksi.|Olen kutsunut häntä Maxiksi.
Aurinko paistoi.|Aurinko on paistanut.
Ajattelin sinua.|Olen ajatellut sinua.
Astuin lavalle.|Olen astunut lavalle.
Astelin hitaasti.|Olen astellut hitaasti.
Se onnistui minulle.|Se on onnistunut minulle.
Löin palloa.|Olen lyönyt palloa.
Tunsin hänet.|Olen tuntenut hänet.
Heitin pallon.|Olen heittänyt pallon.
Pyysin apua.|Olen pyytänyt apua.
Kasvi kuoli.|Kasvi on kuollut.
Istuin täällä.|Olen istunut täällä.
Söin leipää.|Olen syönyt leipää.
Lastasin auton.|Olen lastannut auton.
Tartuin lasiin.|Olen tarttunut lasiin.
Luin kirjaa.|Olen lukenut kirjaa.
Kutsuin ystäväni paikalle.|Olen kutsunut ystäväni paikalle.
Lapsi kasvoi nopeasti.|Lapsi on kasvanut nopeasti.
Osoitin tien.|Olen osoittanut tien.
Neuvoin sinua.|Olen neuvonut sinua.
Kutsuin sinut.|Olen kutsunut sinut.
Juoksin nopeasti.|Olen juossut nopeasti.
Sidoin kengät.|Olen sitonut kengät.
Laiva painui pinnan alle.|Laiva on painunut pinnan alle.
Taulu roikkui siellä.|Taulu on roikkunut siellä.
Pidin kahvista.|Olen pitänyt kahvista.
Se kuulosti hyvältä.|Se on kuulostanut hyvältä.
Lensin Saksaan.|Olen lentänyt Saksaan.
Suosittelin kirjaa.|Olen suositellut kirjaa.
Nautin lomasta.|Olen nauttinut lomasta.
Mursin leivän.|Olen murtanut leivän.
Oksa katkesi.|Oksa on katkennut.
Mitä täällä tapahtui?|Mitä täällä on tapahtunut?
Työnsin ovea.|Olen työntänyt ovea.
Törmäsin pöytään.|Olen törmännyt pöytään.
Kärsin päänsärystä.|Olen kärsinyt päänsärystä.
Harrastin urheilua.|Olen harrastanut urheilua.
Leikkasin leivän.|Olen leikannut leivän.
Muistutit isääsi.|Olet muistuttanut isääsi.
Ponnistelin ratkaisun löytämiseksi.|Olen ponnistellut ratkaisun löytämiseksi.
Koira katosi.|Koira on kadonnut.
Hän varasti rahaa.|Hän on varastanut rahaa.
Otin valokuvan.|Olen ottanut valokuvan.
Maalasin seinän.|Olen maalannut seinän.
Mittasin pöydän.|Olen mitannut pöydän.
Nostin laatikon.|Olen nostanut laatikon.
Unohdin nimen.|Olen unohtanut nimen.
Sää pakotti minut jäämään kotiin.|Sää on pakottanut minut jäämään kotiin.
Lauloin laulun.|Olen laulanut laulun.
Vesi virtasi nopeasti.|Vesi on virrannut nopeasti.
Otin pallon kiinni.|Olen ottanut pallon kiinni.
Hyppäsin aidan yli.|Olen hypännyt aidan yli.
Join vettä.|Olen juonut vettä.
Tuli paloi.|Tuli on palanut.
Repäisin paperin.|Olen repäissyt paperin.
Käänsin lihan.|Olen kääntänyt lihan.
Väistin autoa.|Olen väistänyt autoa.
Työnsin kärryä.|Olen työntänyt kärryä.
Nukuin pitkään.|Olen nukkunut pitkään.
He ylistivät tuotetta.|He ovat ylistäneet tuotetta.
Kissa pakeni.|Kissa on paennut.
Uin mielelläni.|Olen uinut mielelläni.
Olin hiljaa.|Olen ollut hiljaa.
Lähetin viestin.|Olen lähettänyt viestin.
Mehiläinen pisti minua.|Mehiläinen on pistänyt minua.
Riitelin veljeni kanssa.|Olen riidellyt veljeni kanssa.
Kastelin kukat.|Olen kastellut kukat.
Vältin stressiä.|Olen välttänyt stressiä.
Vesi tunkeutui taloon.|Vesi on tunkeutunut taloon.
Leivoin kakkua.|Olen leiponut kakkua.
En valehdellut.|En ole valehdellut.
Koira puri.|Koira on purrut.
Kaivoin kuopan.|Olen kaivanut kuopan.
Vauva huusi.|Vauva on huutanut.
Pesin käteni.|Olen pessyt käteni.
Koira söi lihaa.|Koira on syönyt lihaa.
Kukat tuoksuivat hyvältä.|Kukat ovat tuoksuneet hyvältä.
Kello heilui.|Kello on heilunut.
Taivutin metallia.|Olen taivuttanut metallia.
Tie kääntyi vasemmalle.|Tie on kääntynyt vasemmalle.
Hän petti ystävänsä.|Hän on pettänyt ystävänsä.
Vihelsin laulua.|Olen viheltänyt laulua.
Ratsastin hevosella.|Olen ratsastanut hevosella.
Sulatin voita.|Olen sulattanut voita.
Jää suli.|Jää on sulanut.
Lainasin rahaa.|Olen lainannut rahaa.
Tuuli puhalsi voimakkaasti.|Tuuli on puhaltanut voimakkaasti.
Heitin pallon.|Olen heittänyt pallon.
Säikähdin helposti.|Olen säikähtänyt helposti.
Kissa hiipi hiljaa.|Kissa on hiipinyt hiljaa.
Paistoin kalaa.|Olen paistanut kalaa.
Vene liukui veden yli.|Vene on liukunut veden yli.
Vannoin sen.|Olen vannonut sen.
Minulla oli kylmä.|Minulla on ollut kylmä.
Annoin sinulle anteeksi.|Olen antanut sinulle anteeksi.
Sade pilasi ruoan.|Sade on pilannut ruoan.
Ruoka pilaantui nopeasti.|Ruoka on pilaantunut nopeasti.
En käskenyt mitään.|En ole käskenyt mitään.
Vauva ryömi.|Vauva on ryöminyt.'''

# Corrected, tense-neutral present examples, still based on the original set.
CORRECTIONS = {
3: ('Kykenen uimaan.', 'Ich kann schwimmen.'),
65: ('Laiva painuu pinnan alle.', 'Das Schiff sinkt.'),
81: ('Ponnistelen ratkaisun löytämiseksi.', 'Ich ringe um eine Lösung.'),
96: ('Repäisen paperin.', 'Ich reiße das Papier.'),
7: ('Tulen ajoissa.', 'Ich komme rechtzeitig.'),
22: ('Lippu on voimassa.', 'Das Ticket gilt.'),
26: ('Tarjoamme apua.', 'Wir bieten Hilfe.'),
33: ('Lasi putoaa maahan.', 'Das Glas fällt zu Boden.'),
34: ('Aloitan työn.', 'Ich beginne die Arbeit.'),
37: ('Nousen portaita.', 'Ich steige die Treppe hinauf.'),
39: ('Luon uuden teoksen.', 'Ich schaffe ein neues Werk.'),
45: ('Astun lavalle.', 'Ich trete auf die Bühne.'),
55: ('Lastaan auton.', 'Ich lade das Auto.'),
56: ('Tartun lasiin.', 'Ich greife nach dem Glas.'),
58: ('Kutsun ystäväni paikalle.', 'Ich rufe meinen Freund.'),
72: ('Murran leivän.', 'Ich breche das Brot.'),
80: ('Muistutat isääsi.', 'Du gleichst deinem Vater.'),
89: ('Sää pakottaa minut jäämään kotiin.', 'Das Wetter zwingt mich, zu Hause zu bleiben.'),
93: ('Hyppään aidan yli.', 'Ich springe über den Zaun.'),
98: ('Väistän autoa.', 'Ich weiche dem Auto.'),
104: ('Olen hiljaa.', 'Ich schweige.'),
109: ('Vältän stressiä.', 'Ich vermeide Stress.'),
124: ('Ratsastan hevosella.', 'Ich reite auf einem Pferd.'),
135: ('Minulla on kylmä.', 'Ich friere.'),
}


def build():
    ranked = {int(r.get('source_rank', r['rank'])): r for r in read('saksa_epasaannolliset_verbit_ranked.csv')}
    source = read('cleanup/archive/saksa_epasaannolliset_verbit_lauseet_praesens.csv')[:140]
    tables = {t: {int(r.get('source_rank', r['rank'])): r for r in read(f'saksa_epasaannolliset_verbit_{t}.csv')}
              for t in ('praesens', 'praeteritum', 'perfekt')}
    translations = [line.split('|') for line in PAST_FI.splitlines()]
    assert len(source) == len(translations) == 140
    outputs = {t: [] for t in tables}
    for base in source:
        rank = int(base['rank'])
        if rank not in ranked:
            continue
        fi, de = CORRECTIONS.get(rank, (base['sentence_fi'], base['sentence_de']))
        # Explicitly retain the actual grammatical subject, not the old batch label.
        if de.startswith('Ich '): subject, person = 'Ich', 'ich'
        elif de.startswith('Du '): subject, person = 'Du', 'du'
        elif de.startswith('Wir '): subject, person = 'Wir', 'wir'
        elif de.startswith('Sie ') or rank == 118:
            subject, person = ('Sie' if rank != 118 else 'Die Blumen'), 'sie'
        elif de.startswith('Er '): subject, person = 'Er', 'er'
        else:
            # All other curated examples start with a singular subject, including Was.
            finite = tables['praesens'][rank]['er']
            assert finite and f' {finite} ' in ' ' + de.replace('.', ' .').replace('?', ' ?') + ' ', (rank, de, finite)
            subject = de.split(' ' + finite, 1)[0]
            person = 'er'
        remainder = de[len(subject):].strip().rstrip('.?')
        finite, _, complement = remainder.partition(' ')
        punctuation = '?' if de.endswith('?') else '.'
        # Separable prefixes become part of the participle in Perfekt.
        particle = {37: 'hinauf', 62: 'ein'}.get(rank)
        if particle:
            assert complement.endswith(particle)
            complement = complement[:-len(particle)].strip()
        for tense in outputs:
            form = tables[tense][rank][person]
            assert form, (rank, tense, person)
            variants = form.split('|')
            tail = ''
            if tense == 'perfekt':
                heads, tails = zip(*(v.split(' ', 1) for v in variants))
                assert len(set(heads)) == 1
                answer = heads[0]
                tail = '|'.join(dict.fromkeys(tails))
                if rank in (3, 5, 6, 9, 25):
                    # Ersatzinfinitiv: hat schwimmen können, not hat schwimmen gekonnt.
                    tail = complement + ' ' + ranked[rank]['infinitive']
                    complement_for_tense = ''
                else:
                    complement_for_tense = complement
                if rank == 37: tail = 'hinaufgestiegen'
                template = subject + ' {finite}' + (' ' + complement_for_tense if complement_for_tense else '') + ' {tail}' + punctuation
            else:
                # einladen has the particle in its paradigm cell; the cloze keeps it visible.
                answer = '|'.join(v.removesuffix(' ein') for v in variants) if rank == 62 else form
                template = subject + ' {finite}' + (' ' + complement if complement else '') + (' ' + particle if particle else '') + punctuation
            if rank == 89 and tense == 'perfekt':
                template = 'Das Wetter {finite} mich {tail}, zu Hause zu bleiben.'
            sentence = template.replace('{finite}', answer.split('|')[0]).replace('{tail}', tail.split('|')[0])
            row = dict(rank=int(ranked[rank]['rank']), source_rank=rank, infinitive=ranked[rank]['infinitive'], suomi=ranked[rank]['suomi'],
                       tense=tense, person=person, sentence_fi=fi if tense == 'praesens' else translations[rank-1][0 if tense == 'praeteritum' else 1],
                       sentence_de=sentence, cloze_de=template, answer_finite=answer, answer_tail=tail)
            outputs[tense].append(row)
    # Additional verbs have independent authored examples and stable identifiers.
    import importlib.util
    spec = importlib.util.spec_from_file_location('new_verbs', ROOT / 'data/new_verbs.py')
    new_verbs = importlib.util.module_from_spec(spec); spec.loader.exec_module(new_verbs)
    for inf, entry in new_verbs.entries().items():
        sid = int(entry['source_rank'])
        if sid not in ranked: continue
        subject, complement, particle, finnish, english = entry['example']
        person = 'ich' if subject == 'Ich' else 'er'
        for index, tense in enumerate(outputs):
            form = tables[tense][sid][person]
            if tense == 'perfekt':
                answer, tail = form.split(' ', 1)
                template = subject + ' {finite}' + (' ' + complement if complement else '') + ' {tail}.'
            else:
                answer = form.removesuffix(' ' + particle) if particle else form
                tail = ''
                template = subject + ' {finite}' + (' ' + complement if complement else '') + (' ' + particle if particle else '') + '.'
            sentence = template.replace('{finite}', answer).replace('{tail}', tail)
            outputs[tense].append(dict(rank=int(ranked[sid]['rank']),source_rank=sid,infinitive=inf,suomi=ranked[sid]['suomi'],
                                      tense=tense,person=person,sentence_fi=finnish[index],sentence_de=sentence,
                                      cloze_de=template,answer_finite=answer,answer_tail=tail))
    article_hints = json.loads((ROOT / 'data/sentence_article_hints_fi.json').read_text())
    for rows in outputs.values():
        for row in rows:
            row['article_hint'] = article_hints.get(row['infinitive'], '')

        rows.sort(key=lambda row: row['rank'])
        assert len(rows) == 100 and len({row['infinitive'] for row in rows}) == 100
    for tense, rows in outputs.items():
        name = f'saksa_epasaannolliset_verbit_lauseharjoitus_{tense}.csv'
        with (ROOT / name).open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
        print(f'{name}: {len(rows)} sentences')

if __name__ == '__main__':
    build()
