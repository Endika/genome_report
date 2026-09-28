# -*- coding: utf-8 -*-

import getopt
import sys

from genome import GenomeReport


def _print_help():
    help_text = ('{} -g <genome_file.txt> '
                 '[-o my_report_name] [-l es]'.format(sys.argv[0]))
    print(help_text)
    sys.exit(2)


def _parse_params(argv, opts, conf):
    for opt, arg in opts:
        if opt == '-h':
            _print_help()
        elif opt in ("-g", "--genome"):
            conf['genome_file'] = arg
        elif opt in ("-o", "--output"):
            conf['output'] = arg
        elif opt in ("-l", "--lang"):
            conf['lang'] = arg


def get_opt(argv, conf):
    """Get OPT."""
    try:
        opts, args = getopt.getopt(
            argv, "g:o:l:", ["genome=", "output=", "lang="])
    except getopt.GetoptError:
        _print_help()
    _parse_params(argv, opts, conf)
    if not conf['genome_file']:
        _print_help()


def main(argv):
    """Run program."""
    conf = {'genome_file': False,
            'output': 'my_report',
            'lang': 'es'}
    get_opt(argv, conf)
    genome_obj = GenomeReport(
        conf['genome_file'], output=conf['output'], lang=conf['lang'])
    genome_obj.make_report()

if __name__ == "__main__":
    main(sys.argv[1:])
