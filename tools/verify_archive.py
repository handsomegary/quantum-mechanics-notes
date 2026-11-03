"""Check note coverage, portable TeX inputs, and published or rebuilt PDFs."""

from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def verify_pdf(path, part, pages, checksum=None):
    from pypdf import PdfReader
    require(path.is_file(), f"Missing PDF: {path}")
    reader = PdfReader(path)
    require(len(reader.pages) == part["output_pages"], f"Page-count mismatch: {path}")
    require((reader.metadata or {}).get("/Author") == "Anonymous", f"Author metadata: {path}")
    require(not reader.attachments, f"Unexpected PDF attachments: {path}")
    for item in pages:
        page = reader.pages[item["pdf_page"] - 1]
        text = page.extract_text()
        compact = re.sub(r"\s+", "", text.upper())
        require(f"NOTE{item['note_label'].upper()}" in compact, f"Missing note label: {path}: {item['note_label']}")
        require(not page.images, f"Raster scan in PDF: {path}")
        require(not re.search(r"[\u3400-\u9fff]|[A-Za-z]:[\\/]|Users[\\/]", text), f"Unexpected language or local path: {path}")
    if checksum:
        require(hashlib.sha256(path.read_bytes()).hexdigest() == checksum, f"Checksum mismatch: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", action="store_true", help="Check published PDFs using pypdf")
    parser.add_argument("--built", action="store_true", help="Also check .build outputs")
    args = parser.parse_args()
    require(not args.built or args.pdf, "--built requires --pdf")
    coverage = json.loads((ROOT / "source-coverage.json").read_text(encoding="utf-8"))
    pages = coverage["pages"]
    expected = [str(n) for n in range(5, 15)] + ["15a", "15b"] + [str(n) for n in range(16, 85)]
    require([p["note_label"] for p in pages] == expected, "Source-sheet labels are missing, duplicated, or out of order")
    require(len(pages) == coverage["total_source_pages"] == 81, "Expected 81 supplied sheets")
    sources = [(p["source_file"], p["source_page"]) for p in pages]
    require(len(set(sources)) == 81, "Duplicate source physical page")
    require(sum(d["pages"] for d in coverage["source_documents"]) == 81, "Source-document total mismatch")
    for document in coverage["source_documents"]:
        physical = sorted(p["source_page"] for p in pages if p["source_file"] == document["file"])
        require(physical == list(range(1, document["pages"] + 1)), f"Incomplete source-file coverage: {document['file']}")
    for item in pages:
        path = ROOT / item["tex"]
        require(path.is_file(), f"Missing TeX fragment: {path}")
        if item["note_label"] != "5":
            require(f"\\notepage{{{item['note_label']}}}" in path.read_text(encoding="utf-8"), f"Wrong fragment label: {path}")

    for path in [*ROOT.glob("notes/**/*.tex"), *ROOT.glob("tex/*.tex")]:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"[\u3400-\u9fff]|[A-Za-z]:[\\/]|Users[\\/]", text), f"Unexpected language or local path: {path}")
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            dependency = (path.parent / name).resolve()
            if not dependency.suffix:
                dependency = dependency.with_suffix(".tex")
            require(dependency.is_relative_to(ROOT) and dependency.is_file(), f"Missing or external TeX input: {path}: {name}")
        require("\\includegraphics" not in text, f"Unexpected external image dependency: {path}")
    for path in ROOT.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if not target.startswith(("https://", "http://", "#")):
                require((path.parent / target.split("#")[0]).is_file(), f"Broken link: {path}: {target}")

    allowed = {part["pdf"] for part in coverage["parts"]}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.glob("notes/**/*.pdf")}
    require(actual == allowed, "Unexpected or missing published PDF")
    checksums = {}
    for line in (ROOT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        checksums[name] = digest
    require(set(checksums) == allowed, "PDF checksum coverage mismatch")
    if args.pdf:
        for part in coverage["parts"]:
            selected = [p for p in pages if p["part"] == part["id"]]
            require(len(selected) == part["source_pages"], f"Part coverage mismatch: {part['id']}")
            verify_pdf(ROOT / part["pdf"], part, selected, checksums[part["pdf"]])
            if args.built:
                verify_pdf(ROOT / ".build" / part["id"] / Path(part["pdf"]).name, part, selected)
    print("PASS: 81 source sheets, complete TeX inputs and reading links, five published PDF paths" +
          (", PDF contents and checksums" if args.pdf else "") +
          (", and fresh build outputs." if args.built else "."))


if __name__ == "__main__":
    main()
