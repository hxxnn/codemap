# Language, output and bookkeeping rules (shared by every codemap skill)

## Language
Write all prose, captions and labels in the language the user used to ask for the work (Korean request → Korean output, English → English). Skill instructions are English; the output is not. File names, code identifiers and paths are never translated.

## Where output goes
Write into the target project's `docs/codemap/`:

| Skill | File |
|---|---|
| architecture-overview | `architecture.md` |
| dependency-graph | `dependency-graph.md` |
| mindmap | `mindmap.md` |
| sequence-flow | `sequence-flow.md` |
| design-doc | `design-doc.md` |
| present | `present.md` |

HTML versions (only when the user passes `--html` or asks for HTML) go to `docs/codemap/html/<same-name>.html`.

**Never overwrite silently.** If `docs/codemap/` already holds a file you are about to write, ask the user first (suggest `/codemap refresh` as the alternative). Text between `<!-- codemap:manual-start -->` and `<!-- codemap:manual-end -->` belongs to the user and must be preserved byte-for-byte whenever a file is rewritten.

## Front matter (first lines of every generated file)
```yaml
---
codemap: 1
skill: <skill name>
generated_at: <ISO-8601 date>
commit: <git HEAD sha, or null when not a git repo>
sources: {<relative/path>: <sha256 of that file when read>, ...}
---
```
`sources` lists every file the artifact was derived from. Compute hashes with `sha256sum` (or `shasum -a 256`). `codemap-refresh` relies on this block, so keep it accurate. Artifacts derived from other artifacts (design-doc, present) list those artifact paths in `sources` too.

## Paths
In prose always write the full repo-relative path in backticks (`src/index.ts`, never a bare `index.ts`). Sibling artifacts may be named by file name (`architecture.md`). Build or install folders that do not exist in the repo (`dist/`, `node_modules/`) are written without backticks and labelled as build output.

## Unverified content
Anything you could not confirm in the code is never stated as fact. Mark it with a visible label in the user's language (for example "(inferred)" / "(확인 필요)") **and** add the marker `<!-- codemap:unverified -->` on the same line. Design rationale ("why it was built this way") with no evidence in the code is always unverified.

## Project summary (built once by `/codemap`, handed to every skill)
A bullet list with these keys:
- `languages`: detected languages
- `frameworks`: frameworks/libraries that shape the structure
- `entry_points`: files where execution starts (main, server start, CLI)
- `core_modules`: the 5–15 modules/folders that carry the logic
- `external_systems`: databases, APIs, queues, users
- `unread_scope`: what you did not read (large folders, generated code, vendored code), or `none`

## Unread-scope footer
Every generated file ends with a short section naming `unread_scope` in the user's language (e.g. "Not covered" / "다루지 않은 범위"). For a small repo that was read completely, say so.

## Large repositories
Do not try to read everything. Start from `entry_points`, follow imports along the main paths, skip generated/vendored/build folders, and record what was skipped in `unread_scope`.
