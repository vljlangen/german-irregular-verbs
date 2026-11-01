# Shared Bookdown data and widget helpers.
for (loc in c("en_US.UTF-8", "C.UTF-8", "en_US.utf8")) {
  if (!is.na(Sys.setlocale("LC_CTYPE", loc))) break
}
read_conj_csv <- function(path) {
  df <- read.csv(path, stringsAsFactors = FALSE, fileEncoding = "UTF-8", strip.white = TRUE, na.strings = NULL, colClasses = "character")
  df$rank <- as.integer(df$rank)
  df
}
emit_json <- function(id, rows) {
  cat('<script type="application/json" id="', id, '">',
      jsonlite::toJSON(rows, dataframe = "rows", auto_unbox = TRUE),
      "</script>\n", sep = "")
}
emit_heart_data <- function() {
  emit_json("verbs-heart-data", read_conj_csv("saksa_epasaannolliset_verbit_ranked.csv"))
}
emit_conj_data <- function() {
for (loc in c("en_US.UTF-8", "C.UTF-8", "en_US.utf8")) {
  if (!is.na(Sys.setlocale("LC_CTYPE", loc))) break
}

library(jsonlite)

read_conj_csv <- function(path) {
  df <- read.csv(path, stringsAsFactors = FALSE, fileEncoding = "UTF-8", strip.white = TRUE, na.strings = NULL, colClasses = "character")
  df$rank <- as.integer(df$rank)
  df
}

p_cols <- c("ich", "du", "er", "wir", "ihr", "sie")

row_forms <- function(df) {
  apply(df[p_cols], 1, function(r) as.list(setNames(as.character(r), p_cols)))
}

strip_de_pronoun <- function(text, person) {
  text <- trimws(text)
  prefix <- switch(
    person,
    ich = "ich ",
    du = "du ",
    er = if (startsWith(text, "es ")) "es " else "er ",
    wir = "wir ",
    ihr = "ihr ",
    sie = "sie ",
    ""
  )
  if (nzchar(prefix) && startsWith(tolower(text), prefix)) {
    trimws(substr(text, nchar(prefix) + 1L, nchar(text)))
  } else {
    text
  }
}

row_present_fi <- function(row) {
  fi_col <- c(
    ich = "minä", du = "sinä", er = "hän", wir = "me", ihr = "te", sie = "he"
  )
  forms <- vector("list", length(p_cols))
  names(forms) <- p_cols
  for (pk in p_cols) {
    forms[[pk]] <- list(
      fi = as.character(row[[fi_col[[pk]]]]),
      answer = strip_de_pronoun(as.character(row[[pk]]), pk)
    )
  }
  forms
}

fi_pr <- read_conj_csv("saksa_epasaannolliset_verbit_fi_praesens.csv")
pt <- read_conj_csv("saksa_epasaannolliset_verbit_praeteritum.csv")
pf <- read_conj_csv("saksa_epasaannolliset_verbit_perfekt.csv")

present_fi <- lapply(seq_len(nrow(fi_pr)), function(i) row_present_fi(fi_pr[i, , drop = FALSE]))

pt_m <- pt[match(fi_pr$rank, pt$rank), , drop = FALSE]
pf_m <- pf[match(fi_pr$rank, pf$rank), , drop = FALSE]

verbs_conj <- data.frame(
  rank = fi_pr$rank,
  infinitive = fi_pr$infinitive,
  suomi = fi_pr$suomi,
  present = I(present_fi),
  preterite = I(row_forms(pt_m)),
  perfect = I(row_forms(pf_m)),
  stringsAsFactors = FALSE
)

cat(
  '<script type="application/json" id="verbs-conj-data">',
  toJSON(verbs_conj, dataframe = "rows", auto_unbox = TRUE),
  "</script>\n",
  sep = ""
)
}
emit_sentence_data <- function() {
  rows <- lapply(c("praesens", "praeteritum", "perfekt"), function(tense) {
    read_conj_csv(paste0("saksa_epasaannolliset_verbit_lauseharjoitus_", tense, ".csv"))
  })
  emit_json("sentence-drill-data", do.call(rbind, rows))
}
drill_widget <- function(file, tense, title) {
  html <- readLines(file, encoding = "UTF-8", warn = FALSE)
  html <- gsub("__TENSE__", tense, html, fixed = TRUE)
  html <- gsub("__TITLE__", title, html, fixed = TRUE)
  htmltools::HTML(paste(html, collapse = "\n"))
}
drill_scripts <- function(type) {
  htmltools::tagList(
    htmltools::tags$script(src = "www/drill-common.js"),
    htmltools::tags$script(src = paste0("www/drill-", type, ".js"))
  )
}
