# Reza Aliasgari Renani

Personal website: **https://rezaaliasgarirenani.github.io/**

A small, static, multipage site built with HTML, CSS, and JavaScript. The screen palette is exactly `rgb(0, 0, 0)` for the background and `rgb(200, 200, 200)` for text, with system monospace fonts.

## Source files

- `index.html` — personal details, roles, and education timelines.
- `research.html` — RTL and verification, semiconductor physics, and plasma systems.
- `publications.html` — journal articles, conference papers, posters, and presentations.
- `about.html` — background, skills, languages, contacts, and academic profiles.
- `src/site.css` — shared layout, typography, and responsive/print styles.
- `src/terminal.js` — brief line-by-line reveal on Home. Visitors can skip it; reduced-motion preferences show everything immediately. All content and navigation also work without JavaScript.
- `assets/reza_aliasgari_renani.png` — portrait used in the circular Home link and favicon.
- `assets/reza_aliasgari_renani_cv.pdf` — downloadable English two-page CV.

Each HTML file is directly accessible and has its own title, canonical URL, and active navigation. The header and footer are plain HTML in each file; update all four copies when changing shared links. There is no client-side router, framework, or package installation required.

## Preview

From this repository in WSL:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$PWD"
```

From Windows PowerShell:

```powershell
.\preview.ps1
```

Open **http://localhost:8000/** in Chrome. Save edits and refresh. Press `Ctrl+C` to stop the preview. Use another port if one is already occupied.

## Verify and publish

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
```

Use `python` in native Windows if that is the installed command.

The build stages only the four public HTML pages, `assets/`, `src/`, `.nojekyll`, and crawler files in `dist/`. It validates all required inputs before replacing that generated directory. Source documentation, scripts, and tests are not published. `dist/` is ignored by Git and is not needed for local preview.

Commit and push to `main` to publish through GitHub Actions. The workflow runs the deployment tests and build before deploying. Changes to any root HTML page trigger publication; every page is listed in `sitemap.xml`.

## Updating information

The English two-page CV in `../reza/documents/CVR/english/2_page/` is the default content reference. Check Home's role and education timelines, the Research details, the Publications list, and About's skill groups when updating professional information. Keep the two profile READMEs in `../reza/` and `../rezaaliasgarirenani/` synchronized separately.

Replace `assets/reza_aliasgari_renani_cv.pdf` when that CV changes and update the `?v=` value on CV links in all four pages to refresh browser caches. Update the stylesheet version in all four pages after changing shared CSS.
