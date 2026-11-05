# codemap

> Turn any codebase into architecture diagrams, dependency graphs, a mindmap, sequence flows and an onboarding guide — so you can **explain how it is built** to other people.

[한국어 README](README.md)

`codemap` is a plugin for Claude Code. Claude reads your code, then writes Mermaid diagrams and a written walkthrough into `docs/codemap/` (optionally as interactive HTML pages). Nothing to install besides the plugin, and it works with any language Claude can read.

## Install

In Claude Code:

```
/plugin marketplace add hxxnn/codemap
/plugin install codemap@codemap
```

## Update

Installed copies are not updated automatically unless you turn that on. Either enable it in `/plugin` → **Marketplaces** → `codemap` → **Enable auto-update**, or update by hand and restart Claude Code:

```
/plugin marketplace update codemap
/plugin install codemap@codemap
```

or from a terminal: `claude plugin update codemap@codemap`. This plugin has no fixed version number: every new commit on `main` counts as a new version for people who update.

## Use

Open your project in Claude Code and run:

```
/codemap
```

or pick one output (HTML pages are created by default; add `--no-html` for Markdown only):

```
/codemap architecture --no-html
/codemap deps
/codemap mindmap
/codemap sequence
/codemap doc
/codemap present
/codemap refresh
```

You can also just ask in plain words ("draw the architecture of this project", "프로젝트 구조를 마인드맵으로 보여줘"). Output is written in Korean by default; ask for another language explicitly (for example "in English") to change it.

## Use in cloud sessions (claude.ai/code, mobile, `--cloud`)

Cloud sessions cannot install marketplace plugins (there is no `/plugin` there), but they do load the `.claude/` folder that is committed to your repository. This script copies codemap into a project's `.claude/` folder:

```
git clone https://github.com/hxxnn/codemap
python3 codemap/scripts/install_into_project.py /path/to/your/project
```

Then commit and push the project's `.claude/` folder. In a cloud session on that repository, `/codemap` and the skills work like in the plugin (the skill names just have no `codemap:` prefix).

- To update, pull the latest `codemap` and run the script again. Files you edited are never overwritten: the script reports a conflict and writes nothing (`--force` overwrites).
- Use either the plugin or this copy in one project, not both, or every skill shows up twice.

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

Every Markdown file is accompanied by `docs/codemap/html/<name>.html` (unless you pass `--no-html`): a contents sidebar, a color legend, zoomable diagrams that scroll instead of shrinking, collapsible sections, search, a light/dark toggle and print-friendly pages on one page (styles and scripts are shared in `html/assets/`, so move the whole `html/` folder). The presentation outline (`present.html`) has a slide mode (arrow keys, `Esc` to leave). Text is set in the Pretendard font loaded from a CDN with a pinned version; offline, text falls back to system fonts and diagrams show their source with a note.

## Trust

- Every file and module in the output is something Claude actually read. Anything it could not confirm is labelled as inferred and carries the marker `<!-- codemap:unverified -->`.
- Each file ends with a "not covered" section naming what was skipped (large repositories are read from the entry points outward).
- Text between `<!-- codemap:manual-start -->` and `<!-- codemap:manual-end -->` is yours; `refresh` never overwrites it.
- Existing `docs/codemap/` files are never overwritten without asking. The exception is `refresh`: you asked for the update, and it keeps your manual-edit blocks. Edits you make outside those blocks are replaced on refresh.

## Examples

Generated from the small sample projects in this repository (after cloning, open `index.html` in a browser for a gallery of all 18 pages):

- [`examples/python-todo-api/docs/codemap/`](examples/python-todo-api/docs/codemap/)
- [`examples/ts-notes-cli/docs/codemap/`](examples/ts-notes-cli/docs/codemap/)
- [`examples/edge-names/docs/codemap/`](examples/edge-names/docs/codemap/) — file names with spaces and non-ASCII characters

## Customize the look

| To change | Edit |
|---|---|
| HTML colors, layout, fonts, print look | `skills/_shared/assets/codemap.css` |
| HTML behaviour (contents, zoom, slide mode) and its wording | `skills/_shared/assets/codemap.js` |
| The HTML page skeleton | `skills/_shared/html-template.html` |
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
python3 scripts/rebuild_example_html.py   # re-apply the HTML template to the example pages
node scripts/browser_check.js <page.html> [--deck] [--offline]   # open a page in a real browser (needs Playwright)
```

The design and implementation plan are in [`docs/design/codemap-design.md`](docs/design/codemap-design.md) and [`docs/superpowers/plans/2026-11-05-codemap-plugin.md`](docs/superpowers/plans/2026-11-05-codemap-plugin.md).

## License

MIT — see [LICENSE](LICENSE).
