Make your genome report
===

Only tested with 23andme file

The code is Python 2 (`genome/__init__.py` uses an implicit relative import) and `requirements.txt` doesn't install as it stands: Jinja2 3.1.6 needs MarkupSafe 2.0 or later and Python 3, and `wsgiref` is Python 2 only.

# Install

```
git clone https://github.com/Endika/genome_report
sudo apt-get install wkhtmltopdf
pip install -r requirements.txt
```

# How to run

```
python report.py -g my_genome_file.txt -f html

python report.py -g demo/male01.txt
```

Options: `-o` output name (default `my_report`), `-l` language, `es` (default) or `en`. `-f pdf` writes HTML too: `report.py` maps both formats to `html`, so wkhtmltopdf is never called.

# TODO
- Desing report
- Add more SNP in report
- Bring the English data up to the Spanish (108 of 138 tests, 191 of 317 SNPs)
