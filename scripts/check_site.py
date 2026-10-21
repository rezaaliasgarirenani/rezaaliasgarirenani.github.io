"""Exercise the live page in normal Chrome; optionally check deployment exclusions."""

import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright
from browser_tools import normal_chrome

ROOT = Path(__file__).resolve().parents[1]
CV_PATH = "assets/reza_aliasgari_renani_cv.pdf"


def check_site(url, check_exclusions=False):
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    errors, failed_assets = [], []
    with sync_playwright() as p:
        with normal_chrome(p) as context:
            page = context.pages[0]
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("response", lambda response: failed_assets.append(
                f"{response.status} {response.url}") if response.url.startswith(url)
                and response.status >= 400 else None)
            response = page.goto(url, wait_until="networkidle")
            assert response.status == 200
            expect(page.get_by_role("navigation", name="Main navigation")).to_have_count(1)
            page.screenshot(path=str(artifacts / "desktop_check.png"))
            print("PASS: personal website and external styles/scripts load")

            with page.expect_download() as download_event:
                page.locator(".hero-actions a[download]").click()
            download = download_event.value
            assert download.suggested_filename == "reza_aliasgari_renani_cv.pdf"
            pdf = page.request.get(url + CV_PATH)
            assert pdf.status == 200 and pdf.body().startswith(b"%PDF")
            assert pdf.body() == (ROOT / CV_PATH).read_bytes()
            print("PASS: the unchanged CV downloads with its snake_case filename")

            for label, count in [("Journal", 1), ("Conferences", 5), ("All", 6)]:
                page.get_by_role("button", name=label, exact=True).click()
                expect(page.locator(".publication:visible")).to_have_count(count)
            print("PASS: publication filters show the right contributions")

            page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            canvas = page.locator("#binary-field")
            page.wait_for_timeout(400)
            before = canvas.evaluate("canvas => canvas.toDataURL()")
            page.wait_for_timeout(400)
            assert before != canvas.evaluate("canvas => canvas.toDataURL()"), "Binary background is not moving"
            page.get_by_role("button", name="Pause animation", exact=True).click()
            before = canvas.evaluate("canvas => canvas.toDataURL()")
            page.wait_for_timeout(400)
            assert before == canvas.evaluate("canvas => canvas.toDataURL()"), "Pause does not freeze animation"
            page.get_by_role("button", name="Play animation", exact=True).click()
            page.wait_for_timeout(400)
            assert before != canvas.evaluate("canvas => canvas.toDataURL()"), "Play does not restart animation"
            print("PASS: the original binary animation moves, pauses, and resumes")

            # Native disclosure controls still expose the research detail text.
            for details in page.locator(".research-card details").all():
                details.locator("summary").click()
                expect(details.locator("p")).to_be_visible()
                details.locator("summary").click()
            print("PASS: research method disclosures work")

            for width in (1440, 1024, 768, 390, 320):
                page.set_viewport_size({"width": width, "height": 900})
                page.wait_for_timeout(100)
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"Horizontal overflow at {width}px"
            print("PASS: no horizontal overflow from 320px to 1440px")

            page.set_viewport_size({"width": 390, "height": 844})
            page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            menu = page.get_by_role("button", name="Open menu", exact=True)
            menu.click()
            nav = page.get_by_role("navigation", name="Main navigation")
            expect(nav).to_be_visible()
            nav.get_by_role("link", name="Research", exact=True).click()
            expect(nav).to_be_hidden()
            assert page.evaluate("location.hash") == "#research"
            page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            menu.click()
            page.keyboard.press("Escape")
            expect(nav).to_be_hidden()
            page.screenshot(path=str(artifacts / "mobile_check.png"))
            print("PASS: mobile menu navigates and closes with Escape")

            page.set_viewport_size({"width": 1440, "height": 1000})
            page.emulate_media(reduced_motion="reduce")
            page.reload(wait_until="networkidle")
            expect(page.get_by_role("button", name="Play animation", exact=True)).to_be_visible()
            before = canvas.evaluate("canvas => canvas.toDataURL()")
            page.wait_for_timeout(500)
            assert before == canvas.evaluate("canvas => canvas.toDataURL()"), "Reduced-motion preference is ignored"
            print("PASS: reduced-motion preference keeps the background still")

            broken = page.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
                .map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1)))""")
            assert not broken, broken
            assert page.locator("h1").count() == 1
            assert page.locator("img").evaluate_all("imgs => imgs.every(img => img.complete && img.naturalWidth > 0)")
            page.evaluate("document.activeElement.blur()")
            page.keyboard.press("Control+Home")
            page.keyboard.press("Tab")
            expect(page.get_by_role("link", name="Skip to content", exact=True)).to_be_focused()
            print("PASS: SVG originals, section links, and keyboard skip link work")

            if check_exclusions:
                for name in ("README.md", "scripts/build_site.py", "design/exports/binary_background.png", "documents/cv/cv_body.tex"):
                    response = page.request.get(url + name)
                    assert response.status == 404, f"Repository-only material published: {name}"
                print("PASS: documentation, development scripts, PNG exports, and CV sources are not served")
            assert not errors, errors
            assert not failed_assets, failed_assets

        with normal_chrome(p, java_script_enabled=False) as context:
            page = context.pages[0]
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(url, wait_until="networkidle")
            expect(page.locator(".publication:visible")).to_have_count(6)
            expect(page.get_by_role("navigation", name="Main navigation").get_by_role("link", name="Research", exact=True)).to_be_visible()
            print("PASS: content and navigation work without JavaScript")
    print(json.dumps({"url": url, "javascript_errors": errors, "failed_assets": failed_assets}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--check_exclusions", action="store_true")
    arguments = parser.parse_args()
    check_site(arguments.url.rstrip("/") + "/", arguments.check_exclusions)
