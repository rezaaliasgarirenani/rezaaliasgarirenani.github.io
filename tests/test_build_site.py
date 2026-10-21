"""Check that deployment contains runtime files and excludes project materials."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_site import build_site


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        self.root.mkdir()
        for name in ("index.html", "robots.txt", "sitemap.xml", ".nojekyll"):
            (self.root / name).write_text(name, encoding="utf-8")
        self.write("src/site.css", "body { background: black; }")
        self.write("src/binary_background.js", "// actual runtime code")
        self.write("assets/reza_aliasgari_renani_cv.pdf", "%PDF-test")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_only_runtime_files_are_published(self):
        self.write("design/exports/binary_background.png", "design export")
        self.write("documents/cv/cv_body.tex", "CV source")
        self.write("scripts/private_development_file.py", "development tool")
        self.write("tests/test_example.py", "test")
        self.write("README.md", "repository documentation")
        self.write(".git/config", "git metadata")
        self.write(".env", "not a runtime file")
        output = build_site(self.root)
        self.assertEqual(output, self.root / "dist")
        self.assertEqual(
            {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()},
            {"index.html", "robots.txt", "sitemap.xml", ".nojekyll",
             "src/site.css", "src/binary_background.js", "assets/reza_aliasgari_renani_cv.pdf"},
        )
        self.assertEqual((output / "src/site.css").read_bytes(), (self.root / "src/site.css").read_bytes())

    def test_rebuild_removes_outdated_downloads(self):
        output = build_site(self.root)
        stale = output / "assets/old_cv.pdf"
        stale.write_bytes(b"old CV")
        build_site(self.root)
        self.assertFalse(stale.exists())
        self.assertTrue((output / "assets/reza_aliasgari_renani_cv.pdf").is_file())

    def test_invalid_source_does_not_destroy_previous_output(self):
        output = build_site(self.root)
        before = (output / "index.html").read_bytes()
        (self.root / "index.html").unlink()
        with self.assertRaises(FileNotFoundError):
            build_site(self.root)
        self.assertEqual((output / "index.html").read_bytes(), before)

    def symlink(self, destination, source):
        try:
            destination.symlink_to(source, target_is_directory=source.is_dir())
        except OSError as error:
            self.skipTest(f"Symlinks unavailable on this machine: {error}")

    def test_output_symlink_cannot_delete_another_directory(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        keep = outside / "keep.txt"
        keep.write_text("preserve", encoding="utf-8")
        self.symlink(self.root / "dist", outside)
        with self.assertRaises(ValueError):
            build_site(self.root)
        self.assertEqual(keep.read_text(encoding="utf-8"), "preserve")

    def test_linked_source_cannot_publish_outside_files(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("outside source", encoding="utf-8")
        self.symlink(self.root / "assets/linked_file.txt", outside)
        with self.assertRaises(ValueError):
            build_site(self.root)


if __name__ == "__main__":
    unittest.main()
