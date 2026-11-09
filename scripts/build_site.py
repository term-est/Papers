"""Fill the HTML page with paper links and copy its assets. Standard library only."""

import argparse
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import quote


class PaperTitle(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Directory containing the built HTML papers")
    output = parser.parse_args().output
    if not output.is_dir():
        parser.error(f"Paper output directory does not exist: {output}")

    site = Path(__file__).resolve().parents[1] / "site"
    template = (site / "index.html").read_text(encoding="utf-8")
    if template.count("<!-- PAPERS -->") != 1:
        parser.error("The HTML template must contain exactly one <!-- PAPERS -->")

    papers = sorted(p for p in output.glob("*.html") if p.name != "index.html")
    entries = []
    for paper in papers:
        number, separator, filename_title = paper.stem.partition(" - ")
        title_parser = PaperTitle()
        title_parser.feed(paper.read_text(encoding="utf-8", errors="replace"))
        title = " ".join("".join(title_parser.parts).split()) or filename_title or paper.stem
        if "\ufffd" in title:
            title = filename_title or paper.stem
        if separator:
            title = title.removeprefix(f"{number}: ")
        entries.append(
            '<li><a class="paper-link" href="' + quote(paper.name, safe="") + '">'
            '<span class="paper-id">' + escape(number if separator else "C++") + '</span> — '
            '<span class="paper-title">' + escape(title) + '</span></a></li>'
        )

    page = template.replace("<!-- PAPERS -->", "\n          ".join(entries))
    (output / "index.html").write_text(page, encoding="utf-8")
    shutil.copytree(site / "assets", output / "assets", dirs_exist_ok=True)
    print(f"Built {output / 'index.html'} with {len(papers)} papers.")


if __name__ == "__main__":
    main()
