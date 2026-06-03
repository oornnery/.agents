# .mem

Durable project memory for agents.

Use `.mem/` for stable, reusable facts that help future sessions. Keep it concise and safe to read. Do not store secrets, credentials, private user data, raw transcripts, speculative guesses, or large command output.

Temperature:

- `hot.md`: high-value facts loaded often, max 80 lines
- `decisions.md`: accepted decisions and rationale
- `open-loops.md`: unresolved questions and follow-ups
- `private/`: local-only sensitive notes, ignored by the template gitignore
