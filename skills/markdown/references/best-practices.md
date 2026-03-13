# Markdown Best Practices

Use these conventions when writing or refactoring docs.

## Headings

- Start with a single `#` title.
- Increase heading depth one level at a time.
- Keep headings short and descriptive.
- Avoid empty sections and one-off headings with a single sentence under them.

## Paragraphs and Lists

- Prefer short paragraphs over dense walls of text.
- Use bullets for enumerations, commands, and checklists.
- Keep bullet phrasing parallel where possible.
- Avoid deeply nested lists unless hierarchy is essential.

## Code Blocks

- Always fence multi-line code blocks.
- Add an info string such as `bash`, `python`, `toml`, `js`, or `html`.
- Keep examples minimal but executable-looking.
- Prefer one command per line in shell examples.

## Links and References

- Use descriptive link text.
- Link the first meaningful mention of a tool or spec when it helps orientation.
- Avoid dumping raw URLs in the middle of prose unless the URL itself matters.

## Tables

- Use tables for compact comparisons or matrices.
- Keep cell text short.
- Prefer bullets or sections when explanations are longer than a phrase.

## Readability

- Keep documents scannable.
- Prefer explicit names over shorthand.
- Avoid decorative formatting that does not add structure.
- When editing an existing doc, preserve local style unless it blocks
  readability or lint compliance.
