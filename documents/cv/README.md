# CV sources

- `reza_aliasgari_renani_cv.tex`: the original general English CV layout and preamble.
- `cv_body.tex`: the original general English CV content.
- Published PDF: [`assets/reza_aliasgari_renani_cv.pdf`](../../assets/reza_aliasgari_renani_cv.pdf).

These sources were copied from the general English CV in the adjacent `reza` repository's `documents/CVR/` directory. Only the filenames and the `\input{cv_body}` reference were changed. Other language variants, applications, transcripts, and unrelated personal documents were not copied.

## Rebuild

Install a LaTeX distribution with **LuaLaTeX** and the packages named in the preamble, including `fontspec`, `newtx`, `mhchem`, `fontawesome5`, `academicons`, and `simpleicons`. From this directory, run twice so the page count resolves:

```powershell
lualatex -interaction=nonstopmode reza_aliasgari_renani_cv.tex
lualatex -interaction=nonstopmode reza_aliasgari_renani_cv.tex
```

Review the generated PDF, then replace the website copy:

```powershell
Copy-Item -LiteralPath .\reza_aliasgari_renani_cv.pdf -Destination ..\..\assets\reza_aliasgari_renani_cv.pdf
```

The published PDF was preserved from the original file rather than recompiled during this website reorganization. LuaLaTeX was not installed in that Windows environment, so source compilation was not reverified. The existing PDF itself was checked for byte-for-byte preservation and correct downloading.

LaTeX sources are available in GitHub but excluded from the Pages artifact. Intermediate LaTeX files and the locally generated PDF in this directory are ignored by Git; the PDF under `assets/` is the tracked, published copy.
