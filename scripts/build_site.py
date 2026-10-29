"""Stage only the public runtime files in dist/; no transpiler or bundler."""

import shutil
from pathlib import Path

SITE_FILES = (
    "index.html", "research.html", "publications.html", "about.html",
    "robots.txt", "sitemap.xml", ".nojekyll",
)
SITE_DIRECTORIES = ("assets", "src")


def build_site(repository_root):
    root = Path(repository_root).resolve()
    output = root / "dist"

    # A rebuild may remove only this repository's real, generated dist directory.
    if output.is_symlink() or output.resolve() != root / "dist":
        raise ValueError("Refusing to replace a linked or external output directory")
    if output.exists() and not output.is_dir():
        raise ValueError("dist must be a generated directory")

    # Validate all inputs before changing an existing deployment preview.
    sources = []
    for name in SITE_FILES:
        source = root / name
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError(f"Linked source is not allowed: {name}")
        if not source.is_file():
            raise FileNotFoundError(f"Required website file is missing: {name}")
        sources.append(source)
    for name in SITE_DIRECTORIES:
        source = root / name
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError(f"Linked source directory is not allowed: {name}")
        if not source.is_dir():
            raise FileNotFoundError(f"Required website directory is missing: {name}")
        for entry in source.rglob("*"):
            if entry.is_symlink() or not entry.resolve().is_relative_to(root):
                raise ValueError(f"Linked source is not allowed: {entry.relative_to(root)}")
            if entry.is_file():
                sources.append(entry)

    # output has been resolved and checked to be exactly root/dist above.
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    for source in sources:
        destination = output / source.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return output


if __name__ == "__main__":
    output = build_site(Path(__file__).resolve().parents[1])
    print(f"Website staged in {output}")
    print("Only the four public pages, assets/, src/, and crawler files are published.")
