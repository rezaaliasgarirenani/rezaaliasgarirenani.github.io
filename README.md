# Reza Aliasgari Renani

Personal research website: **https://rezaaliasgarirenani.github.io/**

Plain HTML, CSS, and JavaScript. No framework, build step, external fonts, or runtime dependencies. The page uses the GitHub Dark Colorblind VS Code palette, with topic-based navigation and an optional animated binary background.

## Preview on Windows

Open this repository in VS Code, then run in PowerShell:

```powershell
.\preview.ps1
```

Open **http://127.0.0.1:8000/** in Chrome. Keep the terminal running and press `Ctrl+C` to stop the server. The script always serves its own folder, even when invoked from another directory, so another repository's files cannot be served by mistake.

If port 8000 is already in use, use a different port:

```powershell
.\preview.ps1 -Port 8001
```

If your PowerShell policy prevents scripts, run Python directly from the repository folder:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory .
```

## Make an edit

- Text, publications, projects, and navigation: edit `index.html`.
- Colors and layout: edit the `<style>` section near the top of `index.html`. Colors are defined in `:root`.
- Binary animation, publication filters, and mobile menu: edit the `<script>` section near the bottom.
- Downloadable CV: replace `assets/Reza-Aliasgari-Renani-CV.pdf` using the same filename. This is a separate copy; changes to the CV in another repository do not automatically update it.

Save, then refresh Chrome. If an old version persists, press `Ctrl+Shift+R`. Check a narrow window as well as a desktop-sized window. The animation has a pause/play control, automatically pauses when out of view, and starts still when the visitor requests reduced motion. Content and navigation also work without JavaScript.

## Publish an edit

From this repository's PowerShell terminal:

```powershell
git status
git diff
git add index.html
git commit -m "Update website content"
git push origin main
```

If you changed the CV or other assets, explicitly add those files before committing too, for example:

```powershell
git add assets/Reza-Aliasgari-Renani-CV.pdf
```

GitHub Pages publishes the root of `main` automatically after a push. Deployment usually takes a minute or two. Check the repository's **Actions** tab for the Pages deployment, then refresh the public address. `.nojekyll` tells GitHub to serve the static files directly.

## Content sources and design references

Research, publications, education, projects, and contact links come from Reza's profile README and CV in the adjacent `reza` repository (reviewed October 2026), cross-checked against his public GitHub profile and repositories. The downloadable PDF is the general English CV from `documents/CVR/`.

The design adapts the topic navigation and information hierarchy of [FBI.gov](https://www.fbi.gov/), the technical presentation of [Visual Studio Code](https://code.visualstudio.com/), and the research-focused organization of academic personal sites. The colors come from the locally installed GitHub Dark Colorblind theme. The FPGA illustration and binary animation are original, implemented directly in SVG and canvas; the illustration is a schematic, not measured data.

## Files

```text
index.html                         Page, styles, and interactions
assets/favicon.svg                 Browser icon
assets/Reza-Aliasgari-Renani-CV.pdf  Downloadable CV
preview.ps1                        Windows local preview helper
robots.txt                         Search crawler guidance
sitemap.xml                        Canonical page URL
.nojekyll                          Static GitHub Pages publishing
```
