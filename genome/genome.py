# -*- coding: utf-8 -*-

import csv
import os

from jinja2 import Environment, FileSystemLoader

import pdfkit

import yaml


class GenomeReport():
    """Genome report."""

    conf = {'report': 'data/report.yml',
            'snp': 'data/snp.yml',
            'report_format': 'html',
            'output_name': 'my_report'}
    report = {}
    snp = {}
    genoma_data = {}

    def __init__(self, genome_file, report_format='html'):
        """Init."""
        self.conf['genome_file'] = genome_file
        self.conf['report_format'] = report_format
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
            data_tmp[data[0]] = data[3]
        self.genoma_data = data_tmp

    def check_snp(self, snp_list):
        """Check SNP and return results."""
        result = []
        good = 0
        bad = 0
        repute = None
        for snp in snp_list:
            genotype = self.genoma_data.get(snp, False)
            if genotype:
                genotype_results = self.snp.get(snp, False)
                if genotype_results:
                    result_info = genotype_results.get(genotype, False)
                    if result_info:
                        result.append({
                            'snp': snp,
                            'genotype': genotype,
                            'info': result_info[0]})
                        if result_info[1] is not None:
                            if result_info[1] is True:
                                good += 1
                            elif result_info[1] is False:
                                bad += 1
        if len(result) <= 0:
            return False, False
        if good > bad:
            repute = True
        elif bad > good:
            repute = False
        return result, repute

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
                test_result['snp'], test_result['repute'] = self.check_snp(
                    test_data['snp'])
                if test_result['snp'] and test_data.get('icon_result', False):
                    test_result['icon'] = test_data['icon_result'].get(
                        test_result['repute'], False)
                if test_result['snp'] and len(test_result['snp']) > 0:
                    result[category]['data'].append(test_result)
            # if len(result[category]['data']) <= 0:
            #     del result[category]
        self.render({'result': result})
