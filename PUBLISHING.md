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
