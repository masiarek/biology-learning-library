# Biology — Learning Library / Biblioteka biologii

High-school biology, term by term, **in two languages**. Every keyword from the course vocabulary list gets its own page: the same explanation side by side in **English and Polish** at the level of a North Carolina high-school Biology course (non-AP), and below it an **AP Biology deep dive** for anyone who wants to go further.

Biologia licealna, termin po terminie, **w dwóch językach**. Każde hasło z kursowej listy słownictwa ma własną stronę: to samo wyjaśnienie obok siebie **po angielsku i po polsku** na poziomie licealnego kursu biologii w Karolinie Północnej (nie-AP), a poniżej — **rozszerzenie na poziomie AP Biology** dla każdego, kto chce wiedzieć więcej.

**Browse the site:** <https://masiarek.github.io/biology-learning-library/> · **Full A–Z index:** [GLOSSARY.md](GLOSSARY.md) · **Which standards apply?** [STANDARDS.md](STANDARDS.md) · **Objective-by-objective map:** [NC_STANDARDS.md](NC_STANDARDS.md)

## The seven units / Siedem działów

| Unit | Dział po polsku | Terms |
|---|---|---|
| [Unit 1 · The Chemistry of Life](01_Chemistry_of_Life/README.md) | Chemia życia | 37 |
| [Unit 2 · Cells as Living Systems](02_Cells_as_Living_Systems/README.md) | Komórki jako układy żywe | 31 |
| [Unit 3 · Cellular Processes](03_Cellular_Processes/README.md) | Procesy komórkowe | 30 |
| [Unit 4 · DNA and Cell Division](04_DNA_and_Cell_Division/README.md) | DNA i podziały komórkowe | 38 |
| [Unit 5 · Genetics and Biotechnology](05_Genetics_and_Biotechnology/README.md) | Genetyka i biotechnologia | 50 |
| [Unit 6 · Evolution and Diversity of Life](06_Evolution_and_Diversity_of_Life/README.md) | Ewolucja i różnorodność życia | 49 |
| [Unit 7 · Ecological Principles](07_Ecological_Principles/README.md) | Podstawy ekologii | 32 |

**267 terms**, one folder per term, one page per folder — plus the occasional **extra page** for something the course list leans on without naming (currently [Ion](01_Chemistry_of_Life/ion/README.md)).

## How each page works / Jak działa każda strona

Every term page has the same shape:

1. **A two-column table — English | Polski.** Row by row: definition, plain-words restatement, a concrete example, and why the idea matters. The two columns say the same thing, so you can read whichever language is easier today and check yourself against the other. The English column is written at the level of the NC high-school Biology course (the guided-notes level, not AP).
2. **Po polsku — ujęcie podręcznikowe.** An independently written Polish take on the same concept — the way a Polish liceum textbook or Polish Wikipedia would frame it, with Polish terminology, synonyms, and school context. It is *not* a translation of the English column, and it ends with the exact Polish search terms for reading further.
3. **An AP Biology deep dive (English).** Below the divider, the same term at Advanced Placement depth: mechanisms, molecular details, classic experiments, and where it sits in the AP Biology course framework. Read it when the top half feels easy — it is enrichment, not required for the class.

Każda strona haseł ma ten sam układ: dwukolumnowa tabela (angielski | polski) na poziomie liceum, niezależne ujęcie po polsku — jak z polskiego podręcznika, a pod kreską — pogłębienie na poziomie AP Biology (po angielsku).

## Where the term list comes from

The units and their keyword lists mirror the vocabulary list of an Honors Biology course in Wake County, NC (seven units, from the chemistry of life through ecology). The explanations here are written from scratch for this library — it is a study companion, not a copy of any classroom material.

## Local preview

```bash
uv run --group docs mkdocs serve
```

The docs toolchain is pinned in `pyproject.toml` (`docs` dependency group) + `uv.lock`; the site deploys automatically from `.github/workflows/docs.yml` on every push to master.
