"""Build-time fixes that would otherwise cost a pinned plugin dependency.

MkDocs derives a sidebar *section* label from the folder name on disk, so
`01_Chemistry_of_Life/` would read as "01 Chemistry Of Life" and `ph/` as "Ph".
The numeric prefix sets reading order in a file listing; it should not be
visible in the nav, and biology's acronyms (pH, DNA, mRNA, ATP…) have a fixed
casing no naive title-caser gets right.

Two jobs:

1. **Clean section labels** — unit folders get their full course names, keyword
   folders get title-cased names with acronym fixups.
2. **Order the root nav** — ``NAV_ORDER`` pins the reading order of the
   top-level entries; anything unlisted keeps its alphabetical slot after them.
"""

from __future__ import annotations

import posixpath
import re

# Unit folders → the label the course itself uses.
SECTION_LABELS = {
    "01_Chemistry_of_Life": "Unit 1 · The Chemistry of Life",
    "02_Cells_as_Living_Systems": "Unit 2 · Cells as Living Systems",
    "03_Cellular_Processes": "Unit 3 · Cellular Processes",
    "04_DNA_and_Cell_Division": "Unit 4 · DNA and Cell Division",
    "05_Genetics_and_Biotechnology": "Unit 5 · Genetics and Biotechnology",
    "06_Evolution_and_Diversity_of_Life": "Unit 6 · Evolution and Diversity of Life",
    "07_Ecological_Principles": "Unit 7 · Ecological Principles",
}

# Whole-folder-name overrides for keyword slugs the word-level pass can't fix.
NAME_OVERRIDES = {
    "ph": "pH",
    "atp": "ATP",
    "dna": "DNA",
    "mrna": "mRNA",
    "rrna": "rRNA",
    "trna": "tRNA",
    "crispr": "CRISPR",
    "dna_replication": "DNA Replication",
    "dna_fingerprint": "DNA Fingerprint",
    "recombinant_dna": "Recombinant DNA",
    "down_syndrome": "Down Syndrome (Trisomy 21)",
    "genetically_modified_organism": "Genetically Modified Organism (GMO)",
    "chlorofluorocarbons": "Chlorofluorocarbons (CFCs)",
    "huntingtons_disease": "Huntington's Disease",
    "sex_linked_traits": "Sex-Linked Traits",
}

# Word-level casing fixes applied after a naive title-case.
FIXUPS = {
    "And": "and",
    "Of": "of",
    "Vs": "vs",
    "In": "in",
    "The": "the",
    "Non": "Non-",
}

# Reading order of the root nav, by on-disk name. Unlisted entries sort
# alphabetically after these.
NAV_ORDER = [
    "index.md",
    "GLOSSARY.md",
    "STANDARDS.md",
    "NC_STANDARDS.md",
    "01_Chemistry_of_Life",
    "02_Cells_as_Living_Systems",
    "03_Cellular_Processes",
    "04_DNA_and_Cell_Division",
    "05_Genetics_and_Biotechnology",
    "06_Evolution_and_Diversity_of_Life",
    "07_Ecological_Principles",
]


def _pretty(name: str) -> str:
    if name in SECTION_LABELS:
        return SECTION_LABELS[name]
    if name in NAME_OVERRIDES:
        return NAME_OVERRIDES[name]
    name = re.sub(r"^\d+_", "", name)
    words = [w.capitalize() for w in name.split("_")]
    words = [FIXUPS.get(w, w) for w in words]
    label = " ".join(words)
    return label.replace("- ", "-")


def _dir_of(item) -> str:
    """TOP-LEVEL on-disk name of a nav item — used only for root nav ordering."""
    if hasattr(item, "file") and item.file is not None:
        return item.file.src_path.split("/")[0]
    for child in getattr(item, "children", None) or []:
        got = _dir_of(child)
        if got:
            return got
    return ""


def _first_src(item) -> str:
    """src_path of the first descendant page of a nav item."""
    if hasattr(item, "file") and item.file is not None:
        return item.file.src_path
    for child in getattr(item, "children", None) or []:
        got = _first_src(child)
        if got:
            return got
    return ""


def _relabel(items, depth: int = 0) -> None:
    # A section's own folder is the DEPTH-th segment of any descendant page's
    # path — labeling from segment 0 at every level is how all 37 term entries
    # inside a unit once read as the unit's name.
    for item in items:
        if getattr(item, "is_section", False):
            parts = _first_src(item).split("/")
            if depth < len(parts) - 1:
                item.title = _pretty(parts[depth])
            _relabel(item.children, depth + 1)


def on_nav(nav, config, files):
    _relabel(nav.items)
    order = {name: i for i, name in enumerate(NAV_ORDER)}
    nav.items.sort(key=lambda it: (order.get(_dir_of(it), len(order)), _dir_of(it)))
    return nav


def on_page_markdown(markdown, page, config, files):
    """Retarget links to the repo-root README at the site's homepage.

    The root README.md is excluded from the build (index.md inlines it), so a
    unit page's "← All units" link to ``../README.md`` would 404 on the site
    while working fine on GitHub. Rewriting at build time keeps the source
    authored for GitHub's file-relative rendering — links to any *folder's*
    README are left alone.
    """
    src_dir = posixpath.dirname(page.file.src_path)

    def repl(m):
        href = m.group(2)
        if posixpath.normpath(posixpath.join(src_dir, href)) == "README.md":
            return m.group(1) + href[: -len("README.md")] + "index.md" + m.group(3)
        return m.group(0)

    return re.sub(r"(\]\()([^)\s#]*README\.md)([#)])", repl, markdown)
