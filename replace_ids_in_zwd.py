
import csv
import os
import glob
import re


from zwd2rnacentral import get_folders, get_not_for_rfam_info


def get_zwd_rnacentral_mapping():
    """
    URS0000C93932	ZWD	NC_008357.1/80290-80170	287	ncRNA
    URS0000D6769E	ZWD	NZ_JH376463.1/143717-143786	287	ncRNA
    URS0000D68612	ZWD	NC_009739.1/22315-22194	287	ncRNA
    """
    data = {}
    with open('/data/rnacentral/zwd-rnacentral-ids.tsv', 'r') as f:
        reader = csv.DictReader(f, delimiter='\t', fieldnames=('urs', 'label', 'seq_id', 'taxid', 'rna_type'))
        for record in reader:
            data[record['seq_id']] = record['urs'] + '_' + record['taxid']
    return data


def main():

    location = '/data/zashaweinbergdata/'

    not_for_rfam = get_not_for_rfam_info(os.path.join(location, 'not-for-Rfam'))
    rnacentral_mapping = get_zwd_rnacentral_mapping()

    for folder in get_folders():
        if '224' not in folder:
            continue
        for filename in glob.glob(os.path.join(location, folder, '*.sto')):

            rna_name = os.path.basename(filename).replace('.sto', '')
            print(rna_name)
            if os.path.join(folder, rna_name + '.sto') in not_for_rfam:
                continue

            unique_lines = []
            with open(filename, 'r') as zwd_stockholm:
                with open("/data/rnacentral/zwd-rnacentral-ids/{}.sto".format(rna_name), 'w') as output:
                    for line in zwd_stockholm:

                        if line.startswith('#=GC SS_cons'):
                            output.write('#=GC SS_cons'.ljust(35) + line.replace('#=GC SS_cons', '').lstrip())
                        elif line.startswith('#') or line.startswith('//'):
                            output.write(line)
                        else:
                            seq_id = re.search(r'(^\S+)(\s+)(.+)', line)
                            sequence_ungapped = seq_id.group(3).replace('.', '')
                            if seq_id and seq_id.group(1) in rnacentral_mapping:
                                rnacentral_id = '{}/1-{}'.format(rnacentral_mapping[seq_id.group(1)], len(sequence_ungapped)).ljust(35)
                                new_line = '{}{}\n'.format(rnacentral_id, seq_id.group(3))
                                if new_line not in unique_lines:
                                    output.write(new_line)
                                    unique_lines.append(new_line)


if __name__ == '__main__':
    main()
