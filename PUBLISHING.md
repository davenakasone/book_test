# PUBLISHING — where the outputs go and what they must look like

The pipeline's targets, in the order a first-time indie author (David's
friend) would actually use them. Everything below is compatible with what
this repo produces: **6×9" PDF interior + EPUB3 + HTML site**.

> **Figures as of 2026-07. Every fee, royalty %, spec, and free-tier number
> below silently rots — verify each against its source before you act on
> it.** The "verify before upload" checklist at the bottom names each
> external number and where to re-check it. When a number here disagrees
> with the platform's own page, the platform is right and this doc is old.

## The three doors

| Channel | What it takes | Cost | Reach | Notes |
|---|---|---|---|---|
| **Amazon KDP** | RGB PDF (6×9) + EPUB + cover | $0 | Amazon print-on-demand + Kindle | The default first door. Free ISBN offered but Amazon-locked. **Ebook royalty is 35% or 70% — see the royalty box, the #1 number authors get wrong.** Print royalty = 60% of list − print cost at list **≥$9.99**, but only **50% at ≤$9.98**. |
| **IngramSpark** | **PDF/X-1a + CMYK** interior + cover w/ spine | setup **free**, revisions **free** (Feb 2026 sheet), ~1.875% per-unit distribution fee | bookstores, libraries, everyone-not-Amazon | Use *with* KDP. Offers a **free (Ingram-owned) ISBN**, or bring your own. Decide the **wholesale discount (40–55%)** and the **returns** flag — the biggest bookstore-channel choices. **Our pipeline emits RGB, not PDF/X-1a — see the gap note below.** |
| **Draft2Digital** | EPUB | ~10% of list + **$20 one-time activation** | Apple/Kobo/B&N/libraries | Easiest wide-ebook button. Can also generate print-ready files, adequately. |

Sequence for a real book: **KDP + D2D first** (both free, no gatekeeping),
add IngramSpark when bookstore/library distribution matters — *but* see the
KDP Select fork, which you must decide before "KDP + D2D" even makes sense.

### KDP Select: the exclusivity fork (decide this first)

Enrolling an ebook in **KDP Select** locks it to **Amazon-only for 90
auto-renewing days** — no D2D/Apple/Kobo, no direct ebook sales. In
exchange you get **Kindle Unlimited** per-page-read income and the
**free/countdown promo days** the pricing section leans on. You **cannot**
be in Select *and* "wide" (KDP + D2D) at once — the launch plan's "free
launch via Select promo days" silently assumes enrollment.

- **Default for a no-audience debut: start in Select.** KU readers are the
  discovery engine; the promo tools are real; wide distribution earns
  ~nothing without a list to drive it.
- **Go wide at book 2**, or once the email list can push off-Amazon sales.

### IngramSpark PDF/X-1a (wired: `build.py --ingram`)

KDP accepts our stock **RGB** LaTeX PDF. IngramSpark strictly requires
**PDF/X-1a:2001 + CMYK + flattened transparency**. This is now handled:
`python build.py --ingram` (or `python scripts/make_pdfx.py`) runs a
**Ghostscript** pass that converts the RGB PDF to a conforming PDF/X-1a:2001
CMYK interior at `book/_book/The-Starlight-Engine-PDFX.pdf`. Notes:

- Requires Ghostscript (`brew install ghostscript` / `apt install
  ghostscript`); the script finds gs and its CMYK profile automatically.
- gs **outlines the text** (no embedded fonts to break) and **flattens
  transparency** as PDF/X-1a demands — so the file is larger (~30 MB) and
  not text-searchable. That's correct and normal for a print interior; the
  RGB PDF stays the searchable KDP/download copy.
- gs produces a *conforming* file; **IngramSpark's uploader runs the
  authoritative preflight.** Building once to Ingram's stricter spec also
  passes KDP.

### The KDP ebook royalty trap (read before pricing anything)

KDP ebook royalty is **two tiers, not a range**:

- **70%** — *only* if list price is **$2.99–$9.99**, and Amazon subtracts a
  **per-MB delivery fee** from each sale (figure-heavy books cost more to
  deliver). Also not available in every territory.
- **35%** — everywhere else: any price below $2.99 or **above $9.99**, all
  territories, no delivery fee.

The cliff is the point: a **$12.99** ebook earns **35%** (~$4.55), while a
**$9.99** ebook earns **70%** (~$6.99 − delivery) — the cheaper book pays
the author *more*. Price inside the band unless you have a specific reason
not to. (Earlier drafts of this doc said "~60–70%"; that was wrong — 60% is
the *print* rate. The error would have silently halved ebook revenue.)

## Pricing strategy (the number three other docs already reference)

Welcome-email 4 pitches "the price," the launch plan has "buy links live" —
so the price has to exist. Defaults for this book:

- **Ebook: $4.99–$6.99.** Inside the 70% band, humor/impulse-priced, room
  to discount to $0.99/free for launch or promos without touching the 35%
  floor. A first-book unknown author priced at $9.99 is leaving money on
  the table via zero sales, not via royalty rate.
- **Paperback (6×9, ~90pp B&W):** run the page count through **KDP's
  printing-cost calculator** (printing ≈ fixed + per-page; ~90pp B&W is
  cheap). Set list = printing-cost ÷ (1 − 0.60) plus margin, then sanity
  it against comps. Don't price the print edition to lose money to hit a
  round number.
- **Launch pricing:** email 4 wants "a deadline device." A 3-day $0.99
  launch (or free via KDP Select's promo days) is the deadline; regular
  price after. This is not begging — it's a countdown. "Chocolate Daddy
  does not beg" survives intact.
- **Price parity:** keep list price identical across KDP/D2D/Apple/Kobo —
  retailers price-match and Amazon will drop you to $0 (killing your
  royalty) if it finds you cheaper elsewhere.

## Metadata & discoverability (upload-day decisions that drive sales)

Cheapest marketing in the whole kit; all of it is editable post-launch, so
imperfect first picks cost nothing.

- **KDP 7 keyword slots:** reader search phrases, not single words —
  "ancient aliens parody," "science humor gift," "pseudoscience satire."
- **Categories:** pick **Humor & Entertainment › Parody** (and a
  science-humor adjacent), *not* straight Archaeology/Physics. Miscategorizing
  satire as nonfiction invites the exact miscitation the disclaimer exists
  to prevent — and buries a funny book among textbooks it can't outrank.
- **Book description:** written in voice, carrying the satire line, with a
  hook in the first 2 lines (Amazon truncates the rest behind "read more").
- **Series / contributor fields:** "Institute for Forbidden Metrology,
  Vol. 1" primes a backlist even if Vol. 2 never ships.
- **AI-content disclosure (mandatory at KDP upload):** KDP now requires you
  to declare **AI-generated** vs **AI-assisted** content, with different
  rules (AI-*assisted* human work needn't be declared; AI-*generated* must
  be). This book's position, ready for the dry-run: **prose = human-
  authored** (not AI-generated); **figures = programmatically generated**
  (matplotlib/TikZ scripts — document as tool-generated). Policies differ by
  retailer and rot fast — on the verify checklist.

## Spec checklist (what "print-ready" means)

- **Trim:** 6×9 in (this repo's PDF is already at trim size).
- **Margins:** ≥0.75" gutter (inner), ≥0.5" outside; ours: 0.75/0.5.
- **Bleed:** only needed if images run off-page. Ours don't → no bleed,
  which keeps KDP happy at 6×9 exactly.
- **Fonts embedded:** LaTeX/TinyTeX embeds everything by default. KDP's
  checker will confirm.
- **Page count:** KDP paperback minimum 24 pages; spine text needs ≥79.
- **Cover:** *separate file* from the interior. Print cover = single
  wraparound PDF: back + spine + front. **Spine width = pages × 0.002252"
  (white paper) or × 0.0025" (cream)** — use **KDP's cover-size calculator**
  as the source of truth; a wrong multiplier misplaces the spine and fails
  the cover check. `figures/cover.png` here is the *ebook* cover
  (1600×2560); the print wrap is a later Inkscape/Affinity job.
- **EPUB:** must pass `epubcheck` (KDP/D2D run it server-side; local run
  now automated in CI — see NOTES.md). See accessibility box next.
- **ISBN — tie the decision to your channels, not to price:** the moment
  you intend **both KDP and Ingram**, buy **one owned ISBN** (~$125/1,
  ~$295/10 Bowker *(verify)*) so a *single edition* spans both platforms
  under *your* imprint. Free platform ISBNs (KDP's, or Ingram's own) are
  fine **only** if that format lives on that one platform forever — they're
  format-and-platform-locked and stamp "Independently published." Buy the
  block of 10 only if you'll publish multiple formats/titles.

### EPUB accessibility (EAA, in force June 2025)

The European Accessibility Act applies to ebooks sold into the EU from
**28 June 2025**, and the recommended wide path (D2D → Apple/Kobo) ships
straight into the EU. **Wired in this repo:**

- **Alt text on every figure** — `fig-alt="…"` on each `![...](...)` in the
  `.qmd` sources (screen-reader descriptions distinct from the witty
  captions); it lands as `alt` in the EPUB and doubles as SEO for the HTML.
  *When templating a new book, add `fig-alt` to every image — see the
  existing figures for the pattern.*
- **Accessibility metadata** — `book/epub-metadata.xml` (schema.org
  `accessMode`, `accessibilityFeature: alternativeText/tableOfContents/…`,
  `accessibilityHazard: none`, summary), referenced from `_quarto.yml`;
  verified present in the EPUB OPF after render.
- **Still recommended:** validate with **DAISY ACE** alongside `epubcheck`
  (CI runs epubcheck; ACE is a manual check).
- **Microenterprise exemption:** whether the EAA exempts a solo self-
  published author is **unsettled; verify** — but the work above is cheaper
  than the question.

## Money: where it's actually worth spending

The interior pipeline is genuinely $0 — this repo is the proof. Ranked by
value for a real book (ranges are market rough, *verify current rates*):

1. **Human editing** ($500–$3,000) — the thing no tool replaces; biggest
   quality delta per dollar. (Copyedit rates run per-word; see the EFA rate
   chart. A 25k-word humor book copyedits for hundreds, not thousands.)
2. **Cover design** ($100–$800, or DIY with Inkscape/GIMP/Krita free,
   Affinity ~$70 one-time) — covers sell books; interiors don't.
3. **ISBNs** (~$295/10) — only if going wide under an imprint name.
4. **Vellum** ($249, Mac) or **Atticus** ($147, cross-platform) *(verify)* —
   the "just works" typesetters. After this test: they buy *convenience*,
   not capability. Quarto+TinyTeX matched the output classes; Vellum is
   faster for a non-technical author who wants drag-and-drop.
5. ~~Word/InDesign subscriptions~~ — no. InDesign wins only for
   photo-heavy/coffee-table layouts.

## Direct sales (only if a CTA promises a PDF)

Retailers (KDP/D2D) sell Kindle/EPUB — **not** a PDF. If any funnel CTA
offers a reader-facing PDF (welcome-email 4 currently does), that implies
**direct sales**, which means **you** are the seller and owe VAT/sales tax.
Two clean options:

1. **Drop "PDF" from the CTA**, sell only via retailers — simplest, zero
   tax admin.
2. **Sell direct through a merchant-of-record** that collects and remits EU
   VAT and US sales tax **for** you. **Gumroad** is full MoR since Jan 2025:
   **10% + $0.50/transaction** on direct sales (30% via its Discover feed),
   no monthly fee. Payhip / Lemon Squeezy are alternatives *(verify fees)*.
   Never hand-roll a Stripe button for digital goods unless you want to
   become a tax filer in 40 jurisdictions.

## Audiobook (defer, then ACX)

Audio is the fastest-growing format and a natural title-2+ lever — a fake-
authority satire is unusually audio-friendly. Two ACX models: **pay-for-
production** (~$1,500–$2,800 for this length, ~6–7 finished hours) or
**Royalty Share** (no cash upfront, 50/50 with the narrator for 7 years).
**Defer book-1 audio** until sales justify cash, or take Royalty Share to
ship at $0 upfront. A backlist-era lever, not a launch spend.

## Economics, earn-out, tax → BUSINESS.md

What a copy nets, how many copies recover the spend, the <$100/mo debut
median, the backlist thesis, genre comps, and the Schedule-C-vs-hobby tax
question (the OBBBA made hobby expenses permanently nondeductible) all live
in [BUSINESS.md](BUSINESS.md) — the investor-frame companion to this doc.

## Licensing & copyright (the serious section)

> **Not legal advice.** This is an engineer's plain-language map, not
> counsel. Statutes and fees below carry sources; verify current text and
> talk to an IP attorney before anything consequential. US-centric; the
> Berne Convention makes the *ownership* part automatic in ~180 countries.

### Ownership is automatic; *enforcement* is not

- Copyright exists the moment the words are fixed — no filing needed to
  **own** a book. The © line has not been legally required since 1989.
- But in the US you cannot **sue** without registering
  (copyright.gov, ~$45–65 online *(verify fee schedule)*, takes months —
  file early; **17 U.S.C. §411**). And unless you register **within 3
  months of publication** (or before the infringement), you forfeit
  statutory damages (**$750–$150k/work, 17 U.S.C. §504(c)**) and attorney's
  fees (**§412**) — leaving only provable actual damages, which for an
  indie book is approximately nothing. **Register within the 3-month
  window. The single highest-leverage ~$65 in this file.**
- Pen names are fine: you can register under a pseudonym. Term trade-off:
  an anonymous/pseudonymous work runs **95 years from publication OR 120
  years from creation, whichever expires first** — versus life+70 for a
  named author. (Also: book *titles* aren't copyrightable at all; a
  *series* name can sometimes be trademarked.)

### The copyright page (the book's legal front door)

Every trade book carries one; ours is still a TODO. Minimum block:
© year + name (or pen name) · "All rights reserved" + the standard
no-reproduction paragraph · the disclaimer (fiction boilerplate — or for
this book, the satire notice) · ISBN(s) · edition line · imprint name.

### Choosing an outbound license

| Choice | When it's right |
|---|---|
| **All rights reserved** (default) | Almost every commercial book. Doing nothing = this. |
| **Creative Commons** (BY / BY-SA / BY-NC / BY-ND combos) | Platform-building: free spread of the ebook drives print/audio/next-book sales (the Doctorow model). **Irrevocable forever** — decide soberly. NC ≠ "I still control it"; others can't *sell* it, but they can give your ebook away at $0. |
| **Split license** | Books with code/tooling: prose reserved, repo MIT/Apache. Readers reuse the machinery, not the manuscript. |
| CC0 / public domain | Almost never what an author wants. |

For **this repo**: recommendation is the split — `scripts/`, configs, and
LaTeX/HTML templates under MIT; the manuscript (`book/*.qmd`, figures) all
rights reserved. The repo currently has **no LICENSE file, which legally
equals all-rights-reserved** (GitHub's TOS only grants view/fork). One
line from David, then a LICENSE file makes it explicit.

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
  protection (*Campbell v. Acuff-Rose*, 1994); satire that borrows a work
  to mock *something else* gets meaningfully less. A book like this one —
  satirizing a genre's *moves* without reproducing anyone's text — is a
  **lower-risk posture, not a cleared right.** If a specific passage
  quotes or closely parodies an identifiable work, get counsel.

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

## Verify-before-upload checklist (the numbers that rot)

Re-check each against its source the week you publish:

- [ ] **KDP ebook royalty band** + delivery fee — KDP royalty help page
- [ ] **KDP print royalty** (60%) + printing-cost calculator — KDP
- [ ] **KDP spine multiplier** + cover-size calculator — KDP
- [ ] **IngramSpark** setup/revision fees, wholesale discount, ISBN policy
- [ ] **Draft2Digital** distribution cut (~10%?)
- [ ] **Bowker ISBN** pricing ($125/$295?)
- [ ] **Copyright registration** fee — copyright.gov fee schedule
- [ ] **Vellum / Atticus** prices ($249 / $147?)
- [ ] **Merchant-of-record** fees (Gumroad/Payhip/Lemon Squeezy) if selling direct
- [ ] **EAA microenterprise exemption** applicability to a solo author
- [ ] **Email provider free-tier caps** (see PLATFORM.md)
