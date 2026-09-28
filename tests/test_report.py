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
