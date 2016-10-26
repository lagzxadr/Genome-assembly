# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:51:55 2016

@author: yanj
"""
'''
'time java -XX:+UseSerialGC -cp "/mnt/projects/guanp/hcc/HBV/visp.20151230.jar:/mnt/projects/guanp/hcc
/HBV/lib/*" -Xms8g -Xmx32g visp.VISP /mnt/projects/yanj/hcc/HPV.VISP/vispcfgFile/visp.HPV.cfg /mnt/proj
ects/yanj/hcc/HPV.VISP/samplecfgFile/visp.samples.SRR161XXXX.cfg /mnt/projects/yanj/hcc/HPV.VISP/Ana
lysis/SRR161XXXX.out/ > /mnt/projects/yanj/hcc/HPV.VISP/Analysis/SRR1611084.log.txt
echo SRR161XXXXOK>SRR161XXXX.ok'->jpb_visp_SRR161XXXX.sh
    '''
    
'''
qsub -cwd -pe OpenMP 20 -l mem_free=32G,h_rt=10:0:0 /mnt/projects/yanj/hcc/
HPV.VISP/jobFile/job_visp_SRR161XXXX.sh
'''
fileList = '/mnt/projects/yanj/hcc/HPV.VISP/hpv.file.list.txt'
#fileList = 'hpv.file.list.txt'

flist = open(fileList, 'r')
submitf = open('/mnt/projects/yanj/hcc/HPV.VISP/jobFile/toSubmit.sh', 'w')
linecount = 0
for line in flist:
    linecount += 1
    if linecount%2 ==1:
        sampleNM = line.rstrip().split('/')[-1].split('.')[0].split('_')[0]
        print sampleNM
        string1 = 'time java -XX:+UseSerialGC -cp "/mnt/projects/guanp/hcc/HBV/visp'\
        '.20151230.jar:/mnt/projects/guanp/hcc/HBV/lib/*" -Xms8g -Xmx32g visp.VISP '\
        '/mnt/projects/yanj/hcc/HPV.VISP/vispcfgFile/visp.HPV.cfg '\
        '/mnt/projects/yanj/hcc/HPV.VISP/samplecfgFile/visp.samples.'+sampleNM+'.cfg '\
        '/mnt/projects/yanj/hcc/HPV.VISP/Analysis/'+sampleNM+'.out/ > '\
        '/mnt/projects/yanj/hcc/HPV.VISP/Analysis/'+sampleNM+'.log.txt\n'
        
        string2 = 'echo '+sampleNM+'OK >'+sampleNM+'.ok'
        
        string3 = 'qsub -cwd -pe OpenMP 20 -l mem_free=32G,h_rt=10:0:0 '\
        '/mnt/projects/yanj/hcc/HPV.VISP/jobFile/job_visp_'+sampleNM+'.sh\n'
        
        jobf = open('/mnt/projects/yanj/hcc/HPV.VISP/jobFile/job_visp_'+sampleNM+'.sh', 'w')
        jobf.write(string1)
        jobf.write(string2)
        jobf.close()
        
        submitf.write(string3)


flist.close()    
submitf.close()



   