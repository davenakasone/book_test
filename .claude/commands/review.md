---
description: Prose review of the manuscript — judgment feedback, stored so it can't evaporate
---

You are reviewing the book manuscript in this repo as an editor. The author
invoked `/review $ARGUMENTS` (arguments may name chapters, e.g.
`chapters/ch03-*.qmd`, or be empty = review what changed).

## Scope

1. Read `tool_output/log.jsonl` (if present) and find the last entry with
   `"type": "review"` — that SHA is where the previous prose review ended.
   Run `git diff --stat <that-sha>..HEAD -- book/` to see what changed since.
   No prior review or no log → review the whole of `book/`.
2. If `$ARGUMENTS` names files, review those regardless of diff state.
3. Read the newest `tool_output/report-*.md` first — do NOT repeat anything
   the mechanical checker already flags (unicode, refs, alt-text, spelling).

## What to review (the judgment layer — things a script can't)

- Grammar and usage *in context*; words that are spelled right but wrong.
- Style: sentences that fight the book's voice, tone drift between
  chapters, tics (same opener three paragraphs running, pet words).
- Structure: arguments that don't land, chapters that should split or
  merge, missing transitions, pacing.
- Continuity: facts, names, numbers, or claims that contradict another
  chapter (check the actual other chapter before claiming contradiction).
- Reader experience: where a first-time reader gets lost or bored.

## The authorship boundary (hard rule)

**You scaffold; the author authors.** Never rewrite the author's prose in
place. Every recommendation is delivered as:

1. An inline marker at the exact spot, in the author's file:
   `<!-- TODO(review): <specific, actionable note>. -->`
   — `check.py` keeps these alive as WARNs until the author resolves them.
2. A review record the conversation can't lose:
   `tool_output/review-<YYYYMMDD-HHMMSS>-<shortsha>.md` — findings grouped
   by severity (structural / style / nit), each with file:line and a
   one-line rationale. Suggested rewordings are allowed **in the report**,
   clearly labeled as suggestions.

If the author asks you to apply a fix, apply it as a **separate commit**
(`review: <what>` in the message) so it is revertable in one step.

## Closing the loop

- Append one line to `tool_output/log.jsonl`:
  `{"type": "review", "ts": "<ISO>", "sha": "<short HEAD>", "files": N, "findings": N}`
- End your reply with the ritual: **fix → commit → `python check.py`** —
  the checker nags every unresolved `TODO(review)` marker until it's gone.
- Tell the author the 2–3 highest-impact items in plain words, first.
