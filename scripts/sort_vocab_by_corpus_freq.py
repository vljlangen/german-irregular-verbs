#!/usr/bin/env python3
"""Sort GER–FIN vocabulary by corpus frequency of one headword per row.

Uses deu_news_2025_1M-words.txt. Each entry is ranked by a single lemma (not the
sum of all conjugated forms listed in the cell — that inflated phrasal verbs).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "cleanup" / "deu_news_2025_1M" / "deu_news_2025_1M-words.txt"
SENTENCES = ROOT / "cleanup" / "deu_news_2025_1M" / "deu_news_2025_1M-sentences.txt"
DEFAULT_IN = ROOT / "tmp" / "saksan_perussanasto_no_duplicates_korjauksia.xlsx"
DEFAULT_OUT = ROOT / "tmp" / "_sorted.csv"
DEFAULT_VERBS = ROOT / "tmp" / "500_most_common_verbs_german.csv"

AUX = {
    "hat",
    "ist",
    "sind",
    "war",
    "waren",
    "bin",
    "bist",
    "seid",
    "haben",
    "sein",
    "war",
    "wird",
    "werden",
    "wurde",
    "wurden",
    "sind",
    "bin",
    "bist",
    "seid",
    "waren",
    "hatte",
    "hattest",
    "hatten",
    "gewesen",
    "hätte",
    "wäre",
    "wären",
}
SKIP_PARTICLES = {"ein", "eine", "einem", "einen", "einer", "eines"}
ARTICLES = {
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einer",
    "einem",
    "einen",
    "eines",
}
STOP = ARTICLES | SKIP_PARTICLES | AUX | {
    "und",
    "oder",
    "aber",
    "in",
    "an",
    "auf",
    "ab",
    "aus",
    "bei",
    "mit",
    "nach",
    "von",
    "zu",
    "vor",
    "über",
    "unter",
    "durch",
    "für",
    "um",
    "am",
    "im",
    "zum",
    "zur",
    "nicht",
    "kein",
    "keine",
    "sich",
    "es",
    "man",
    "auch",
    "noch",
    "nur",
    "schon",
    "sehr",
    "wie",
    "als",
    "wenn",
    "dass",
    "daß",
    "hier",
    "dort",
    "da",
    "so",
    "ja",
    "nein",
    "mit",
    "weg",
    "hin",
    "her",
    "zurück",
    "etwas",
    "nichts",
    "alles",
    "viel",
    "wenig",
}

TOKEN_RE = re.compile(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß'-]*")
PAREN_PREFIX_RE = re.compile(r"^\s*(\([^)]*\)\s*)+")


def load_freq(path: Path) -> dict[str, int]:
    freq: dict[str, int] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                w = parts[1].lower()
                freq[w] = freq.get(w, 0) + int(parts[2])
    return freq


_COMMON_VERBS: set[str] | None = None


def load_common_verbs(path: Path = DEFAULT_VERBS) -> set[str]:
    """Infinitives from col A of 500_most_common_verbs_german.csv (1st word before comma)."""
    verbs: set[str] = set()
    if not path.is_file():
        return verbs
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            inf = row[0].split(",")[0].strip().strip('"').lower()
            if inf and TOKEN_RE.match(inf):
                verbs.add(inf)
    return verbs


def get_common_verbs() -> set[str]:
    global _COMMON_VERBS
    if _COMMON_VERBS is None:
        _COMMON_VERBS = load_common_verbs()
    return _COMMON_VERBS


def tokenize(text: str) -> list[str]:
    return [t.lower().strip("'") for t in TOKEN_RE.findall(text)]


def clean_declension_tail(tail: str) -> str:
    """Drop noun declension hints like '-er', '-e', '+' so 'er' is not counted."""
    t = re.sub(r"[+■]", " ", tail)
    t = re.sub(r"-\s*(?:er|e|en|em|es|n|s)\b", " ", t, flags=re.I)
    return t


TAIL_SKIP = {"er", "e", "s", "n", "en", "em", "es"}
HEAD_VERBS = {"sein", "haben", "werden", "können", "müssen", "sollen", "wollen", "dürfen"}
# Verbs that head “light” constructions (leiser machen) — not the lexical head of the row
LIGHT_VERBS = HEAD_VERBS | {
    "machen",
    "tun",
    "lassen",
    "stellen",
    "setzen",
    "halten",
    "geben",
    "gehen",
    "kommen",
    "fahren",
    "bringen",
    "nehmen",
    "arbeiten",
    "sprechen",
    "fragen",
    "sagen",
    "helfen",
    "denken",
    "finden",
    "glauben",
    "zeigen",
    "legen",
    "stehen",
    "liegen",
    "spielen",
    "lernen",
    "hören",
    "sehen",
    "schreiben",
    "lesen",
    "kaufen",
    "verkaufen",
}
# Conjugated surface forms — must not drive ranking (Gott sei Dank → not sei)
SURFACE_FORM_SKIP = {
    "sei",
    "bin",
    "bist",
    "ist",
    "sind",
    "seid",
    "war",
    "waren",
    "hat",
    "hast",
    "hatte",
    "habt",
    "habe",
    "wird",
    "wirst",
    "werde",
    "wurde",
    "wurden",
    "wirds",
    "kann",
    "kannst",
    "konnte",
    "will",
    "willst",
    "wollte",
    "soll",
    "sollst",
    "sollte",
    "muß",
    "musst",
    "musste",
    "muss",
    "darf",
    "darfst",
    "durfte",
    "mag",
    "magst",
    "mochte",
    "hätte",
    "wäre",
    "wären",
    # Common present/preterite/participle — never rank phrasal entries (gehen geht → gehen)
    "geht",
    "gehe",
    "gehst",
    "ging",
    "gegangen",
    "steht",
    "stehe",
    "stehst",
    "stand",
    "gestanden",
    "macht",
    "mache",
    "machst",
    "machte",
    "gemacht",
    "gibt",
    "gab",
    "gegeben",
    "kommt",
    "kam",
    "gekommen",
    "tut",
    "tat",
    "getan",
    "sagt",
    "sagte",
    "gesagt",
    "findet",
    "fand",
    "gefunden",
    "denkt",
    "dachte",
    "gedacht",
}
KEIN_FORMS = {"kein", "keine", "keinen", "keinem", "keiner", "keines"}
REFLEXIVE = {"sich", "mich", "dich", "uns", "euch"}
PREPOSITIONS = {
    "in",
    "im",
    "am",
    "ins",
    "ans",
    "zum",
    "zur",
    "vom",
    "beim",
    "mit",
    "von",
    "zu",
    "auf",
    "an",
    "bei",
    "nach",
    "für",
    "um",
    "aus",
    "vor",
    "über",
    "unter",
    "durch",
    "bis",
    "ohne",
    "seit",
    "gegen",
    "ab",
    "hinter",
    "neben",
    "zwischen",
    "innerhalb",
    "außerhalb",
    "wider",
    "entlang",
    "gegenüber",
    "trotz",
    "während",
    "wegen",
    "statt",
    "außer",
}
GRAMMAR_CASE = re.compile(r"\+\s*[ADG]\b|\(prep\.\)|\(\s*\+\s*[ADG]\s*\)", re.I)
GRAMMAR_PAREN_RE = re.compile(r"\([^)]*\)")
ELLIPSIS_RE = re.compile(r"\s*\.{3}\s*")
# Idioms with sein/haben (Lust haben, in Ordnung sein): phrase freq or content word — never nicht/haben.
IDIOM_AUX = {"sein", "haben"}
IDIOM_FUNCTION_SKIP = (
    PREPOSITIONS
    | ARTICLES
    | REFLEXIVE
    | AUX
    | SURFACE_FORM_SKIP
    | {
        "nicht",
        "kein",
        "keine",
        "keinen",
        "keinem",
        "keiner",
        "etwas",
        "auch",
        "noch",
        "schon",
        "sehr",
        "gar",
        "so",
        "nur",
        "ja",
        "doch",
        "weder",
        "hier",
        "dort",
        "da",
        "mal",
        "man",
        "es",
        "zu",
        "tun",
    }
)
CASE_TAG_TOKENS = {"a", "d", "g", "ak", "dat", "gen", "inf", "subst", "mon"}
GRAMMAR_TEMPLATE_RE = re.compile(
    r"\(prep\.\)|\+\s*subst|was\s+für|/\s*für\s+\+|mon\.\s*was",
    re.I,
)
# Two-word phrases scored in corpus (not by first particle alone)
LEXICAL_PHRASE_HEADS = frozenset(
    {"als ob", "wie lange", "wie spät", "keine ahnung", "es gibt"}
)

# Fixed multi-word function phrases (ab und zu): rank only as a phrase in the corpus,
# not by max frequency of und/zu/ab. Single-word rows (ab, zu, und) stay unigram-scored.
PHRASE_CONNECTORS = {
    "und",
    "oder",
    "als",
    "noch",
    "weder",
    "sowohl",
    "entweder",
    "auch",
}
DIRECTION_PARTICLES = {
    "hin",
    "her",
    "zurück",
    "weg",
    "hinauf",
    "hinab",
    "herauf",
    "herab",
    "hinein",
    "hinaus",
    "rauf",
    "runter",
    "rein",
    "raus",
    "drauf",
    "drunter",
    "drin",
    "draus",
    "oben",
    "unten",
    "vorwärts",
    "rückwärts",
}
PARTICLE_LEXICON = (
    PREPOSITIONS
    | PHRASE_CONNECTORS
    | DIRECTION_PARTICLES
    | {
        "so",
        "da",
        "hier",
        "dort",
        "mal",
        "ab",
        "zu",
        "an",
        "in",
        "um",
        "am",
        "im",
        "vom",
        "zum",
        "zur",
        "aus",
        "bei",
        "nach",
        "von",
        "vor",
        "über",
        "unter",
        "durch",
        "für",
        "bis",
        "ohne",
        "auf",
    }
)

# Ellipsis correlatives: match with gap in sentences (sowohl … als auch)
PHRASE_REGEX: dict[str, str] = {
    "sowohl als auch": r"\bsowohl\b.{0,40}?\bals auch\b",
    "weder noch": r"\bweder\b.{0,40}?\bnoch\b",
    "entweder oder": r"\bentweder\b.{0,40}?\boder\b",
}


def content_tokens(
    head_tokens: list[str], *, skip_verbs: bool = False, skip_reflexive: bool = True
) -> list[str]:
    out: list[str] = []
    for t in head_tokens:
        if t in PREPOSITIONS or t in ARTICLES or t in TAIL_SKIP:
            continue
        if skip_reflexive and t in REFLEXIVE:
            continue
        if t in AUX:
            continue
        if len(t) < 2:
            continue
        if skip_verbs and t in HEAD_VERBS:
            continue
        out.append(t)
    return out


def head_infinitive(head_tokens: list[str], tail_set: set[str]) -> str:
    for t in head_tokens:
        if len(t) >= 4 and t.endswith("en") and t not in tail_set:
            return t
    return ""


def pick_lemma(candidates: list[str], freq: dict[str, int]) -> str:
    if not candidates:
        return ""
    return max(candidates, key=lambda t: freq.get(t, 0))


def strip_grammar_suffix(text: str) -> str:
    """Drop case-frame tails: mit + D, (auf+ A), + Inf., + subst."""
    t = text
    t = re.sub(r"\s*\([^)]*\+\s*[ADG][^)]*\).*$", "", t, flags=re.I)
    # prep + case as one unit (… haben mit + D); omit um — es geht um + A keeps um
    t = re.sub(
        r"\s+(?:mit|auf|an|in|von|zu|für|über|unter|bei|nach|aus|vor)\s+\+\s*[ADG].*$",
        "",
        t,
        flags=re.I,
    )
    # bare + case (es geht um + A → es geht um)
    t = re.sub(r"\s+\+\s*[ADG]\b.*$", "", t, flags=re.I)
    t = re.sub(r"\s+\+\s*(?:Inf\.?|inf\.?|subst\.?)\b.*$", "", t, flags=re.I)
    return t.strip()


def is_infinitive_token(t: str, common_verbs: set[str] | None = None) -> bool:
    if t in REFLEXIVE or t in SURFACE_FORM_SKIP:
        return False
    verbs = common_verbs if common_verbs is not None else get_common_verbs()
    if t in verbs:
        return True
    return len(t) >= 4 and t.endswith("en")


def conjugated_after_infinitive(token: str, infinitive: str) -> bool:
    if token in SURFACE_FORM_SKIP:
        return True
    if not infinitive.endswith("en") or len(infinitive) < 4:
        return False
    stem = infinitive[:-2]  # gehen → geh, machen → mach
    return len(stem) >= 3 and token.startswith(stem)


def truncate_head_at_conjugation(tokens: list[str]) -> list[str]:
    """Drop conjugated forms after an infinitive (gehen geht → gehen; machen macht → machen)."""
    out: list[str] = []
    last_inf = ""
    for t in tokens:
        if last_inf and conjugated_after_infinitive(t, last_inf):
            break
        if is_infinitive_token(t):
            last_inf = t
        out.append(t)
    return out


def infer_paradigm_lemma(ger: str) -> str:
    """Recover lemma from split paradigm rows (vor, kam vor, ist vorgekommen → vorkommen)."""
    low = ger.lower()
    if "vorgekommen" in low or "vorkommen" in tokenize(low):
        return "vorkommen"
    return ""


def head_main_infinitive(head_tokens: list[str], tail_set: set[str]) -> str:
    """Rightmost infinitive in head (einen Arzt rufen → rufen; nicht brauchen zu → brauchen)."""
    candidates = [
        t
        for t in head_tokens
        if len(t) >= 4
        and t.endswith("en")
        and t not in tail_set
        and t not in REFLEXIVE
        and t not in SURFACE_FORM_SKIP
    ]
    return candidates[-1] if candidates else ""


def light_verb_content_tokens(head_tokens: list[str]) -> list[str]:
    """Lexical head before a light verb (Sauna gehen → sauna; frisch machen → frisch)."""
    if len(head_tokens) < 2 or head_tokens[-1] not in LIGHT_VERBS:
        return []
    return [
        t
        for t in head_tokens[:-1]
        if t not in LIGHT_VERBS
        and t not in PREPOSITIONS
        and t not in ARTICLES
        and t not in REFLEXIVE
        and t not in SURFACE_FORM_SKIP
        and t not in IDIOM_FUNCTION_SKIP
        and t not in KEIN_FORMS
        and len(t) >= 3
    ]


def is_declension_variant_row(ger: str) -> bool:
    """Pronoun/noun inflection note (andere, die anderen) — not a primary lemma row."""
    s = PAREN_PREFIX_RE.sub("", ger.strip())
    if "," not in s:
        return False
    head, _, tail = s.partition(",")
    ht = tokenize(head.strip())
    tt = tokenize(GRAMMAR_PAREN_RE.sub(" ", tail))
    return len(ht) == 1 and len(tt) >= 2 and tt[0] in ARTICLES


def detect_verb_phrase(ger: str) -> str | None:
    """Phrasal/light-verb row (ins Bett gehen, Schlange stehen) — corpus phrase score."""
    if (
        not ger
        or is_aux_paradigm_row(ger)
        or is_declension_variant_row(ger)
        or is_interjection(ger)
    ):
        return None
    _, tokens, _ = extract_ranking_head(ger)
    if len(tokens) < 2 or tokens[-1] not in LIGHT_VERBS:
        return None
    if tokens[0] in LIGHT_VERBS and len(tokens) <= 2:
        return None
    if is_infinitive_token(tokens[0]) and tokens[0] == tokens[-1]:
        return None
    if light_verb_content_tokens(tokens) or tokens[0] in PREPOSITIONS | REFLEXIVE:
        return " ".join(tokens)
    return None


def is_verb_paradigm_row(ger: str, common_verbs: set[str] | None = None) -> bool:
    """Plain conjugation row: gehen geht… / machen macht… (verb is first head token)."""
    verbs = common_verbs if common_verbs is not None else get_common_verbs()
    if is_aux_paradigm_row(ger):
        return True
    _, head_tokens, _ = extract_ranking_head(ger)
    if not head_tokens or head_tokens[0] not in verbs:
        return False
    verb = head_tokens[0]
    if len(head_tokens) == 1:
        return True
    return all(
        t == verb or conjugated_after_infinitive(t, verb) for t in head_tokens[1:]
    )


def detect_compound_verb(
    ger: str, common_verbs: set[str] | None = None
) -> tuple[str, str] | None:
    """Modifier + verb (gut tun) — not a paradigm row; phrase key + infinitive lemma."""
    if (
        not ger
        or is_interjection(ger)
        or is_declension_variant_row(ger)
        or detect_idiom_phrase(ger)
        or is_verb_paradigm_row(ger, common_verbs)
    ):
        return None
    verbs = common_verbs if common_verbs is not None else get_common_verbs()
    _, head_tokens, _ = extract_ranking_head(ger)
    if len(head_tokens) < 2:
        return None
    entry_verbs = [t for t in head_tokens if t in verbs and is_infinitive_token(t)]
    if not entry_verbs:
        return None
    main_verb = entry_verbs[-1]
    if head_tokens[0] == main_verb:
        return None
    idx = len(head_tokens) - 1 - head_tokens[::-1].index(main_verb)
    phrase_tokens = head_tokens[: idx + 1]
    if len(phrase_tokens) < 2:
        return None
    return " ".join(phrase_tokens), main_verb


def compound_verb_lemma(ger: str, freq: dict[str, int]) -> str:
    """Lemma for modifier+verb rows — never an unrelated high-freq particle (gut tun → tun)."""
    compound = detect_compound_verb(ger)
    if not compound:
        return ""
    phrase_key, main_verb = compound
    phrase_tokens = phrase_key.split()
    # werden/sein/haben + modifier (übel werden → übel, not werden)
    if main_verb in IDIOM_AUX | {"werden"} and len(phrase_tokens) >= 2:
        content = light_verb_content_tokens(phrase_tokens)
        if content:
            return pick_lemma(content, freq)
    if main_verb in LIGHT_VERBS:
        content = light_verb_content_tokens(phrase_tokens)
        strong = [t for t in content if len(t) >= 5]
        if strong:
            return pick_lemma(strong, freq)
    return main_verb


def detect_compound_verb_phrase(ger: str) -> str | None:
    compound = detect_compound_verb(ger)
    return compound[0] if compound else None


def detect_lexical_phrase(ger: str) -> str | None:
    """Fixed multi-word phrases — corpus phrase score."""
    if not ger or is_interjection(ger):
        return None
    s = PAREN_PREFIX_RE.sub("", ger.strip())
    head = strip_grammar_suffix(s.split(",")[0])
    head = GRAMMAR_PAREN_RE.sub(" ", head)
    head = re.sub(r"\s+", " ", head).strip()
    tokens = truncate_head_at_conjugation(tokenize(head))
    if not tokens:
        return None
    key = " ".join(tokens)
    if key in LEXICAL_PHRASE_HEADS:
        return key
    if len(tokens) == 2 and tokens[0] in KEIN_FORMS:
        return key
    if len(tokens) >= 2 and tokens[0] == "es" and tokens[1] == "gibt":
        return "es gibt"
    return None


def detect_scored_phrase(ger: str) -> str | None:
    """Any row ranked by multi-word corpus hit."""
    return (
        detect_fixed_particle_phrase(ger)
        or detect_idiom_phrase(ger)
        or detect_lexical_phrase(ger)
        or detect_compound_verb_phrase(ger)
        or detect_verb_phrase(ger)
    )


def is_pure_grammar_template(ger: str) -> bool:
    """Pure grammar slot (+ subst., was für …, gegen+ A/für + A) — no fair vocab rank."""
    if detect_idiom_phrase(ger) or detect_lexical_phrase(ger):
        return False
    s = ger.strip()
    if re.search(r"\bes geht um\s+\+\s*[ADG]", s, re.I):
        return True
    if GRAMMAR_TEMPLATE_RE.search(s):
        return True
    if re.search(r"gegen\s*\+\s*[ADG].*für\s+\+", s, re.I):
        return True
    if re.match(r"^es\s+geht\s+um\b", strip_grammar_suffix(s.split(",")[0]), re.I):
        return True
    head = strip_grammar_suffix(s.split(",")[0])
    tokens = tokenize(GRAMMAR_PAREN_RE.sub(" ", head))
    if "+" in s and tokens and all(
        t in CASE_TAG_TOKENS
        or t in PREPOSITIONS
        or t in PHRASE_CONNECTORS
        or t in {"als", "wie", "was", "für", "gegen", "subst"}
        for t in tokens
    ):
        return True
    return False


def is_aux_paradigm_row(ger: str) -> bool:
    """Dictionary paradigm (haben hat, hatte / sein ist, war) — not an idiom row."""
    s = PAREN_PREFIX_RE.sub("", ger.strip())
    head = s.split(",")[0]
    tokens = tokenize(head)
    if not tokens:
        return False
    t0 = tokens[0]
    if t0 not in HEAD_VERBS:
        return False
    if t0 in {"können", "müssen", "sollen", "wollen", "dürfen"}:
        return len(tokens) <= 2
    if t0 in {"sein", "haben", "werden"}:
        if len(tokens) == 1:
            return True
        if len(tokens) == 2 and tokens[1] in SURFACE_FORM_SKIP:
            return True
    return False


def extract_idiom_head(ger: str) -> list[str]:
    """Head tokens for idioms: no grammar parens, +A/D, or conjugation tail."""
    s = PAREN_PREFIX_RE.sub("", ger.strip())
    head = strip_grammar_suffix(s.split(",")[0])
    head = GRAMMAR_PAREN_RE.sub(" ", head)
    head = re.sub(r"\s+", " ", head).strip()
    tokens: list[str] = []
    for t in tokenize(head):
        if t in CASE_TAG_TOKENS:
            break
        if tokens and tokens[-1] in IDIOM_AUX and t in SURFACE_FORM_SKIP:
            break
        tokens.append(t)
    return tokens


def idiom_content_candidates(tokens: list[str]) -> list[str]:
    """Lexical head of a sein/haben idiom (Lust, Ordnung) — not nicht/haben."""
    pool = tokens[:-1] if tokens and tokens[-1] in IDIOM_AUX else tokens
    return [
        t
        for t in pool
        if t not in IDIOM_FUNCTION_SKIP
        and t not in LIGHT_VERBS
        and t not in CASE_TAG_TOKENS
        and len(t) >= 3
    ]


def detect_idiom_phrase(ger: str) -> str | None:
    """Fixed expression with sein/haben (nicht in Ordnung sein, Lust haben)."""
    if not ger or not str(ger).strip():
        return None
    if is_interjection(ger) or is_aux_paradigm_row(ger):
        return None
    if detect_fixed_particle_phrase(ger):
        return None
    tokens = extract_idiom_head(ger)
    if len(tokens) < 2 or tokens[-1] not in IDIOM_AUX:
        return None
    if not idiom_content_candidates(tokens):
        return None
    return " ".join(tokens)


def extract_ranking_head(ger: str) -> tuple[str, list[str], set[str]]:
    """Clean head string, tokens, and declension tail set for rank_lemma."""
    s = PAREN_PREFIX_RE.sub("", str(ger).strip())
    head_raw, _, tail = s.partition(",")
    head_raw = strip_grammar_suffix(head_raw)
    head_raw = GRAMMAR_PAREN_RE.sub(" ", head_raw)
    head_raw = re.sub(r"\s+", " ", head_raw).strip()
    head_tokens: list[str] = []
    for t in tokenize(head_raw):
        if t in CASE_TAG_TOKENS:
            break
        if head_tokens and head_tokens[-1] in IDIOM_AUX and t in SURFACE_FORM_SKIP:
            break
        head_tokens.append(t)
    head_tokens = truncate_head_at_conjugation(head_tokens)
    tail_set = set(tokenize(clean_declension_tail(tail)))
    return head_raw, head_tokens, tail_set


def normalize_phrase_head(ger: str) -> str:
    head = ger.split(",")[0]
    head = ELLIPSIS_RE.sub(" ", head)
    head = re.sub(r"\s+", " ", head).strip()
    return head


def detect_fixed_particle_phrase(ger: str) -> str | None:
    """Multi-word function phrase (ab und zu), not a single prep/particle entry."""
    if not ger or not str(ger).strip():
        return None
    s = PAREN_PREFIX_RE.sub("", str(ger).strip())
    if "+" in s or "!" in s or GRAMMAR_CASE.search(s):
        return None
    head = normalize_phrase_head(s)
    tokens = tokenize(head)
    if len(tokens) < 2:
        return None
    if any(t in ARTICLES for t in tokens):
        return None
    if not all(t in PARTICLE_LEXICON for t in tokens):
        return None
    has_connector = any(t in PHRASE_CONNECTORS for t in tokens)
    n_prep = sum(1 for t in tokens if t in PREPOSITIONS)
    has_hin_her = "hin" in tokens and (
        "her" in tokens or "zurück" in tokens or "auf" in tokens or "ab" in tokens
    )
    if not (has_connector or n_prep >= 2 or has_hin_her or len(tokens) == 2):
        return None
    return " ".join(tokens)


def count_phrases_in_corpus(
    sentences_path: Path,
    token_phrases: dict[str, list[str]],
    regex_phrases: dict[str, str],
) -> dict[str, int]:
    """Count exact token sequences (and regex correlatives) in Leipzig sentences."""
    counts = {k: 0 for k in token_phrases}
    counts.update({k: 0 for k in regex_phrases})
    if not counts:
        return counts
    from collections import defaultdict

    by_first: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    for key, ptoks in token_phrases.items():
        by_first[ptoks[0]].append((key, ptoks))
    for first in by_first:
        by_first[first].sort(key=lambda x: -len(x[1]))
    compiled = [(k, re.compile(p, re.I)) for k, p in regex_phrases.items()]
    with sentences_path.open(encoding="utf-8") as f:
        for line in f:
            text = line.split("\t", 1)[-1] if "\t" in line else line
            toks = tokenize(text)
            for i, t in enumerate(toks):
                for key, ptoks in by_first.get(t, ()):
                    n = len(ptoks)
                    if i + n <= len(toks) and toks[i : i + n] == ptoks:
                        counts[key] += 1
            for key, rx in compiled:
                if rx.search(text):
                    counts[key] += 1
    return counts


def collect_phrase_specs(ger_rows: list[str]) -> tuple[dict[str, list[str]], dict[str, str]]:
    token_phrases: dict[str, list[str]] = {}
    regex_phrases: dict[str, str] = {}
    for ger in ger_rows:
        key = detect_scored_phrase(ger)
        if not key:
            continue
        if key in PHRASE_REGEX:
            regex_phrases[key] = PHRASE_REGEX[key]
        elif key not in token_phrases:
            token_phrases[key] = key.split()
    return token_phrases, regex_phrases


def is_interjection(ger: str) -> bool:
    s = ger.strip()
    return s.endswith("!") and len(tokenize(s)) <= 6


def modifier_tokens(head_tokens: list[str]) -> list[str]:
    """Content words for ranking — not preps, aux, or sentence particles."""
    skip = (
        PREPOSITIONS
        | ARTICLES
        | TAIL_SKIP
        | REFLEXIVE
        | AUX
        | SURFACE_FORM_SKIP
        | {
            "nicht",
            "auch",
            "noch",
            "schon",
            "sehr",
            "gar",
            "so",
            "nur",
            "ja",
            "doch",
            "weder",
            "hier",
            "dort",
            "da",
            "mal",
        }
    )
    return [t for t in head_tokens if t not in skip and len(t) >= 3]


def is_grammar_primary_row(ger: str) -> bool:
    """Bare case frame (+ D) or grammar template — not a lexical idiom."""
    if is_pure_grammar_template(ger):
        return True
    if detect_idiom_phrase(ger):
        return False
    s = ger.strip()
    if re.fullmatch(r"[A-Za-zÄÖÜäöüß+ ]+", s) and re.search(
        r"^\s*(?:[A-Za-zÄÖÜäöüß]+\s+)?\+\s*[ADG]\s*$", s, re.I
    ):
        return True
    if re.match(r"^\s*[a-zäöüß]+\s*\+\s*[ADG]\s*(?:\(prep\.\))?\s*$", s, re.I):
        return True
    head = strip_grammar_suffix(s.split(",")[0])
    tokens = tokenize(GRAMMAR_PAREN_RE.sub(" ", head))
    if "+" in s and not idiom_content_candidates(
        tokens if tokens and tokens[-1] in IDIOM_AUX else tokens
    ):
        content = content_tokens(tokens, skip_verbs=True)
        if not content or all(t in CASE_TAG_TOKENS for t in content):
            return True
    return False


def row_kind(ger: str, lemma: str) -> str:
    """vocab | interjection | grammar."""
    if is_interjection(ger):
        return "interjection"
    if is_grammar_primary_row(ger):
        return "grammar"
    if not lemma:
        return "grammar"
    return "vocab"


def rank_lemma(ger: str, freq: dict[str, int]) -> str:
    """One dictionary headword per vocabulary row (for fair ranking)."""
    if not ger or not str(ger).strip():
        return ""

    s = PAREN_PREFIX_RE.sub("", str(ger).strip())
    tokens = tokenize(s)
    if not tokens:
        return ""
    if len(tokens) == 1:
        return tokens[0]

    _, head_tokens, tail_set = extract_ranking_head(ger)
    if not head_tokens:
        return tokens[0]

    paradigm = infer_paradigm_lemma(ger)
    if paradigm:
        return paradigm

    compound = detect_compound_verb(ger)
    if compound:
        return compound_verb_lemma(ger, freq)

    # Interjection / formula (Gott sei Dank!) — content word, never sei/war/…
    if is_interjection(s):
        mods = modifier_tokens(head_tokens)
        if mods:
            return pick_lemma(mods, freq)
        return ""

    # Main paradigm row: machen macht… / können kann… (verb is first token)
    t0 = head_tokens[0]
    if (
        len(t0) >= 4
        and t0.endswith("en")
        and t0 not in ARTICLES
        and t0 not in REFLEXIVE
        and t0 not in SURFACE_FORM_SKIP
    ):
        return t0

    # wie lange / wie spät → lange / spät (not wie)
    if len(head_tokens) == 2 and head_tokens[0] == "wie":
        return head_tokens[1]

    # brauchen zu / verb zu + Inf. → main verb (not nicht)
    if "zu" in head_tokens:
        verb = head_main_infinitive(head_tokens, tail_set)
        if verb:
            return verb

    # kein/keine + noun (keine Ahnung → ahnung)
    if len(head_tokens) == 2 and head_tokens[0] in KEIN_FORMS:
        return head_tokens[1]

    # Impersonal es gibt → phrase es gibt (not es)
    if len(head_tokens) >= 2 and head_tokens[0] == "es" and head_tokens[1] == "gibt":
        return "gibt"

    # Light-verb / phrasal verb: Schlange stehen, Bett machen, Sauna gehen
    lv_content = light_verb_content_tokens(head_tokens)
    if lv_content:
        return pick_lemma(lv_content, freq)

    # einen Arzt rufen → rufen (article + noun + infinitive, rufen not light-verb ranked)
    if head_tokens[0] in ARTICLES:
        verb = head_main_infinitive(head_tokens, tail_set)
        if verb and verb not in LIGHT_VERBS:
            return verb
        if verb and not lv_content:
            noun = [
                t
                for t in head_tokens[1:-1]
                if t not in ARTICLES and t not in PREPOSITIONS and len(t) >= 3
            ]
            if noun:
                return pick_lemma(noun, freq)
            return verb

    # so etwas = so was → etwas (not was)
    if "etwas" in head_tokens and "was" in head_tokens:
        return "etwas"

    # etwas zum Schreiben → schreiben (not etwas)
    if (
        len(head_tokens) >= 3
        and head_tokens[0] == "etwas"
        and head_tokens[1] in {"zu", "zum", "zur"}
    ):
        noun = head_tokens[-1]
        if len(noun) >= 4 and noun.endswith("en"):
            return noun

    # sein/haben idioms: content word only (in Ordnung sein → ordnung)
    if len(head_tokens) >= 2 and head_tokens[-1] in IDIOM_AUX:
        content = idiom_content_candidates(head_tokens)
        if content:
            return pick_lemma(content, freq)

    # Case frames / reflexive patterns (skip when idiom has lexical content)
    if ("+" in s or GRAMMAR_CASE.search(s)) and not idiom_content_candidates(
        head_tokens if head_tokens and head_tokens[-1] in IDIOM_AUX else []
    ):
        content = content_tokens(head_tokens, skip_verbs=True)
        if content:
            return pick_lemma(content, freq)
        return ""

    # der Mann, das Haus, … (ignore tail: may repeat noun in "die Soße, -n")
    if head_tokens[0] in ARTICLES:
        for t in head_tokens[1:]:
            if len(t) >= 2:
                return t

    # Conjugation list after comma: geben gibt, gab, … → geben (not long phrases before comma)
    if (
        "," in s
        and head_tokens[0] not in ARTICLES
        and head_tokens[0] not in REFLEXIVE
        and len(head_tokens) <= 2
    ):
        t0 = head_tokens[0]
        if t0 not in tail_set:
            return t0

    # Reflexive + verb early (before comma rule could pick sich)
    if head_tokens and head_tokens[0] in REFLEXIVE:
        verb = head_infinitive(head_tokens, tail_set)
        if verb:
            return verb

    # fertig werden / schwindlig werden / nicht schlecht → modifier, not werden/nicht
    modifiers = modifier_tokens(head_tokens)
    if modifiers and any(t in LIGHT_VERBS for t in head_tokens):
        heavy = [
            t
            for t in modifiers
            if t not in LIGHT_VERBS and t not in SURFACE_FORM_SKIP
        ]
        if heavy:
            return pick_lemma(heavy, freq)
    if modifiers and "nicht" in head_tokens:
        heavy = [t for t in modifiers if t != "nicht"]
        if heavy:
            return pick_lemma(heavy, freq)

    # Phrase starting with a preposition: content noun, not gehen/stehen alone
    if head_tokens and head_tokens[0] in PREPOSITIONS:
        lv = light_verb_content_tokens(head_tokens)
        if lv:
            return pick_lemma(lv, freq)
        content = content_tokens(head_tokens, skip_verbs=True)
        if content:
            return pick_lemma(content, freq)

    # Main verb infinitive (sich Mühe geben → geben; plain werden → werden)
    for t in head_tokens:
        if len(t) >= 4 and t.endswith("en") and t not in tail_set:
            if t not in IDIOM_AUX or is_aux_paradigm_row(ger):
                return t

    # … sein / haben only for paradigm rows, not idioms
    if is_aux_paradigm_row(ger):
        for t in reversed(head_tokens):
            if t in HEAD_VERBS and t not in SURFACE_FORM_SKIP:
                return t

    if modifiers:
        return pick_lemma(modifiers, freq)

    return head_tokens[0]


def sanitize_cell(value: object) -> str:
    """One physical line per CSV row (Rainbow CSV / Excel friendly)."""
    if value is None:
        return ""
    s = str(value).replace("\xad", "")
    s = s.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    s = re.sub(r"  +", " ", s)
    return s.strip()


def score_lemma(lemma: str, freq: dict[str, int]) -> tuple[int, str]:
    n = freq.get(lemma, 0)
    if n:
        return n, f"{lemma}:{n}"
    return 0, ""


def score_entry(
    ger_s: str,
    freq: dict[str, int],
    phrase_freq: dict[str, int],
) -> dict[str, object]:
    """Lemma, frequency, kind, and freq_forms for one vocabulary row."""
    if is_interjection(ger_s):
        _, ht, _ = extract_ranking_head(ger_s)
        mods = modifier_tokens(ht)
        lemma = pick_lemma(mods, freq) if mods else ""
        total, freq_forms = score_lemma(lemma, freq)
        return {
            "kind": "interjection",
            "lemma": lemma,
            "freq_total": total,
            "freq_forms": freq_forms,
        }

    if is_pure_grammar_template(ger_s):
        return {"kind": "grammar", "lemma": "", "freq_total": 0, "freq_forms": ""}

    if is_declension_variant_row(ger_s):
        return {"kind": "grammar", "lemma": "", "freq_total": 0, "freq_forms": ""}

    # Subordinate-clause marker rows (wenn (alottaa …)) — grammar, not high-freq wenn
    if re.search(r"\(alottaa\s+sivu", ger_s, re.I) and rank_lemma(ger_s, freq) in {
        "wenn",
        "als",
        "dass",
        "daß",
    }:
        return {"kind": "grammar", "lemma": "", "freq_total": 0, "freq_forms": ""}

    phrase_key = detect_scored_phrase(ger_s)
    if phrase_key:
        total = phrase_freq.get(phrase_key, 0)
        if total:
            return {
                "kind": "vocab",
                "lemma": phrase_key,
                "freq_total": total,
                "freq_forms": f"phrase:{phrase_key}:{total}",
            }
        idiom = detect_idiom_phrase(ger_s)
        if idiom:
            content = pick_lemma(idiom_content_candidates(idiom.split()), freq)
            lemma = content or idiom
            total, freq_forms = score_lemma(lemma, freq)
            return {
                "kind": "vocab" if total else "idiom_miss",
                "lemma": lemma,
                "freq_total": total,
                "freq_forms": freq_forms,
            }
        if detect_verb_phrase(ger_s) or detect_lexical_phrase(ger_s):
            lemma = rank_lemma(ger_s, freq)
            total, freq_forms = score_lemma(lemma, freq)
            return {
                "kind": "vocab" if total else "idiom_miss",
                "lemma": lemma,
                "freq_total": total,
                "freq_forms": freq_forms,
            }
        compound = detect_compound_verb(ger_s)
        if compound:
            lemma = compound_verb_lemma(ger_s, freq)
            total, freq_forms = score_lemma(lemma, freq)
            return {
                "kind": "vocab" if total else "idiom_miss",
                "lemma": lemma,
                "freq_total": total,
                "freq_forms": freq_forms,
            }
        return {
            "kind": "phrase_miss",
            "lemma": phrase_key,
            "freq_total": 0,
            "freq_forms": "",
        }

    lemma = rank_lemma(ger_s, freq)
    total, freq_forms = score_lemma(lemma, freq)
    kind = row_kind(ger_s, lemma)
    if kind == "grammar" and is_pure_grammar_template(ger_s):
        return {"kind": "grammar", "lemma": "", "freq_total": 0, "freq_forms": ""}
    return {
        "kind": kind,
        "lemma": lemma,
        "freq_total": total,
        "freq_forms": freq_forms,
    }


def main() -> None:
    in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IN
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUT

    try:
        import openpyxl
    except ImportError as e:
        raise SystemExit("openpyxl required: pip install openpyxl") from e

    if not WORDS.is_file():
        raise SystemExit(f"Corpus word list not found: {WORDS}")
    if not in_path.is_file():
        raise SystemExit(f"Input not found: {in_path}")

    freq = load_freq(WORDS)
    common_verbs = load_common_verbs()
    if common_verbs:
        global _COMMON_VERBS
        _COMMON_VERBS = common_verbs
    wb = openpyxl.load_workbook(in_path, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [sanitize_cell(c) for c in rows[0]]
    data = rows[1:]

    ger_rows = [sanitize_cell(r[0]) for r in data]
    token_phrases, regex_phrases = collect_phrase_specs(ger_rows)
    phrase_freq: dict[str, int] = {}
    if token_phrases or regex_phrases:
        if not SENTENCES.is_file():
            raise SystemExit(f"Corpus sentences not found: {SENTENCES}")
        phrase_freq = count_phrases_in_corpus(
            SENTENCES, token_phrases, regex_phrases
        )

    scored: list[dict] = []
    for r in data:
        cells = list(r) + [None] * 4
        ger, c2, fin, ex = cells[:4]
        ger_s = sanitize_cell(ger)
        scored_row = score_entry(ger_s, freq, phrase_freq)
        scored.append(
            {
                "kind": scored_row["kind"],
                "lemma": scored_row["lemma"],
                "freq_total": scored_row["freq_total"],
                "freq_forms": scored_row["freq_forms"],
                "ger": ger_s,
                "col2": sanitize_cell(c2),
                "fin": sanitize_cell(fin),
                "example": sanitize_cell(ex),
            }
        )

    kind_order = {
        "vocab": 0,
        "interjection": 1,
        "grammar": 2,
        "phrase_miss": 3,
        "idiom_miss": 3,
    }
    scored.sort(
        key=lambda row: (
            kind_order.get(row["kind"], 1),
            -row["freq_total"],
            row["ger"].lower(),
        )
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(["rank", "kind", "lemma", "freq_total", "freq_forms", *header])
        for i, row in enumerate(scored, 1):
            w.writerow(
                [
                    i,
                    row["kind"],
                    row["lemma"],
                    row["freq_total"],
                    row["freq_forms"],
                    row["ger"],
                    row["col2"],
                    row["fin"],
                    row["example"],
                ]
            )

    zero = sum(1 for r in scored if r["freq_total"] == 0)
    print(f"Wrote {out_path} ({len(scored)} rows, {zero} with freq_total=0)")
    print("Top 10:")
    for r in scored[:10]:
        print(f"  {r['freq_total']:>8}  {r['ger'][:60]}")


if __name__ == "__main__":
    main()
