"""Extract reviewer feedback into structured markdown.

Reviewers return: annotated PDFs (highlights/notes from Preview, Acrobat,
most e-readers), .docx with margin comments, or plain text/email. Drop
whatever each reviewer sent into feedback/<round>-<name>/ and run:

    python scripts/extract_feedback.py feedback/r1-gary/

Output: feedback/r1-gary/extracted.md — every annotation with its page
number and quoted text, every docx comment with its anchor text, every
.txt/.md passed through — one file a session (or the author) can triage.

Extraction only; triage/judgment is the /feedback command's job.
"""

import re
import sys
import zipfile
from pathlib import Path

import fitz  # pymupdf — already a pipeline dependency


def pdf_annotations(pdf: Path):
    out = []
    doc = fitz.open(pdf)
    for pno, page in enumerate(doc, 1):
        for annot in page.annots() or []:
            kind = annot.type[1]
            note = (annot.info.get("content") or "").strip()
            quoted = ""
            try:
                if annot.vertices:  # highlight/underline quads → grab the text
                    quads = [annot.vertices[i:i + 4] for i in range(0, len(annot.vertices), 4)]
                    quoted = " ".join(
                        page.get_textbox(fitz.Quad(q).rect).strip() for q in quads
                    ).strip()
                elif annot.rect:
                    quoted = page.get_textbox(annot.rect).strip()
            except Exception:
                pass
            if note or quoted:
                out.append((pno, kind, quoted[:200], note))
    return out


def docx_comments(docx: Path):
    out = []
    try:
        with zipfile.ZipFile(docx) as z:
            if "word/comments.xml" not in z.namelist():
                return out
            xml = z.read("word/comments.xml").decode(errors="ignore")
            for m in re.finditer(
                r'<w:comment[^>]*w:author="([^"]*)"[^>]*>(.*?)</w:comment>', xml, re.S
            ):
                text = re.sub(r"<[^>]+>", " ", m.group(2))
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    out.append((m.group(1), text))
    except Exception as e:
        out.append(("extractor", f"could not parse {docx.name}: {e}"))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/extract_feedback.py feedback/<round-dir>/")
    rd = Path(sys.argv[1])
    if not rd.is_dir():
        sys.exit(f"not a directory: {rd}")

    lines = [f"# Extracted feedback — {rd.name}", ""]
    n = 0
    for f in sorted(rd.iterdir()):
        if f.suffix.lower() == ".pdf":
            annots = pdf_annotations(f)
            lines.append(f"## {f.name} — {len(annots)} annotation(s)\n")
            for pno, kind, quoted, note in annots:
                n += 1
                lines.append(f"- **p{pno}** [{kind}]"
                             + (f' on "{quoted}"' if quoted else "")
                             + (f" — {note}" if note else ""))
            lines.append("")
        elif f.suffix.lower() == ".docx":
            comments = docx_comments(f)
            lines.append(f"## {f.name} — {len(comments)} comment(s)\n")
            for author, text in comments:
                n += 1
                lines.append(f"- **{author}**: {text}")
            lines.append("")
        elif f.suffix.lower() in (".txt", ".md") and f.name != "extracted.md":
            body = f.read_text().strip()
            n += 1
            lines.append(f"## {f.name} (verbatim)\n\n{body}\n")

    out = rd / "extracted.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"{n} item(s) → {out}")
    print("Next: open Claude Code and run  /feedback " + str(rd))


if __name__ == "__main__":
    main()
