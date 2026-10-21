"""Shared browser setup for local checks and asset exports."""

import tempfile
from contextlib import contextmanager


@contextmanager
def normal_chrome(playwright, **options):
    # A persistent context opens normal Chrome, rather than an incognito context.
    # The temporary profile avoids interfering with the user's everyday profile.
    with tempfile.TemporaryDirectory(prefix="reza_website_chrome_") as profile:
        context = playwright.chromium.launch_persistent_context(
            profile,
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 1000},
            device_scale_factor=1,
            args=["--no-first-run", "--no-default-browser-check"],
            **options,
        )
        try:
            yield context
        finally:
            context.close()
