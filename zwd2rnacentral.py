"""
Copyright [2009-present] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import json
import glob
import os
import re

from Bio import AlignIO


def get_taxid_data(taxid_file):
    taxids = {}
    with open(taxid_file, 'r') as infile:
        for line in infile.readlines():
            accession, taxid = line.strip().split('\t')
            taxids[accession] = taxid
    return taxids


def get_stockholm_annotations(filename):
    annotations = {}
    with open(filename, 'r') as stockholm:
        for line in stockholm.readlines():
            if line.startswith('#=GF '):
                (key, value) = line.replace('#=GF ', '').strip().split(' ', 1)
                annotations[key] = value
    if 'TP' not in annotations:
        print('TP line not found %s' % filename)
    return annotations


def get_papers_info(filename):
    """
    104	https://www.ncbi.nlm.nih.gov/pubmed/20230605
    """
    papers = {}
    with open(filename, 'r') as infile:
        for line in infile.readlines():
            fields = line.strip().split('\t')
            if 'https' in fields[1]:
                papers[fields[0]] = fields[1].replace('https://www.ncbi.nlm.nih.gov/pubmed/', '')
    return papers


def get_not_for_rfam_info(filename):
    """
    104/aceE.sto
    104/Bacteroides-2.sto
    """
    excluded = []
    with open(filename, 'r') as infile:
        for line in infile.readlines():
            excluded.append(line.strip())
    return excluded


def get_obsolete_taxid_mapping(filename):
    """
    Obsolete taxid Current taxid
    279263  420662
    469595  1639133
    """
    mapping = {}
    with open(filename, 'r') as infile:
        for i, line in enumerate(infile.readlines()):
            if i == 0:
                continue
            old, new = line.strip().split('  ')
            mapping[old] = new
    return mapping


def check_sequence(sequence):
    return re.match(r'^[ACGTYRNSMWBKU]+$', sequence)


def get_folders():
    return [
        '104',
        '22',
        '224',
        'MoCo',
        'NiCo',
        'SAH',
        'SAM-IV',
        'SAM-VI',
        'THF',
        'c-di-GMP-II',
        'exceptional',
        # 'patches',
        'preQ1-III',
        'ts',
        'twister',
        'variants',
    ]


def get_so_term(tp_line):
    so_term = 'SO:0000655'  # ncRNA
    if tp_line == 'Cis-reg;':
        so_term = 'SO:0005836'  # regulatory_region
    elif tp_line == 'Cis-reg; leader;':
        so_term = 'SO:0000204'  # five_prime_UTR
    elif tp_line == 'Cis-reg; riboswitch;':
        so_term = 'SO:0000035'  # riboswitch
    elif tp_line == 'Gene; antisense;':
        so_term = 'SO:0000077'  # antisense
    elif tp_line in ['Gene; ribozyme;', 'Gene;ribozyme;']:
        so_term = 'SO:0000374'  # ribozyme
    elif tp_line == 'Gene; sRNA;':
        so_term = 'SO:0000370'  # small_regulatory_ncRNA
    return so_term


def main():

    location = '/data/zashaweinbergdata/'
    entries = []

    taxid_data = get_taxid_data(os.path.join(location, 'sto-seqid-taxid.tab'))
    papers_data = get_papers_info(os.path.join(location, 'PAPERS'))
    excluded = get_not_for_rfam_info(os.path.join(location, 'not-for-Rfam'))
    taxid_mapping = get_obsolete_taxid_mapping('taxid-mapping.tsv')

    for folder in get_folders():
        for filename in glob.glob(os.path.join(location, folder, '*.sto')):
            rna_name = os.path.basename(filename).replace('.sto', '')

            if os.path.join(folder, rna_name + '.sto') in excluded:
                print('Not for Rfam: {}'.format(filename))
                continue
            else:
                print(filename)

            alignment = AlignIO.read(open(filename), 'stockholm')
            annotations = get_stockholm_annotations(filename)

            # if alignment.column_annotations['secondary_structure'].count('>') != alignment.column_annotations['secondary_structure'].count('<'):
            #     import pdb; pdb.set_trace()

            for record in alignment:
                sequence = str(record.seq.ungap('-')).upper().replace('U', 'T')
                if not check_sequence(sequence):
                    'Check sequence: %s' % sequence
                    continue

                if record.name in taxid_data:
                    taxid = taxid_data[record.name]
                    if taxid in taxid_mapping:
                        taxid = taxid_mapping[taxid]
                else:
                    taxid = '12908'  # unclassified sequences

                entries.append({
                    'primaryId': 'ZWD:' + record.id,
                    'taxonId': 'NCBITaxon:{}'.format(taxid),
                    'soTermId': get_so_term(annotations['TP'] if 'TP' in annotations else ''),
                    'sequence': sequence,
                    'name': annotations['DE'] if 'DE' in annotations else '{} RNA'.format(rna_name),
                    'url': 'https://bitbucket.org/zashaw/zashaweinbergdata/src/ba3b34e5418b990a87595ba150865be4d1d0bd35/{}/{}.sto'.format(folder, rna_name),
                    'publications' : [
                        'PMID:{}'.format(papers_data[folder]),
                    ],
                })

    data = {
        'data': entries,
        'metaData': {
                "dateProduced": "2018-08-24T00:00:00+01:00",
                'dataProvider': 'ZWD',
                'release': '1.0',
                'schemaVersion': '0.2.0',
                'publications': [
                    'PMID:28977401',
                ],
        }
    }

    with open('/data/rnacentral/zwd.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
