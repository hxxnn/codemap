#!/usr/bin/env python3
"""Dev tool: re-apply the HTML shell and assets to the example HTML pages.

Keeps each page's body content, language and title; refills the shell's other
placeholders from the sibling Markdown file's front matter and copies
skills/_shared/assets/* next to the pages (html/assets/). Usage:
  rebuild_example_html.py [EXAMPLES_DIR]    (default: examples)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "skills" / "_shared" / "html-template.html"
ASSETS = ROOT / "skills" / "_shared" / "assets"


def front_matter(md_text):
    end = md_text.index("\n---", 4)
    data = {}
    for line in md_text[4:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return data


def source_count(sources):
    inner = sources.strip()[1:-1]
    entries = [i.strip() for i in inner.split(",") if i.strip()]
    return sum(1 for e in entries if not e.rpartition(":")[0].strip().startswith("docs/codemap/"))


def rebuild(page, project):
    old = page.read_text(encoding="utf-8")
    lang = re.search(r'<html lang="([^"]*)"', old).group(1)
    heading = re.search(r"<h1>(.*?)</h1>", old, re.S)
    title = heading.group(1) if heading else re.search(r"<title>(.*?)</title>", old, re.S).group(1)
    suffix = f" - {html.escape(project)}"
    while title.endswith(suffix):  # earlier runs appended the project name to the title
        title = title[: -len(suffix)]
    content = re.search(r'<main id="cm-main">\n(.*?)\n</main>', old, re.S).group(1)
    md = front_matter((page.parent.parent / f"{page.stem}.md").read_text(encoding="utf-8"))
    values = {
        "{{LANG}}": lang, "{{TITLE}}": title, "{{PROJECT}}": html.escape(project),
        "{{GENERATED}}": html.escape(md.get("generated_at", "")), "{{SOURCES}}": str(source_count(md.get("sources", "{}"))),
        "{{CONTENT}}": content,
    }
    out = TEMPLATE.read_text(encoding="utf-8")
    for key, value in values.items():
        out = out.replace(key, value)
    page.write_text(out, encoding="utf-8")


def main(argv):
    examples = Path(argv[0]) if argv else ROOT / "examples"
    count = 0
    for page in sorted(examples.glob("*/docs/codemap/html/*.html")):
        rebuild(page, page.parents[3].name)
        assets = page.parent / "assets"
        assets.mkdir(exist_ok=True)
        for asset in ASSETS.iterdir():
            (assets / asset.name).write_bytes(asset.read_bytes())
        count += 1
    print(f"rebuilt {count} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
