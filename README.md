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
- `assets/reza_aliasgari_renani_cv.pdf` — downloadable CV.
- `documents/cv/` — original LaTeX sources for the CV.

## Preview and publish

Run `.\preview.ps1` in PowerShell, then open **http://127.0.0.1:8000/**. Save edits and refresh Chrome. Press `Ctrl+C` to stop the preview.

Commit and push changes to `main` to publish. GitHub Actions uses `scripts/build_site.py` to stage only the page, `src/`, `assets/`, and crawler files in `dist/`. CV LaTeX sources and repository documentation stay on GitHub, outside the website deployment.

To update the CV, replace `assets/reza_aliasgari_renani_cv.pdf`. The two `.tex` files in `documents/cv/` can be compiled with LuaLaTeX; editing them does not automatically replace the published PDF.

The current CV PDF and LaTeX sources come from `reza/documents/CVR/english/2_page` in the WSL checkout. Update the `?v=` value in the CV download links after replacing the PDF to refresh browser caches.
