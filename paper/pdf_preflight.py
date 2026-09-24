#!/usr/bin/env python3
"""Check the generated manuscript PDF for structural and text-extraction problems.

Usage: python3 paper/pdf_preflight.py /path/to/QEC1435_NO_BINARY_14_3_5.pdf

Uses optional Poppler commands pdfinfo, pdffonts, pdftotext when installed.
Without them the test cannot certify PDF font embedding / extracted paper text.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str | None:
    if shutil.which(cmd[0]) is None:
        print(f"CHECK UNAVAILABLE: install {cmd[0]} (Poppler) to inspect PDF")
        return None
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode:
        print(f"ERROR: {' '.join(cmd[:1])}: {p.stderr.strip()[:240]}")
        return ""
    return p.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 paper/pdf_preflight.py PATH_TO_FINAL_PDF")
        return 2
    p = Path(sys.argv[1])
    errors: list[str] = []
    warnings: list[str] = []
    if not p.exists() or not p.is_file():
        print(f"ERROR: PDF not found: {p}")
        return 1
    data = p.read_bytes()
    if not data.startswith(b"%PDF-"):
        errors.append("Not a PDF file (missing PDF header)")
    if b"%%EOF" not in data[-4096:]:
        warnings.append("PDF EOF marker not detected at file end")
    if re.search(rb"/(?:JavaScript|JS)\b", data):
        errors.append("Possible embedded JavaScript; remove it from the PDF")
    if b"/Encrypt" in data:
        errors.append("Possible PDF encryption; inspect the PDF")
    print(f"PDF: {p.name}; bytes: {len(data):,}")

    info = run(["pdfinfo", str(p)])
    if info is not None:
        for line in info.splitlines():
            if line.startswith(("Title:", "Author:", "Pages:", "Page size:", "PDF version:", "Encrypted:")):
                print(line)
        if re.search(r"^Encrypted:\s+yes", info, re.M):
            errors.append("PDF is encrypted")
        if not re.search(r"^Title:\s+No binary \[\[14,3,d≥5\]\] quantum stabilizer code exists\s*$", info, re.M):
            errors.append("PDF metadata title is missing or stale")
        if not re.search(r"^Author:\s+Brandon Li\s*$", info, re.M):
            errors.append("PDF metadata author is missing or stale")
        pages = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
        if pages is None:
            errors.append("PDF page count is unavailable")
        elif not 1 <= int(pages.group(1)) <= 40:
            errors.append(f"Unexpected PDF page count: {pages.group(1)}")

    fonts = run(["pdffonts", str(p)])
    if fonts is not None:
        print("FONT AUDIT")
        for line in fonts.splitlines()[2:]:
            if not line.strip():
                continue
            print(line)
            if re.search(r"\bType\s*3\b", line, re.I):
                errors.append("Type 3/bitmap font present")
            # Poppler last columns: emb sub uni object ID
            m = re.search(r"\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
            if m and m.group(1) == "no":
                warnings.append("Non-embedded font: " + line.split()[0])
        if not fonts.splitlines()[2:]:
            warnings.append("Could not inspect any embedded fonts")

    txt = run(["pdftotext", "-layout", str(p), "-"])
    if txt is not None:
        expected = {
            "author name": "Brandon Li",
            "abstract": "Abstract",
            "one-proof conclusion": "Conclusion",
            "references": "References",
            "AI disclosure": "AI-assisted tools",
            "complete additive census": "37",
            "Hall obstruction": "Hall",
        }
        for label, needle in expected.items():
            if needle.casefold() not in txt.casefold():
                errors.append(f"Missing extractable {label}: {needle!r} (PDF may be stale)")
        if any(x in txt for x in (
            "The specific tools and extent of use should be confirmed",
            "historical monomial-automorphism manuscript is retained",
            "The proof is TBD",
            "frozen repository snapshot",
            "A green certificate",
        )):
            errors.append("Internal source note / placeholder found in PDF")
        if re.search(r"\brhs\s+⟨\s*0\b", txt):
            errors.append("Strict inequality was rendered as a left angle bracket; fix math renderer")
        print(f"Extractable text chars: {len(txt):,}")

    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(" -", w)
    if errors:
        print("FAIL:")
        for e in errors:
            print(" -", e)
        return 1
    if info is None or fonts is None or txt is None:
        print("INCOMPLETE PREFLIGHT: install Poppler utilities and rerun")
        return 2
    print("PASS: mechanical PDF checks. Human page-by-page inspection and specialist proof review remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
