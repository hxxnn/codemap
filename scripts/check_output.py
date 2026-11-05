#!/usr/bin/env python3
"""Dev-only checker for generated codemap outputs.

Usage: check_output.py <fixture_dir> <output_dir> [--render]
Exit code 1 if any problem is found.
"""
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED_KEYS = ("codemap", "skill", "generated_at", "sources")
NO_DIAGRAM_SKILLS = {"design-doc", "present"}
SOURCE_EXTS = (".py", ".ts", ".tsx", ".js", ".go", ".rs", ".java", ".md", ".json", ".toml")
UNVERIFIED = "<!-- codemap:unverified -->"
# Generated/vendored folders legitimately do not exist in a fresh checkout.
GENERATED_DIRS = {"dist", "build", "node_modules", ".venv", "venv", "target", "__pycache__", "out"}
ARTIFACT_NAMES = {"architecture.md", "dependency-graph.md", "mindmap.md", "sequence-flow.md", "design-doc.md", "present.md"}
FENCE = re.compile(r"^```")


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
    rel = rel[2:] if rel.startswith("./") else rel
    rel = re.sub(r":[\w.\-]+$", "", rel)
    if rel.split("/", 1)[0] in GENERATED_DIRS or rel in ARTIFACT_NAMES:
        return True
    root = Path(fixture_dir)
    if (root / rel).exists():
        return True
    words = rel.split()
    return len(words) > 1 and (root / words[-1]).exists()


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
    stripped = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    if re.search(r"<[^>]*\son[a-z]+\s*=", stripped, flags=re.IGNORECASE):
        problems.append(f"{html_path}: inline event handler found")
    if re.search(r"javascript:", stripped, flags=re.IGNORECASE):
        problems.append(f"{html_path}: javascript: URL found")
    return problems


def render_mermaid(body):
    """Return None if the diagram renders, else an error string."""
    with tempfile.TemporaryDirectory() as tmp:
        src, out, cfg = Path(tmp, "d.mmd"), Path(tmp, "d.svg"), Path(tmp, "p.json")
        src.write_text(body, encoding="utf-8")
        cfg.write_text('{"executablePath": "/opt/pw-browsers/chromium", "args": ["--no-sandbox"]}')
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
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
