Make your genome report
===

Only tested with 23andme file

# Install

Needs Python 3.10 or later.

```
git clone https://github.com/Endika/genome_report
cd genome_report
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

# How to run

```
python report.py -g my_genome_file.txt

python report.py -g demo/male01.txt
```

Options: `-o` output name (default `my_report`), `-l` language, `es` (default) or `en`. The report is written as `<output>.html`; to get a PDF, open it in the browser and print to PDF. It loads its styles from `template/`, so it only renders styled when written at the repo root.

# Tests

```
pip install pytest
python -m pytest -q
```

# TODO
- Desing report
- Add more SNP in report
- Bring the English data up to the Spanish (108 of 138 tests, 191 of 317 SNPs)
