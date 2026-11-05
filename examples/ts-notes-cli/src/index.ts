#!/usr/bin/env node
import { addNote, listNotes } from "./notes-store";
import { currentUser } from "./user-profile";

const [command, ...rest] = process.argv.slice(2);

if (command === "add") {
  addNote(rest.join(" "), currentUser());
} else if (command === "list") {
  listNotes().forEach((line) => console.log(line));
} else {
  console.error("usage: notes add <text> | notes list");
  process.exit(1);
}
