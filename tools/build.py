"""Build the native TeX notes from any checkout or extracted repository ZIP."""

from pathlib import Path
import argparse
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "005": ("notes/005-matrix-elements", "note"),
    "006-020": ("notes/006-020-foundations", "main"),
    "021-041": ("notes/021-041-dynamics", "main"),
    "042-063": ("notes/042-063-angular-momentum", "main"),
    "064-084": ("notes/064-084-approximation-and-scattering", "main"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default="pdflatex", help="pdfLaTeX command or full path")
    parser.add_argument("--target", choices=["all", "remaining", *TARGETS], default="all")
    parser.add_argument("--publish", action="store_true", help="Copy built PDFs beside their TeX entry points")
    args = parser.parse_args()
    engine = shutil.which(args.engine)
    if engine is None:
        parser.error(f"LaTeX engine not found: {args.engine}")
    selected = TARGETS if args.target == "all" else (
        {k: v for k, v in TARGETS.items() if k != "005"}
        if args.target == "remaining" else {args.target: TARGETS[args.target]}
    )
    for key, (directory, stem) in selected.items():
        source = ROOT / directory
        output = ROOT / ".build" / key
        output.mkdir(parents=True, exist_ok=True)
        command = [engine, "-halt-on-error", "-interaction=nonstopmode",
                   "-file-line-error", "-no-shell-escape", "-recorder",
                   f"-output-directory={output}", f"{stem}.tex"]
        if "miktex" in engine.lower():
            command.insert(1, "--disable-installer")
        for run in (1, 2):
            result = subprocess.run(command, cwd=source, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, errors="replace")
            (output / f"console-{run}.txt").write_text(result.stdout, encoding="utf-8")
            if result.returncode:
                print(result.stdout)
                raise SystemExit(result.returncode)
        pdf = output / f"{stem}.pdf"
        if not pdf.is_file():
            raise SystemExit(f"Expected PDF missing: {pdf}")
        if args.publish:
            shutil.copyfile(pdf, source / pdf.name)
        print(f"Built {key}: {pdf.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
