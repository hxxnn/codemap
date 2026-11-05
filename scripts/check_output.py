#!/usr/bin/env python3
"""Dev-only checker for generated codemap outputs.

Usage: check_output.py <fixture_dir> <output_dir> [--render]
Exit code 1 if any problem is found.
"""
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
        if re.search(r"[\s*<>{}]", token) or token.startswith("http"):
            continue
        if token in SOURCE_EXTS:
            continue
        if "/" in token or token.endswith(SOURCE_EXTS):
            refs.append(token)
    return refs


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
    if front.get("skill") not in NO_DIAGRAM_SKILLS and not mermaid_blocks(text):
        problems.append(f"{md_path}: no mermaid block")
    for line in _prose_lines(text):
        if UNVERIFIED in line:
            continue
        for ref in path_refs(line):
            rel = ref[2:] if ref.startswith("./") else ref
            rel = re.sub(r":[\w.\-]+$", "", rel)  # `path:function` or `path:12-20`
            if rel.split("/", 1)[0] in GENERATED_DIRS:
                continue
            if not (Path(fixture_dir) / rel).exists():
                problems.append(f"{md_path}: path does not exist: {ref}")
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
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
