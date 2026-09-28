import html
from pathlib import Path

import pytest
import yaml

from genome import GenomeReport

DEMO = Path(__file__).resolve().parent.parent / 'demo' / 'male01.txt'
DEMOS = sorted(DEMO.parent.glob('*.txt'))


@pytest.mark.parametrize('lang, categories, snp_result', [
    ('es', ['Salud', 'Enfermedades', 'Social', 'Rasgos', 'Dieta'],
     'Alteraci&oacute;n del rendimiento muscular, posible corredor.'),
    ('en', ['Health', 'Diseases', 'Social', 'Features', 'Diet'],
     'Alteration of muscle performance, possible runner.'),
])
def test_report_over_demo_genome(tmp_path, monkeypatch, lang, categories,
                                 snp_result):
    monkeypatch.chdir(tmp_path)

    GenomeReport(str(DEMO), output='report', lang=lang).make_report()

    html = (tmp_path / 'report.html').read_text(encoding='utf-8')
    for category in categories:
        assert '{} <span'.format(category) in html
    assert 'rs1815739' in html
    assert snp_result in html


SPANISH_LABELS = ['Informe', 'analizadas', 'Malas', 'Buenas', 'encontradas',
                  'Cromosoma', 'Tu genotipo', 'No hay resultados']


def test_english_report_has_no_spanish_labels(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    GenomeReport(str(DEMO), output='report', lang='en').make_report()

    html = (tmp_path / 'report.html').read_text(encoding='utf-8')
    assert '<html lang="en">' in html
    for label in ['Genetic report', 'analysed', 'Bad:', 'Good:', 'found:',
                  'Chromosome', 'Your genotype']:
        assert label in html
    for label in SPANISH_LABELS:
        assert label not in html


@pytest.mark.parametrize('genome', DEMOS, ids=lambda p: p.stem)
def test_english_report_has_no_spanish_characters(tmp_path, monkeypatch,
                                                  genome):
    monkeypatch.chdir(tmp_path)

    GenomeReport(str(genome), output='report', lang='en').make_report()

    text = html.unescape(
        (tmp_path / 'report.html').read_text(encoding='utf-8'))
    assert not set(text) & set('áéíóúñÁÉÍÓÚÑ¿¡´')


@pytest.mark.parametrize('lang', ['es', 'en'])
def test_every_snp_result_is_good_bad_or_neutral(lang):
    snp_file = DEMO.parent.parent / 'data' / lang / 'snp.yml'
    snps = yaml.safe_load(snp_file.read_text(encoding='utf-8'))

    invalid = [(rsid, genotype, result[1])
               for rsid, genotypes in snps.items()
               for genotype, result in genotypes.items()
               if result[1] not in (True, False, None)]
    assert invalid == []
