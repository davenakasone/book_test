"""Generate all matplotlib figures for The Starlight Engine.

Run with the shared venv:  ~/dkn314/bin/python scripts/make_figures.py
Outputs PNG (for EPUB/HTML) + PDF (vector, for LaTeX) into book/figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

FIGDIR = Path(__file__).resolve().parent.parent / "book" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    }
)

# name: (lat, lon, grid function)
SITES = {
    "Giza": (29.979, 31.134, "generator"),
    "Puma Punku": (-16.562, -68.680, "parts depot"),
    "Stonehenge": (51.179, -1.826, "controller"),
    "Nazca": (-14.739, -75.130, "test range"),
    "Antikythera": (35.862, 23.307, "terminal"),
    "Göbekli Tepe": (37.223, 38.923, "sentinel"),
    "Chichén Itzá": (20.684, -88.568, "scheduler"),
    "Great Wall": (40.354, 116.000, "antenna"),
    "Easter Island": (-27.113, -109.350, "repeater"),
}

ARCS = [  # "primary transmission trunks"
    ("Giza", "Stonehenge"),
    ("Giza", "Göbekli Tepe"),
    ("Giza", "Great Wall"),
    ("Stonehenge", "Puma Punku"),
    ("Stonehenge", "Nazca"),
    ("Nazca", "Chichén Itzá"),
    ("Nazca", "Easter Island"),
    ("Göbekli Tepe", "Antikythera"),
]


def _to_xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def great_circle(p1, p2, n=100):
    """Slerp between two (lat, lon) points; returns lat/lon arrays."""
    a, b = _to_xyz(*p1), _to_xyz(*p2)
    omega = np.arccos(np.clip(a @ b, -1, 1))
    t = np.linspace(0, 1, n)
    pts = (
        np.sin((1 - t)[:, None] * omega) * a + np.sin(t[:, None] * omega) * b
    ) / np.sin(omega)
    lat = np.degrees(np.arcsin(pts[:, 2]))
    lon = np.degrees(np.arctan2(pts[:, 1], pts[:, 0]))
    return lat, lon


def split_dateline(lat, lon):
    """Split a path where it crosses the ±180° meridian so no line streaks across."""
    jumps = np.where(np.abs(np.diff(lon)) > 180)[0]
    segs, start = [], 0
    for j in jumps:
        segs.append((lat[start : j + 1], lon[start : j + 1]))
        start = j + 1
    segs.append((lat[start:], lon[start:]))
    return segs


def fig_world():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.set_facecolor("#f4efe3")  # aged-chart parchment
    for lo in range(-180, 181, 30):
        ax.axvline(lo, color="#c9bfa5", lw=0.4, zorder=1)
    for la in range(-90, 91, 30):
        ax.axhline(la, color="#c9bfa5", lw=0.4, zorder=1)
    ax.axhline(0, color="#b0a487", lw=0.8, zorder=1)

    for s1, s2 in ARCS:
        lat, lon = great_circle(SITES[s1][:2], SITES[s2][:2])
        for sl, so in split_dateline(lat, lon):
            ax.plot(so, sl, color="#8c2f2f", lw=1.1, zorder=2)

    # hand-placed label offsets: (dx pts, dy pts, ha) — the clusters overlap otherwise
    label_pos = {
        "Giza": (10, -16, "left"),
        "Puma Punku": (8, -14, "left"),
        "Stonehenge": (8, 6, "left"),
        "Nazca": (-9, 4, "right"),
        "Antikythera": (-9, 6, "right"),
        "Göbekli Tepe": (6, 12, "left"),
        "Chichén Itzá": (-9, 6, "right"),
        "Great Wall": (-4, -22, "right"),
        "Easter Island": (10, -6, "left"),
    }
    for name, (la, lo, fn) in SITES.items():
        ax.scatter(lo, la, s=42, marker="^", color="#1a1a1a", zorder=3)
        dx, dy, ha = label_pos[name]
        ax.annotate(
            f"{name}\n[{fn}]",
            (lo, la),
            textcoords="offset points",
            xytext=(dx, dy),
            ha=ha,
            fontsize=6.5,
            style="italic",
            zorder=4,
        )

    ax.set_xlim(-180, 180)
    ax.set_ylim(-65, 75)
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("IFM GLOBAL SURVEY — PRIMARY TRANSMISSION ARCS (SHEET 1 OF 1)")
    ax.text(
        178,
        -62,
        "projection: plate carrée — the grid does not respect Mercator, and neither should you",
        ha="right",
        fontsize=5.5,
        style="italic",
        color="#6b6353",
    )
    for ext in ("png", "pdf"):
        fig.savefig(FIGDIR / f"world-alignments.{ext}")
    plt.close(fig)


def fig_grid():
    rng = np.random.default_rng(432)  # of course
    lons = np.array([SITES[k][1] for k in SITES])
    names = list(SITES)
    true = 7.83 + 3.2 * np.sin(np.radians(lons) * 2 + 0.9)
    meas = true + rng.normal(0, 0.08, len(lons))  # "consensus trimming" was applied

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    xs = np.linspace(-180, 180, 500)
    ax.plot(
        xs,
        7.83 + 3.2 * np.sin(np.radians(xs) * 2 + 0.9),
        "--",
        color="#8c2f2f",
        lw=1.2,
        label="IFM grid model (fit)",
    )
    ax.errorbar(
        lons,
        meas,
        yerr=0.35,
        fmt="^",
        color="#1a1a1a",
        ms=6,
        capsize=3,
        lw=1,
        label="measured output",
    )
    for n, x, y in zip(names, lons, meas):
        ax.annotate(n, (x, y), textcoords="offset points", xytext=(4, 6), fontsize=6)
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel(r"Telluric output (kW·baktun$^{-1}$)")
    ax.set_title("Global Telluric Output Survey, 2025–26")
    ax.legend(fontsize=7, loc="lower left")
    ax.text(
        0.98,
        0.06,
        r"$R^2 = 0.9971$ (after consensus trimming)",
        transform=ax.transAxes,
        ha="right",
        fontsize=8,
        bbox=dict(boxstyle="round", fc="#f4efe3", ec="#8c2f2f"),
    )
    for ext in ("png", "pdf"):
        fig.savefig(FIGDIR / f"the-grid.{ext}")
    plt.close(fig)


def fig_constants():
    # Monument "measurements" vs fundamental constants, all miraculously on y = x.
    pts = [
        ("φ  (hallway ÷ kitchen)", 1.618),
        ("Schumann (refrigerator, Hz)", 7.83),
        ("α⁻¹  (fox snout, °×8.06)", 137.036),
        ("432  (bluestone, Hz)", 432.0),
        ("c  (Giza latitude ×10⁷)", 2.99792458e8),
    ]
    labels, vals = zip(*pts)
    vals = np.array(vals)

    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    xs = np.array([1e-1, 1e10])
    ax.plot(xs, xs, "--", color="#8c2f2f", lw=1.2, label="y = x  (the Universe agreeing)")
    ax.scatter(vals, vals, s=48, marker="^", color="#1a1a1a", zorder=3)
    offsets = [(8, -3), (8, -3), (8, -3), (8, -3), (-6, 6)]
    ha = ["left", "left", "left", "left", "right"]
    for (lbl, v), off, h in zip(pts, offsets, ha):
        ax.annotate(
            lbl, (v, v), textcoords="offset points", xytext=off, fontsize=7, ha=h
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-1, 1e10)
    ax.set_ylim(1e-1, 1e10)
    ax.set_xlabel("Value extracted from monument")
    ax.set_ylabel("Fundamental constant (SI)")
    ax.set_title("Monuments vs. Constants")
    ax.legend(fontsize=7, loc="upper left")
    ax.text(
        0.97,
        0.05,
        r"$R^2 = 1.000$ (after rounding)",
        transform=ax.transAxes,
        ha="right",
        fontsize=8,
        bbox=dict(boxstyle="round", fc="#f4efe3", ec="#8c2f2f"),
    )
    for ext in ("png", "pdf"):
        fig.savefig(FIGDIR / f"constants.{ext}")
    plt.close(fig)


def fig_topology():
    # Single-line diagram of the grid: manual layout, no graph libs needed.
    nodes = {
        "GIZA\n(generator)": (0.0, 0.0),
        "STONEHENGE\n(controller)": (-2.4, 1.5),
        "GÖBEKLI TEPE\n(sentinel)": (2.4, 1.5),
        "GREAT WALL\n(antenna)": (2.9, -0.9),
        "PUMA PUNKU\n(parts)": (-4.4, 0.2),
        "NAZCA\n(test range)": (-3.4, -1.6),
        "LONG COUNT\n(scheduler)": (-1.2, -2.4),
        "ANTIKYTHERA\n(terminal)": (1.4, -2.4),
    }
    edges = [
        ("GIZA\n(generator)", "STONEHENGE\n(controller)", "trunk A"),
        ("GIZA\n(generator)", "GÖBEKLI TEPE\n(sentinel)", "trunk B"),
        ("GIZA\n(generator)", "GREAT WALL\n(antenna)", "downlink feed"),
        ("STONEHENGE\n(controller)", "PUMA PUNKU\n(parts)", "spares req."),
        ("STONEHENGE\n(controller)", "NAZCA\n(test range)", "cal loop"),
        ("NAZCA\n(test range)", "LONG COUNT\n(scheduler)", ""),
        ("GREAT WALL\n(antenna)", "ANTIKYTHERA\n(terminal)", "last mile"),
        ("GÖBEKLI TEPE\n(sentinel)", "LONG COUNT\n(scheduler)", "burst sched."),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    for a, b, lbl in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        style = "--" if lbl == "last mile" else "-"
        ax.plot([x1, x2], [y1, y2], style, color="#8c2f2f", lw=1.2, zorder=1)
        if lbl:
            ax.annotate(
                lbl,
                ((x1 + x2) / 2, (y1 + y2) / 2),
                fontsize=6,
                style="italic",
                color="#6b3030",
                ha="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
                zorder=2,
            )
    for name, (x, y) in nodes.items():
        weight = "bold" if "GIZA" in name else "normal"
        ax.annotate(
            name,
            (x, y),
            fontsize=7.5,
            ha="center",
            va="center",
            weight=weight,
            bbox=dict(boxstyle="round,pad=0.45", fc="#f4efe3", ec="#1a1a1a", lw=1.1),
            zorder=3,
        )
    ax.set_xlim(-5.6, 4.2)
    ax.set_ylim(-3.2, 2.4)
    ax.axis("off")
    ax.set_title("THE GRID — SINGLE-LINE DIAGRAM (IFM DWG 0001 REV J)")
    for ext in ("png", "pdf"):
        fig.savefig(FIGDIR / f"grid-topology.{ext}")
    plt.close(fig)


def fig_cover():
    # EPUB cover, KDP-friendly 1600×2560.
    fig = plt.figure(figsize=(6.25, 10), dpi=256)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.6)
    ax.axis("off")  # hides the axes patch too — paint the background by hand

    gold, faint = "#d9a441", "#3a4a63"
    ax.add_patch(
        plt.Rectangle((0, 0), 1, 1.6, fc="#0d1b2a", ec="none", zorder=-10)
    )
    # starfield
    rng = np.random.default_rng(2026)
    ax.scatter(
        rng.uniform(0.03, 0.97, 90),
        rng.uniform(0.05, 1.55, 90),
        s=rng.uniform(0.3, 2.5, 90),
        color="white",
        alpha=0.7,
    )
    # graticule ghost
    for y in np.linspace(0.1, 1.5, 8):
        ax.plot([0, 1], [y, y], color=faint, lw=0.3, alpha=0.4, zorder=-5)
    # Sirius + beam + pyramid
    star = (0.75, 1.00)
    apex = (0.5, 0.74)
    ax.scatter(*star, s=350, marker="*", color="white", zorder=5)
    ax.annotate(
        "SIRIUS (PUMP)", star, textcoords="offset points", xytext=(0, 13),
        color=gold, fontsize=7, ha="center", family="monospace",
    )
    ax.plot(
        [star[0], apex[0]], [star[1], apex[1]], "--", color=gold, lw=1.4, zorder=4
    )
    ax.add_patch(
        Polygon(
            [(0.18, 0.40), (0.82, 0.40), apex],
            closed=True, fill=False, edgecolor=gold, lw=2.4, zorder=5,
        )
    )
    ax.plot([0.06, 0.94], [0.40, 0.40], color=gold, lw=1.0)
    # title block
    ax.text(0.5, 1.47, "THE", color="white", fontsize=20, ha="center", family="serif")
    ax.text(
        0.5, 1.42, "STARLIGHT\nENGINE", color=gold, fontsize=31, ha="center",
        va="top", family="serif", weight="bold", linespacing=1.05,
    )
    ax.text(
        0.5, 1.13, "HOW THE ANCIENTS WIRED THE EARTH",
        color="white", fontsize=10.5, ha="center", family="serif",
    )
    ax.text(
        0.5, 0.305, "DR. CHOCOLATE DADDY",
        color="white", fontsize=13, ha="center", family="serif",
    )
    ax.text(
        0.5, 0.262, "PhD (pending) · MD · DDS · PPM · PSI · MBA · Esq. · HVAC · AM/FM",
        color="#8a97ad", fontsize=6.2, ha="center", family="monospace",
    )
    ax.text(
        0.5, 0.215, "Institute for Forbidden Metrology · Vol. 1",
        color=gold, fontsize=8, ha="center", family="serif", style="italic",
    )
    ax.text(
        0.5, 0.07, "A WORK OF SATIRE. EVERY CLAIM IS FALSE, INCLUDING THIS ONE.",
        color="#8a97ad", fontsize=6.5, ha="center", family="monospace",
    )
    fig.savefig(FIGDIR / "cover.png", dpi=256)
    plt.close(fig)


if __name__ == "__main__":
    fig_world()
    fig_grid()
    fig_constants()
    fig_topology()
    fig_cover()
    print(f"figures written to {FIGDIR}")
