#!/usr/bin/env python3
"""Regenerate NC_STANDARDS.md — the map from each NC Biology objective to the pages that teach it.

The mapping itself lives in ``STRANDS`` below; everything else is resolved from
disk, so a term page that gets written later turns into a link on the next run.
Run from the repo root:

    python3 tools/build_nc_standards.py

Three integrity rules, all enforced here rather than by eye:

1. **Every reference must resolve.** A slug that names no folder, and is not in
   ``PENDING``, fails the build — that is a typo, not a gap.
2. **A gap stays visible.** A term in ``PENDING`` renders as plain text with a
   dagger, never as a link, so the page never ships a 404 and doubles as the
   to-write list. Delete the entry once the page exists.
3. **Nothing is silently unmapped.** Term pages claimed by no objective are
   reported to stderr and counted on the page.

NC_STANDARDS.md is generated — edit this file, not the Markdown.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

UNITS = [
    "01_Chemistry_of_Life",
    "02_Cells_as_Living_Systems",
    "03_Cellular_Processes",
    "04_DNA_and_Cell_Division",
    "05_Genetics_and_Biotechnology",
    "06_Evolution_and_Diversity_of_Life",
    "07_Ecological_Principles",
]

# Unit number by folder, for the "u1"-style short refs used in the map below.
U = {f"u{i + 1}": name for i, name in enumerate(UNITS)}

# Term pages not written yet. A reference to one of these renders unlinked with
# a dagger instead of failing the build; the value is the name to print.
# Delete an entry the moment its README.md lands.
PENDING = {
    "u5/nondisjunction": "Nondisjunction",
    "u5/pedigree": "Pedigree",
    "u5/phenotype": "Phenotype",
    "u5/polygenic_inheritance": "Polygenic Inheritance",
    "u5/recessive_allele": "Recessive Allele",
    "u5/recombinant_dna": "Recombinant DNA",
    "u5/restriction_enzyme": "Restriction Enzyme",
    "u5/sex_chromosomes": "Sex Chromosomes",
    "u5/sex_linked_traits": "Sex-Linked Traits",
    "u5/sexual_reproduction": "Sexual Reproduction",
    "u5/sickle_cell_anemia": "Sickle Cell Anemia",
    "u5/transgenic_organism": "Transgenic Organism",
    "u5/vaccine": "Vaccine",
    "u5/zygote": "Zygote",
    "u6/taxonomy": "Taxonomy",
    "u6/territoriality": "Territoriality",
    "u6/trial_and_error_learning": "Trial and Error Learning",
    "u6/tropism": "Tropism",
    "u6/vestigial_structure": "Vestigial Structure (Organ)",
}

# The NC Standard Course of Study for Biology, approved July 2023, required in
# classrooms from 2024–25. Four strands, ten standards, twenty-seven objectives.
#
# "what" is a faithful short restatement of the official objective, keeping the
# Science and Engineering Practice verb the 2023 rewrite put at the front of
# every one — that verb is what the EOC actually asks students to do. The
# verbatim text is in the source PDF linked at the foot of the page.
#
# EOC weights come from NCDPI's EOC NC Biology Test Specifications, which drops
# the "LS." prefix (Bio.1.1); the standards document keeps it (LS.Bio.1.1).
STRANDS = [
    {
        "no": 1,
        "en": "From Molecules to Organisms — Structures and Processes",
        "pl": "Od cząsteczek do organizmów — budowa i procesy",
        "weight": "26–34%",
        "items": "13–17 items",
        "standards": [
            {
                "code": "LS.Bio.1",
                "title": "Analyze how the relationship between structure and function supports life processes within organisms.",
                "objectives": [
                    {
                        "code": "LS.Bio.1.1",
                        "what": "Construct an explanation of how structure and function relate in the major macromolecules of life.",
                        "terms": [
                            "u1/monomer", "u1/polymer", "u1/organic", "u1/carbohydrate",
                            "u1/monosaccharide", "u1/polysaccharide", "u1/glucose", "u1/starch",
                            "u1/glycogen", "u1/cellulose", "u1/lipid", "u1/protein",
                            "u1/amino_acid", "u1/peptide_bond", "u1/polypeptide",
                            "u1/nucleic_acid", "u1/nucleotide", "u1/hemoglobin", "u1/insulin",
                            "u1/hormone",
                        ],
                    },
                    {
                        "code": "LS.Bio.1.2",
                        "what": "Carry out investigations showing how enzymes catalyze biochemical reactions — and how environmental factors change enzyme activity.",
                        "terms": [
                            "u1/enzymes", "u1/catalyst", "u1/active_site", "u1/substrate",
                            "u1/lock_and_key_model", "u1/activation_energy",
                            "u1/denatured_enzyme", "u1/reactant", "u1/product",
                            "u1/metabolism", "u1/endothermic", "u1/exothermic",
                            "u1/ph", "u1/acid", "u1/base", "u1/buffer",
                        ],
                    },
                    {
                        "code": "LS.Bio.1.3",
                        "what": "Use models to explain how an organelle's structure determines its function and supports the whole cell.",
                        "terms": [
                            "u2/cell", "u2/organelle", "u2/cytoplasm", "u2/nucleus",
                            "u2/nucleolus", "u2/ribosome", "u2/endoplasmic_reticulum",
                            "u2/golgi_apparatus", "u2/vesicles", "u2/lysosome",
                            "u2/mitochondria", "u2/chloroplast", "u2/vacuoles",
                            "u2/central_vacuole", "u2/contractile_vacuole", "u2/cytoskeleton",
                            "u2/centrioles", "u2/cilia", "u2/flagella", "u2/pseudopod",
                            "u2/eyespot", "u2/cell_membrane", "u2/phospholipid_bilayer",
                            "u2/cell_wall",
                        ],
                    },
                    {
                        "code": "LS.Bio.1.4",
                        "what": "Construct explanations comparing prokaryotic and eukaryotic cells — structures, and degree of complexity.",
                        "terms": [
                            "u2/prokaryote", "u2/eukaryote", "u2/plasmid",
                            "u2/unicellular", "u2/multicellular", "u2/tissue", "u2/organ",
                            "u4/binary_fission",
                        ],
                    },
                    {
                        "code": "LS.Bio.1.5",
                        "what": "Construct an explanation of how DNA and RNA direct the synthesis of proteins.",
                        "terms": [
                            "u4/dna", "u4/deoxyribose", "u4/ribose", "u4/nitrogenous_base",
                            "u4/complementary_base_pairing", "u4/gene", "u4/protein_synthesis",
                            "u4/transcription", "u4/translation", "u4/mrna", "u4/trna",
                            "u4/rrna", "u4/codon", "u4/anticodon",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.2",
                "title": "Analyze the growth and development processes of organisms.",
                "objectives": [
                    {
                        "code": "LS.Bio.2.1",
                        "what": "Use models to illustrate how cell division produces reproduction, growth and repair.",
                        "terms": [
                            "u4/cell_cycle", "u4/interphase", "u4/mitosis", "u4/cytokinesis",
                            "u4/dna_replication", "u4/chromosome", "u4/chromatin",
                            "u4/centromere", "u4/sister_chromatids", "u4/spindle_fibers",
                            "u4/diploid", "u4/haploid", "u4/somatic_cells",
                            "u4/asexual_reproduction",
                        ],
                    },
                    {
                        "code": "LS.Bio.2.2",
                        "what": "Construct an explanation of how proteins regulate gene expression — giving differentiation, specialized cells, and uncontrolled growth.",
                        "terms": [
                            "u4/cell_differentiation", "u4/adult_stem_cells",
                            "u4/embryonic_stem_cells", "u4/mutation", "u4/cancer", "u4/tumor",
                            "u4/benign", "u4/malignant", "u4/metastasize",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.3",
                "title": "Analyze the relationship between biochemical processes and energy use.",
                "objectives": [
                    {
                        "code": "LS.Bio.3.1",
                        "what": "Carry out investigations to explain how homeostasis is maintained through feedback mechanisms.",
                        "terms": [
                            "u1/homeostasis", "u3/dynamic_equilibrium",
                            "u3/selectively_permeable", "u3/concentration_gradient",
                            "u3/diffusion", "u3/osmosis", "u3/passive_transport",
                            "u3/facilitated_diffusion", "u3/active_transport",
                            "u3/endocytosis", "u3/exocytosis", "u3/hypertonic",
                            "u3/hypotonic", "u3/isotonic", "u3/turgor_pressure",
                            "u3/plasmolysis", "u3/solute", "u3/solvent", "u3/solution",
                            "u5/diabetes",
                        ],
                    },
                    {
                        "code": "LS.Bio.3.2",
                        "what": "Use models to illustrate how photosynthesis transforms light energy into chemical energy.",
                        "terms": [
                            "u3/photosynthesis", "u3/light_energy", "u3/chlorophyll",
                            "u3/autotroph", "u3/chemosynthesis",
                        ],
                    },
                    {
                        "code": "LS.Bio.3.3",
                        "what": "Use models to illustrate how cellular respiration — aerobic and anaerobic — transforms chemical energy into ATP.",
                        "terms": [
                            "u3/cellular_respiration", "u3/aerobic_respiration",
                            "u3/anaerobic_respiration", "u3/alcoholic_fermentation",
                            "u3/lactic_acid_fermentation", "u3/atp", "u3/heterotroph",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "no": 2,
        "en": "Ecosystems — Interactions, Energy, and Dynamics",
        "pl": "Ekosystemy — zależności, energia i dynamika",
        "weight": "14–22%",
        "items": "7–11 items",
        "standards": [
            {
                "code": "LS.Bio.4",
                "title": "Analyze the relationships between matter and energy within ecosystems.",
                "objectives": [
                    {
                        "code": "LS.Bio.4.1",
                        "what": "Use models to illustrate how processes in organisms feed the flow of energy and the cycling of matter in an ecosystem.",
                        "terms": [
                            "u7/producer", "u7/consumer", "u7/decomposer",
                            "u7/nitrogen_fixation", "u7/carbon_sink", "u7/fossil_fuels",
                        ],
                    },
                    {
                        "code": "LS.Bio.4.2",
                        "what": "Use models to explain the relationship between energy flow and matter cycling among an ecosystem's organisms.",
                        "terms": [
                            "u7/trophic_levels", "u7/biomass", "u7/bioaccumulation",
                            "u7/biological_magnification",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.5",
                "title": "Understand ecosystem dynamics, functioning, and resilience.",
                "objectives": [
                    {
                        "code": "LS.Bio.5.1",
                        "what": "Use mathematics and computational thinking to explain how predator/prey relations and competition affect carrying capacity and stability.",
                        "terms": [
                            "u7/population", "u7/community", "u7/niche",
                            "u7/carrying_capacity", "u7/limiting_factor",
                            "u7/exponential_growth", "u7/logistic_growth",
                            "u7/predator", "u7/prey", "u7/symbiosis", "u7/mutualism",
                            "u7/commensalism", "u7/parasitism",
                        ],
                    },
                    {
                        "code": "LS.Bio.5.2",
                        "what": "Engage in argument from evidence to evaluate solutions that reduce human impact on biodiversity and ecosystem health.",
                        "terms": [
                            "u6/biodiversity", "u7/invasive_species",
                            "u7/non_native_species", "u7/acid_rain", "u7/algal_bloom",
                            "u7/eutrophication", "u7/climate_change",
                            "u7/greenhouse_gases", "u7/chlorofluorocarbons",
                            "u7/mitigation",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "no": 3,
        "en": "Heredity — Inheritance and Variation of Traits",
        "pl": "Dziedziczność — dziedziczenie i zmienność cech",
        "weight": "24–32%",
        "items": "12–16 items",
        "standards": [
            {
                "code": "LS.Bio.6",
                "title": "Understand genetic mechanisms for variation.",
                "objectives": [
                    {
                        "code": "LS.Bio.6.1",
                        "what": "Use models to explain how DNA passes from parents to offspring through meiosis and fertilization.",
                        "terms": [
                            "u5/meiosis", "u5/gametes", "u5/fertilization", "u5/zygote",
                            "u5/sexual_reproduction", "u5/homologous_chromosomes",
                            "u5/autosomal_chromosomes", "u5/sex_chromosomes",
                            "u5/karyotype", "u5/genome",
                        ],
                    },
                    {
                        "code": "LS.Bio.6.2",
                        "what": "Construct an explanation of where heritable variation comes from: new combinations in meiosis, mutations during replication, mutations caused by the environment.",
                        "terms": [
                            "u5/crossing_over", "u5/independent_assortment",
                            "u5/genetic_recombination", "u5/nondisjunction",
                            "u5/down_syndrome", "u4/mutation",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.7",
                "title": "Understand types of inheritance and how the environment can influence traits.",
                "objectives": [
                    {
                        "code": "LS.Bio.7.1",
                        "what": "Use mathematics and computational thinking to predict trait distributions — Mendelian, co-dominance, incomplete dominance, multiple alleles, sex-linked.",
                        "terms": [
                            "u5/genetics", "u5/inheritance", "u5/allele",
                            "u5/dominant_allele", "u5/recessive_allele", "u5/homozygous",
                            "u5/heterozygous", "u5/genotype", "u5/phenotype",
                            "u5/monohybrid_cross", "u5/codominance",
                            "u5/incomplete_dominance", "u5/multiple_alleles",
                            "u5/sex_linked_traits", "u5/color_blindness", "u5/hemophilia",
                            "u5/pedigree", "u5/cystic_fibrosis", "u5/huntingtons_disease",
                        ],
                    },
                    {
                        "code": "LS.Bio.7.2",
                        "what": "Analyze and interpret data to explain how polygenic traits give a wide range of phenotypes.",
                        "terms": ["u5/polygenic_inheritance", "u5/phenotype"],
                    },
                    {
                        "code": "LS.Bio.7.3",
                        "what": "Construct an explanation of how traits come from genetic factors and environmental factors interacting.",
                        "terms": [
                            "u5/polygenic_inheritance", "u5/sickle_cell_anemia",
                            "u5/diabetes",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.8",
                "title": "Understand applications of genetics and biotechnology.",
                "objectives": [
                    {
                        "code": "LS.Bio.8.1",
                        "what": "Analyze and interpret data to compare DNA samples.",
                        "terms": [
                            "u5/dna_fingerprint", "u5/gel_electrophoresis",
                            "u5/restriction_enzyme", "u5/karyotype",
                        ],
                    },
                    {
                        "code": "LS.Bio.8.2",
                        "what": "Obtain and communicate information on how biotechnology affects the individual, society and the environment — including agriculture and medicine.",
                        "terms": [
                            "u5/biotechnology", "u5/bioethics", "u5/recombinant_dna",
                            "u5/genetically_modified_organism", "u5/transgenic_organism",
                            "u5/bacterial_transformation", "u5/cloning", "u5/crispr",
                            "u5/gene_therapy", "u5/vaccine",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "no": 4,
        "en": "Biological Evolution — Unity and Diversity",
        "pl": "Ewolucja biologiczna — jedność i różnorodność",
        "weight": "20–28%",
        "items": "10–14 items",
        "standards": [
            {
                "code": "LS.Bio.9",
                "title": "Understand natural selection as a mechanism for biological evolution.",
                "objectives": [
                    {
                        "code": "LS.Bio.9.1",
                        "what": "Analyze and interpret data on how geographic isolation, pesticide resistance and antibiotic resistance influence natural selection.",
                        "terms": [
                            "u6/geographic_isolation", "u6/antibiotic_resistance",
                            "u6/pesticide_resistance", "u6/selective_pressure",
                            "u6/gene_pool",
                        ],
                    },
                    {
                        "code": "LS.Bio.9.2",
                        "what": "Construct an explanation of how several independent lines of evidence support common ancestry and evolution.",
                        "terms": [
                            "u6/evolution", "u6/fossil_record", "u6/homologous_structures",
                            "u6/analogous_structures", "u6/vestigial_structure",
                            "u6/embryological_development", "u6/morphology", "u6/primitive",
                        ],
                    },
                    {
                        "code": "LS.Bio.9.3",
                        "what": "Use models to illustrate what natural selection requires: overproduction of offspring, inherited variation, and the struggle to survive.",
                        "terms": [
                            "u6/natural_selection", "u6/fitness",
                            "u6/external_fertilization", "u6/internal_fertilization",
                            "u6/spores", "u6/seeds", "u6/placenta",
                        ],
                    },
                    {
                        "code": "LS.Bio.9.4",
                        "what": "Construct an explanation of how natural selection leads to adaptations within populations.",
                        "terms": [
                            "u6/adaptation", "u6/camouflage", "u6/estivation",
                            "u6/hibernation", "u6/innate_behavior", "u6/habituation",
                            "u6/imprinting", "u6/classical_conditioning",
                            "u6/trial_and_error_learning", "u6/taxis", "u6/tropism",
                            "u6/courtship", "u6/pheromone", "u6/territoriality",
                            "u6/suckling",
                        ],
                    },
                ],
            },
            {
                "code": "LS.Bio.10",
                "title": "Analyze evolutionary relationships among organisms.",
                "objectives": [
                    {
                        "code": "LS.Bio.10.1",
                        "what": "Construct explanations of how changing environmental conditions change population sizes, produce new species, or drive species extinct.",
                        "terms": ["u6/speciation", "u6/extinction"],
                    },
                    {
                        "code": "LS.Bio.10.2",
                        "what": "Use models — dichotomous keys, scientific nomenclature, cladograms, phylogenetic trees — to identify organisms and show how they are related.",
                        "terms": [
                            "u6/classification", "u6/taxonomy", "u6/binomial_nomenclature",
                            "u6/dichotomous_key", "u6/cladogram", "u6/phylogenetic_tree",
                            "u6/domain", "u6/kingdom", "u6/phylum", "u6/genus", "u6/species",
                        ],
                    },
                ],
            },
        ],
    },
]

HEADER = """# Where each NC standard is covered / Gdzie znaleźć każdy standard

The **North Carolina Standard Course of Study for Biology** — approved July 2023, in classrooms from 2024–25 — is four strands, ten standards, twenty-seven objectives. This page lists all twenty-seven and links every term page in this library that teaches them, so you can go the other way round: from the objective on the packet's unit cover sheet to the pages that explain it.

**Podstawa programowa z biologii dla Karoliny Północnej** (przyjęta w lipcu 2023, obowiązuje od roku 2024–25) to cztery działy tematyczne, dziesięć standardów i dwadzieścia siedem celów kształcenia. Ta strona wymienia wszystkie dwadzieścia siedem i linkuje do haseł, które je omawiają — od celu wypisanego na okładce działu w szkolnym pakiecie do stron, które go tłumaczą.

Why these standards and not some other set — Honors vs standard, and how AP Biology differs: [STANDARDS.md](STANDARDS.md). Every term A–Z: [GLOSSARY.md](GLOSSARY.md).

## How to read this page

- **The codes.** The standards document writes `LS.Bio.1.1`; NCDPI's EOC test specifications drop the prefix and write `Bio.1.1`. Same objective — expect to see both.
- **The verbs are load-bearing.** Every 2023 objective opens with a Science and Engineering Practice — *use models*, *construct an explanation*, *carry out investigations*, *analyze and interpret data*, *use mathematics and computational thinking*, *engage in argument from evidence*. Between 50% and 70% of EOC items pair a science idea with one of those practices, so "explain photosynthesis" is not the same task as "use a model to illustrate photosynthesis." The wording below is shortened; the official text is in the source PDF at the foot of this page.
- **Honors changes the depth, not the list.** An Honors section covers exactly these objectives and takes exactly this EOC. See [STANDARDS.md](STANDARDS.md).
- **A dagger (†) means the page is not written yet.** Those terms are on the list and unlinked on purpose.
- **A term can appear under two objectives.** Phenotype belongs to both `7.1` and `7.2`; mutation to both `2.2` and `6.2`. That is the standards' own overlap, not a mistake.

## What the EOC weighs

Fifty operational items, and the strands are not equal. If study time has to be rationed, ration it by this table:

| Strand | Objectives | Weight | Items |
|---|---|---|---|
"""

FOOTER_SOURCES = """
## Sources

- [NC DPI — Science Standard Course of Study](https://www.dpi.nc.gov/districts-schools/classroom-resources/office-teaching-and-learning/standard-course-study/science) and the [NC K-12 Science Standards Resource Hub](https://sites.google.com/dpi.nc.gov/k-12science/home) — the official home of the 2023 standards, crosswalks and support documents. NCDPI serves them from the Hub rather than as a stable public PDF link.
- [NC Standard Course of Study — K-12 Science, approved July 2023](https://www.poehealth.org/wp-content/uploads/2025/07/NC-DPI-Science-Standards.pdf) — a **mirror copy** (hosted by a third party, not NCDPI), and the one directly linkable full text: every page is footed "Approved July 2023", and its Biology section carries the verbatim wording of all twenty-seven objectives shortened above.
- [NC DPI — EOC NC Biology Test Specifications](https://www.dpi.nc.gov/documents/accountability/testing/eoc/eoc-nc-biology-test-specifications) — strand weights, item counts, and the practice/core-idea split quoted above.
- [NC DPI — Honors Level Coursework](https://www.dpi.nc.gov/students-families/enhanced-opportunities/advanced-learning-and-gifted-education/honors-level-coursework) — the honors framework: same standards, greater depth and scope.
"""


def page_name(path: Path) -> str | None:
    """English half of a term page's ``# English / Polski`` H1."""
    first = path.read_text(encoding="utf-8").lstrip().splitlines()[0]
    m = re.match(r"#\s+(.+?)\s+/\s+(.+)", first)
    return m.group(1).strip() if m else None


def main() -> int:
    problems: list[str] = []
    claimed: set[str] = set()

    def render(ref: str) -> str:
        unit_key, slug = ref.split("/", 1)
        unit_dir = U.get(unit_key)
        if unit_dir is None:
            problems.append(f"unknown unit key in reference: {ref}")
            return f"`{ref}`"
        readme = REPO / unit_dir / slug / "README.md"
        if readme.is_file():
            claimed.add(f"{unit_dir}/{slug}")
            name = page_name(readme)
            if name is None:
                problems.append(f"{unit_dir}/{slug}/README.md: H1 is not '# English / Polski'")
                return f"`{ref}`"
            return f"[{name}]({unit_dir}/{slug}/README.md)"
        if ref in PENDING:
            claimed.add(f"{unit_dir}/{slug}")
            return f"{PENDING[ref]}&nbsp;†"
        problems.append(
            f"{ref}: no {unit_dir}/{slug}/README.md and not listed in PENDING "
            "(a typo, or a page that needs a PENDING entry)"
        )
        return f"`{ref}`"

    # Body: one section per strand, one sub-heading per standard, one row per objective.
    body: list[str] = []
    weights: list[str] = []
    n_objectives = 0
    for strand in STRANDS:
        codes = [s["code"].replace("LS.Bio.", "") for s in strand["standards"]]
        weights.append(
            f"| Strand {strand['no']} · {strand['en']} | LS.Bio.{codes[0]}–{codes[-1]} "
            f"| **{strand['weight']}** | {strand['items']} |\n"
        )
        body.append(
            f"\n## Strand {strand['no']} · {strand['en']}\n\n"
            f"*{strand['pl']}* — **{strand['weight']}** of the EOC ({strand['items']}).\n"
        )
        for standard in strand["standards"]:
            body.append(f"\n### {standard['code']} — {standard['title']}\n\n")
            body.append("| Objective | What it asks | Pages here |\n|---|---|---|\n")
            for obj in standard["objectives"]:
                n_objectives += 1
                terms = ", ".join(render(ref) for ref in obj["terms"])
                body.append(f"| **{obj['code']}** | {obj['what']} | {terms} |\n")

    if problems:
        for p in problems:
            print(f"PROBLEM: {p}", file=sys.stderr)
        return 1

    # Reverse check: every term page should be claimed by some objective.
    all_terms = {
        f"{unit}/{page.parent.name}"
        for unit in UNITS
        for page in (REPO / unit).glob("*/README.md")
    }
    unclaimed = sorted(all_terms - claimed)
    for ref in unclaimed:
        print(f"NOTE: not tied to an objective: {ref}", file=sys.stderr)

    n_written = len(all_terms)
    n_pending = len(PENDING)
    coverage = (
        f"\n## Coverage\n\n"
        f"**{n_objectives} objectives**, mapped onto all **{n_written} term pages written so far**"
        + (
            f" — plus **{n_pending} terms still to write**, the daggered ones "
            f"({n_written + n_pending} course terms in total). They sit in Units 5 and 6, "
            f"and Heredity is the heaviest strand on the test, so that is where the gap costs most"
            if n_pending
            else ""
        )
        + ".\n"
    )
    if unclaimed:
        coverage += (
            f"\n{len(unclaimed)} page"
            + ("s are" if len(unclaimed) != 1 else " is")
            + " supporting vocabulary the standards do not name directly: "
            + ", ".join(
                f"[{page_name(REPO / ref / 'README.md') or ref}]({ref}/README.md)"
                for ref in unclaimed
            )
            + ".\n"
        )

    out = (
        HEADER
        + "".join(weights)
        + "| **Total** | | **100%** | **50 operational** (60 with field-test items) |\n"
        + "".join(body)
        + coverage
        + FOOTER_SOURCES
    )
    out += (
        "\n*(Generated by `tools/build_nc_standards.py` — edit the mapping in that "
        "script, not this page.)*\n"
    )
    (REPO / "NC_STANDARDS.md").write_text(out, encoding="utf-8")
    print(
        f"NC_STANDARDS.md written: {n_objectives} objectives, "
        f"{len(claimed) - n_pending} linked pages, {n_pending} pending, "
        f"{len(unclaimed)} unclaimed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
