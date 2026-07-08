---
description: Triage a round of reviewer feedback with the author — discuss, decide, route into the loop
---

The author has reviewer feedback in `$ARGUMENTS` (a `feedback/<round>/`
directory). Your job is to run the triage **with** the author — this is a
conversation, not a batch job.

## Steps

1. If `extracted.md` is missing from the round directory, run
   `python scripts/extract_feedback.py $ARGUMENTS` first. Read it, plus any
   raw files the extractor passed over.
2. Group the items: duplicates across reviewers merge (note "2 reviewers"
   — convergent feedback is the highest-signal kind); order by impact
   (structural → scene/paragraph → line → nit).
3. **Walk the list with the author, top down.** For each item give: what
   the reviewer means (interpret charitably), whether you agree and why in
   one or two sentences, and a recommendation: **accept / adapt / reject**.
   Then let the author decide. Batch the nits; discuss the big ones
   individually. Disagreeing with a reviewer is fine — say so and why.
4. Record every decision in `feedback/<round>/triage.md` (this file IS
   committed — it's the editorial record):
   `| # | item | reviewer(s) | decision | why |`
5. Route accepted items into the loop:
   - Insert `<!-- TODO(feedback:<round>): <actionable note> -->` at the
     exact spot in the author's file — `check.py` nags until resolved.
   - If the author says "apply it," edit as a separate commit
     (`feedback(<round>): <what>`), one concern per commit, revertable.
   - The authorship boundary holds: rejected feedback is recorded, not
     silently dropped; applied feedback is visible in git, not blended in.
6. Append to `tool_output/log.jsonl`:
   `{"type": "feedback", "ts": "...", "sha": "...", "round": "<round>", "items": N, "accepted": N}`
7. Close with the state of the round: accepted/adapted/rejected counts,
   what markers now exist, and the ritual — **fix → commit →
   `python check.py`** until the round's markers are gone.
