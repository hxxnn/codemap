---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Sequence flows

Three scenarios traced through the code: `notes add`, `notes list`, and an unknown command. They were chosen as the write path, the read path and the only error path in `src/index.ts`.

## notes add

Trigger: the user runs `notes add <text>`.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  participant P as src/user-profile.ts
  participant S as src/notes-store.ts
  U->>I: notes add text
  I->>P: currentUser()
  P-->>I: USER or "anonymous"
  I->>S: addNote(text, author)
  S->>S: push Note into notes array
```

The text is the remaining arguments joined by spaces, and the new note is appended to the in-memory array.

1. `src/index.ts:top level` reads `process.argv`, matches `command === "add"`, and joins the remaining args.
2. `src/user-profile.ts:currentUser` returns `process.env.USER ?? "anonymous"`.
3. `src/notes-store.ts:addNote` builds `{ id, text, author }` with `id = notes.length + 1` and pushes it.

Nothing is printed on success, because `src/index.ts` ignores the returned `Note`.

## notes list

Trigger: the user runs `notes list`.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  participant S as src/notes-store.ts
  participant F as src/format.ts
  U->>I: notes list
  I->>S: listNotes()
  loop each note
    S->>F: formatNote(note)
    F-->>S: "#id text (author)"
  end
  S-->>I: string array
  I->>U: console.log per line
```

Each stored note is formatted into one line and printed.

1. `src/index.ts:top level` matches `command === "list"`.
2. `src/notes-store.ts:listNotes` maps `formatNote` over the notes array.
3. `src/format.ts:formatNote` returns `#${id} ${text} (${author})`.
4. `src/index.ts:top level` prints each line with `console.log`.

Because the array is in memory only, a fresh process always lists nothing.

## Unknown command

Trigger: the user runs `notes` with no command or an unknown one.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  U->>I: notes other
  I->>U: console.error usage message
  I->>I: process.exit(1)
```

The usage line goes to stderr and the process exits with code 1.

1. `src/index.ts:top level` falls through to the `else` branch, prints `usage: notes add <text> | notes list`, and exits with status 1.

## Not covered

Nothing was skipped; all source files on these paths were read. Node's own `process` and `console` internals are library boundaries and were not traced.
