"""Check the deployment boundary with real files in a temporary checkout."""

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_site.py"
SPEC = importlib.util.spec_from_file_location("build_site", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in (
            "index.html", "research.html", "publications.html", "about.html",
            "robots.txt", "sitemap.xml", ".nojekyll",
        ):
            (self.root / name).write_text(f"public content: {name}")
        for name in ("assets", "src"):
            (self.root / name).mkdir()
            (self.root / name / "fixture.txt").write_text(f"shared {name}")

    def test_all_navigation_destinations_are_deployed(self):
        output = MODULE.build_site(self.root)
        for name in ("index.html", "research.html", "publications.html", "about.html"):
            with self.subTest(page=name):
                self.assertEqual(
                    (output / name).read_text() if (output / name).exists() else None,
                    f"public content: {name}",
                )

    def test_missing_page_preserves_previous_deployment(self):
        output = self.root / "dist"
        output.mkdir()
        (output / "previous.html").write_text("previous working deployment")
        (self.root / "research.html").unlink()
        with self.assertRaises(FileNotFoundError):
            MODULE.build_site(self.root)
        self.assertEqual((output / "previous.html").read_text(), "previous working deployment")

    def test_linked_page_is_rejected(self):
        page = self.root / "research.html"
        page.unlink()
        try:
            page.symlink_to(self.root / "index.html")
        except OSError:
            self.skipTest("Creating symbolic links is not available on this system")
        with self.assertRaises(ValueError):
            MODULE.build_site(self.root)

    def test_private_source_files_are_not_published(self):
        (self.root / "README.md").write_text("source documentation")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "private.py").write_text("not a runtime file")
        output = MODULE.build_site(self.root)
        self.assertFalse((output / "README.md").exists())
        self.assertFalse((output / "scripts").exists())
        self.assertEqual((output / "src" / "fixture.txt").read_text(), "shared src")


if __name__ == "__main__":
    unittest.main()
