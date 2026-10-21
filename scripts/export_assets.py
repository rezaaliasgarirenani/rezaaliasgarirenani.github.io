"""Render the actual SVG/canvas sources as PNGs and capture reference previews."""

import argparse
import base64
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright
from browser_tools import normal_chrome

ROOT = Path(__file__).resolve().parents[1]


def export_assets(url):
    exports = ROOT / "design/exports"
    previews = ROOT / "design/previews"
    exports.mkdir(parents=True, exist_ok=True)
    previews.mkdir(parents=True, exist_ok=True)
    sizes = {
        "fpga_schematic": (1040, 940),
        "digital_design": (192, 192),
        "device_physics": (192, 192),
        "plasma_space": (192, 192),
        "favicon": (256, 256),
    }
    with sync_playwright() as p, normal_chrome(p) as context:
        page = context.pages[0]
        for name, (width, height) in sizes.items():
            source = "assets/favicon.svg" if name == "favicon" else f"assets/graphics/{name}.svg"
            response = page.goto(url + source, wait_until="networkidle")
            if response.status != 200:
                raise RuntimeError(f"Could not load {source}: HTTP {response.status}")
            page.set_viewport_size({"width": width, "height": height})
            page.locator("svg").evaluate(
                "(el, size) => { el.style.width = size[0] + 'px'; el.style.height = size[1] + 'px'; }",
                [width, height],
            )
            page.locator("svg").screenshot(path=str(exports / f"{name}.png"), omit_background=True)
            print(f"Exported {name}.png")

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(350)
        pause = page.get_by_role("button", name="Pause animation", exact=True)
        if pause.count():
            pause.click()
        encoded = page.locator("#binary-field").evaluate("canvas => canvas.toDataURL('image/png').split(',')[1]")
        (exports / "binary_background.png").write_bytes(base64.b64decode(encoded))
        page.screenshot(path=str(previews / "desktop_preview.png"))
        page.screenshot(path=str(previews / "desktop_full_page.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(150)
        page.screenshot(path=str(previews / "mobile_preview.png"))
        print("Exported raw binary canvas and desktop/mobile previews")

    css = (ROOT / "src/site.css").read_text(encoding="utf-8")
    colors = dict(re.findall(r"--([a-z_]+):\s*(#[0-9a-fA-F]{6})\s*;", css))
    palette = {
        "theme_name": "GitHub Dark Colorblind (Beta)",
        "reference_extension": "github.github-vscode-theme 6.3.5",
        "source_of_truth": "src/site.css :root",
        "colors": colors,
    }
    (ROOT / "design/theme_palette.json").write_text(json.dumps(palette, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    arguments = parser.parse_args()
    export_assets(arguments.url.rstrip("/") + "/")
