# Profile synchronization and mobile layout plan

**Goal:** Propagate the three-page CV's GPA rankings and scholarship to the default English two-page CV, both profile READMEs, and website; publish the updated PDF and improve mobile navigation/footer.

**Architecture:** Preserve static HTML/CSS and the desktop layout. Use a native HTML disclosure for mobile navigation, with no JavaScript dependency. On phones, stack footer categories, using a two-column link list within each category.

**Scope:** Only the English two-page CV is updated; the three-page CV remains the source for these facts. Existing unrelated edits in reza stay untouched.

- [ ] Update the two-page LaTeX body and both READMEs with regular-weight Top 5% (master's), Top 15% (bachelor's), and Russian Government Scholarship for Foreign Citizens, MIPT, 2020–2026. Rebuild and verify two pages, text, and layout.
- [ ] Update home education and About awards; replace the downloadable PDF byte-for-byte with the new two-page PDF. Set every PDF URL to version 20261031 and header label to CV.pdf ↗.
- [ ] Add a native mobile Menu disclosure to all four pages, retaining the portrait/Home link and clocks. Stack and left-align footer categories at widths up to 720 px; use comfortably sized link targets.
- [ ] Verify real browser behavior at 320, 390, 600, 720, 721, 768, 1024, and 1440 px on all pages: menu by keyboard and without JavaScript, links reachable, no horizontal scrolling, footer alignment and readable text. Run the existing build tests and build.
- [ ] Review the scoped diff, commit and push all three repositories, watch Pages deployment, and verify public HTML and PDF.

**Review focus:** Desktop header fit after CV.pdf rename; footer link/copyright overlap at narrow widths; CV text overflowing the education subheading; no stale admission offers; all four pages share the same PDF and navigation markup.
