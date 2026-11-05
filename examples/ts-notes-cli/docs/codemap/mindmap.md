---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---

# Mindmap

The `notes-cli` project at a glance, grouped by what the code does.

```mermaid
mindmap
  root((notes-cli))
    a1["CLI"]
      a2["src/index.ts: parses add / list"]
    a3["Storage"]
      a4["src/notes-store.ts: in-memory notes"]
        a5["addNote()"]
        a6["listNotes()"]
    a7["Identity"]
      a8["src/user-profile.ts: reads USER"]
        a9["currentUser()"]
    a10["Presentation"]
      a11["src/format.ts: one-line note text"]
        a12["formatNote()"]
    a13["Types"]
      a14["src/types.ts: Note interface"]
```

The five groups map one-to-one onto the five files in `src/`.

## Groups

- CLI: command-line entry and usage message.
- Storage: keeps notes in a module-level array and adds or lists them.
- Identity: picks the author name from `USER`, falling back to "anonymous".
- Presentation: turns a `Note` into a printable line.
- Types: the shared `Note` shape (`id`, `text`, `author`).

## Not covered

Nothing was skipped; the whole repository was read.
