# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 22:03:41 2016
put the file to /mnt/proijects/yanj/hcc/HPVsra.download
@author: yanj


"""
import os
inpath1 = os.getcwd() + '/job.fastqdump.SRA189003/'
putpath1 = os.getcwd() + '/toSubmit/'
fileList = os.listdir(inpath1)
fileList.sort()
print fileList
f = open(putpath1+'toSubmitFastqdumpJob_SRA189003.sh', 'w')
f.close()
for fileName in fileList:
    string = 'qsub -cwd -q medium.q -pe OpenMP 1 -m a -M yanj@gis.a-star.edu.sg '\
            '-l mem_free=10G,h_rt=12:0:0 '\
            '/mnt/projects/yanj/hcc/HPVsra.download/job.fastqdump.SRA189003/' + fileName + '\n' 
    with open(putpath1+'toSubmitFastqdumpJob_SRA189003.sh', 'a') as outF:
        outF.write(string)




#with open('SRA189003_SraRunInfo.csv', 'rb') as csvfile: #there would be 135 libs
#    freader = csv.reader(csvfile, delimiter = ',')
#    for row in freader:
#        if row[0].startswith('SRR'):
#            count += 1
#            if count%10 == 1:
#                i += 1
#                f = open(outpath1+'toSubmitJob_SRA189003_'+str(i)+'.sh', 'w')
#                f.close()
#            string = 'qsub -cwd -q ionode.q -pe OpenMP 1 -m ae -M yanj@gis.a-star.edu.sg '\
#            '-l mem_free=10G,h_rt=5:0:0 '\
#            '/mnt/projects/yanj/hcc/HPVsra.download/job.SRA189003/downLoad_' + row[0] + '.sh\n' 
#        
#            with open(outpath1+'toSubmitJob_SRA189003_'+str(i)+'.sh', 'a') as outf:
#                outf.write(string)
#                
    

