# PLATFORM — the machine around the book

The book is the product; the platform is the distribution. This doc is the
strategy layer; per-channel playbooks live next to it. Everything here is
demonstrated with Chocolate Daddy content so the friend can see each piece
*populated*, not just described.

## The blunt ROI ranking (solo author, finite hours)

1. **Email list** — the only channel you *own*. Every platform below exists
   to feed it. Start it 6–12 months before launch, not at launch.
2. **Website** — already free: the Quarto HTML render *is* the site. Add a
   domain and a signup form and stop.
3. **One video/audio channel** — YouTube *if and only if* the author will
   actually talk to a camera weekly. A dead channel is worse than none.
4. **One social feed** — pick IG *or* LinkedIn by where the readers are
   (visual/lifestyle → IG; nonfiction/professional → LinkedIn). Running
   both solo means doing both badly.

Consistency beats coverage. Two channels done weekly outperform five done
monthly. The failure mode is launching everything in week 1 and abandoning
everything by week 6 — structure the calendar (see `launch-plan.md`), not
the willpower.

## Stack (open source / free tier first)

| Piece | Free/OSS pick | Paid worth it? |
|---|---|---|
| Email list | Buttondown or Kit (free tiers; check current caps) | Yes at scale — email is the one bill worth paying |
| Signup form | provider embed pasted into the Quarto site (demo: `book/html/newsletter.html`) | no |
| Website | Quarto HTML → GitHub Pages / Netlify (free) | **Domain ~$12/yr — the one near-mandatory spend** |
| Video edit | DaVinci Resolve (free), OBS for capture | no, Resolve free tier is absurd |
| Graphics | matplotlib templates (`scripts/make_social.py`), Inkscape, GIMP | Canva Pro only if templates save real hours |
| Scheduling | native platform schedulers | Buffer et al. — skip until volume forces it |
| Analytics | provider opens/clicks + GoatCounter (free) | no |

## Rules of the machine

- **Every channel's call-to-action is the email list.** Not "buy the book"
  — the list. The list sells the book, the backlist, and the next book.
- **One content atom, many cuts (the content-atom rule).** Each chapter
  yields: 1 newsletter, 1 long video outline, 3 shorts, 3 IG posts, 2
  LinkedIn posts. Write once, slice five ways (worked example across the
  playbooks: ch13 dark ledger).

  | Chapter atom | → | Newsletter | Long video | Shorts | IG | LinkedIn |
  |---|---|---|---|---|---|---|
  | ch01 Giza | → | dispatch #1 | Long #3 | Short #1 | reactor carousel | post 1 |
  | ch11 vortex | → | dispatch #2 | — | Short #2 | checksum carousel | post 2 |
  | ch13 dark ledger | → | dispatch #4 | Long #7 | Short #4 | "5 true things" | post 4 |

- **The satire disclaimer travels.** Every bio, banner, and About block
  carries the "work of satire" line. Non-negotiable — it's also the brand.
- **Deployment:** the repo has a live GitHub remote
  (`github.com/davenakasone/book_test`) and pushes are authorized. The
  website step — `quarto publish gh-pages` or Netlify — is **documented but
  not yet executed**; running it is the friend's one-command go-live.

## What this kit contains

- `email/welcome-sequence.md` — 5-email onboarding, in voice
- `social/youtube.md` — channel concept + 8 videos, 2 shorts fully scripted
- `social/instagram.md` — 12 posts with captions
- `social/linkedin.md` — 8 posts, 3 written out (the Doctor does LinkedIn-brain)
- `launch-plan.md` — 8-week calendar, all channels interlocked
- `../scripts/make_social.py` — thumbnail/card/banner templates → `assets/`
- `../book/html/newsletter.html` — signup CTA embedded in the web edition
