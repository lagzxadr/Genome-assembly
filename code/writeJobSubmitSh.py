# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 22:03:41 2016

@author: yanj


"""
import csv
import os

outpath1 = os.getcwd() + '/SRA189003/'
#createf = open('toSubmitJob_SRA189003.sh', 'w')
#createf.close()
count = 0
i = 0
with open('SRA189003_SraRunInfo.csv', 'rb') as csvfile: #there would be 135 libs
    freader = csv.reader(csvfile, delimiter = ',')
    for row in freader:
        if row[0].startswith('SRR'):
            count += 1
            if count%10 == 1:
                i += 1
                f = open(outpath1+'toSubmitJob_SRA189003_'+str(i)+'.sh', 'w')
                f.close()
            string = 'qsub -cwd -q ionode.q -pe OpenMP 1 -m ae -M yanj@gis.a-star.edu.sg '\
            '-l mem_free=10G,h_rt=5:0:0 '\
            '/mnt/projects/yanj/hcc/HPVsra.download/job.SRA189003/downLoad_' + row[0] + '.sh\n' 
        
            with open(outpath1+'toSubmitJob_SRA189003_'+str(i)+'.sh', 'a') as outf:
                outf.write(string)
                
    
outpath2 = os.getcwd() + '/SRA180295/'
#createf = open('toSubmitJob_SRA180295.sh', 'w')
#createf.close()
count = 0
i = 0
with open('SRA180295_SraRunInfo.csv', 'rb') as csvfile: #there would be 16 libs
    freader = csv.reader(csvfile, delimiter = ',')
    for row in freader:
        if row[0].startswith('SRR'):
            count += 1
            if count%10 == 1:
                i += 1
                f = open(outpath2+'toSubmitJob_SRA180295_'+str(i)+'.sh', 'w')
                f.close()
            string = 'qsub -cwd -q ionode.q -pe OpenMP 1 -m ae -M yanj@gis.a-star.edu.sg '\
            '-l mem_free=10G,h_rt=5:0:0 '\
            '/mnt/projects/yanj/hcc/HPVsra.download/job.SRA180295/downLoad_' + row[0] + '.sh\n' 
        
            with open(outpath2+'toSubmitJob_SRA180295_'+str(i)+'.sh', 'a') as outf:
                outf.write(string)
