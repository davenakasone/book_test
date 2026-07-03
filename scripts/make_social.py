"""Generate social/platform assets for The Starlight Engine.

Run:  ~/dkn314/bin/python scripts/make_social.py
Outputs to platform/assets/. Templates: swap the TEXT constants per post;
the layouts are the deliverable.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle

OUT = Path(__file__).resolve().parent.parent / "platform" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, GOLD, PARCH, INK, FAINT = "#0d1b2a", "#d9a441", "#f4efe3", "#1a1a1a", "#3a4a63"
DISCLAIMER = "A WORK OF SATIRE. EVERY CLAIM IS FALSE, INCLUDING THIS ONE."


def _canvas(w_px, h_px, dpi=160, bg=NAVY):
    fig = plt.figure(figsize=(w_px / dpi, h_px / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=bg, ec="none", zorder=-10))
    return fig, ax


def _stars(ax, n=70, seed=9):
    rng = np.random.default_rng(seed)
    ax.scatter(
        rng.uniform(0.02, 0.98, n), rng.uniform(0.02, 0.98, n),
        s=rng.uniform(0.3, 2.2, n), color="white", alpha=0.6, zorder=-5,
    )


def _pyramid(ax, cx, cy, w, color=GOLD, lw=2.2):
    apex = (cx, cy + w * 0.62)
    ax.add_patch(Polygon(
        [(cx - w / 2, cy), (cx + w / 2, cy), apex],
        closed=True, fill=False, edgecolor=color, lw=lw, zorder=2,
    ))
    ax.plot([cx + w * 0.18, cx + w * 0.42], [cy + w * 0.40, cy + w * 0.66],
            "--", color=color, lw=lw * 0.6, zorder=2)
    ax.scatter([cx + w * 0.45], [cy + w * 0.70], s=140, marker="*",
               color="white", zorder=3)


def yt_thumbnail():
    """1280x720 — big claim + asterisk gag."""
    fig, ax = _canvas(1280, 720)
    _stars(ax)
    _pyramid(ax, 0.80, 0.16, 0.30)
    ax.text(0.06, 0.72, "RELATIVITY", color=GOLD, fontsize=54,
            family="serif", weight="bold", va="center")
    ax.text(0.06, 0.50, "IS WRONG*", color="white", fontsize=54,
            family="serif", weight="bold", va="center")
    ax.text(0.06, 0.32, "*locally", color=GOLD, fontsize=22,
            family="monospace", va="center", style="italic")
    ax.text(0.06, 0.10, "FORBIDDEN METROLOGY · EP. 04", color="#8a97ad",
            fontsize=13, family="monospace")
    fig.savefig(OUT / "yt-thumb-relativity.png")
    plt.close(fig)


def ig_quote():
    """1080x1080 — parchment quote card."""
    fig, ax = _canvas(1080, 1080, bg=PARCH)
    ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                           ec=GOLD, lw=2.5))
    ax.text(0.5, 0.83, "“", color=GOLD, fontsize=110, ha="center",
            family="serif", va="center")
    ax.text(0.5, 0.56, "Ritual is maintenance\nwith the manual missing.",
            color=INK, fontsize=34, ha="center", va="center",
            family="serif", style="italic", linespacing=1.4)
    ax.text(0.5, 0.30, "— DR. REX MERIDIAN, PhD (pending)", color=INK,
            fontsize=14, ha="center", family="monospace")
    ax.text(0.5, 0.24, "THE STARLIGHT ENGINE", color=GOLD, fontsize=13,
            ha="center", family="serif", weight="bold")
    ax.text(0.5, 0.10, DISCLAIMER, color="#8a8171", fontsize=8.5,
            ha="center", family="monospace")
    fig.savefig(OUT / "ig-quote-ritual.png")
    plt.close(fig)


def ig_checksum():
    """1080x1080 — the digital-root audit as a challenge card."""
    fig, ax = _canvas(1080, 1080)
    _stars(ax, seed=432)
    ax.text(0.5, 0.90, "THE UNIVERSE HAS A CHECKSUM", color=GOLD,
            fontsize=20, ha="center", family="serif", weight="bold")
    rows = [
        ("25,920", "precession", "2+5+9+2+0 → 18", "9"),
        ("86,400", "the day", "8+6+4 → 18", "9"),
        ("21,600", "the circle", "2+1+6", "9"),
        ("144,000", "one baktun", "1+4+4", "9"),
        ("432", "the carrier", "4+3+2", "9"),
    ]
    y = 0.74
    for big, label, work, root in rows:
        ax.text(0.10, y, big, color="white", fontsize=27, family="monospace",
                weight="bold", va="center")
        ax.text(0.38, y, label, color="#8a97ad", fontsize=15,
                family="serif", style="italic", va="center")
        ax.text(0.60, y, work, color="white", fontsize=13.5,
                family="monospace", va="center")
        ax.text(0.92, y, root, color=GOLD, fontsize=30, family="monospace",
                weight="bold", va="center", ha="center")
        y -= 0.115
    ax.plot([0.08, 0.92], [y + 0.055, y + 0.055], color=FAINT, lw=1)
    ax.text(0.5, y - 0.02, "Now do your house number.", color="white",
            fontsize=19, ha="center", family="serif", style="italic")
    ax.text(0.5, 0.06, DISCLAIMER + "  ·  CH. 11", color="#8a97ad",
            fontsize=8.5, ha="center", family="monospace")
    fig.savefig(OUT / "ig-checksum.png")
    plt.close(fig)


def yt_banner():
    """2560x1440 YouTube channel art; safe area ~1546x423 centered."""
    fig, ax = _canvas(2560, 1440)
    _stars(ax, n=140, seed=2026)
    # safe-area content only
    _pyramid(ax, 0.5, 0.42, 0.10, lw=1.8)
    ax.text(0.5, 0.60, "FORBIDDEN METROLOGY", color=GOLD, fontsize=40,
            ha="center", family="serif", weight="bold")
    ax.text(0.5, 0.53, "Measurements they told you not to take.",
            color="white", fontsize=16, ha="center", family="serif",
            style="italic")
    ax.text(0.5, 0.36, "NEW DISPATCHES WEEKLY · (SATIRE)", color="#8a97ad",
            fontsize=12, ha="center", family="monospace")
    fig.savefig(OUT / "yt-banner.png")
    plt.close(fig)


def li_banner():
    """1584x396 LinkedIn profile banner."""
    fig, ax = _canvas(1584, 396)
    _stars(ax, n=60, seed=137)
    _pyramid(ax, 0.88, 0.16, 0.13, lw=1.8)
    ax.text(0.04, 0.62, "INSTITUTE FOR FORBIDDEN METROLOGY", color=GOLD,
            fontsize=27, family="serif", weight="bold", va="center")
    ax.text(0.04, 0.36, "Founded 2025 · Headcount 1 · Morale high · All applicants root to 9",
            color="white", fontsize=13, family="serif", style="italic",
            va="center")
    ax.text(0.04, 0.14, DISCLAIMER, color="#8a97ad", fontsize=9,
            family="monospace", va="center")
    fig.savefig(OUT / "li-banner.png")
    plt.close(fig)


if __name__ == "__main__":
    yt_thumbnail()
    ig_quote()
    ig_checksum()
    yt_banner()
    li_banner()
    print(f"assets written to {OUT}")
