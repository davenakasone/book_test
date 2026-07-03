# PUBLISHING — where the outputs go and what they must look like

The pipeline's targets, in the order a first-time indie author (David's
friend) would actually use them. Everything below is compatible with what
this repo produces: **6×9" PDF interior + EPUB3 + HTML site**.

## The three doors

| Channel | What it takes | Cost | Reach | Notes |
|---|---|---|---|---|
| **Amazon KDP** | print PDF (6×9) + EPUB + cover | $0 | Amazon print-on-demand + Kindle | The default first door. Free ISBN offered but it's Amazon-locked; ~60–70% ebook royalty, print royalty after printing cost. |
| **IngramSpark** | print-ready PDF/X + cover w/ spine | ~$0 setup (fee waivers standard) | bookstores, libraries, everyone-not-Amazon | Use *with* KDP: KDP for Amazon, Ingram for the rest. Wants its own ISBN. |
| **Draft2Digital** | EPUB | $0 (rev share) | Apple/Kobo/B&N/libraries | Easiest wide-ebook button. Can also generate print-ready files, adequately. |

Sequence for a real book: **KDP + D2D first** (both free, no gatekeeping),
add IngramSpark when bookstore/library distribution matters.

## Spec checklist (what "print-ready" means)

- **Trim:** 6×9 in (this repo's PDF is already at trim size).
- **Margins:** ≥0.75" gutter (inner), ≥0.5" outside; ours: 0.75/0.5.
- **Bleed:** only needed if images run off-page. Ours don't → no bleed,
  which keeps KDP happy at 6×9 exactly.
- **Fonts embedded:** LaTeX/TinyTeX embeds everything by default. KDP's
  checker will confirm.
- **Page count:** KDP paperback minimum 24 pages; spine text needs ≥79.
- **Cover:** *separate file* from the interior. Print cover = single
  wraparound PDF: back + spine + front. Spine width = pages ×
  0.0025" (white paper). The `figures/cover.png` here is the *ebook*
  cover (1600×2560); a print wrap is a later exercise (Inkscape or
  Affinity).
- **EPUB:** must pass `epubcheck` (KDP/D2D run it server-side; running it
  locally needs Java — deferred here, noted in NOTES.md).
- **ISBN:** Bowker (myidentifiers.com) $125/1, $295/10 — buy 10 if the
  friend means it (each format wants its own). Or take KDP's free one and
  accept the Amazon lock + "Independently published" imprint line.

## Money: where it's actually worth spending

The interior pipeline is genuinely $0 — this repo is the proof. Ranked by
value for a real book:

1. **Human editing** ($500–$3,000) — the thing no tool replaces; biggest
   quality delta per dollar.
2. **Cover design** ($100–$800, or DIY with Inkscape/GIMP/Krita free,
   Affinity ~$70 one-time) — covers sell books; interiors don't.
3. **ISBNs** ($295/10) — only if going wide under an imprint name.
4. **Vellum** ($249, Mac) or Atticus ($147) — the "just works" typesetters.
   After this test: they buy *convenience*, not capability. Quarto+TinyTeX
   matched the output classes; Vellum is faster for a non-technical
   author who wants drag-and-drop.
5. ~~Word/InDesign subscriptions~~ — no. InDesign wins only for
   photo-heavy/coffee-table layouts.

## Licensing & copyright (the serious section)

No jokes here — this is the part that costs real money when done wrong.
US-centric; Berne Convention makes the ownership part automatic in ~180
countries.

### Ownership is automatic; *enforcement* is not

- Copyright exists the moment the words are fixed — no filing needed to
  **own** a book. The © line has not been legally required since 1989.
- But in the US you cannot **sue** without registering
  (copyright.gov, ~$45–65 online, takes months — file early). And unless
  you register **within 3 months of publication** (or before the
  infringement), you forfeit statutory damages ($750–$150k/work) and
  attorney's fees — leaving only provable actual damages, which for an
  indie book is approximately nothing. **Rule: register within the
  3-month window. It is the single highest-leverage $65 in this file.**
- Pen names are fine: you can register under a pseudonym. Trade-off:
  identity-concealed pseudonymous works get 95 years from publication
  instead of life+70. (Also: book *titles* are not copyrightable at all —
  only series names can be trademarked.)

### The copyright page (the book's legal front door)

Every trade book carries one; ours is still a TODO. Minimum block:
© year + name (or pen name) · "All rights reserved" + the standard
no-reproduction paragraph · the disclaimer (fiction boilerplate — or for
this book, the satire notice) · ISBN(s) · edition line · imprint name.

### Choosing an outbound license

| Choice | When it's right |
|---|---|
| **All rights reserved** (default) | Almost every commercial book. Doing nothing = this. |
| **Creative Commons** (pick a flavor: BY / BY-SA / BY-NC / BY-ND combos) | Platform-building: free spread of the ebook drives print/audio/next-book sales (the Doctorow model). **Irrevocable forever** — decide soberly. NC ≠ "I still control it"; it means *others* can't sell it, but they can undercut your ebook at $0. |
| **Split license** | Books with code/tooling: prose reserved, repo MIT/Apache. Readers reuse the machinery, not the manuscript. |
| CC0 / public domain | Almost never what an author wants. |

For **this repo**: recommendation is the split — `scripts/`, configs, and
LaTeX/HTML templates under MIT; the manuscript (`book/*.qmd`, figures) all
rights reserved. Currently the repo has **no LICENSE file, which legally
equals all-rights-reserved** (GitHub's TOS only grants view/fork). David's
one-line decision, then a LICENSE file makes it explicit.

### "Licensing" also means the rights you carve up and sell

Copyright is a bundle: print, ebook, audio, translation, each territory,
film/TV option, serial. Self-publishing keeps the bundle — retailers get
**non-exclusive licenses** via their terms. Two traps:

- **KDP Select** demands 90-day ebook *exclusivity* (kills wide
  distribution via D2D/Kobo/Apple while enrolled). KDP standard does not.
  Read which box you're checking.
- A traditional deal **licenses** rights to a publisher — never "sells the
  copyright." The clauses that matter in year 5: reversion terms and the
  out-of-print threshold (insist it's defined by royalty dollars, not
  "availability," or POD keeps rights captive forever).

### Inbound permissions (what you must license FROM others)

- **Song lyrics: never quote without a license.** Music publishers are the
  most litigious rights-holders in publishing; even one line is routinely
  invoiced at hundreds of dollars. Song *titles* are fine.
- Epigraphs from living authors: short + attributed is customarily
  tolerated, but it's permission territory, not a right.
- Images: only what you made, bought, or verified public-domain/CC.
  (This book generates 100% of its figures — clean by construction.)
- Citing real papers and stating facts (as our bibliography does) is not
  infringement; facts and ideas aren't copyrightable, only expression.
- **Fair use is a defense, not a permission** — you find out if it worked
  in court. Parody (targeting the borrowed work itself) has strong
  protection (*Campbell v. Acuff-Rose*); satire that borrows a work to
  mock *something else* gets meaningfully less. A book like this one —
  satirizing a genre's *moves* without reproducing anyone's text — sits
  on the safe side of that line.

## Format gotchas learned here

- EPUB is *reflowable*: wide tables and TikZ-as-PDF don't fly — every
  figure needs a raster (PNG) fallback. This repo generates both.
- The index (`\index{}`) is a **print-only** artifact; EPUB/HTML rely on
  search instead. Don't fight it.
- **The platform around the book** — email list, website, YouTube, IG,
  LinkedIn — lives in `platform/` (strategy, per-channel playbooks with
  written content, 8-week launch calendar, generated assets). Read
  `platform/PLATFORM.md` first: list-first, one video channel, one feed.
- Keep chapter sources in Markdown (qmd): the same files make the print
  PDF, the ebook, and a marketing website. One source, three products —
  that's the whole reason for this pipeline.
