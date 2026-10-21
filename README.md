# Reza Aliasgari Renani

Personal website: **https://rezaaliasgarirenani.github.io/**

Plain HTML, CSS, JavaScript, and original SVG graphics. Colors follow the GitHub Dark Colorblind VS Code theme.

## Source files

- `index.html` — page content.
- `src/site.css` — colors, layout, and responsive styles.
- `src/binary_background.js` — the original animated binary background.
- `src/navigation.js` — mobile navigation.
- `assets/graphics/` — editable graphics used by the site.
- `assets/chip_radiation_logo.png` — supplied logo used in the header, footer, and browser tab.
- `assets/reza_aliasgari_renani_cv.pdf` — CV PDF, opened in a new browser tab.

## Preview and publish

Run `.\preview.ps1` in PowerShell, then open **http://127.0.0.1:8000/**. Save edits and refresh Chrome. Press `Ctrl+C` to stop the preview.

Commit and push changes to `main` to publish. GitHub Actions uses `scripts/build_site.py` to stage only the page, `src/`, `assets/`, and crawler files in `dist/`. This generated folder is not needed for local preview and can be deleted locally.

To update the CV, replace `assets/reza_aliasgari_renani_cv.pdf`.

The current CV PDF comes from `reza/documents/CVR/english/2_page` in the WSL checkout. Update the `?v=` value in the CV links after replacing the PDF to refresh browser caches.
