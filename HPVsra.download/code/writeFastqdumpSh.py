# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 20:56:09 2016
put this file to /mnt/projects/yanj/.hcc/HPVsra.download
@author: yanj
"""
import os

inpath1 = os.getcwd() + '/SRA189003/'
outpath1 = os.getcwd() + '/SRA189003.fastq/'
putpath1 = os.getcwd() + '/job.fastqdump.SRA189003/'
fileList = os.listdir(inpath1)
fileList.sort()
print fileList

for fileName in fileList:
    string = '''/mnt/software/bin/fastq-dump -origfmt -I --split-files ''' + inpath1 + \
            fileName + ' -gzip -O ' + outpath1 

    with open(putpath1+'fastqdump_'+fileName[:-4]+'.sh', 'w') as outF:
        outF.write(string)


    


#with open('SRA189003_SraRunInfo.csv', 'rb') as csvfile:
#    freader = csv.reader(csvfile, delimiter = ',')
#    for row in freader:
#        if row[0].startswith('SRR'):
#            string = '''/mnt/software/bin/ascp -k1 -Tr -l640M -i ~/.ssh/asperaweb_id_dsa.'''\
#            '''openssh anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads'''\
#            '''/ByRun/sra/SRR/SRR161/''' + row[0] + '/' + row[0] + \
#            '''.sra /mnt/projects/yanj/hcc/HPVsra.download/SRA189003/'''
#            with open(outpath2+'downLoad_'+row[0]+'.sh', 'w') as outf:
#                outf.write(string)