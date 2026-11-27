"""Link references after rendering both formats and before Template validation."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from web_crossrefs import (
    equation_labels,
    figure_files,
    link_page,
    pdf_numbers,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output", type=Path, help="Fresh Template Stage 03 output directory"
    )
    output = parser.parse_args().output
    web = output / "web"
    combined = web / "index.html"
    try:
        numbers = pdf_numbers(
            (output / "pdf/_combined_manuscript.aux").read_text(encoding="utf-8")
        )
        figures = figure_files(
            (web / "_combined_manuscript.md").read_text(encoding="utf-8")
        )
        files = [combined, *sorted(web.glob("manuscript__*.html"))]
        originals = {path: path.read_text(encoding="utf-8") for path in files}
        equations = equation_labels(originals[combined])
        if equations != [label for label in numbers if label.startswith("eq:")]:
            raise ValueError("Combined HTML and PDF equation labels differ.")
        expected = set(equations) | set(figures.values())
        prepared = {}
        for path, document in originals.items():
            prepared[path], targets = link_page(document, numbers, figures, expected)
            if path == combined and targets != expected:
                raise ValueError(
                    f"Missing combined targets: {sorted(expected - targets)}"
                )
        for path, content in prepared.items():
            if content == originals[path]:
                continue
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=web, delete=False
            ) as stream:
                temporary = Path(stream.name)
                try:
                    stream.write(content)
                    stream.close()
                    temporary.chmod(path.stat().st_mode & 0o777)
                    os.replace(temporary, path)
                finally:
                    temporary.unlink(missing_ok=True)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    main()
