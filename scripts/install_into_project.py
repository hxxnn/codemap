#!/usr/bin/env python3
"""Copy codemap into a project's .claude/ folder so it also works in cloud sessions.

Cloud sessions (claude.ai/code, mobile Code tab, `claude --cloud`) cannot install
marketplace plugins, but they do load .claude/skills and .claude/commands that are
committed to the repository.

Usage: install_into_project.py [PROJECT_DIR] [--force]
  PROJECT_DIR  project to install into (default: current directory)
  --force      overwrite files even if you edited them
Re-run it from a newer codemap checkout to update. Files you edited are never
overwritten without --force: the script reports a conflict and writes nothing.
"""
import hashlib
import json
import sys
from pathlib import Path

MANIFEST = ".claude/codemap-install.json"
PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}/skills/_shared/"
LOCAL_SHARED = ".claude/skills/_shared/"


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _planned_files(source_root):
    """Yield (relative destination path, bytes) for everything to install."""
    source_root = Path(source_root)
    for path in sorted((source_root / "skills").rglob("*")):
        rel = path.relative_to(source_root / "skills")
        if not path.is_file() or any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        yield f".claude/skills/{rel.as_posix()}", path.read_bytes()
    command = source_root / "commands" / "codemap.md"
    if command.is_file():
        text = command.read_text(encoding="utf-8").replace(PLUGIN_ROOT_VAR, LOCAL_SHARED)
        yield ".claude/commands/codemap.md", text.encode("utf-8")


def install(source_root, target_dir, force=False):
    """Return (exit_code, report_lines). 0 ok, 1 conflict (nothing written), 2 usage error."""
    target = Path(target_dir)
    if not target.is_dir():
        return 2, [f"error: {target} is not a directory"]
    manifest_path = target / MANIFEST
    recorded = {}
    if manifest_path.is_file():
        try:
            recorded = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})
        except (ValueError, OSError):
            recorded = {}

    plan = list(_planned_files(source_root))
    new, updated, unchanged, conflicts = [], [], [], []
    for rel, data in plan:
        dest = target / rel
        if not dest.exists():
            new.append(rel)
            continue
        current = dest.read_bytes()
        if current == data:
            unchanged.append(rel)
        elif force or recorded.get(rel) == _sha(current):
            updated.append(rel)          # untouched since we installed it (or forced)
        else:
            conflicts.append(rel)        # edited by the user, or not ours

    if conflicts:
        lines = [f"conflict: {rel} (you changed it, or it already existed; use --force to overwrite)" for rel in conflicts]
        lines.append("nothing was written")
        return 1, lines

    for rel, data in plan:
        dest = target / rel
        if rel in new or rel in updated:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps({"files": {rel: _sha(data) for rel, data in plan}}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [f"new: {rel}" for rel in new] + [f"updated: {rel}" for rel in updated]
    lines.append(f"unchanged: {len(unchanged)} file(s)")
    if new or updated:
        lines.append("done. Commit and push the .claude/ folder so cloud sessions get it.")
    return 0, lines


def main(argv):
    force = "--force" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) > 1 or any(a.startswith("--") and a != "--force" for a in argv):
        print(__doc__)
        return 2
    code, lines = install(Path(__file__).resolve().parents[1], Path(args[0]) if args else Path.cwd(), force)
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
