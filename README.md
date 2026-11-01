# Learn German Irregular Verbs

Free interactive drills for 100 essential German irregular verbs, in Finnish and English.

**Suomeksi:** Opi saksan epäsäännölliset verbit — maksuttomia taivutus- ja lauseharjoituksia sadasta tärkeästä verbistä.

## Exercises

- **Principal parts:** practise the infinitive, third-person present, third-person simple past and perfect.
- **Conjugation:** practise personal forms in the present, simple past (Präteritum) and perfect.
- **Complete the sentences:** fill in missing verb forms.
- **Write the whole sentence:** translate the same prompts into complete German sentences.

Reference tables cover the selected verbs, the six modal verbs and **sein**. The author-selected verbs are ordered by frequency, with exercises grouped into sets of ten verbs.

Exercises run in the browser using JavaScript, with immediate feedback and highlighted corrections. No account is required.

## View locally

The ready-built site is in `_book/`:

- Finnish: `_book/index.html`
- English: `_book/en/index.html`

To serve it locally, run this command from the project root:

```sh
python3 -m http.server 8000 --directory _book
```

Then open <http://localhost:8000/> or <http://localhost:8000/en/>.

## Build and publish

The site uses R Markdown, bookdown/GitBook and JavaScript. To rebuild both language versions, install Python 3, R, Pandoc and the R packages **bookdown**, **rmarkdown**, **htmltools** and **jsonlite**, then run:

```sh
python3 scripts/build_site.py
```

For Git-connected Netlify deployment, commit the generated `_book/` directory, set the publish directory to `_book` and leave the build command empty.

See [BUILD.md](BUILD.md) for the file layout, maintenance commands and tests.

## License

© 2026 [Ville Langén](https://www.linkedin.com/in/ville-langen/).

This project's original content is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). Bundled third-party libraries retain their own licenses.
