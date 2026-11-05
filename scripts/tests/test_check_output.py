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
    (fx / "src").mkdir(parents=True)
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
