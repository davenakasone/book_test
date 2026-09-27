"""Plot the datasheet's characteristic curves from measurement CSVs.

    python scripts/make_figures.py        # data/*.csv -> figures/*.svg

`build.py` runs this before every render, so a new measurement lands in the
PDF by replacing its CSV. Each CSV: first column = x, every other column =
one curve, header row = axis label + legend labels. Add a curve by adding
an entry to PLOTS.

Output is SVG with live text (small, diffable, crisp at any zoom); Typst
embeds it directly.
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.ticker  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA, FIGS = ROOT / "data", ROOT / "figures"

PLOTS = [
    # csv (in data/)            svg (in figures/)         y-axis label        log x?
    ("efficiency.csv",          "efficiency.svg",         "Efficiency (%)",   True),
    ("line-regulation.csv",     "line-regulation.svg",    "Output voltage (V)", False),
]

plt.rcParams.update({
    "svg.fonttype": "none",       # keep text as text, not outlined paths
    "svg.hashsalt": "datasheet",  # stable element ids -> clean git diffs
    "font.size": 7,
    "axes.grid": True,
    "grid.linewidth": 0.4,
    "grid.color": "#bbbbbb",
    "lines.linewidth": 1.2,
})


def plot(csv_name, svg_name, ylabel, logx):
    with open(DATA / csv_name, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], [[float(v) for v in r] for r in rows[1:] if r]
    x = [r[0] for r in body]
    fig, ax = plt.subplots(figsize=(3.4, 2.3))
    for i, label in enumerate(header[1:], 1):
        ax.plot(x, [r[i] for r in body], label=label)
    if logx:
        ax.set_xscale("log")
        # plain decimals (0.01, 0.1, 1), not 10^-2 mathtext
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel(header[0])
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGS / svg_name, metadata={"Date": None})
    plt.close(fig)
    print(f"  data/{csv_name} -> figures/{svg_name}")


if __name__ == "__main__":
    FIGS.mkdir(exist_ok=True)
    for spec in PLOTS:
        plot(*spec)
