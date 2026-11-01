#!/usr/bin/env Rscript
# Compare fi_praesens.csv ranks 121-140 against expected user batch.

for (loc in c("en_US.UTF-8", "C.UTF-8", "en_US.utf8")) {
  if (!is.na(Sys.setlocale("LC_CTYPE", loc))) break
}

norm_suomi <- function(s) {
  s <- trimws(tolower(s))
  s <- gsub('^"|"$', "", s)
  s <- gsub(",\\s*", "/", s)
  s
}

norm_de <- function(s, person) {
  s <- trimws(tolower(s))
  prefix <- switch(
    person,
    ich = "^ich ",
    du = "^du ",
    er = "^er ",
    wir = "^wir ",
    ihr = "^ihr ",
    sie = "^sie ",
    ""
  )
  sub(prefix, "", s)
}

norm_fi <- function(s) trimws(tolower(s))

user <- list(
  list(rank = 121L, inf = "biegen", su = "kääntyä",
       de = c("biege", "biegst", "biegt", "biegen", "biegt", "biegen"),
       fi = c("minä käännyn", "sinä käännyt", "hän kääntyy", "me käännymme", "te käännytte", "he kääntyvät")),
  list(rank = 122L, inf = "betrügen", su = "pettää",
       de = c("betrüge", "betrügst", "betrügt", "betrügen", "betrügt", "betrügen"),
       fi = c("minä petän", "sinä petät", "hän pettää", "me petämme", "te petätte", "he pettävät")),
  list(rank = 123L, inf = "pfeifen", su = "viheltää",
       de = c("pfeife", "pfeifst", "pfeift", "pfeifen", "pfeift", "pfeifen"),
       fi = c("minä vihellän", "sinä vihellät", "hän viheltää", "me vihellämme", "te vihellätte", "he viheltävät")),
  list(rank = 124L, inf = "reiten", su = "ratsastaa",
       de = c("reite", "reitest", "reitet", "reiten", "reitet", "reiten"),
       fi = c("minä ratsastan", "sinä ratsastat", "hän ratsastaa", "me ratsastamme", "te ratsastatte", "he ratsastavat")),
  list(rank = 125L, inf = "schmelzen", su = "sulattaa",
       de = c("schmelze", "schmilzst", "schmilzt", "schmelzen", "schmilzt", "schmelzen"),
       fi = c("minä sulatan", "sinä sulatat", "hän sulattaa", "me sulatamme", "te sulatatte", "he sulattavat")),
  list(rank = 126L, inf = "schmelzen", su = "sulaa",
       de = c("schmelze", "schmilzst", "schmilzt", "schmelzen", "schmilzt", "schmelzen"),
       fi = c("minä sulan", "sinä sulat", "hän sulaa", "me sulamme", "te sulatte", "he sulavat")),
  list(rank = 127L, inf = "leihen", su = "lainata",
       de = c("leihe", "leihst", "leiht", "leihen", "leiht", "leihen"),
       fi = c("minä lainaan", "sinä lainaat", "hän lainaa", "me lainaamme", "te lainaatte", "he lainaavat")),
  list(rank = 128L, inf = "blasen", su = "puhaltaa",
       de = c("blase", "bläst", "bläst", "blasen", "blast", "blasen"),
       fi = c("minä puhallan", "sinä puhallat", "hän puhaltaa", "me puhallamme", "te puhallatte", "he puhaltavat")),
  list(rank = 129L, inf = "schmeißen", su = "paiskata, heittää",
       de = c("schmeiße", "schmeißt", "schmeißt", "schmeißen", "schmeißt", "schmeißen"),
       fi = c("minä paiskaan", "sinä paiskaat", "hän paiskaa", "me paiskaamme", "te paiskaatte", "he paiskaavat")),
  list(rank = 130L, inf = "erschrecken", su = "pelästyä",
       de = c("erschrecke", "erschrickst", "erschrickt", "erschrecken", "erschrickt", "erschrecken"),
       fi = c("minä pelästyn", "sinä pelästyt", "hän pelästyy", "me pelästymme", "te pelästytte", "he pelästyvät")),
  list(rank = 131L, inf = "schleichen", su = "hiipiä",
       de = c("schleiche", "schleichst", "schleicht", "schleichen", "schleicht", "schleichen"),
       fi = c("minä hiivin", "sinä hiivit", "hän hiipii", "me hiivimme", "te hiivitte", "he hiipivät")),
  list(rank = 132L, inf = "braten", su = "paistaa",
       de = c("brate", "brätst", "brät", "braten", "bratet", "braten"),
       fi = c("minä paistan", "sinä paistat", "hän paistaa", "me paistamme", "te paistatte", "he paistavat")),
  list(rank = 133L, inf = "gleiten", su = "liukua, lipua",
       de = c("gleite", "gleitest", "gleitet", "gleiten", "gleitet", "gleiten"),
       fi = c("minä liu'un", "sinä liu'ut", "hän liukuu", "me liu'umme", "te liu'utte", "he liukuvat")),
  list(rank = 134L, inf = "schwören", su = "vannoa",
       de = c("schwöre", "schwörst", "schwört", "schwören", "schwört", "schwören"),
       fi = c("minä vannon", "sinä vannot", "hän vannoo", "me vannomme", "te vannotte", "he vannovat")),
  list(rank = 135L, inf = "frieren", su = "palella",
       de = c("friere", "frierst", "friert", "frieren", "friert", "frieren"),
       fi = c("minä palelen", "sinä palelet", "hän palelee", "me palelemme", "te palelette", "he palelevat")),
  list(rank = 136L, inf = "verzeihen", su = "antaa anteeksi",
       de = c("verzeihe", "verzeihst", "verzeiht", "verzeihen", "verzeiht", "verzeihen"),
       fi = c("minä annan anteeksi", "sinä annat anteeksi", "hän antaa anteeksi", "me annamme anteeksi", "te annatte anteeksi", "he antavat anteeksi")),
  list(rank = 137L, inf = "verderben", su = "turmella, pilata",
       de = c("verderbe", "verdirbst", "verdirbt", "verderben", "verdirbt", "verderben"),
       fi = c("minä pilaan", "sinä pilaat", "hän pilaa", "me pilaamme", "te pilaatte", "he pilaavat")),
  list(rank = 138L, inf = "verderben", su = "turmeltua, pilaantua",
       de = c("verderbe", "verdirbst", "verdirbt", "verderben", "verdirbt", "verderben"),
       fi = c("minä pilaannun", "sinä pilaannut", "hän pilaantuu", "me pilaannumme", "te pilaannutte", "he pilaantuvat")),
  list(rank = 139L, inf = "jdm befehlen", su = "käskeä",
       de = c("befehle", "befiehlst", "befiehlt", "befehlen", "befehlt", "befehlen"),
       fi = c("minä käsken", "sinä käsket", "hän käskee", "me käskemme", "te käskette", "he käskevät")),
  list(rank = 140L, inf = "kriechen", su = "ryömiä, madella",
       de = c("krieche", "kriechst", "kriecht", "kriechen", "kriecht", "kriechen"),
       fi = c("minä ryömin", "sinä ryömit", "hän ryömii", "me ryömimme", "te ryömitte", "he ryömivät"))
)

df <- read.csv(
  "saksa_epasaannolliset_verbit_fi_praesens.csv",
  stringsAsFactors = FALSE,
  fileEncoding = "UTF-8",
  strip.white = TRUE
)
df$rank <- as.integer(df$rank)

de_cols <- c("ich", "du", "er", "wir", "ihr", "sie")
fi_cols <- c("minä", "sinä", "hän", "me", "te", "he")

issues <- character()
for (u in user) {
  row <- df[df$rank == u$rank, , drop = FALSE]
  if (!nrow(row)) {
    issues <- c(issues, sprintf("%d: missing row", u$rank))
    next
  }
  if (trimws(row$infinitive) != u$inf) {
    issues <- c(issues, sprintf(
      "%d infinitive: file=%s user=%s", u$rank, row$infinitive, u$inf
    ))
  }
  if (norm_suomi(row$suomi) != norm_suomi(u$su)) {
    issues <- c(issues, sprintf(
      "%d suomi: file=%s user=%s", u$rank, row$suomi, u$su
    ))
  }
  for (j in seq_along(de_cols)) {
    pk <- de_cols[j]
    file_de <- norm_de(row[[pk]], pk)
    if (file_de != norm_de(u$de[j], pk)) {
      issues <- c(issues, sprintf(
        "%d DE %s: file=%s user=%s", u$rank, pk, file_de, u$de[j]
      ))
    }
    file_fi <- norm_fi(row[[fi_cols[j]]])
    if (file_fi != norm_fi(u$fi[j])) {
      issues <- c(issues, sprintf(
        "%d FI %s: file=%s user=%s", u$rank, fi_cols[j], file_fi, u$fi[j]
      ))
    }
  }
}

cat("=== Batch 121-140 vs your paste ===\n")
if (!length(issues)) {
  cat("All 20 rows match (12 forms each; suomi comma/slash normalized).\n")
} else {
  cat(paste(issues, collapse = "\n"), "\n")
}

form_cols <- c(de_cols, fi_cols)
bad <- integer()
for (r in seq_len(nrow(df))) {
  for (c in form_cols) {
    if (is.na(df[r, c]) || !nzchar(trimws(df[r, c]))) bad <- c(bad, df$rank[r])
  }
}
bad <- unique(bad)

cat("=== Full file saksa_epasaannolliset_verbit_fi_praesens.csv ===\n")
cat("Rows:", nrow(df), "| ranks:", min(df$rank), "-", max(df$rank), "\n")
cat("840 form cells (140 x 12):", if (length(bad)) "INCOMPLETE" else "all filled", "\n")
if (length(bad)) cat("Ranks with gaps:", paste(bad, collapse = ", "), "\n")
