---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flows

Three runtime scenarios of the CLI, traced through `src/index.ts` and the modules it calls: `add` (the main operation), `list` (reads storage), and an unknown command (the error path).

## Scenario 1: `notes add <text>`

The user runs `notes add "buy milk"`.

```mermaid
sequenceDiagram
  actor U as User
  participant I as src/index.ts
  participant P as src/user-profile.ts
  participant S as src/notes-store.ts
  U->>I: notes add buy milk
  I->>P: currentUser()
  P-->>I: process.env.USER or "anonymous"
  I->>S: addNote(rest.join(" "), author)
  S->>S: push {id, text, author} to notes
```

1. `src/index.ts:top level` — takes `command` and `rest` from `process.argv.slice(2)`; `command === "add"`.
2. `src/user-profile.ts:currentUser` — returns `process.env.USER ?? "anonymous"`.
3. `src/notes-store.ts:addNote` — creates a note with `id = notes.length + 1` and pushes it; the returned note is ignored by the caller and nothing is printed.

## Scenario 2: `notes list`

The user runs `notes list`.

```mermaid
sequenceDiagram
  actor U as User
  participant I as src/index.ts
  participant S as src/notes-store.ts
  participant F as src/format.ts
  U->>I: notes list
  I->>S: listNotes()
  loop each note in notes
    S->>F: formatNote(note)
    F-->>S: formatted line
  end
  S-->>I: string[]
  I->>U: console.log(line) per line
```

1. `src/index.ts:top level` — `command === "list"`.
2. `src/notes-store.ts:listNotes` — maps every stored note through `formatNote`.
3. `src/format.ts:formatNote` — returns `` `#${note.id} ${note.text} (${note.author})` ``.
4. `src/index.ts:top level` — prints each returned line with `console.log`.

Because the array lives only in the running process, a fresh `notes list` invocation starts with an empty array and prints nothing.

## Scenario 3: unknown or missing command

The user runs `notes` with no arguments or an unsupported word.

```mermaid
sequenceDiagram
  actor U as User
  participant I as src/index.ts
  U->>I: notes (other)
  alt command is "add"
    I->>I: add flow
  else command is "list"
    I->>I: list flow
  else anything else
    I->>U: console.error(usage line)
    I->>I: process.exit(1)
  end
```

1. `src/index.ts:top level` — neither branch matches, so the final `else` prints the usage line to stderr and exits with code 1.

## Not covered

All source files on these paths were read completely. `src/types.ts` only contributes the `Note` type and is not a participant. Build output (`dist/`) and Node internals were not examined.
