
import collections
import os
import glob

from Bio import AlignIO

from zwd2rnacentral import get_folders, get_not_for_rfam_info


def get_rfam_annotations():
    data = collections.defaultdict(dict)
    with open('zwd-vs-rfam-14.1-cms.tbl', 'r') as infile:
        for line in infile.readlines():
            if line.startswith('#'):
                continue
            seq_id, _, rfam_acc, rfam_id, rest = line.split(None, 4)
            data[seq_id] = {
                'rfam_acc': rfam_acc,
                'rfam_id': rfam_id,
            }
    return data


def main():
    location = '/data/zashaweinbergdata/'

    rfam_annotations = get_rfam_annotations()
    not_for_rfam = get_not_for_rfam_info(os.path.join(location, 'not-for-Rfam'))

    print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('Folder', 'RNA', 'Rfam ID', 'Rfam accession', '% of sequences matching Rfam', '% of sequences not matching Rfam', 'not for Rfam'))

    for folder in get_folders():
        for filename in glob.glob(os.path.join(location, folder, '*.sto')):

            rna_name = os.path.basename(filename).replace('.sto', '')
            alignment = AlignIO.read(open(filename), 'stockholm')

            excluded = False
            if os.path.join(folder, rna_name + '.sto') in not_for_rfam:
                excluded = True

            families = set()
            accessions = set()
            matched = 0
            not_matched = 0
            num_records = 0

            for record in alignment:
                seq_id = record.id
                num_records += 1
                if seq_id in rfam_annotations:
                    families.add(rfam_annotations[seq_id]['rfam_id'])
                    accessions.add(rfam_annotations[seq_id]['rfam_acc'])
                    matched += 1
                else:
                    not_matched += 1

            line = '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(folder, rna_name, ', '.join(families),
                ', '.join(accessions), matched*100/num_records, not_matched*100/num_records,
                'Not for Rfam' if excluded else '')
            print(line)


if __name__ == '__main__':
    main()
