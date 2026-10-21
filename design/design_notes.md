# Design and asset sources

The site introduces Reza Aliasgari Renani's work in RTL design, semiconductor physics, and plasma systems. It follows a researcher's content hierarchy: research topics, publications and presentations, practical projects, experience and education, then contact details.

## References

- [FBI.gov](https://www.fbi.gov/): clear topic navigation, section hierarchy, topic shortcuts, and direct access to key information.
- [Visual Studio Code](https://code.visualstudio.com/): dark technical presentation, a prominent introduction, and a code-inspired visual atmosphere.
- Academic personal sites, including [Andrej Karpathy's](https://karpathy.ai/): primary emphasis on real research, publications, projects, and career history.
- **GitHub Dark Colorblind (Beta)**: colors read from the locally installed `github.github-vscode-theme` extension, version 6.3.5. `src/site.css` is authoritative; `theme_palette.json` is a regenerable reference export.

These are design references. No external page template, branding, institutional seal, photograph, or another researcher's content was copied into this site.

## Asset inventory

| Original used by the page | Editable source | Repository-only PNG export |
| --- | --- | --- |
| FPGA system illustration | `assets/graphics/fpga_schematic.svg` | `design/exports/fpga_schematic.png` |
| Digital hardware research icon | `assets/graphics/digital_design.svg` | `design/exports/digital_design.png` |
| Device physics research icon | `assets/graphics/device_physics.svg` | `design/exports/device_physics.png` |
| Plasma and space research icon | `assets/graphics/plasma_space.svg` | `design/exports/plasma_space.png` |
| Browser icon | `assets/favicon.svg` | `design/exports/favicon.png` |
| Animated binary field | `src/binary_background.js` | `design/exports/binary_background.png` |

The FPGA illustration and research icons are original SVG artwork made from paths, rectangles, circles, gradients, and text. The illustration is labeled **SCHEMATIC**: it is a conceptual view, not a measured device layout or experimental result. Its title and description are preserved inside the standalone SVG.

The live animation is drawn on a canvas rather than played from a PNG or video. Its PNG export records the raw, transparent canvas; it omits the page text, illustration, and the CSS gradient overlay. See [the binary background notes](binary_background.md) for the original algorithm.

## Reference previews

- `previews/desktop_preview.png`: 1440 × 1000 desktop viewport.
- `previews/mobile_preview.png`: 390 × 844 phone-sized viewport.
- `previews/desktop_full_page.png`: complete desktop page.

Previews are generated from the real page using `python scripts/export_assets.py`. SVG PNGs are direct browser renders of the corresponding originals. The binary export comes from the real canvas's `toDataURL()` output. Exporting introduces no image-generation model or manually edited raster source.

## Content provenance

The initial page content was based on Reza's profile README and general English CV in the adjacent `reza` checkout. The PDF is retained byte-for-byte, with a snake_case filename. The corresponding LaTeX layout and content are now included in `documents/cv/`.

The initial monolithic implementation remains in Git history at commit `95bedf8`. The source organization changes preserve its visual design and binary algorithm. Standard CSS property names, HTML attributes, and existing fragment identifiers retain normal web syntax; descriptive filenames use snake_case.

## Publishing boundary

Only `index.html`, `assets/`, `src/`, `robots.txt`, `sitemap.xml`, and `.nojekyll` enter the Pages artifact. This directory and all other development materials remain in the public GitHub repository but are omitted from the deployed website.
