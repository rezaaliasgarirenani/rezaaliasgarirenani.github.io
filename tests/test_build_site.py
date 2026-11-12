"""Check the deployment boundary with real files in a temporary checkout."""

from html.parser import HTMLParser
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
        for name, destination in (
            ("index.html", "index.html"),
            ("research.html", "research/index.html"),
            ("publications.html", "publications/index.html"),
            ("about.html", "about/index.html"),
        ):
            with self.subTest(page=name):
                self.assertEqual(
                    (output / destination).read_text() if (output / destination).exists() else None,
                    f"public content: {name}",
                )

    def test_old_html_links_keep_canonical_and_no_script_redirects(self):
        class Metadata(HTMLParser):
            def __init__(self):
                super().__init__()
                self.tags = []

            def handle_starttag(self, tag, attrs):
                self.tags.append((tag, dict(attrs)))

        output = MODULE.build_site(self.root)
        for page in ("research", "publications", "about"):
            with self.subTest(page=page):
                document = Metadata()
                document.feed((output / f"{page}.html").read_text())
                self.assertIn(("meta", {"http-equiv": "refresh", "content": f"0;url=/{page}/"}), document.tags)
                self.assertIn(("link", {"rel": "canonical", "href": f"https://rezaaliasgarirenani.github.io/{page}/"}), document.tags)
                self.assertIn(("a", {"href": f"/{page}/"}), document.tags)

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
        (self.root / "artwork").mkdir()
        (self.root / "artwork" / "source.gif").write_bytes(b"source-only artwork")
        output = MODULE.build_site(self.root)
        self.assertFalse((output / "README.md").exists())
        self.assertFalse((output / "scripts").exists())
        self.assertFalse((output / "artwork").exists())
        self.assertEqual((output / "src" / "fixture.txt").read_text(), "shared src")


if __name__ == "__main__":
    unittest.main()
