#!/usr/bin/env python3
"""Generate full Präsens and Präteritum paradigm CSVs from the ranked verb list."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RANKED = ROOT / "saksa_epasaannolliset_verbit_ranked.csv"
OUT_PRES = ROOT / "saksa_epasaannolliset_verbit_praesens.csv"
OUT_PRET = ROOT / "saksa_epasaannolliset_verbit_praeteritum.csv"

PERSON_COLS = ["ich", "du", "er", "wir", "ihr", "sie"]


def normalize_inf(inf: str) -> str:
    s = inf.strip()
    s = re.sub(r"^(jdm|jdn|etw\.)\s+", "", s, flags=re.I)
    s = s.replace("(ver)", "")
    s = re.sub(r"\s*\(wo\?\)\s*", "", s)
    return s.strip()


def clean_form(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s*\(tai:.*?\)", "", s, flags=re.I)
    s = re.sub(r"^\(ver\)", "", s)
    return s.strip()


def deumlaut(s: str) -> str:
    return (
        s.replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ß", "ss")
    )


# fmt: off
PRESENT = {
    "werden": ["werde", "wirst", "wird", "werden", "werdet", "werden"],
    "haben": ["habe", "hast", "hat", "haben", "habt", "haben"],
    "können": ["kann", "kannst", "kann", "können", "könnt", "können"],
    "müssen": ["muss", "musst", "muss", "müssen", "müsst", "müssen"],
    "dürfen": ["darf", "darfst", "darf", "dürfen", "dürft", "dürfen"],
    "sollen": ["soll", "sollst", "soll", "sollen", "sollt", "sollen"],
    "wollen": ["will", "willst", "will", "wollen", "wollt", "wollen"],
    "mögen": ["mag", "magst", "mag", "mögen", "mögt", "mögen"],
    "wissen": ["weiß", "weißt", "weiß", "wissen", "wisst", "wissen"],
    "tun": ["tue", "tust", "tut", "tun", "tut", "tun"],
    "gelten": ["gelte", "giltst", "gilt", "gelten", "geltet", "gelten"],
    "lassen": ["lasse", "lässt", "lässt", "lassen", "lasst", "lassen"],
    "laden": ["lade", "lädst", "lädt", "laden", "ladet", "laden"],
    "einladen": ["lade ein", "lädst ein", "lädt ein", "laden ein", "ladet ein", "laden ein"],
    "geben": ["gebe", "gibst", "gibt", "geben", "gebt", "geben"],
    "nehmen": ["nehme", "nimmst", "nimmt", "nehmen", "nehmt", "nehmen"],
    "sprechen": ["spreche", "sprichst", "spricht", "sprechen", "sprecht", "sprechen"],
    "treffen": ["treffe", "triffst", "trifft", "treffen", "trefft", "treffen"],
    "helfen": ["helfe", "hilfst", "hilft", "helfen", "helft", "helfen"],
    "sehen": ["sehe", "siehst", "sieht", "sehen", "seht", "sehen"],
    "stehlen": ["stehle", "stiehlst", "stiehlt", "stehlen", "stehlt", "stehlen"],
    "empfehlen": ["empfehle", "empfiehlst", "empfiehlt", "empfehlen", "empfehlt", "empfehlen"],
    "befehlen": ["befehle", "befiehlst", "befiehlt", "befehlen", "befehlt", "befehlen"],
    "essen": ["esse", "isst", "isst", "essen", "esst", "essen"],
    "fressen": ["fresse", "frisst", "frisst", "fressen", "fresst", "fressen"],
    "lesen": ["lese", "liest", "liest", "lesen", "lest", "lesen"],
    "messen": ["messe", "misst", "misst", "messen", "messt", "messen"],
    "vergessen": ["vergesse", "vergisst", "vergisst", "vergessen", "vergesst", "vergessen"],
    "treten": ["trete", "trittst", "tritt", "treten", "tretet", "treten"],
    "geschehen": ["geschehe", "geschiehst", "geschieht", "geschehen", "gescheht", "geschehen"],
    "brennen": ["brenne", "brennst", "brennt", "brennen", "brennt", "brennen"],
    "kennen": ["kenne", "kennst", "kennt", "kennen", "kennt", "kennen"],
    "nennen": ["nenne", "nennst", "nennt", "nennen", "nennt", "nennen"],
    "rennen": ["renne", "rennst", "rennt", "rennen", "rennt", "rennen"],
    "senden": ["sende", "sendest", "sendet", "senden", "sendet", "senden"],
    "wenden": ["wende", "wendest", "wendet", "wenden", "wendet", "wenden"],
    "meiden": ["meide", "meidest", "meidet", "meiden", "meidet", "meiden"],
    "halten": ["halte", "hältst", "hält", "halten", "haltet", "halten"],
    "raten": ["rate", "rätst", "rät", "raten", "rat", "raten"],
    "wachsen": ["wachse", "wächst", "wächst", "wachsen", "wachst", "wachsen"],
    "blasen": ["blase", "bläst", "bläst", "blasen", "blast", "blasen"],
    "braten": ["brate", "brätst", "brät", "braten", "brat", "braten"],
    "preisen": ["preise", "preist", "preist", "preisen", "preist", "preisen"],
    "stoßen": ["stoße", "stößt", "stößt", "stoßen", "stoßt", "stoßen"],
    "heißen": ["heiße", "heißt", "heißt", "heißen", "heißt", "heißen"],
    "schließen": ["schließe", "schließt", "schließt", "schließen", "schließt", "schließen"],
    "sitzen": ["sitze", "sitzt", "sitzt", "sitzen", "sitzt", "sitzen"],
    "weisen": ["weise", "weist", "weist", "weisen", "weist", "weisen"],
    "genießen": ["genieße", "genießt", "genießt", "genießen", "genießt", "genießen"],
    "gelingen": ["gelinge", "gelingst", "gelingt", "gelingen", "gelingt", "gelingen"],
}

PRETERITE = {
    "werden": ["wurde", "wurdest", "wurde", "wurden", "wurdet", "wurden"],
    "haben": ["hatte", "hattest", "hatte", "hatten", "hattet", "hatten"],
    "können": ["konnte", "konntest", "konnte", "konnten", "konntet", "konnten"],
    "müssen": ["musste", "musstest", "musste", "mussten", "musstet", "mussten"],
    "dürfen": ["durfte", "durftest", "durfte", "durften", "durftet", "durften"],
    "sollen": ["sollte", "solltest", "sollte", "sollten", "solltet", "sollten"],
    "wollen": ["wollte", "wolltest", "wollte", "wollten", "wolltet", "wollten"],
    "mögen": ["mochte", "mochtest", "mochte", "mochten", "mochtet", "mochten"],
    "wissen": ["wusste", "wusstest", "wusste", "wussten", "wusstet", "wussten"],
    "tun": ["tat", "tatst", "tat", "taten", "tatet", "taten"],
    "gelten": ["galt", "galtst", "galt", "galten", "galtet", "galten"],
    "lassen": ["ließ", "ließest", "ließ", "ließen", "ließet", "ließen"],
    "laden": ["lud", "ludst", "lud", "luden", "ludet", "luden"],
    "einladen": ["lud ein", "ludst ein", "lud ein", "luden ein", "ludet ein", "luden ein"],
    "geben": ["gab", "gabst", "gab", "gaben", "gabt", "gaben"],
    "nehmen": ["nahm", "nahmst", "nahm", "nahmen", "nahmt", "nahmen"],
    "sprechen": ["sprach", "sprachst", "sprach", "sprachen", "spracht", "sprachen"],
    "treffen": ["traf", "trafst", "traf", "trafen", "traft", "trafen"],
    "helfen": ["half", "halfst", "half", "halfen", "halft", "halfen"],
    "sehen": ["sah", "sahst", "sah", "sahen", "sahen", "sahen"],
    "stehlen": ["stahl", "stahlst", "stahl", "stahlen", "stahlt", "stahlen"],
    "empfehlen": ["empfahl", "empfahlst", "empfahl", "empfahlen", "empfahlt", "empfahlen"],
    "befehlen": ["befahl", "befahlst", "befahl", "befahlen", "befahlt", "befahlen"],
    "essen": ["aß", "aßt", "aß", "aßen", "aßt", "aßen"],
    "fressen": ["fraß", "fraßt", "fraß", "fraßen", "fraßt", "fraßen"],
    "lesen": ["las", "last", "las", "lasen", "last", "lasen"],
    "messen": ["maß", "maßest", "maß", "maßen", "maßet", "maßen"],
    "vergessen": ["vergaß", "vergaßt", "vergaß", "vergaßen", "vergaßt", "vergaßen"],
    "sitzen": ["saß", "saßt", "saß", "saßen", "saßt", "saßen"],
    "geschehen": ["geschah", "geschahst", "geschah", "geschahen", "geschaht", "geschahen"],
    "denken": ["dachte", "dachtest", "dachte", "dachten", "dachtet", "dachten"],
    "bringen": ["brachte", "brachtest", "brachte", "brachten", "brachtet", "brachten"],
    "nennen": ["nannte", "nanntest", "nannte", "nannten", "nanntet", "nannten"],
    "kennen": ["kannte", "kanntest", "kannte", "kannten", "kanntet", "kannten"],
    "brennen": ["brannte", "branntest", "brannte", "brannten", "branntet", "brannten"],
    "rennen": ["rannte", "ranntest", "rannte", "rannten", "ranntet", "rannten"],
    "senden": ["sendete|sandte", "sendetest|sandtest", "sendete|sandte", "sendeten|sandten", "sendetet|sandtet", "sendeten|sandten"],
    "wenden": ["wendete|wandte", "wendetest|wandtest", "wendete|wandte", "wendeten|wandten", "wendetet|wandtet", "wendeten|wandten"],
    "raten": ["riet", "rietest", "riet", "rieten", "rietet", "rieten"],
    "backen": ["backte", "backtest", "backte", "backten", "backtet", "backten"],
    "meiden": ["mied", "miedest", "mied", "mieden", "miedet", "mieden"],
    "wachsen": ["wuchs", "wuchsest", "wuchs", "wuchsen", "wuchst", "wuchsen"],
    "genießen": ["genoss", "genossest", "genoss", "genossen", "genosset", "genossen"],
    "blasen": ["blies", "bliesest", "blies", "bliesen", "blieset", "bliesen"],
    "braten": ["briet", "brietest", "briet", "brieten", "brietet", "brieten"],
    "gewinnen": ["gewann", "gewannst", "gewann", "gewannen", "gewannt", "gewannen"],
    "reiten": ["ritt", "rittst", "ritt", "ritten", "rittet", "ritten"],
}
# fmt: on

IHR_PRESENT = {
    "gibt": "gebt", "nimmt": "nehmt", "spricht": "sprecht",
    "isst": "esst", "frisst": "fresst", "liest": "lest",
    "hilft": "helft", "trifft": "trefft", "lässt": "lasst",
    "misst": "messt", "vergisst": "vergesst",
}

PRET_PLURAL = {
    "aß": "aßen", "ass": "aßen", "band": "banden", "bat": "baten", "begann": "begannen",
    "betrog": "betrogen", "biss": "bissen", "blieb": "blieben", "blies": "bliesen",
    "bog": "bogen", "brach": "brachen", "briet": "brieten", "dachte": "dachten",
    "drang": "drangen", "empfahl": "empfahlen", "erschrak": "erschraken", "fand": "fanden",
    "fiel": "fielen", "fing": "fingen", "floh": "flohen", "flog": "flogen", "floss": "flossen",
    "fror": "froren", "fraß": "fraßen", "gab": "gaben", "genoss": "genossen", "geschah": "geschahen",
    "gewann": "gewannen", "glich": "glichen", "glitt": "glitten", "ging": "gingen", "goss": "gossen",
    "grub": "gruben", "half": "halfen", "hielt": "hielten", "hing": "hingen", "hob": "hoben",
    "kam": "kamen", "klang": "klangen", "kroch": "krochen", "lag": "lagen", "las": "lasen",
    "lief": "liefen", "lieh": "liehen", "litt": "litten", "log": "logen", "lud": "luden",
    "maß": "maßen", "mied": "mieden", "nahm": "nahmen", "pfiff": "pfiffen", "rang": "rangen",
    "riet": "rieten", "ritt": "ritten", "roch": "rochen", "sah": "sahen", "sang": "sangen",
    "sank": "sanken", "schlich": "schlichen", "schloss": "schlossen", "schmiss": "schmissen",
    "schmolz": "schmolzen", "schnitt": "schnitten", "schoss": "schossen", "schrie": "schrien",
    "schritt": "schritten", "schuf": "schufen", "schlug": "schlugen", "schwamm": "schwammen",
    "schwang": "schwangen", "schwieg": "schwiegen", "schwor": "schworen", "sprach": "sprachen",
    "sprang": "sprangen", "stach": "stachen", "stand": "standen", "starb": "starben",
    "stahl": "stahlen", "stieg": "stiegen", "stieß": "stießen", "strich": "strichen",
    "stritt": "stritten", "traf": "trafen", "trank": "tranken", "trieb": "trieben",
    "trug": "trugen", "verdarb": "verdarben", "verlor": "verloren", "verzieh": "verziehen",
    "verschwand": "verschwanden", "warf": "warfen", "wuchs": "wuchsen", "wusch": "wuschen",
    "wich": "wichen", "wies": "wiesen", "zog": "zogen", "zwang": "zwangen",
}


def is_weak_pret(er_pret: str) -> bool:
    return er_pret.endswith("te")


def weak_preterite(er_pret: str) -> list[str]:
    s = er_pret
    return [s, s + "st", s, s + "n", s + "t", s + "n"]


def pret_plural(stem: str) -> str:
    return PRET_PLURAL.get(stem, stem + "en")


def pret_du(er_pret: str) -> str:
    if er_pret.endswith("ß"):
        return er_pret + "est"
    if er_pret.endswith("tt"):
        return er_pret + "est"
    if er_pret.endswith("t"):
        return er_pret[:-1] + "test"
    if er_pret.endswith("s"):
        return er_pret + "est"
    return er_pret + "st"


def pret_ihr(er_pret: str) -> str:
    return er_pret + "et" if er_pret.endswith("t") else er_pret + "t"


def strong_preterite(er_pret: str) -> list[str]:
    pl = pret_plural(er_pret)
    return [er_pret, pret_du(er_pret), er_pret, pl, pret_ihr(er_pret), pl]


def present_du(er: str, stem: str) -> str:
    # After ß, du matches 3sg (heißt, not heißst); avoids schießst etc.
    if "ß" in er:
        return er
    return stem + "st"


def weak_present(er: str, inf: str) -> list[str]:
    stem = er[:-1] if er.endswith("t") else er
    return [stem + "e", present_du(er, stem), er, inf, stem + "t", inf]


def strong_present(inf: str, er: str) -> list[str]:
    inf_stem = inf[:-2] if inf.endswith("en") else inf
    er_stem = er[:-1] if er.endswith("t") else er
    ich = inf_stem + "e"
    du = present_du(er, er_stem)
    ihr = IHR_PRESENT.get(er, deumlaut(er_stem) + "t")
    return [ich, du, er, inf, ihr, inf]


def conjugate(inf_raw: str, er: str, tense: str) -> list[str]:
    inf = normalize_inf(inf_raw)
    er = clean_form(er)
    table = PRESENT if tense == "praesens" else PRETERITE

    if inf in table:
        return table[inf]

    if " " in er:
        verb, prefix = er.rsplit(" ", 1)
        base_inf = inf[len(prefix) :] if inf.lower().startswith(prefix.lower()) else inf
        inner = conjugate(base_inf, verb, tense)
        return [f"{f} {prefix}" for f in inner]

    if tense == "praeteritum":
        if is_weak_pret(er):
            return weak_preterite(er)
        return strong_preterite(er)

    # present
    inf_stem = inf[:-2] if inf.endswith("en") else inf
    er_stem = er[:-1] if er.endswith("t") else er
    if er_stem != inf_stem and er_stem != deumlaut(inf_stem):
        return strong_present(inf, er)
    return weak_present(er, inf)


def main():
    rows = list(csv.DictReader(RANKED.open(encoding="utf-8-sig")))
    from rank_verb_candidates import paradigms
    with (ROOT / "data/irregular_candidates.tsv").open(encoding="utf-8") as f:
        candidates = {r["infinitive"]: r for r in csv.DictReader(f, delimiter="\t")}
    header = ["rank", "source_rank", "infinitive", "suomi"] + PERSON_COLS

    for out_path, tense in [(OUT_PRES, "praesens"), (OUT_PRET, "praeteritum")]:
        with out_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            for row in rows:
                if row["infinitive"] in candidates:
                    forms = list(paradigms(candidates[row["infinitive"]])[0 if tense == "praesens" else 1])
                else:
                    forms = conjugate(row["infinitive"], row[tense], tense)
                if normalize_inf(row["infinitive"]) in {"gelten", "gelingen", "geschehen", "entstehen", "stattfinden"}:
                    forms = [form if person in {"er", "sie"} else ""
                             for person, form in zip(PERSON_COLS, forms)]
                w.writerow([row["rank"], row.get("source_rank", row["rank"]), row["infinitive"], row["suomi"], *forms])
        print(f"Wrote {out_path.name} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
