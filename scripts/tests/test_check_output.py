import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_output as co  # noqa: E402

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
    good_hash = "a" * 64
    ok = tmp_path / "ok.md"
    ok.write_text(FM.replace("sources: {{}}", "sources: {{src/real.py: " + good_hash + "}}").format(skill="architecture-overview") + BLOCK)
    assert co.check_file(ok, fx) == []
    bad = tmp_path / "bad.md"
    bad.write_text(FM.replace("sources: {{}}", "sources: {{src/real.py: null}}").format(skill="architecture-overview") + BLOCK)
    assert any("sha256" in p for p in co.check_file(bad, fx))


def test_http_routes_are_not_file_paths(tmp_path):
    fx = fixture(tmp_path)
    md = write(tmp_path, "a.md", BLOCK + "Handles `POST /todos`-style routes at `/todos` and `/api/v1/items`.\n")
    assert co.check_file(md, fx) == []
