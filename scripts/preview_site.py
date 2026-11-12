"""Preview clean site URLs directly from the four editable HTML source files."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from build_site import PAGE_ROUTES

ROOT = Path(__file__).resolve().parents[1]
ROUTE_SOURCES = {route: "/" + source for source, route in PAGE_ROUTES.items()}


class SiteHandler(SimpleHTTPRequestHandler):
    def redirect_legacy(self):
        url = urlsplit(self.path)
        route = PAGE_ROUTES.get(url.path.lstrip("/"))
        if url.path.endswith("/index.html"):
            route = url.path[:-10]
        if url.path + "/" in ROUTE_SOURCES:
            route = url.path + "/"
        if route is None:
            return False
        self.send_response(301)
        self.send_header("Location", route + ("?" + url.query if url.query else ""))
        self.send_header("Content-Length", "0")
        self.end_headers()
        return True

    def do_GET(self):
        if not self.redirect_legacy():
            super().do_GET()

    def do_HEAD(self):
        if not self.redirect_legacy():
            super().do_HEAD()

    def translate_path(self, path):
        return super().translate_path(ROUTE_SOURCES.get(urlsplit(path).path, path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(SiteHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        print(f"Preview: http://127.0.0.1:{args.port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
