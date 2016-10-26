# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 20:56:09 2016

@author: yanj
"""
import os
import csv
outpath1 = os.getcwd() + '/SRA180295/'

with open('SRA180295_SraRunInfo.csv', 'rb') as csvfile:
    freader = csv.reader(csvfile, delimiter = ',')
    for row in freader:
        if row[0].startswith('SRR'):
            string = '''/mnt/software/bin/ascp -k1 -Tr -l640M -i ~/.ssh/asperaweb_id_dsa.'''\
            '''openssh anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads'''\
            '''/ByRun/sra/SRR/SRR160/''' + row[0] + '/' + row[0] + \
            '''.sra /mnt/projects/yanj/hcc/HPVsra.download/SRA180295/'''
            with open(outpath1+'downLoad_'+row[0]+'.sh', 'w') as outf:
                outf.write(string)


outpath2 = os.getcwd() + '/SRA189003/'

with open('SRA189003_SraRunInfo.csv', 'rb') as csvfile:
    freader = csv.reader(csvfile, delimiter = ',')
    for row in freader:
        if row[0].startswith('SRR'):
            string = '''/mnt/software/bin/ascp -k1 -Tr -l640M -i ~/.ssh/asperaweb_id_dsa.'''\
            '''openssh anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads'''\
            '''/ByRun/sra/SRR/SRR161/''' + row[0] + '/' + row[0] + \
            '''.sra /mnt/projects/yanj/hcc/HPVsra.download/SRA189003/'''
            with open(outpath2+'downLoad_'+row[0]+'.sh', 'w') as outf:
                outf.write(string)