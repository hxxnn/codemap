import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import install_into_project as ip  # noqa: E402

REAL_SOURCE = Path(__file__).resolve().parents[2]
SKILLS = ["architecture-overview", "dependency-graph", "mindmap", "design-doc",
          "sequence-flow", "present", "codemap-refresh"]


def fake_source(tmp_path, body="v1"):
    src = tmp_path / "src"
    (src / "skills" / "alpha").mkdir(parents=True, exist_ok=True)
    (src / "skills" / "_shared").mkdir(parents=True, exist_ok=True)
    (src / "commands").mkdir(parents=True, exist_ok=True)
    (src / "skills" / "alpha" / "SKILL.md").write_text(f"alpha {body}\n")
    (src / "skills" / "_shared" / "rules.md").write_text("shared\n")
    (src / "commands" / "codemap.md").write_text("read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/rules.md` first\n")
    return src


def project(tmp_path):
    p = tmp_path / "proj"
    p.mkdir(exist_ok=True)
    return p


def test_installs_all_skills_shared_files_and_a_rewritten_command(tmp_path):
    proj = project(tmp_path)
    code, _ = ip.install(REAL_SOURCE, proj)
    assert code == 0
    for name in SKILLS:
        assert (proj / ".claude" / "skills" / name / "SKILL.md").is_file(), name
    for shared in ["mermaid-rules.md", "language-and-output.md", "html-template.html"]:
        assert (proj / ".claude" / "skills" / "_shared" / shared).is_file(), shared
    cmd = (proj / ".claude" / "commands" / "codemap.md").read_text()
    assert "${CLAUDE_PLUGIN_ROOT}" not in cmd
    assert ".claude/skills/_shared/language-and-output.md" in cmd


def test_second_run_changes_nothing(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    assert ip.install(src, proj)[0] == 0
    before = {p: p.read_bytes() for p in (proj / ".claude").rglob("*") if p.is_file()}
    code, lines = ip.install(src, proj)
    assert code == 0
    assert {p: p.read_bytes() for p in (proj / ".claude").rglob("*") if p.is_file()} == before
    assert any("unchanged" in line for line in lines)


def test_untouched_files_are_updated_when_the_source_changes(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    ip.install(src, proj)
    (src / "skills" / "alpha" / "SKILL.md").write_text("alpha v2\n")
    code, lines = ip.install(src, proj)
    assert code == 0
    assert (proj / ".claude" / "skills" / "alpha" / "SKILL.md").read_text() == "alpha v2\n"
    assert any(line.startswith("updated") for line in lines)


def test_locally_edited_file_is_a_conflict_and_nothing_is_written(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    ip.install(src, proj)
    mine = proj / ".claude" / "skills" / "alpha" / "SKILL.md"
    mine.write_text("my edit\n")
    (src / "skills" / "alpha" / "SKILL.md").write_text("alpha v2\n")
    (src / "skills" / "_shared" / "rules.md").write_text("shared v2\n")
    code, lines = ip.install(src, proj)
    assert code == 1
    assert mine.read_text() == "my edit\n"
    assert (proj / ".claude" / "skills" / "_shared" / "rules.md").read_text() == "shared\n"  # all-or-nothing
    assert any("conflict" in line and "alpha" in line for line in lines)
    code, _ = ip.install(src, proj, force=True)
    assert code == 0
    assert mine.read_text() == "alpha v2\n"


def test_unrelated_project_files_are_left_alone(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    (proj / ".claude" / "skills" / "mine").mkdir(parents=True)
    (proj / ".claude" / "skills" / "mine" / "SKILL.md").write_text("keep me\n")
    (proj / ".claude" / "settings.json").write_text('{"a": 1}\n')
    assert ip.install(src, proj)[0] == 0
    assert (proj / ".claude" / "skills" / "mine" / "SKILL.md").read_text() == "keep me\n"
    assert (proj / ".claude" / "settings.json").read_text() == '{"a": 1}\n'


def test_a_preexisting_different_file_without_a_record_is_a_conflict(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    (proj / ".claude" / "commands").mkdir(parents=True)
    (proj / ".claude" / "commands" / "codemap.md").write_text("someone else's command\n")
    code, lines = ip.install(src, proj)
    assert code == 1
    assert (proj / ".claude" / "commands" / "codemap.md").read_text() == "someone else's command\n"


def test_manifest_records_sha256_of_installed_files(tmp_path):
    src, proj = fake_source(tmp_path), project(tmp_path)
    ip.install(src, proj)
    manifest = json.loads((proj / ".claude" / "codemap-install.json").read_text())
    assert ".claude/skills/alpha/SKILL.md" in manifest["files"]
    assert all(len(v) == 64 for v in manifest["files"].values())


def test_missing_target_directory_is_a_usage_error(tmp_path):
    src = fake_source(tmp_path)
    code, lines = ip.install(src, tmp_path / "does-not-exist")
    assert code == 2
    assert any("not a directory" in line for line in lines)
