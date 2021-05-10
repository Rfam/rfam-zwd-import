from Bio import AlignIO

align = AlignIO.read("/data/rnacentral/zwd-rnacentral-ids/archive/RAGATH-2-HDV.sto", "stockholm")

for i in range(0, align.get_alignment_length()):
    column = align[:,i]
    if column.count('-') == len(column):
        print(column)
        print(i)
