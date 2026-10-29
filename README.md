# Reza Aliasgari Renani

Personal website: **https://rezaaliasgarirenani.github.io/**

A small, static, multipage site built with HTML, CSS, and JavaScript. The base screen palette is `rgb(0, 0, 0)` for the background and `rgb(225, 225, 225)` for text, with system monospace fonts. Restrained GitHub Dark Colorblind blue (`#58a6ff`) and amber (`#d29922`) accents mark terminal title bars, panel numbers, and timeline markers.

## Source files

- `index.html` — three terminal-style panels for personal information, research experience, and education. The profile starts immediately after the name.
- `research.html` — RTL and verification, semiconductor physics, and plasma systems.
- `publications.html` — journal articles, conference papers, posters, and presentations.
- `about.html` — background, skills, languages, contacts, and academic profiles.
- `src/site.css` — shared layout, typography, and responsive/print styles.
- `src/terminal.js` — line-by-line reveal on Home, with `LINE_DELAY_MS = 50` (50 milliseconds between lines). The 30 current output units take approximately 1.45 seconds in total. Footer links remain visible independently of the reveal. Visitors can skip the reveal; reduced-motion preferences show everything immediately. All content and navigation also work without JavaScript.
- `assets/reza_aliasgari_renani.png` — portrait used in the circular Home link.
- `assets/chip_radiation_logo.png` — chip logos on both sides of the header and footer, and the browser favicon.
- `assets/icons/` — contact and profile icons. Scientific, GitHub, and LinkedIn SVGs are copied from `../rezaaliasgarirenani/assets_readme/`; Instagram, Facebook, X, and Gmail icons are from the CC0 Simple Icons project. Email and phone are simple local SVGs.
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

The English two-page CV in `../reza/documents/CVR/english/2_page/` is the default content reference. Check Home's research experience and education timelines, the Research details, the Publications list, and About's skill groups when updating professional information. Keep the two profile READMEs in `../reza/` and `../rezaaliasgarirenani/` synchronized separately.

Replace `assets/reza_aliasgari_renani_cv.pdf` when that CV changes and update the `?v=` value on CV links in all four pages to refresh browser caches. Update the stylesheet version in all four pages after changing shared CSS.

The Instagram, Facebook, X, and LinkedIn destinations were verified against GitHub’s public social-account API for `rezaaliasgarirenani`. The directory sits above the copyright bar on every page, using three category rows with icons and names; addresses and account identifiers remain in the link destinations. Scientific profiles are ordered ORCID, ResearchGate, Google Scholar, Scopus, Web of Science, IEEE Xplore. It also includes GitHub, all six scientific profiles from the profile README, and phone/email/Gmail contact links.

Screen typography uses 16 px body text, at least 14 px for dates and supporting text, and larger headings. Home’s path and centered name share a line on wider screens; small screens wrap the heading to preserve legibility. Contact/profile rows wrap their links instead of shrinking the text.

Home’s three panel titles and numbers identify content rather than simulated live status. The terminal panels stack on smaller screens. Shared footer directories are static HTML in all four pages; keep their link destinations and order synchronized when editing.
