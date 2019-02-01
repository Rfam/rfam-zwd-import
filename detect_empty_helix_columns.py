"""
Copyright [2009-2019] EMBL-European Bioinformatics Institute
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

"""
Usage:
python detect_empty_helix_columns.py

This script finds all alignments that have all gap columns annotated as part
of helices in the SS_cons line. Running esl-reformat --mingap to remove the
all-gap columns will result in an unbalanced secondary structure.
"""

import glob
import os
import re


from zwd2rnacentral import get_folders


def find_gap_helix_columns(filename):
    sequences = []
    accessions = []
    ss_cons = ''

    with open(filename, 'r') as f_in:
        for line in f_in.readlines():
            if line.startswith('#=GC SS_cons'):
                ss_cons = re.sub(r'#=GC SS_cons\s+', '', line)
            if line.startswith('#') or line.startswith('//'):
                continue
            accession, sequence = re.split(r'\s+', line.strip())
            sequences.append(sequence)
            accessions.append(accession)


    width = len(sequence)

    for i in range(width):
        all_gaps = True
        for j in range(len(sequences)):
            if sequences[j][i] != '.':
                all_gaps = False
                break
        if all_gaps and ss_cons[i] in '<>[]{}()':
            print('{}: Column {} is all gaps and SS_cons is a "{}"'.format(os.path.basename(filename.replace('.sto', '')), i+1, ss_cons[i]))


def main():
    location = '/data/zashaweinbergdata/'

    for folder in get_folders():
        for filename in glob.glob(os.path.join(location, folder, '*.sto')):
            find_gap_helix_columns(filename)


if __name__ == '__main__':
    main()
