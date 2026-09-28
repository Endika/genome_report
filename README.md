Make your genome report
===

Only tested with 23andme file

# Install

Needs [uv](https://docs.astral.sh/uv/); it brings Python 3.10 or later itself.

```
git clone https://github.com/Endika/genome_report
cd genome_report
uv sync
```

# How to run

```
uv run report.py -g my_genome_file.txt

uv run report.py -g demo/male01.txt
```

Options: `-o` output name (default `my_report`), `-l` language, `es` (default) or `en`. The report is written as `<output>.html`; to get a PDF, open it in the browser and print to PDF. It loads its styles from `template/`, so it only renders styled when written at the repo root.

# Tests

```
uv run pytest -q
```

# TODO
- Desing report
- Add more SNP in report
- Bring the English data up to the Spanish (108 of 138 tests, 191 of 317 SNPs)
