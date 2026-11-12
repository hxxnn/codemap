#!/usr/bin/env python3
"""Dev-only checker for generated codemap outputs.

Usage: check_output.py <fixture_dir> <output_dir> [--render]
Exit code 1 if any problem is found.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

REQUIRED_KEYS = ("codemap", "skill", "generated_at", "sources")
NO_DIAGRAM_SKILLS = {"design-doc", "present", "mindmap", "relation-map"}  # mindmap is a tree list, not a diagram
SOURCE_EXTS = (".py", ".ts", ".tsx", ".js", ".go", ".rs", ".java", ".md", ".json", ".toml")
UNVERIFIED = "<!-- codemap:unverified -->"
# Generated/vendored folders legitimately do not exist in a fresh checkout.
GENERATED_DIRS = {"dist", "build", "node_modules", ".venv", "venv", "target", "__pycache__", "out"}
ARTIFACT_NAMES = {"architecture.md", "dependency-graph.md", "mindmap.md", "sequence-flow.md", "design-doc.md", "present.md", "relation-map.md"}
FENCE = re.compile(r"^```")
GRAPH_KINDS = {"source", "test", "unverified"}


def parse_front_matter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return data


def mermaid_blocks(text):
    return re.findall(r"```mermaid\n(.*?)```", text, flags=re.DOTALL)


def path_refs(text):
    refs = []
    for token in re.findall(r"`([^`\n]+)`", text):
        if re.search(r"[*<>{}]", token) or token.startswith("http"):
            continue
        if re.search(r"\s", token) and not token.endswith(SOURCE_EXTS):
            continue
        if token in SOURCE_EXTS or token.startswith("/"):  # bare extension or HTTP route
            continue
        if "/" in token or token.endswith(SOURCE_EXTS):
            refs.append(token)
    return refs


LABEL_PATH = re.compile(r"(?:[\w.\-@]+/)+[\w.\-@]+\.(?:py|ts|tsx|js|go|rs|java|md|json|toml)(?::[\w.\-]+)?")
QUOTED_ALIAS = re.compile(r'^\s*(?:participant|actor)\s+\w+\s+as\s+"')


def _exists(rel, fixture_dir):
    if rel.startswith(("./", "../")):
        # Relative import specifier: relative to the importing file, which is unknown here.
        # Accept it when a file with that path suffix exists anywhere in the project.
        core = re.sub(r"^(?:\.{1,2}/)+", "", rel)
        core = re.sub(r":[\w.\-]+$", "", core)
        return any(m.as_posix().endswith(core) for m in Path(fixture_dir).rglob(Path(core).name))
    rel = re.sub(r":[\w.\-]+$", "", rel)
    if rel.split("/", 1)[0] in GENERATED_DIRS or rel in ARTIFACT_NAMES:
        return True
    root = Path(fixture_dir)
    if (root / rel).exists():
        return True
    words = rel.split()
    return len(words) > 1 and (root / words[-1]).exists()


def _claims_a_path(ref, fixture_dir):
    """A slashed token like `if/else` is prose, not a file reference. Treat it as a path only when it
    has a known extension, ends with '/', is relative (./ ../), or starts with a real top-level entry."""
    if ref.endswith(SOURCE_EXTS) or ref.endswith("/") or ref.startswith(("./", "../")):
        return True
    return "/" not in ref or (Path(fixture_dir) / ref.split("/", 1)[0]).exists()


def _prose_lines(text):
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line


def check_file(md_path, fixture_dir):
    text = Path(md_path).read_text(encoding="utf-8")
    front = parse_front_matter(text)
    if front is None:
        return [f"{md_path}: missing front matter"]
    problems = []
    for key in REQUIRED_KEYS:
        if key not in front:
            problems.append(f"{md_path}: front matter lacks '{key}'")
    raw = front.get("sources", "")
    if not (raw.startswith("{") and raw.endswith("}")):
        problems.append(f"{md_path}: sources must be a one-line {{path: sha256}} mapping")
    else:
        for item in filter(None, (i.strip() for i in raw[1:-1].split(","))):
            path, _, digest = item.rpartition(":")
            path, digest = path.strip(), digest.strip()
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                problems.append(f"{md_path}: sources entry '{path}' lacks a sha256 hash")
                continue
            target = Path(fixture_dir) / path
            if not target.is_file():
                problems.append(f"{md_path}: source does not exist: {path}")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                problems.append(f"{md_path}: hash mismatch for source {path}")
    if front.get("skill") not in NO_DIAGRAM_SKILLS and not mermaid_blocks(text):
        problems.append(f"{md_path}: no mermaid block")
    for line in _prose_lines(text):
        if UNVERIFIED in line:
            continue
        for ref in path_refs(line):
            if not _claims_a_path(ref, fixture_dir):
                continue
            if not _exists(ref, fixture_dir):
                problems.append(f"{md_path}: path does not exist: {ref}")
    for body in mermaid_blocks(text):
        block_unverified = "%% codemap:unverified" in body
        for line in body.splitlines():
            if QUOTED_ALIAS.match(line):
                problems.append(f"{md_path}: quoted participant alias (write it without quotes): {line.strip()}")
            if block_unverified or "codemap:unverified" in line:
                continue
            for ref in LABEL_PATH.findall(line):
                if not _exists(ref, fixture_dir):
                    problems.append(f"{md_path}: diagram path does not exist: {ref}")
    return problems


def check_html(html_path):
    """Generated HTML must contain only the template's two script tags and no raw active content."""
    text = Path(html_path).read_text(encoding="utf-8")
    problems = []
    scripts = re.findall(r"<script\b[^>]*>", text, flags=re.IGNORECASE)
    if len(scripts) != 2 or "mermaid@" not in scripts[0]:
        problems.append(f"{html_path}: unexpected script tags ({len(scripts)} found, template has 2)")
    for name in sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text))):
        problems.append(f"{html_path}: unfilled template placeholder {name}")
    for ref in re.findall(r"<link\b[^>]*\bhref=\"([^\"]+)\"|<script\b[^>]*\bsrc=\"([^\"]+)\"", text):
        target = ref[0] or ref[1]
        if re.match(r"(https?:)?//|data:|#", target):
            continue
        if not (Path(html_path).parent / target).is_file():
            problems.append(f"{html_path}: linked file does not exist: {target}")
    stripped = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    if re.search(r"<[^>]*\son[a-z]+\s*=", stripped, flags=re.IGNORECASE):
        problems.append(f"{html_path}: inline event handler found")
    if re.search(r"javascript:", stripped, flags=re.IGNORECASE):
        problems.append(f"{html_path}: javascript: URL found")
    return problems


class _GraphParser(HTMLParser):
    """Collects the nodes of <ul class="cm-graph"> (the relation-map data list)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self._in_graph = False
        self._depth = 0
        self._cur = None
        self._in_code = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "ul":
            if not self._in_graph and "cm-graph" in (a.get("class") or "").split():
                self._in_graph, self._depth = True, 1
            elif self._in_graph:
                self._depth += 1
        elif self._in_graph and tag == "li":
            if self._depth == 1:
                self._cur = {"id": a.get("id", ""), "group": a.get("data-group", ""), "kind": a.get("data-kind", ""),
                             "path": None, "uses": []}
                self.nodes.append(self._cur)
            elif self._depth == 2 and self._cur is not None and "data-to" in a:
                self._cur["uses"].append(a["data-to"])
        elif self._in_graph and tag == "code" and self._cur is not None and self._cur["path"] is None:
            self._in_code, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "ul" and self._in_graph:
            self._depth -= 1
            if self._depth == 0:
                self._in_graph, self._cur = False, None
        elif tag == "code" and self._in_code:
            self._in_code = False
            self._cur["path"] = "".join(self._buf).strip()

    def handle_data(self, data):
        if self._in_code:
            self._buf.append(data)


def parse_graph_html(text):
    """Return one dict per graph node: id, group, kind, path (first <code>), uses (the data-to ids)."""
    parser = _GraphParser()
    parser.feed(text)
    for node in parser.nodes:
        node["path"] = node["path"] or ""
    return parser.nodes


def parse_relation_table(md_text):
    """Map path -> {"uses": [...], "used_by": [...]} from the file table (columns by position)."""
    rows = {}
    for line in md_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        first = re.fullmatch(r"`([^`]+)`", cells[0])
        if first:
            rows[first.group(1)] = {"uses": re.findall(r"`([^`]+)`", cells[2]), "used_by": re.findall(r"`([^`]+)`", cells[3])}
    return rows


def check_relation_graph(html_path, md_path, fixture_dir):
    """Validate the relation-map graph data and cross-check it against the Markdown file table."""
    nodes = parse_graph_html(Path(html_path).read_text(encoding="utf-8"))
    problems, ids = [], {}
    for n in nodes:
        if n["id"] in ids:
            problems.append(f"{html_path}: duplicate id {n['id']}")
        ids[n["id"]] = n
        if not n["group"]:
            problems.append(f"{html_path}: node {n['id']} lacks data-group")
        if n["kind"] not in GRAPH_KINDS:
            problems.append(f"{html_path}: node {n['id']} has invalid data-kind '{n['kind']}'")
        if not n["path"]:
            problems.append(f"{html_path}: node {n['id']} has no <code> path")
        elif not _exists(n["path"], fixture_dir):
            problems.append(f"{html_path}: node path does not exist: {n['path']}")
    edges = set()
    for n in nodes:
        for target in n["uses"]:
            if target == n["id"]:
                problems.append(f"{html_path}: self edge on {n['id']}")
            elif target not in ids:
                problems.append(f"{html_path}: dangling edge {n['id']} -> {target}")
            else:
                edges.add((n["path"], ids[target]["path"]))
    table = parse_relation_table(Path(md_path).read_text(encoding="utf-8"))
    table_edges = {(p, t) for p, row in table.items() for t in row["uses"]}
    used_by_edges = {(u, p) for p, row in table.items() for u in row["used_by"]}
    for a, b in sorted(edges - table_edges):
        problems.append(f"{html_path}: mismatch, graph has {a} -> {b} but the table does not")
    for a, b in sorted(table_edges - edges):
        problems.append(f"{html_path}: mismatch, table has {a} -> {b} but the graph does not")
    if used_by_edges != table_edges:
        problems.append(f"{md_path}: the used-by column does not invert the uses column")
    return problems


def chromium_path():
    """Browser for --render: $CODEMAP_CHROMIUM, else the sandbox default if present, else None (let puppeteer decide)."""
    env = os.environ.get("CODEMAP_CHROMIUM")
    if env:
        return env
    default = "/opt/pw-browsers/chromium"
    return default if Path(default).exists() else None


def render_mermaid(body):
    """Return None if the diagram renders, else an error string."""
    with tempfile.TemporaryDirectory() as tmp:
        src, out, cfg = Path(tmp, "d.mmd"), Path(tmp, "d.svg"), Path(tmp, "p.json")
        src.write_text(body, encoding="utf-8")
        browser = chromium_path()
        config = {"args": ["--no-sandbox"]}
        if browser:
            config["executablePath"] = browser
        cfg.write_text(json.dumps(config))
        result = subprocess.run(
            ["npx", "-y", "@mermaid-js/mermaid-cli@11", "-i", str(src), "-o", str(out), "-p", str(cfg)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return (result.stderr or result.stdout).strip()[-400:]
    return None


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    render = "--render" in argv
    if len(args) != 2:
        print(__doc__)
        return 2
    fixture_dir, output_dir = Path(args[0]), Path(args[1])
    problems = []
    for md in sorted(output_dir.glob("*.md")):
        problems += check_file(md, fixture_dir)
        if render:
            for i, body in enumerate(mermaid_blocks(md.read_text(encoding="utf-8")), 1):
                err = render_mermaid(body)
                if err:
                    problems.append(f"{md}: mermaid block {i} failed to render: {err}")
    for html in sorted((output_dir / "html").glob("*.html")):
        problems += check_html(html)
    graph = output_dir / "html" / "relation-map.html"
    if graph.is_file():
        graph_md = output_dir / "relation-map.md"
        if graph_md.is_file():
            problems += check_relation_graph(graph, graph_md, fixture_dir)
        else:
            problems.append(f"{graph}: relation-map.md is missing")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
