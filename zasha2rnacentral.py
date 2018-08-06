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
    return annotations


def check_sequence(sequence):
    ok = 'ACGYRNSMWBKU'
    return all(c in ok for c in sequence)


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
        'patches',
        'preQ1-III',
        'ts',
        'twister',
        'variants',
    ]


def main():

    location = '/data/zashaweinbergdata/'
    entries = []

    taxid_file = '{}/sto-seqid-taxid.tab'.format(location)
    taxid_data = get_taxid_data(taxid_file)

    for folder in get_folders():
        for filename in glob.glob(os.path.join(location, folder, '*.sto')):
            rna_name = os.path.basename(filename).replace('.sto', '')

            alignment = AlignIO.read(open(filename), 'stockholm')
            annotations = get_stockholm_annotations(filename)

            # if alignment.column_annotations['secondary_structure'].count('>') != alignment.column_annotations['secondary_structure'].count('<'):
            #     import pdb; pdb.set_trace()

            for record in alignment:
                sequence = str(record.seq.ungap('-')).upper()
                if check_sequence(sequence) != True:
                    'Check sequence: %s' % sequence
                    import pdb; pdb.set_trace()
                # assert check_sequence(sequence) == True, 'Check sequence: %s' % sequence

                if record.name in taxid_data:
                    taxid = taxid_data[record.name]
                else:
                    taxid = '12908'  # unclassified sequences

                entries.append({
                    'primaryId': record.id,
                    'taxonId': taxid,
                    'soTermId': '',
                    'sequence': sequence,
                    'name': annotations['DE'] if 'DE' in annotations else '{} RNA'.format(rna_name),
                    # 'version': '1',
                    'url': 'https://bitbucket.org/zashaw/zashaweinbergdata/src/ba3b34e5418b990a87595ba150865be4d1d0bd35/{}/{}.sto'.format(folder, rna_name),
                    'publications' : [
                        'PMID:',
                    ],
                })

    data = {
        'data': entries,
        'metaData': {
                'dateProduced': '2018-06-08',
                'dataProvider': 'Zasha Weinberg Data',
                'release': '1.0',
                'schemaVersion': '0.2.0'
        }
    }

    with open('zwd.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    main()



# {
#         'data': [{
#                 'primaryId': 'FLYBASE:FBtr0346876',
#                 'taxonId': 'NCBITaxon:7227',
#                 'soTermId': 'SO:0000651',
#                 'sequence': 'ACGU',
#                 'name': '28S ribosomal RNA',
#                 'version': '1',
#                 'gene': {
#                         'geneId': 'FLYBASE:FBgn0267497',
#                         'symbol': 'Dmel\\28SrRNA:CR45837'
#                 },
#                 'genomeLocations': [{
#                         'assembly': 'BDGP6',
#                         'exons': [{
#                                 'INSDC_accession': 'CP007120.1',
#                                 'startPosition': 46770,
#                                 'endPosition': 49484,
#                                 'strand': '+'
#                         }]
#                 }],
#                 'url': 'http://flybase.org/reports/FBgn0267497.html',
#                 'publications': [
#                         'PMID:11679670',
#                         'PMID:15183728',
#                         'PMID:12554860',
#                         'PMID:14573789',
#                         'PMID:15325244',
#                         'PMID:17604727',
#                         'PMID:17616659',
#                         'PMID:17989717',
#                         'PMID:20158877'
#                 ]
#         }],
#         'metaData': {
#                 'dateProduced': '2017-11-20T22:19:12+01:00',
#                 'dataProvider': 'FLYBASE',
#                 'release': '2.0',
#                 'schemaVersion': '0.2.0'
#         }
# }
