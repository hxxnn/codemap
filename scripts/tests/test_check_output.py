import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_output as co  # noqa: E402

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


FM = "---\ncodemap: 1\nskill: {skill}\ngenerated_at: 2026-11-05\ncommit: null\nsources: {{}}\n---\n"
BLOCK = "```mermaid\nflowchart TD\n  A --> B\n```\n"


def write(tmp_path, name, body, skill="architecture-overview", front=True):
    p = tmp_path / name
    text = (FM.format(skill=skill) if front else "") + body
    p.write_text(text, encoding="utf-8")
    return p


def fixture(tmp_path):
    fx = tmp_path / "fx"
    (fx / "src").mkdir(parents=True, exist_ok=True)
    (fx / "src" / "real.py").write_text("x = 1\n")
    (fx / "my notes.md").write_text("n\n")
    return fx


def test_missing_front_matter_is_reported(tmp_path):
    md = write(tmp_path, "a.md", BLOCK, front=False)
    problems = co.check_file(md, fixture(tmp_path))
    assert any("front matter" in p for p in problems)


def test_nonexistent_path_is_reported(tmp_path):
    md = write(tmp_path, "a.md", BLOCK + "See `src/ghost.py`.\n")
    problems = co.check_file(md, fixture(tmp_path))
    assert any("src/ghost.py" in p for p in problems)


def test_unverified_line_may_reference_unknown_path(tmp_path):
    md = write(tmp_path, "a.md", BLOCK + "See `src/ghost.py`. <!-- codemap:unverified -->\n")
    assert co.check_file(md, fixture(tmp_path)) == []


def test_no_mermaid_block_fails_for_architecture_only(tmp_path):
    fx = fixture(tmp_path)
    arch = write(tmp_path, "a.md", "no diagram\n")
    doc = write(tmp_path, "d.md", "no diagram\n", skill="design-doc")
    assert any("mermaid" in p for p in co.check_file(arch, fx))
    assert co.check_file(doc, fx) == []


def test_valid_file_passes(tmp_path):
    md = write(tmp_path, "a.md", BLOCK + "Entry is `src/real.py`.\n")
    assert co.check_file(md, fixture(tmp_path)) == []


def test_paths_inside_code_fences_are_ignored(tmp_path):
    md = write(tmp_path, "a.md", BLOCK + "```\n`src/ghost.py`\n```\n")
    assert co.check_file(md, fixture(tmp_path)) == []


def test_main_returns_1_on_problems_and_0_when_clean(tmp_path, capsys):
    fx = fixture(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    write(out, "a.md", BLOCK + "`src/ghost.py`\n")
    assert co.main([str(fx), str(out)]) == 1
    assert "src/ghost.py" in capsys.readouterr().out
    (out / "a.md").unlink()
    write(out, "b.md", BLOCK)
    assert co.main([str(fx), str(out)]) == 0


def test_render_flag_reports_render_failures(tmp_path, monkeypatch, capsys):
    fx = fixture(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    write(out, "a.md", BLOCK)
    monkeypatch.setattr(co, "render_mermaid", lambda body: "boom")
    assert co.main([str(fx), str(out), "--render"]) == 1
    assert "boom" in capsys.readouterr().out


def test_generated_and_vendored_dirs_may_be_mentioned(tmp_path):
    fx = fixture(tmp_path)
    body = BLOCK + "Built into `dist/index.js`; deps live in `node_modules/` and `.venv/bin/python`.\n"
    assert co.check_file(write(tmp_path, "a.md", body), fx) == []
    md2 = write(tmp_path, "b.md", BLOCK + "See `distro/ghost.py`.\n")
    assert any("distro/ghost.py" in p for p in co.check_file(md2, fx))


def test_bare_extensions_are_not_treated_as_paths(tmp_path):
    md = write(tmp_path, "a.md", BLOCK + "Only `.py` and `.ts` files were read.\n")
    assert co.check_file(md, fixture(tmp_path)) == []


def test_path_with_symbol_or_line_suffix_checks_only_the_path(tmp_path):
    fx = fixture(tmp_path)
    ok = write(tmp_path, "a.md", BLOCK + "Calls `src/real.py:main` and `src/real.py:12-20`.\n")
    assert co.check_file(ok, fx) == []
    bad = write(tmp_path, "b.md", BLOCK + "Calls `src/ghost.py:main`.\n")
    problems = co.check_file(bad, fx)
    assert any("src/ghost.py" in p for p in problems)


def test_sibling_artifact_names_may_be_referenced(tmp_path):
    fx = fixture(tmp_path)
    md = write(tmp_path, "d.md", "See `architecture.md` and `sequence-flow.md`.\n", skill="design-doc")
    assert co.check_file(md, fx) == []
    bad = write(tmp_path, "e.md", "See `notes.md`.\n", skill="design-doc")
    assert any("notes.md" in p for p in co.check_file(bad, fx))


def test_source_hashes_must_be_sha256(tmp_path):
    fx = fixture(tmp_path)
    ok = tmp_path / "ok.md"
    ok.write_text(FM.replace("sources: {{}}", "sources: {{src/real.py: " + sha(fx / "src" / "real.py") + "}}").format(skill="architecture-overview") + BLOCK)
    assert co.check_file(ok, fx) == []
    bad = tmp_path / "bad.md"
    bad.write_text(FM.replace("sources: {{}}", "sources: {{src/real.py: null}}").format(skill="architecture-overview") + BLOCK)
    assert any("sha256" in p for p in co.check_file(bad, fx))



def test_http_routes_are_not_file_paths(tmp_path):
    fx = fixture(tmp_path)
    md = write(tmp_path, "a.md", BLOCK + "Handles `POST /todos`-style routes at `/todos` and `/api/v1/items`.\n")
    assert co.check_file(md, fx) == []


def with_sources(tmp_path, name, mapping, body=BLOCK, skill="architecture-overview"):
    items = ", ".join(f"{k}: {v}" for k, v in mapping.items())
    p = tmp_path / name
    p.write_text(FM.replace("sources: {{}}", "sources: {{" + items + "}}").format(skill=skill) + body)
    return p


def test_sources_key_must_exist_and_hash_must_match(tmp_path):
    fx = fixture(tmp_path)
    real = sha(fx / "src" / "real.py")
    assert co.check_file(with_sources(tmp_path, "a.md", {"src/real.py": real}), fx) == []
    wrong = with_sources(tmp_path, "b.md", {"src/real.py": "a" * 64})
    assert any("hash mismatch" in p and "src/real.py" in p for p in co.check_file(wrong, fx))
    ghost = with_sources(tmp_path, "c.md", {"src/ghost.py": "a" * 64})
    assert any("source does not exist" in p and "src/ghost.py" in p for p in co.check_file(ghost, fx))


def test_block_style_sources_are_rejected(tmp_path):
    fx = fixture(tmp_path)
    md = tmp_path / "a.md"
    md.write_text("---\ncodemap: 1\nskill: architecture-overview\ngenerated_at: 2026-11-05\nsources:\n  src/real.py: null\n---\n" + BLOCK)
    assert any("one-line" in p for p in co.check_file(md, fx))


def test_ghost_path_inside_mermaid_label_is_reported(tmp_path):
    fx = fixture(tmp_path)
    bad_block = "```mermaid\nflowchart TD\n  g[\"Ghost (app/ghost.py)\"] --> r[\"Real (src/real.py)\"]\n```\n"
    problems = co.check_file(write(tmp_path, "a.md", bad_block), fx)
    assert any("app/ghost.py" in p for p in problems)
    assert not any("src/real.py" in p for p in problems)
    ok_block = "```mermaid\nflowchart TD\n  %% codemap:unverified\n  g[\"Ghost (app/ghost.py)\"]\n  n[\"Node.js and read/write, dist/index.js\"]\n```\n"
    assert co.check_file(write(tmp_path, "b.md", ok_block), fx) == []


def test_paths_with_spaces_are_checked(tmp_path):
    fx = fixture(tmp_path)
    assert co.check_file(write(tmp_path, "a.md", BLOCK + "See `my notes.md` and run `pytest src/real.py`.\n"), fx) == []
    problems = co.check_file(write(tmp_path, "b.md", BLOCK + "See `ghost file.md`.\n"), fx)
    assert any("ghost file.md" in p for p in problems)


def test_quoted_sequence_alias_is_reported(tmp_path):
    fx = fixture(tmp_path)
    seq = "```mermaid\nsequenceDiagram\n  participant C as \"HTTP client\"\n  C->>C: x\n```\n"
    assert any("alias" in p for p in co.check_file(write(tmp_path, "a.md", seq), fx))
    ok = "```mermaid\nsequenceDiagram\n  participant C as HTTP client\n  C->>C: x\n```\n"
    assert co.check_file(write(tmp_path, "b.md", ok), fx) == []


HTML_OK = (
    '<html><head><title>T</title></head><body><main><p>a &lt;b&gt;</p></main>'
    '<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>'
    '<script>/* template */</script></body></html>'
)


def test_html_with_injected_script_or_handler_is_reported(tmp_path):
    ok = tmp_path / "ok.html"
    ok.write_text(HTML_OK)
    assert co.check_html(ok) == []
    extra = tmp_path / "extra.html"
    extra.write_text(HTML_OK.replace("<main>", "<main><script>alert(1)</script>"))
    assert any("script" in p for p in co.check_html(extra))
    handler = tmp_path / "h.html"
    handler.write_text(HTML_OK.replace("<p>", '<p onclick="x()">'))
    assert any("event handler" in p for p in co.check_html(handler))
    js = tmp_path / "j.html"
    js.write_text(HTML_OK.replace("<p>", '<a href="javascript:x()">').replace("</p>", "</a>"))
    assert any("javascript:" in p for p in co.check_html(js))


def test_chromium_path_prefers_env_then_existing_default_else_none(monkeypatch):
    monkeypatch.setenv("CODEMAP_CHROMIUM", "/custom/chrome")
    assert co.chromium_path() == "/custom/chrome"
    monkeypatch.delenv("CODEMAP_CHROMIUM")
    monkeypatch.setattr(co.Path, "exists", lambda self: str(self) == "/opt/pw-browsers/chromium")
    assert co.chromium_path() == "/opt/pw-browsers/chromium"
    monkeypatch.setattr(co.Path, "exists", lambda self: False)
    assert co.chromium_path() is None


def test_relative_import_specifiers_match_a_file_anywhere_in_the_project(tmp_path):
    fx = fixture(tmp_path)
    ok = write(tmp_path, "a.md", BLOCK + "Imports `./real.py` and `../src/real.py` and `./my notes.md`.\n")
    assert co.check_file(ok, fx) == []
    bad = write(tmp_path, "b.md", BLOCK + "Imports `./ghost.py`.\n")
    assert any("./ghost.py" in p for p in co.check_file(bad, fx))


def test_unfilled_template_placeholders_are_reported(tmp_path):
    page = tmp_path / "p.html"
    page.write_text(HTML_OK.replace("<main>", "<main>{{PROJECT}}"))
    assert any("placeholder" in p and "{{PROJECT}}" in p for p in co.check_html(page))


def test_html_must_have_the_asset_files_it_links_to(tmp_path):
    html_dir = tmp_path / "html"
    html_dir.mkdir()
    page = html_dir / "p.html"
    page.write_text(
        HTML_OK.replace("<title>", '<link rel="stylesheet" href="assets/codemap.css"><title>')
        .replace("<script>/* template */</script>", '<script src="assets/codemap.js"></script>')
    )
    problems = co.check_html(page)
    assert any("assets/codemap.css" in p for p in problems)
    assert any("assets/codemap.js" in p for p in problems)
    (html_dir / "assets").mkdir()
    (html_dir / "assets" / "codemap.css").write_text("/* css */")
    (html_dir / "assets" / "codemap.js").write_text("/* js */")
    assert co.check_html(page) == []


def test_mindmap_tree_needs_no_diagram_but_its_paths_are_still_checked(tmp_path):
    fx = fixture(tmp_path)
    tree = "- **proj**: demo\n  - **Core**: logic\n    - `src/real.py`: the code\n"
    ok = write(tmp_path, "m.md", tree, skill="mindmap")
    assert co.check_file(ok, fx) == []
    bad = write(tmp_path, "n.md", tree + "    - `src/ghost.py`: made up\n", skill="mindmap")
    assert any("src/ghost.py" in p for p in co.check_file(bad, fx))


def test_slashed_code_phrases_are_not_paths_but_real_looking_paths_still_are(tmp_path):
    fx = fixture(tmp_path)
    ok = write(tmp_path, "a.md", BLOCK + "Use `async/await`, `if/else` and `read/write` freely.\n")
    assert co.check_file(ok, fx) == []
    ghost_in_real_dir = write(tmp_path, "b.md", BLOCK + "See `src/ghost`.\n")
    assert any("src/ghost" in p for p in co.check_file(ghost_in_real_dir, fx))
    ghost_folder = write(tmp_path, "c.md", BLOCK + "See `nowhere/`.\n")
    assert any("nowhere/" in p for p in co.check_file(ghost_folder, fx))
    ghost_file = write(tmp_path, "d.md", BLOCK + "See `lib/util.py`.\n")
    assert any("lib/util.py" in p for p in co.check_file(ghost_file, fx))


# ---- relation-map -----------------------------------------------------------

def graph_html(nodes):
    items = []
    for nid, group, kind, path, to in nodes:
        kids = "".join(f'<li data-to="{t}"></li>' for t in to)
        items.append(f'<li id="{nid}" data-group="{group}" data-kind="{kind}"><code>{path}</code> 역할<ul>{kids}</ul></li>')
    return '<ul class="cm-graph">' + "".join(items) + "</ul>"


def rel_md(rows):
    def cell(paths):
        return ", ".join(f"`{p}`" for p in paths) or "—"
    head = "| 파일 | 역할 | 쓰는 파일 | 쓰이는 파일 |\n|---|---|---|---|\n"
    return head + "".join(f"| `{p}` | 역할 | {cell(u)} | {cell(b)} |\n" for p, u, b in rows)


def rel_setup(tmp_path, nodes, rows, files=("src/a.py", "src/b.py")):
    fx = fixture(tmp_path)
    for f in files:
        p = fx / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x\n", encoding="utf-8")
    html = tmp_path / "relation-map.html"
    html.write_text(f"<main>{graph_html(nodes)}</main>", encoding="utf-8")
    md = write(tmp_path, "relation-map.md", rel_md(rows), skill="relation-map")
    return html, md, fx


GOOD_NODES = [("g1", "src", "source", "src/a.py", ["g2"]), ("g2", "src", "source", "src/b.py", [])]
GOOD_ROWS = [("src/a.py", ["src/b.py"], []), ("src/b.py", [], ["src/a.py"])]


def test_relation_graph_valid_passes(tmp_path):
    html, md, fx = rel_setup(tmp_path, GOOD_NODES, GOOD_ROWS)
    assert co.check_relation_graph(html, md, fx) == []


def test_relation_graph_dangling_edge_is_reported(tmp_path):
    nodes = [("g1", "src", "source", "src/a.py", ["g9"]), GOOD_NODES[1]]
    html, md, fx = rel_setup(tmp_path, nodes, GOOD_ROWS)
    assert any("dangling" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_duplicate_id_is_reported(tmp_path):
    nodes = [GOOD_NODES[0], ("g1", "src", "source", "src/b.py", [])]
    html, md, fx = rel_setup(tmp_path, nodes, GOOD_ROWS)
    assert any("duplicate id" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_self_edge_is_reported(tmp_path):
    nodes = [("g1", "src", "source", "src/a.py", ["g1"]), GOOD_NODES[1]]
    html, md, fx = rel_setup(tmp_path, nodes, GOOD_ROWS)
    assert any("self" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_ghost_node_path_is_reported(tmp_path):
    nodes = [GOOD_NODES[0], ("g2", "src", "source", "src/ghost.py", [])]
    html, md, fx = rel_setup(tmp_path, nodes, GOOD_ROWS)
    assert any("does not exist" in p and "src/ghost.py" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_bad_kind_or_missing_group_is_reported(tmp_path):
    html, md, fx = rel_setup(tmp_path, [("g1", "src", "weird", "src/a.py", []), GOOD_NODES[1]], GOOD_ROWS)
    assert any("data-kind" in p for p in co.check_relation_graph(html, md, fx))
    html, md, fx = rel_setup(tmp_path, [("g1", "", "source", "src/a.py", []), GOOD_NODES[1]], GOOD_ROWS)
    assert any("data-group" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_must_match_markdown_table(tmp_path):
    rows = [("src/a.py", [], []), ("src/b.py", [], [])]  # table lacks the a->b edge the graph has
    html, md, fx = rel_setup(tmp_path, GOOD_NODES, rows)
    assert any("mismatch" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_table_used_by_must_invert_uses(tmp_path):
    rows = [("src/a.py", ["src/b.py"], []), ("src/b.py", [], [])]  # b should list a as a user
    html, md, fx = rel_setup(tmp_path, GOOD_NODES, rows)
    assert any("used-by" in p for p in co.check_relation_graph(html, md, fx))


def test_relation_graph_paths_with_spaces_and_korean_work(tmp_path):
    nodes = [("g1", "src", "source", "src/내 파일 1.py", ["g2"]), GOOD_NODES[1]]
    rows = [("src/내 파일 1.py", ["src/b.py"], []), ("src/b.py", [], ["src/내 파일 1.py"])]
    html, md, fx = rel_setup(tmp_path, nodes, rows, files=("src/내 파일 1.py", "src/b.py"))
    assert co.check_relation_graph(html, md, fx) == []
    assert co.parse_graph_html(html.read_text(encoding="utf-8"))[0]["path"] == "src/내 파일 1.py"


def test_relation_map_markdown_needs_no_diagram(tmp_path):
    html, md, fx = rel_setup(tmp_path, GOOD_NODES, GOOD_ROWS)
    assert co.check_file(md, fx) == []
