# -*- coding: utf-8 -*-

import csv
import os

from jinja2 import Environment, FileSystemLoader

import pdfkit

import yaml


class GenomeReport():
    """Genome report."""

    conf = {}
    report = {}
    snp = {}
    genoma_data = {}

    def __init__(self, genome_file,
                 report_format='html',
                 output='my_report', lang='es'):
        """Init."""
        self.conf = {
            'genome_file': genome_file,
            'report_format': report_format,
            'output_name': output,
            'report': 'data/{}/report.yml'.format(lang),
            'snp': 'data/{}/snp.yml'.format(lang)
        }
        self.load_files()

    def render(self, context, template='template/report.html'):
        """Make report to html."""
        path, filename = os.path.split(template)
        result = Environment(
            loader=FileSystemLoader(path or './')).get_template(
            filename).render(context)
        open('{}.html'.format(self.conf['output_name']), 'w').write(result)
        if self.conf['report_format'] == 'pdf':
            pdfkit.from_file(
                '{}.html'.format(self.conf['output_name']),
                '{}.pdf'.format(self.conf['output_name']))
            os.system('rm {}.html'.format(self.conf['output_name']))

    def load_files(self):
        """Load all files YAML and CSV."""
        self.report = yaml.load(open(self.conf['report'], 'r').read())
        self.snp = yaml.load(open(self.conf['snp'], 'r').read())
        self.genoma_data = list(
            csv.reader(open(self.conf['genome_file'], 'r'), delimiter='\t'))
        self.genoma_data = [x for x in self.genoma_data if len(x) == 4][1:]
        data_tmp = {}
        for data in self.genoma_data:
            data_tmp[data[0]] = [data[1], data[3]]
        self.genoma_data = data_tmp

    def search_alelo(self, genotype_results, g):
        """Detect alelo for example -C."""
        if '-' in g:
            g = g.replace('-', '')
        for genotype in genotype_results.keys():
            if '-' in genotype:
                alelo = genotype.replace('-', '')
                if len(alelo) == 1:
                    if alelo == g or alelo == g[::-1]:
                        return genotype_results[genotype]
        return False

    def check_snp(self, snp_list):
        """Check SNP and return results."""
        result = []
        good = 0
        bad = 0
        repute = None
        for snp in snp_list:
            genotype = self.genoma_data.get(snp, False)
            if genotype:
                chromosome = genotype[0]
                genotype = genotype[1]
                genotype_results = self.snp.get(snp, False)
                if genotype_results:
                    result_info = genotype_results.get(genotype, False)
                    if not result_info:
                        result_info = self.search_alelo(
                            genotype_results, genotype)
                    if result_info:
                        result.append({
                            'snp': snp,
                            'chromosome': chromosome,
                            'genotype': genotype,
                            'info': result_info[0]})
                        if result_info[1] is not None:
                            if result_info[1] is True:
                                good += 1
                            elif result_info[1] is False:
                                bad += 1
        if len(result) <= 0:
            return False, False, good, bad
        if good > bad:
            repute = True
        elif bad > good:
            repute = False
        return result, repute, good, bad

    def make_report(self):
        """Create custom report."""
        result = {}
        for category in self.report:
            category_data = self.report[category]
            result[category] = {'title': category_data['title'],
                                'icon': category_data['icon'],
                                'data': []}
            for test_data in category_data['data']:
                test_result = {'title': test_data['title']}
                test_result['snp'], test_result['repute'], test_result['good'], test_result['bad'] = self.check_snp(test_data['snp'])
                if test_result['snp'] and test_data.get('icon_result', False):
                    test_result['icon'] = test_data['icon_result'].get(
                        test_result['repute'], False)
                if test_result['snp'] and len(test_result['snp']) > 0:
                    result[category]['data'].append(test_result)
                elif test_data.get('default', False):
                    test_result['default'] = test_data['default']
                    test_result['repute'] = True
                    result[category]['data'].append(test_result)
                else:
                    test_result['default'] = '''
No hay resultados que cumplan los criterios.'''
                    test_result['repute'] = None
                    result[category]['data'].append(test_result)
            # if len(result[category]['data']) <= 0:
            #     del result[category]
        self.render({'result': result})
