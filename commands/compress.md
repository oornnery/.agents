---
name: compress
description: Engine-agnostic structural compression for natural-language instruction files. Use when reducing tokens in AGENTS, CLAUDE, memory, todo, preference, Markdown, or text files with active model only.
---

# Compress

Compress natural-language instruction/memory files using active model only. Optimize token reduction by structural rewrite first, phrase shortening second. Preserve prompt effectiveness: compressed output must keep same or better instruction-following power.

## Scope

Compress only natural-language files:

- `.md`
- `.txt`
- extensionless prose files

Never compress:

- code/config/data files: `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.env`, `.lock`, `.css`, `.html`, `.xml`, `.sql`, `.sh`
- backup files ending in `.original.md`
- files that look sensitive: secrets, credentials, tokens, private keys, auth dumps

Mixed prose + code is OK: compress prose only; preserve kept code exactly.

## Modes

| Mode         | Target         | Use For                                      | Allowed Changes                                      |
| ------------ | -------------- | -------------------------------------------- | ---------------------------------------------------- |
| `light`      | 5-15% tokens   | specs, commands, risky docs                  | sentence/bullet tightening; preserve structure       |
| `structural` | 20-40% tokens  | default for skills, refs, README, AGENTS     | merge/delete sections, dedupe, convert prose shape   |
| `aggressive` | 40-60%+ tokens | always-loaded docs, repeated examples, notes | rewrite whole sections; keep only ops-critical facts |

Default: `structural`.

If user gives no mode, pick by file type:

- always-loaded instruction files (`AGENTS*`, `CLAUDE*`, memory): `aggressive`
- commands and short workflow docs: `light`
- skills, references, README: `structural`

## Process

1. Resolve target path and confirm file exists.
2. Refuse non-natural-language or sensitive-looking files.
3. Classify file: always-loaded, command, skill, reference, README, notes.
4. Pick mode and token budget.
5. Inspect original for keep-set, delete-set, and move-set.
6. Rely on git for rollback; do not create `.original.md` backups.
7. Compress in-place using structural rules.
8. Validate operational semantics, then Markdown.
9. Report target path, mode, token/word delta, validation, warnings.

Run Markdown lint when available:

```bash
rumdl check <compressed_path>
```

Measure tokens when possible:

```bash
uvx --with tiktoken python <token_count_script>
```

## Keep-Set

Always preserve meaning of:

- requirements, constraints, safety rules, invariants
- workflows, ordering, triggers, mode selection
- task intent, decision criteria, priority order, and refusal/stop conditions
- instruction strength: MUST/NEVER/ALWAYS semantics must not weaken
- commands, paths, URLs, env vars, config keys, APIs
- public names, technical terms, versions, numbers, dates
- examples that are unique or canonical
- code blocks kept in output, byte-for-byte
- inline code/backtick spans kept in output, exactly

## Delete-Set

Prefer deleting before shortening:

- duplicate guidance stated nearby
- repeated examples showing same pattern
- motivational prose, pleasantries, hedging
- generic best-practice filler
- obvious explanation already implied by heading
- restatements of same rule in different words
- long rationale that does not affect behavior

## Move-Set

Prefer moving detail out of always-loaded files when repo has matching structure:

- base/startup docs keep only high-priority policy, routing, and safety rules
- skills keep trigger, policy, process, and reference map; long examples move to refs
- references hold deep examples, edge cases, troubleshooting, and background
- README keeps orientation and install/use flows; detailed operating doctrine moves to commands/skills
- hooks/memory carry session continuity; do not restate recoverable context everywhere

Use progressive disclosure: metadata and triggers stay small; details load only when needed.

## Structural Rules

In `structural` or `aggressive` mode:

- preserve operational behavior, not exact wording
- preserve or improve prompt effectiveness
- optimize context placement, not only local word count
- headings may change, merge, move, or disappear
- prose may become bullets, tables, checklists, or command blocks
- multiple examples may become one canonical example
- repeated rules must collapse to one source of truth
- long sections may become short decision tables
- split or move detail only if repo already has matching reference structure

## Measurement Rules

- measure before/after tokens where possible; otherwise words/bytes
- count always-loaded files separately from on-demand refs
- prefer reducing startup/always-loaded tokens over rarely loaded references
- report if token count rises because content moved into this file or prompt strength improved
- do not guess gains when tokenizer is available

In `light` mode:

- preserve headings and section order
- preserve all examples unless clearly redundant
- tighten wording only

## Compression Prompt

Use this prompt with current model/context, not external CLI:

```text
Compress structurally, not cosmetically.

MODE: [light | structural | aggressive]
TARGET: reduce tokens by [budget]. If unable to hit target without semantic loss, explain blocker.

PRESERVE:
- operational behavior: requirements, constraints, workflows, triggers, invariants
- prompt effectiveness: task intent, decision criteria, priority, force, examples needed for correct behavior
- MUST/NEVER/ALWAYS meaning; do not soften mandatory rules
- commands, paths, URLs, APIs, env vars, config keys, versions, numbers, dates
- proper nouns and technical terms
- unique/canonical examples
- kept fenced code blocks exactly
- kept inline code exactly

MAY CHANGE:
- headings, section order, prose shape
- prose into bullets/tables/checklists
- several examples into one canonical example
- repeated rules into one source of truth
- long rationale into terse rationale
- context placement: move details to existing refs/skills when startup file should stay small

DELETE:
- duplicate guidance
- generic best-practice filler
- motivational prose
- obvious explanations
- repeated examples
- restatements of heading text
- detail that does not change agent behavior

STYLE:
- short operational fragments OK
- use direct imperatives
- prefer deletion/deduplication over word-level edits
- keep scanability better than original
- keep instructions testable: actor, action, trigger, constraint, output all clear
- keep triggers narrow; avoid broad catch-all instructions when specific routing works

Return only compressed file body. No explanation. No outer markdown fence.
```

## Validation Checklist

- [ ] Requirements/constraints still present
- [ ] Workflows/triggers/modes still actionable
- [ ] Prompt remains equally or more effective for target agent/user
- [ ] Mandatory rules keep force; no MUST/NEVER/ALWAYS weakened
- [ ] Decision criteria and priority order preserved
- [ ] Always-loaded content reduced or justified
- [ ] Deep details moved only to discoverable existing refs/skills
- [ ] Commands, paths, URLs, APIs, env vars unchanged unless intentionally deleted
- [ ] Kept code blocks byte-for-byte same
- [ ] Kept inline code byte-for-byte same
- [ ] Unique examples preserved or replaced by equivalent canonical example
- [ ] Duplicate/filler content removed without semantic loss
- [ ] Markdown lint passes
- [ ] No `.original.md` backup created
- [ ] Token target met or blocker reported

## Output

Report:

- compressed target path(s)
- mode used
- token/word delta
- always-loaded token impact when relevant
- validation checks/result
- budget misses and why
- warnings

## Constraints

- No external dependencies beyond normal file tools and optional Markdown/token lint.
- Do not call `claude`, `anthropic`, or remote APIs unless user explicitly asks.
- Do not overwrite existing backup without explicit permission.
- Do not compress secrets or private credential files.
- Do not trade prompt effectiveness for token reduction.
- Preserve exact code/backtick regions that remain in output.
