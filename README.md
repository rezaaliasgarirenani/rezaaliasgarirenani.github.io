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
name. A small pause/resume control at the animation's bottom-right freezes its
current frame and resumes from there. All five motion buttons share one pause
state through `src/motion.js`: any button pauses or resumes Earth and both binary
streams together, and every button displays the same state.
Playback pauses in hidden tabs; reduced motion uses the still picture. The
original picture remains available if JavaScript or playback setup is unavailable.
The show-all control remains in the Profile title bar.

`src/orbit.js` plays the existing APNG on a canvas through the locally vendored
[apng-js 1.1.5](https://github.com/davidmz/apng-js) (MIT). Its minified browser
build and license are in `src/vendor/`; no external runtime request is needed.
The original animation asset and frame timing are unchanged.

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
linked to the shared motion state, for four rail controls total.
`SPEED_PX_PER_SECOND = 60` and `DIGIT_UPDATE_MS = 70` control motion and digit updates. Pausing freezes both;
hidden tabs and page lifecycle events suspend activity. Reduced motion and
JavaScript-free reading show static decorative digits.

The footer divider follows the content width, aligned with the main panels.
It retains the two outer chip logos, the single-line desktop copyright, and all
14 contact/profile icons. Icons have 4 px gaps within groups; decorative `|`
separators have 14 px of space on each side. Group names are accessible labels
only. "United States" is right-aligned before the right chip logo.
Copyright and country text are 11.83 px (a 1 pt increase from 10.5 px); icons are
18 px with 24 px link targets, and desktop chip logos are 32 px. Smaller screens
retain responsive text wrapping and center the three groups in two rows of icons,
with the country on its own right-aligned line.

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
