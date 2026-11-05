# codemap

> Turn any codebase into architecture diagrams, dependency graphs, a mindmap, sequence flows and an onboarding guide — so you can **explain how it is built** to other people.

[한국어 README](README.ko.md)

`codemap` is a plugin for Claude Code. Claude reads your code, then writes Mermaid diagrams and a written walkthrough into `docs/codemap/` (optionally as interactive HTML pages). Nothing to install besides the plugin, and it works with any language Claude can read.

## Install

In Claude Code:

```
/plugin marketplace add hxxnn/codemap
/plugin install codemap@codemap
```

## Use

Open your project in Claude Code and run:

```
/codemap
```

or pick one output, and add `--html` for an interactive page:

```
/codemap architecture --html
/codemap deps
/codemap mindmap
/codemap sequence
/codemap doc
/codemap present
/codemap refresh
```

You can also just ask in plain words ("draw the architecture of this project", "프로젝트 구조를 마인드맵으로 보여줘"). Output is written in the language you ask in.

## What you get

| Command | Skill | Output (`docs/codemap/`) |
|---|---|---|
| `/codemap architecture` | `architecture-overview` | `architecture.md` — system context → containers → components (C4-style zoom) |
| `/codemap deps` | `dependency-graph` | `dependency-graph.md` — real import graph, circular dependencies flagged |
| `/codemap mindmap` | `mindmap` | `mindmap.md` — folders and features as one mindmap |
| `/codemap sequence` | `sequence-flow` | `sequence-flow.md` — 2–3 runtime scenarios traced through the code |
| `/codemap doc` | `design-doc` | `design-doc.md` — design overview, key choices, "read these files in this order" |
| `/codemap present` | `present` | `present.md` — 5–7 slide outline built from the other outputs |
| `/codemap refresh` | `codemap-refresh` | updates only the files whose source code changed, keeping your manual edits |

`--html` additionally writes `docs/codemap/html/<name>.html`: zoomable diagrams, collapsible sections and search in a single file.

## Trust

- Every file and module in the output is something Claude actually read. Anything it could not confirm is labelled as inferred and carries the marker `<!-- codemap:unverified -->`.
- Each file ends with a "not covered" section naming what was skipped (large repositories are read from the entry points outward).
- Text between `<!-- codemap:manual-start -->` and `<!-- codemap:manual-end -->` is yours; `refresh` never overwrites it.
- Existing `docs/codemap/` files are never overwritten without asking.

## Examples

Generated from the small sample projects in this repository:

- [`examples/python-todo-api/docs/codemap/`](examples/python-todo-api/docs/codemap/)
- [`examples/ts-notes-cli/docs/codemap/`](examples/ts-notes-cli/docs/codemap/)

## Customize the look

| To change | Edit |
|---|---|
| HTML colors, layout, fonts, controls | `skills/_shared/html-template.html` |
| Mermaid style and labelling rules | `skills/_shared/mermaid-rules.md` |
| Language, file locations, front matter | `skills/_shared/language-and-output.md` |
| What each document contains | `skills/<name>/SKILL.md` |

## Develop

Try the plugin from a local checkout:

```
claude --plugin-dir /path/to/codemap
```

Check generated output against the project it describes (every referenced path must exist, diagrams must render):

```
python3 scripts/check_output.py <project_dir> <project_dir>/docs/codemap --render
pytest scripts/tests
```

The design and implementation plan are in [`docs/design/codemap-design.md`](docs/design/codemap-design.md) and [`docs/superpowers/plans/2026-11-05-codemap-plugin.md`](docs/superpowers/plans/2026-11-05-codemap-plugin.md).

## License

MIT — see [LICENSE](LICENSE).
