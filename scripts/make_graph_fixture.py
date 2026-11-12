#!/usr/bin/env python3
"""Dev tool: generate a synthetic project plus its relation-map artifacts, for tests and performance checks.

Usage: make_graph_fixture.py --nodes N --groups G --out DIR

Writes under DIR: empty source files, docs/codemap/relation-map.md and
docs/codemap/html/relation-map.html (+ html/assets/). The result passes
`check_output.py DIR DIR/docs/codemap`. The graph is deterministic: node i uses
(i*7+1) % N and (i*13+5) % N, node 0 is a hub used by every 5th node, nodes 1 and 2
use each other, nodes 0..3 form a chain, every 10th node (index 9, 19, ...) is a test
and node 3 is unverified.
"""
import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_example_html import ASSETS, TEMPLATE  # noqa: E402

DATE = "2026-11-12"


def group_name(g, groups):
    if groups >= 2 and g == 0:
        return "a/utils"
    if groups >= 2 and g == 1:
        return "b/utils"
    return f"pkg{g}"


def graph(nodes, groups):
    paths = [f"{group_name(i % groups, groups)}/mod{i}.py" for i in range(nodes)]
    uses = []
    for i in range(nodes):
        targets = {(i * 7 + 1) % nodes, (i * 13 + 5) % nodes}
        if i != 0 and i % 5 == 0:
            targets.add(0)
        if i < 3:
            targets.add(i + 1)
        if i == 1:
            targets.add(2)
        if i == 2:
            targets.add(1)
        uses.append(sorted(t for t in targets if t != i and t < nodes))
    kinds = []
    for i in range(nodes):
        kinds.append("test" if i % 10 == 9 else "unverified" if i == 3 else "source")
    return paths, uses, kinds


def build(nodes, groups, out):
    out = Path(out)
    paths, uses, kinds = graph(nodes, groups)
    used_by = [[] for _ in range(nodes)]
    for i, targets in enumerate(uses):
        for t in targets:
            used_by[t].append(i)

    for p in paths:
        f = out / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# fixture\n", encoding="utf-8")

    def cell(indexes):
        return ", ".join(f"`{paths[i]}`" for i in indexes) or "—"

    rows = "".join(f"| `{paths[i]}` | 역할 {i} | {cell(uses[i])} | {cell(sorted(used_by[i]))} |\n" for i in range(nodes))
    hub = max(range(nodes), key=lambda i: len(used_by[i]))
    md = (
        f"---\ncodemap: 1\nskill: relation-map\ngenerated_at: {DATE}\ncommit: null\nsources: {{}}\n---\n"
        "<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->\n\n"
        "# 파일 관계 지도\n\n합성 프로젝트의 파일 관계입니다.\n\n"
        "## 파일 표\n\n| 파일 | 한 줄 역할 | 쓰는 파일 | 쓰이는 파일 |\n|---|---|---|---|\n" + rows +
        f"\n## 많이 쓰이는 파일\n\n- `{paths[hub]}` — {len(used_by[hub])}개 파일이 사용합니다.\n\n"
        "## 순환 의존\n\n" + (f"- `{paths[1]}` → `{paths[2]}` → `{paths[1]}`\n" if nodes > 2 else "찾지 못했습니다.\n") +
        "\n## 다루지 않은 범위\n\n합성 프로젝트라 전부 읽었습니다.\n"
    )
    codemap = out / "docs" / "codemap"
    (codemap / "html" / "assets").mkdir(parents=True, exist_ok=True)
    (codemap / "relation-map.md").write_text(md, encoding="utf-8")

    items = []
    for i in range(nodes):
        kids = "".join(f'<li data-to="g{t + 1}"></li>' for t in uses[i])
        items.append(f'<li id="g{i + 1}" data-group="{html.escape(paths[i].rsplit("/", 1)[0])}" data-kind="{kinds[i]}">'
                     f"<code>{html.escape(paths[i])}</code> 역할 {i}<ul>{kids}</ul></li>")
    table = "".join(
        f"<tr><td><code>{html.escape(paths[i])}</code></td><td>역할 {i}</td>"
        f"<td>{', '.join('<code>' + html.escape(paths[t]) + '</code>' for t in uses[i]) or '—'}</td>"
        f"<td>{', '.join('<code>' + html.escape(paths[t]) + '</code>' for t in sorted(used_by[i])) or '—'}</td></tr>"
        for i in range(nodes))
    content = (
        '<section class="cm-section"><h2>관계 그래프</h2><ul class="cm-graph">' + "".join(items) + "</ul></section>\n"
        '<section class="cm-section"><h2>파일 표</h2><table><thead><tr><th>파일</th><th>한 줄 역할</th><th>쓰는 파일</th>'
        "<th>쓰이는 파일</th></tr></thead><tbody>" + table + "</tbody></table></section>\n"
        f'<section class="cm-section"><h2>많이 쓰이는 파일</h2><ul><li><code>{html.escape(paths[hub])}</code> — '
        f"{len(used_by[hub])}개 파일이 사용합니다.</li></ul></section>\n"
        '<section class="cm-section"><h2>순환 의존</h2><p>'
        + (f"<code>{html.escape(paths[1])}</code> → <code>{html.escape(paths[2])}</code> → <code>{html.escape(paths[1])}</code>"
           if nodes > 2 else "찾지 못했습니다.") + "</p></section>\n"
        '<section class="cm-section"><h2>다루지 않은 범위</h2><p>합성 프로젝트라 전부 읽었습니다.</p></section>'
    )
    page = TEMPLATE.read_text(encoding="utf-8")
    for key, value in {"{{LANG}}": "ko", "{{TITLE}}": "파일 관계 지도", "{{PROJECT}}": "fixture",
                       "{{GENERATED}}": DATE, "{{SOURCES}}": "0", "{{CONTENT}}": content}.items():
        page = page.replace(key, value)
    (codemap / "html" / "relation-map.html").write_text(page, encoding="utf-8")
    for asset in ASSETS.iterdir():
        (codemap / "html" / "assets" / asset.name).write_bytes(asset.read_bytes())


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--nodes", type=int, required=True)
    parser.add_argument("--groups", type=int, required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.nodes < 1 or args.groups < 1:
        parser.error("--nodes and --groups must be at least 1")
    build(args.nodes, args.groups, args.out)
    print(f"wrote {args.nodes} files in {args.groups} groups under {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
