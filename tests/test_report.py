from pathlib import Path

import pytest

from genome import GenomeReport

DEMO = Path(__file__).resolve().parent.parent / 'demo' / 'male01.txt'


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
