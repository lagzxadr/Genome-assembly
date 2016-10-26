# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:21:30 2016
test engBP integration
@author: yanj
"""

import funcSum as fs
import os

bpFilePath = os.getcwd()+'/bpFiles/'

filelist = os.listdir(bpFilePath)
filelist.sort()
HBV_refName = '/mnt/projects/yanj/hcc/reference/NC_003977/NC_003977.fa'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
#1. extract data
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)    
#print len(rawData)
#rawData = fs.excludeLowPE(rawData, 1)
#print 'after excludeLowPE', len(rawData)
rawData, excludeData = fs.excludeEndBP(rawData)
#print 'after excludeEndBP', len(rawData)

fl = 1000
seqResult = fs.extractRefSeq(HBV_refName, hg_refName, excludeData,fl)
sortedSeqResult = fs.sortPECount(seqResult)


fs.writeSeq2Csv('EndBP.csv', sortedSeqResult)
locations = fs.excelLocation(sortedSeqResult, fl)
with open('blueList.txt','w') as bluef:
    for blue in locations[0]:
        bluef.writelines(str(blue)+'\n')
with open('redList.txt','w') as redf:
    for red in locations[1]:
        redf.writelines(str(red)+'\n')
with open('blackList.txt', 'w') as greyf:
    for grey in locations[2]:
        greyf.writelines(str(grey)+'\n')
with open('greyList.txt', 'w') as greyf:
    for grey in locations[3]:
        greyf.writelines(str(grey)+'\n')        