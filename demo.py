import yaml

data = {
    'category01': {
        'icon': '01.png',
        'snp': {
            'rs53576': {'AA': 'bla bla bla bla..',
                        'AG': 'blablablablaaaa',
                        'GG': 'blablalbaaaaaaaaaa'},
        }
    }
}

with open('data.yml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)