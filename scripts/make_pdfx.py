"""Convert the RGB book PDF -> PDF/X-1a:2001 + CMYK for IngramSpark.

KDP accepts the stock RGB LaTeX PDF; IngramSpark strictly requires
PDF/X-1a:2001 (CMYK, embedded output intent, flattened transparency, all
fonts embedded). Ghostscript does the conversion; this script finds gs and
its bundled CMYK ICC profile at runtime (no hardcoded version paths) and
generates the PDF/X definition itself.

    python scripts/make_pdfx.py                     # -> book/_book/The-Starlight-Engine-PDFX.pdf
    python scripts/make_pdfx.py in.pdf out.pdf      # explicit paths

Note: gs produces a *conforming* PDF/X-1a; IngramSpark's uploader runs the
authoritative preflight. Build the interior once to this stricter spec and
it also passes KDP.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = ROOT / "book" / "_book" / "The-Starlight-Engine.pdf"
DEFAULT_OUT = ROOT / "book" / "_book" / "The-Starlight-Engine-PDFX.pdf"


def find_gs():
    for name in ("gs", "gswin64c", "gswin32c"):
        hit = shutil.which(name)
        if hit:
            return hit
    sys.exit("Ghostscript not found. Install it: `brew install ghostscript` "
             "(macOS), `apt install ghostscript` (Linux), or gsview (Windows).")


def find_cmyk_icc(gs_bin):
    """Locate a CMYK ICC profile shipped with Ghostscript, version-agnostically."""
    prefix = Path(gs_bin).resolve().parent.parent  # .../bin/gs -> prefix
    roots = [prefix, Path("/usr"), Path("/usr/local"), Path("/opt/homebrew"),
             Path("/opt/local")]
    for r in roots:
        for icc in r.glob("share/ghostscript/*/iccprofiles/default_cmyk.icc"):
            return icc
        for icc in r.glob("**/iccprofiles/default_cmyk.icc"):
            return icc
    sys.exit("No CMYK ICC profile found near Ghostscript. Point make_pdfx.py "
             "at one, or install a full Ghostscript with iccprofiles/.")


def pdfx_def(icc_path, title):
    # Unconditional PDF/X-1a:2001 header (we control this file, so don't rely
    # on gs's -dPDFX version heuristics). /N 4 = CMYK output intent profile.
    icc = str(icc_path).replace("\\", "/")
    return f"""%!
[ /GTS_PDFXVersion (PDF/X-1a:2001)
  /Title ({title})
  /Trapped /False
/DOCINFO pdfmark

/ICCProfile ({icc}) def

[/_objdef {{icc_PDFX}} /type /stream /OBJ pdfmark
[{{icc_PDFX}} << /N 4 >> /PUT pdfmark
[{{icc_PDFX}} ICCProfile (r) file /PUT pdfmark

[/_objdef {{OutputIntent_PDFX}} /type /dict /OBJ pdfmark
[{{OutputIntent_PDFX}} <<
  /Type /OutputIntent
  /S /GTS_PDFX
  /OutputCondition (Commercial and specialty offset printing)
  /Info (none)
  /OutputConditionIdentifier (CGATS TR001)
  /RegistryName (http://www.color.org)
  /DestOutputProfile {{icc_PDFX}}
>> /PUT pdfmark
[{{Catalog}} << /OutputIntents [ {{OutputIntent_PDFX}} ] >> /PUT pdfmark
"""


def verify(out_pdf):
    """Confirm the output actually declares PDF/X-1a (cheap sniff, not preflight)."""
    blob = out_pdf.read_bytes()
    ok_marker = b"PDF/X-1a:2001" in blob or b"GTS_PDFXVersion" in blob
    ok_intent = b"OutputIntent" in blob
    return ok_marker and ok_intent


def main():
    args = sys.argv[1:]
    src = Path(args[0]) if len(args) >= 1 else DEFAULT_IN
    dst = Path(args[1]) if len(args) >= 2 else DEFAULT_OUT
    if not src.exists():
        sys.exit(f"input PDF not found: {src} — render the book first "
                 "(python build.py).")

    gs = find_gs()
    icc = find_cmyk_icc(gs)

    with tempfile.NamedTemporaryFile("w", suffix=".ps", delete=False) as f:
        f.write(pdfx_def(icc, "The Starlight Engine"))
        defps = f.name

    cmd = [
        gs, "-dPDFX", "-dBATCH", "-dNOPAUSE", "-dNOSAFER", "-dNOOUTERSAVE",
        "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/prepress",
        "-sColorConversionStrategy=CMYK",
        "-sProcessColorModel=DeviceCMYK",
        "-dOverrideICC=true",
        # Downsample images to print-appropriate resolution (keeps figures
        # crisp at 300 dpi, stops gs bloating the file with oversized rasters).
        "-dDownsampleColorImages=true", "-dColorImageResolution=300",
        "-dDownsampleGrayImages=true", "-dGrayImageResolution=300",
        "-dDownsampleMonoImages=true", "-dMonoImageResolution=1200",
        f"-sOutputFile={dst}",
        defps, str(src),
    ]
    print(f"→ gs {gs}\n→ CMYK profile {icc}\n→ converting {src.name} → {dst.name}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    Path(defps).unlink(missing_ok=True)
    if proc.returncode != 0 or not dst.exists():
        print(proc.stdout[-1500:])
        print(proc.stderr[-1500:])
        sys.exit("Ghostscript PDF/X conversion failed (log tail above).")

    if verify(dst):
        kb = dst.stat().st_size // 1024
        print(f"✓ PDF/X-1a:2001 written: {dst} ({kb} KB). "
              "IngramSpark's uploader does the final preflight.")
    else:
        sys.exit(f"gs produced {dst} but it lacks PDF/X markers — inspect it "
                 "before trusting it for Ingram.")


if __name__ == "__main__":
    main()
