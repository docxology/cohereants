"""Bind the CohereAnts HTML reader's legacy references to its PDF counters."""

from __future__ import annotations

import re
from pathlib import Path

LABEL = r"(?:eq|fig):[A-Za-z0-9_.:-]+"
NUMBER = r"[0-9]+(?:\.[0-9]+)*"
AUX = re.compile(
    rf"^\\newlabel\{{(?P<label>{LABEL})\}}\{{\{{(?P<number>{NUMBER})\}}"
    r".*\{(?P<kind>equation|figure)\.[^{}]+\}",
    re.MULTILINE,
)
DISPLAY = re.compile(r'<span\s+class="math display">(?P<tex>.*?)</span>', re.DOTALL)
EQ_DECLARATION = re.compile(r"\\label\{(eq:[A-Za-z0-9_.:-]+)\}")
EQ_REFERENCE = re.compile(
    r'<span\s+class="math inline">\s*\\\(\\eqref\{(eq:[A-Za-z0-9_.:-]+)\}\\\)\s*</span>'
)
FIG_REFERENCE = re.compile(r"\\Cref\{(fig:[A-Za-z0-9_.:-]+)\}")
FIG_SOURCE = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.DOTALL)
FIG_LABEL = re.compile(r"\\label\{(fig:[A-Za-z0-9_.:-]+)\}")
FIG_PATH = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}")
FIGURE = re.compile(r"<figure(?P<attrs>[^>]*)>(?P<body>.*?)</figure>", re.DOTALL)
IMAGE_PATH = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"')
CAPTION = re.compile(r"<figcaption\b[^>]*>.*?</figcaption>", re.DOTALL)
PREFIX = "cohereants-reference-"
TARGET = re.compile(
    rf'<span id="{PREFIX}(?:eq|fig)-[A-Za-z0-9_.:-]+" class="cohereants-reference-target">'
    r"[^<>]+</span>"
)
LINK = re.compile(
    rf'<a class="cohereants-reference" href="(?:index\.html)?#{PREFIX}'
    r'(?P<kind>eq|fig)-(?P<name>[A-Za-z0-9_.:-]+)" aria-label="[^"]+">[^<>]+</a>'
)


def equation_labels(document: str) -> list[str]:
    """Return equation labels in HTML display order, including aligned rows."""
    return [
        label
        for display in DISPLAY.finditer(document)
        for label in EQ_DECLARATION.findall(display["tex"])
    ]


def pdf_numbers(aux: str) -> dict[str, str]:
    """Read only equation- and figure-kind auxiliary records."""
    result = {}
    for entry in AUX.finditer(aux):
        label = entry["label"]
        if entry["kind"] != ("equation" if label.startswith("eq:") else "figure"):
            continue
        if label in result:
            raise ValueError(f"Duplicate numbered PDF label: {label}")
        result[label] = entry["number"]
    return result


def figure_files(source: str) -> dict[str, str]:
    """Associate each authored figure label with its unique source image name."""
    result = {}
    for entry in FIG_SOURCE.finditer(source):
        labels, paths = FIG_LABEL.findall(entry[0]), FIG_PATH.findall(entry[0])
        if len(labels) != 1 or len(paths) != 1:
            raise ValueError(
                "Cannot bind a source figure to exactly one label and image."
            )
        name = Path(paths[0]).name
        if name in result or labels[0] in result.values():
            raise ValueError(f"Ambiguous source figure: {name}")
        result[name] = labels[0]
    return result


def _restore_reference(match: re.Match[str]) -> str:
    kind, name = match["kind"], match["name"]
    if kind == "fig":
        return rf"\Cref{{fig:{name}}}"
    return rf'<span class="math inline">\(\eqref{{eq:{name}}}\)</span>'


def link_page(
    document: str,
    numbers: dict[str, str],
    figures: dict[str, str],
    combined_targets: set[str],
) -> tuple[str, set[str]]:
    """Return the linked HTML and its local static target labels."""
    original = document
    document = LINK.sub(_restore_reference, TARGET.sub("", document))
    local = set()
    if f'id="{PREFIX}' in document:
        raise ValueError("Malformed existing cross-reference target.")

    def target(label: str) -> str:
        if label in local or label not in numbers:
            raise ValueError(f"Duplicate or unnumbered HTML target: {label}")
        local.add(label)
        anchor = PREFIX + label.replace(":", "-", 1)
        number = numbers[label]
        text = f"({number})" if label.startswith("eq:") else f"Figure {number}"
        return f'<span id="{anchor}" class="cohereants-reference-target">{text}</span>'

    def display(match: re.Match[str]) -> str:
        # A multiline align block keeps its authored math tree. Its static
        # numbers appear in row order and remain usable with scripting off.
        return match[0] + "".join(
            target(label) for label in EQ_DECLARATION.findall(match["tex"])
        )

    def figure(match: re.Match[str]) -> str:
        image = IMAGE_PATH.search(match["body"])
        label = figures.get(Path(image[1]).name) if image else None
        if label is None:
            return match[0]
        return target(label) + match[0]

    def link(match: re.Match[str]) -> str:
        label = match[1]
        if label not in combined_targets or label not in numbers:
            raise ValueError(f"Missing combined HTML target: {label}")
        name = "Equation" if label.startswith("eq:") else "Figure"
        number = numbers[label]
        prefix = "" if label in local else "index.html"
        href = f"{prefix}#{PREFIX}{label.replace(':', '-', 1)}"
        text = f"({number})" if name == "Equation" else f"Figure {number}"
        return f'<a class="cohereants-reference" href="{href}" aria-label="{name} {number}">{text}</a>'

    linked = FIGURE.sub(figure, DISPLAY.sub(display, document))
    linked = EQ_REFERENCE.sub(link, linked)
    linked = CAPTION.sub(lambda match: FIG_REFERENCE.sub(link, match[0]), linked)
    if EQ_REFERENCE.search(linked) or FIG_REFERENCE.search(linked):
        raise ValueError("Unexpected raw reference context in the generated reader.")
    if original != document and original != linked:
        raise ValueError("Existing links do not match the current PDF and sources.")
    return linked, local
