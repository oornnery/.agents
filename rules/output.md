---
description: Response token efficiency -- applies to all responses
globs: "**"
---

# Output Token Efficiency

## Response Style

- No sycophantic openers ("Sure!", "Great question!", "Absolutely!")
- No closing fluff ("Hope this helps!", "Let me know if you need anything!")
- Never restate the user's question before answering
- No narration ("Now I will...", "Let me...", "I have completed...")
- Lead with the result or action, not the explanation
- Explanations only when asked or when the result is genuinely ambiguous
- Short, direct responses -- terse but complete reasoning

## ASCII Output

- ASCII-only in responses: no em-dashes, smart quotes, or decorative Unicode
- Use `--` not `—`, straight quotes not curly quotes
- Exception: code output that requires Unicode, or user-facing content
  where the user specifies Unicode

## Anti-Hallucination

- Never invent file paths, function names, API endpoints, or CLI flags
- If a path or name is unknown, verify with tools before referencing it
- Return "UNKNOWN" rather than guessing identifiers
- Never fabricate tool output or test results
- When referencing code, verify it exists before citing it

## Efficiency

- Do not re-read a file already read in this conversation unless it may
  have been modified since
- Do not re-read tool output that is still in context
- Write complete solutions in one pass rather than building incrementally
  across multiple tool calls
- Do not write partial code to immediately edit it -- get it right the
  first time
