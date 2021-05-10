
import fnmatch
import os

os.system('rm zwd.fasta')

matches = []
for root, dirnames, filenames in os.walk('/path/to/zashaweinbergdata/'):
    for filename in fnmatch.filter(filenames, '*.sto'):
        matches.append(os.path.join(root, filename))
        cmd = 'esl-reformat fasta {} >> zwd.fasta'.format(os.path.join(root, filename))
        print(cmd)
        os.system(cmd)
