# Reza Aliasgari Renani

Personal website: **https://rezaaliasgarirenani.github.io/**

Static HTML, CSS, and JavaScript, with a black `rgb(0, 0, 0)` background,
`rgb(225, 225, 225)` text, monospace fonts, and restrained blue/amber accents.

## Pages and URLs

| Editable source | Public URL |
| --- | --- |
| `index.html` | `/` |
| `research.html` | `/research/` |
| `publications.html` | `/publications/` |
| `about.html` | `/about/` |

`scripts/build_site.py` stages real directory pages in `dist/`; these URLs do
not depend on a client-side router. It generates redirects for old `.html`
links, preserving query strings and fragments when JavaScript is available.
A meta redirect and normal link also work without JavaScript.
`src/clean_urls.js` removes explicit `/index.html` endings from the address bar.
Canonical metadata, navigation, and `sitemap.xml` use directory URLs.

Keep shared navigation, footer markup, and script/style cache versions in sync
across all four source pages. Absolute `/assets/` and `/src/` URLs work from
both the home page and nested public routes.

## Home and shared layout

Home starts immediately below the header with a centered Earth/satellite
animation up to 520 px wide. The separate visible name and research-area labels
are omitted. The centered paragraph beneath begins with the supplied greeting,
introduces Reza, and continues with the FPGA-based ISP summary. Text stays 16 px
(14 px on phones). A visually hidden main heading retains the page's accessible
name. The show-all control remains in the Profile title bar.

The Profile, Research Experience, and Education terminal panels retain their
content and timelines. `src/terminal.js` reveals their 29 output units at 50 ms
intervals (about 1.4 seconds), with a show-all control and reduced-motion fallback.
The introduction and footer do not wait for that reveal.

The sticky header retains its portrait, chip logos, city clocks, and navigation.
`src/header_layout.js` measures its height for anchor offsets and the side rails.
`src/header_clocks.js` displays seconds in `America/New_York` and `Asia/Singapore`,
with daylight-saving changes handled by `Intl.DateTimeFormat`.

`src/side_binary.js` runs two narrow, fixed vertical binary streams outside the
content: left moves down, right moves up. Each has top and bottom pause buttons
controlling the same side, for four controls total. `SPEED_PX_PER_SECOND = 60`
and `DIGIT_UPDATE_MS = 70` control motion and digit updates. Pausing freezes both;
hidden tabs and page lifecycle events suspend activity. Reduced motion and
JavaScript-free reading show static decorative digits.

The footer is a single compact desktop row: chip logo, copyright notice, all
14 contact/profile icons centered relative to the page, Fidelity · Bravery ·
Integrity motto, and chip logo. Icons are 16 px with 24 px link targets; group
headings and divider rules are omitted. Smaller screens wrap the text and icon
strip into compact rows, with two even rows of seven icons on narrow phones.

## Artwork and content

- `assets/earth_satellite.png`: unchanged optimized APNG, 530,362 bytes,
  720 × 420, 144 frames, 7.2-second loop. Original satellite and orbit.
- `assets/earth_satellite_still.png`: identical first-frame PNG selected by
  `<picture>` for reduced motion.
- `assets/chip_radiation_logo.png`: supplied transparent logo optimized to
  320 × 320, about 48 KB, used in the header/footer and favicon.
- `assets/reza_aliasgari_renani.png`: portrait/Home link.
- `assets/reza_aliasgari_renani_cv.pdf`: default English two-page CV.
- `assets/icons/`: contact/profile icons; keep every existing destination/order.
- `artwork/`: source animation and unused legacy artwork moved from both README
  repositories, deduplicated by content. See [artwork notes](artwork/README.md).
- `scripts/render_satellite_orbit.py`: rebuilds the APNG from the original source.

Only artwork used by the website lives in `assets/`. The source/archive in
`artwork/`, scripts, tests, README, and other documentation are not published.
Both profile repositories retain only the SVGs referenced by their READMEs.

Use `../reza/documents/CVR/english/2_page/` as the default professional-content
reference, and keep `../reza/README.md` and `../rezaaliasgarirenani/README.md`
synchronized. The current CV facts include master's Top 5%, bachelor's Top 15%,
and the Russian Government Scholarship for Foreign Citizens, MIPT, 2020–2026.
When replacing the PDF, update its `?v=` value on every page.

## Preview

From this website repository in WSL:

```bash
python3 scripts/preview_site.py --port 8000
```

From Windows PowerShell:

```powershell
.\preview.ps1
```

Open **http://127.0.0.1:8000/**. This preview serves clean directory URLs directly
from the editable source files. Save and refresh; press `Ctrl+C` to stop.

## Verify and publish

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
```

Use `python` in native Windows if that is the installed command. To inspect the
exact generated public files instead, serve `dist/` with `python3 -m http.server
8000 --directory dist` after building.

The build validates inputs before replacing `dist/`, rejects symlinked sources,
and publishes only directory pages, legacy redirects, `assets/`, `src/`, and
crawler files. `dist/` is ignored. Push `main` to deploy through GitHub Actions;
root HTML source edits trigger the existing workflow.
