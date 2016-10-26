#!/mnt/software/unstowable/anaconda/bin/python
"""
this script is for study the distribution of BP
Created on Wed Feb 10 10:03:30 2016

@author: yanj
"""

import funcSum as fs
import os

writeBPList = True
writeRecurrentBPList = False
###############################################################################
bpFilePath = '/mnt/projects/yanj/hcc/hccVISPNC_003977.2015.12.29/bpFiles/'

filelist = os.listdir(bpFilePath)
filelist.sort() ##sort
HBV_refName = '/mnt/projects/yanj/hcc/reference/NC_003977/NC_003977.fa'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
#1. extract data
N_filelist, T_filelist = fs.sepNT(filelist)
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)
    
#rawData_filtered = rawData
rawData_filtered = fs.excludeLowPE_v2(rawData, 1) 
#rawData_filtered, seqResult_filtered = fs.theSmallFilter(HBV_refName, hg_refName, rawData, 100)  
print 'finish filter  PE > 1 integrations...'  
print '{} integrations with PE > 1 are for analysis...'.format(len(rawData_filtered))

if writeBPList: 
    fs.writeExcelBPList(rawData_filtered, 'rawBPforHomer')    
if writeRecurrentBPList: 
    fs.repeatBP(rawData_filtered, 'rawBPforHomer')
###############################################################################    
    
hgbedFileName = 'hg4homer.bed'
hbvbedFileName = 'hbv4homer.bed'
fs.writeBed(rawData_filtered, hgbedFileName, hbvbedFileName)
print 'finish write bed...'

from subprocess import call 
command_line1 = 'annotatePeaks.pl ' + hgbedFileName + \
        ' hg19 -annStats annHgStats.txt > annHgOutput.txt'
call(command_line1, shell = True)

#
#command_line2 = 'annotatePeaks.pl ' + hbvbedFileName + \
#        ' /mnt/projects/yanj/hcc/hccVISPNC_003977.2015.12.29/annotation/tracks/HBV.bed '\
#        '-annStats annHbvStats.txt > annHbvOutput.txt'
#call(command_line2, shell = True)   
print 'finish annotating...'

############################################################################### 
#writ the annotation result to CSV 
import csv
from operator import itemgetter
ann2write = []
annHg = open('annHgOutput.txt', 'r')
with open('annHgOutput.csv','wb') as outF:
    a = csv.writer(outF,delimiter = ',')
    for line in annHg:
        if line.startswith('PeakID'):
            col = line.rstrip().split('\t')
            del col[0]
            col.insert(0, '#withinID')
            col.insert(0, 'sampleID')
            a.writerows([col])
        else:
            col = line.rstrip().split('\t')
            sampleID = col[0].split('-')
            del col [0]
            col.insert(0, int(sampleID[1]))
            col.insert(0, sampleID[0])
            #col[0] and col[16] are sample ID and gene name
            
            ann2write.append(col)
    sortedann2write = sorted(ann2write, key = itemgetter(0,1), reverse = False)
    a.writerows(sortedann2write)            
annHg.close()
print 'finish writing annotation result to csv...'
###############################################################################
from collections import defaultdict

    
tempData = [(dataEntry[0],dataEntry[16]) for dataEntry in sortedann2write if \
            len(dataEntry) == 20]
            
            
tally = defaultdict(list)
for (sampleID, geneName) in tempData:
    tally[geneName].append(sampleID)
result = [[key, sorted(set(sampleID)), len(set(sampleID))] for key, sampleID in tally.items()]
resultSorted = sorted(result, key = itemgetter(2,0), reverse = True) #sort on sample numver and genename
with open('recurrentGene.csv', 'wb') as outF:
    a = csv.writer(outF,delimiter = ',') 
    a.writerows([['geneName','sampleID', 'totalSample']]) 
    for rcGene in resultSorted:
        a.writerows([[rcGene[0],' '.join(rcGene[1]), rcGene[2]]])
print 'finish writing recurrentGene.csv file...'
    
    
    
#def repeatBP(rawData, excelprifix = ''):
#    from collections import defaultdict
#    import csv
#    requiredData = [('.').join(dataEntry[:5]) for dataEntry in rawData]
#    tally = defaultdict(list)
#    for i, e in enumerate(requiredData):
#        tally[e].append(rawData[i][9])
#    result = ((key, locs) for key, locs in tally.items() if len(locs)>1 )
#    with open(excelprifix+'_recurrentBP.csv', 'wb') as outF:
#        a = csv.writer(outF,delimiter = ',') 
#        a.writerows([['HBV strand','HBV position',\
#        'hg chr', 'hg strand', 'hg pos', 'sampleIDs']])   
#        for dup in result:
#            print dup
#            BPposition = dup[0].split('.')
#            BPposition.extend(dup[1])
#            a.writerows([BPposition]) 
#    return