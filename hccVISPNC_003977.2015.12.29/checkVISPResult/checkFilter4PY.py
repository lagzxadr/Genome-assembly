# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:21:30 2016
test engBP integration
@author: yanj
"""

import funcSum as fs
import os
import random
writeAllSeq = False
writeAllShortSeq = False
writeFalseShortSeq = False
writeSuspiciousShortSeq = False
writeLeftShortSeq = False
writeHighMuSeq = True
###############################################################################
bpFilePath = '/mnt/projects/yanj/hcc/hccVISPNC_003977.2015.12.29/bpFiles/'
filelist = os.listdir(bpFilePath)
filelist.sort()
print 'totlly read {} files...'.format(len(filelist))
###############################################################################

#1. extract data
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)    
print 'totlly get {} integrations...'.format(len(rawData))
###############################################################################

HBV_refName = '/mnt/projects/yanj/hcc/reference/NC_003977/NC_003977.fa'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
fl = 500 # flanking region length
seqResult = fs.extractRefSeq(HBV_refName, hg_refName, rawData, fl)
seqResultSorted = fs.sortPECount(seqResult)

if writeAllSeq == True: #write all the files to excel
    fs.writeSeq2Csv(str(len(seqResultSorted))+'allBP.csv', seqResultSorted)
    colorList = fs.excelLocation(seqResultSorted, fl)
    fs.writeColorTxt(colorList, str(len(rawData))+'integrations')

#find the short seq
shortSeqList = fs.shortSeqFilter(seqResultSorted, fl) 
shortSeqdataSorted = [seqResultSorted[i] for i in shortSeqList]

otherSeqList = list(set(range(len(seqResultSorted)))-set(shortSeqList))
otherSeq = [seqResultSorted[i] for i in otherSeqList]

if writeAllShortSeq == True: # wite the shortseq to csv
    fs.writeSeq2Csv(str(len(shortSeqdataSorted))+'shortSeqBP.csv', shortSeqdataSorted)
    colorList = fs.excelLocation(shortSeqdataSorted, fl)
    fs.writeColorTxt(colorList, str(len(shortSeqdataSorted))+'integrations')
print '{} integrations are short sequence...'.format(len(shortSeqList))    
###############################################################################    
#find high MH short seq
MHList, MHrate = fs.checkMH_debugmode(shortSeqdataSorted, fl) 
wrongList1, leftList1 = [], []
for i in range(len(MHrate)):
    if MHrate[i][1] >= MHrate[i][0] or MHrate[i][2] >= MHrate[i][3]:
#        print '#{}'.format(i+1)
#        print MHrate[i]
        wrongList1.append(i)
    else:
#        print MHrate[i]
        leftList1.append(i)
wrongSeqdata1 = [shortSeqdataSorted[i] for i in wrongList1]

if writeFalseShortSeq == True: ## wite the wrongseq to csv
    fs.writeSeq2Csv(str(len(wrongSeqdata1))+'FalseSeq.csv', wrongSeqdata1)
    colorList = fs.excelLocation(wrongSeqdata1, fl)
    fs.writeColorTxt(colorList, str(len(wrongSeqdata1))+'integrations')
print 'totally {} integrations are false...'.format(len(wrongSeqdata1))
print '    reason: hbvMH > hbvSimilarity or hgMH > hgSimilarity'
print '    example: {}'.format(MHrate[random.choice(wrongList1)])
###############################################################################
wrongList2, leftList2 = [], []
for i in leftList1:
    if MHrate[i][1]> 0.5 or MHrate[i][2] > 0.5:
#        print MHrate[i]
        wrongList2.append(i)
    else:
        leftList2.append(i)
wrongSeqdata2 = [shortSeqdataSorted[i] for i in wrongList2]
leftSeqdata2 = [shortSeqdataSorted[i] for i in leftList2]

if writeSuspiciousShortSeq == True: # wite the suspiciousseq to csv
    fs.writeSeq2Csv(str(len(wrongSeqdata2))+'SuspiciousSeq.csv', wrongSeqdata2)
    colorList = fs.excelLocation(wrongSeqdata2, fl)
    fs.writeColorTxt(colorList, str(len(wrongSeqdata2))+'integrations')

if writeLeftShortSeq == True: # wite the leftseq to csv
    fs.writeSeq2Csv(str(len(leftSeqdata2))+'LeftSeq.csv', leftSeqdata2)
    colorList = fs.excelLocation(leftSeqdata2, fl)
    fs.writeColorTxt(colorList, str(len(leftSeqdata2))+'integrations')       

print 'totally {} integration are suspicious...'.format(len(wrongSeqdata2))
print '    reason: hbvMH > 0.5 or hgMH > 0.5'
print '    example: {}'.format(MHrate[random.choice(wrongList2)])
print '****'
print 'totally {} integration are left....'.format(len(leftSeqdata2))   
###############################################################################

mutationLists = fs. checkMutation(otherSeq, fl) 
print 'totally {} integration for Mu check...'.format(len(otherSeq))
mutationCount = fs. quantifyMutation(mutationLists)
highMuList = fs. highMutationFilter(mutationCount, fl) 
highMuSeqdata = [otherSeq[i] for i in highMuList]

if writeHighMuSeq == True: # wite the shortseq to csv
    fs.writeSeq2Csv(str(len(highMuSeqdata))+'highMuBP.csv', highMuSeqdata)
    colorList = fs.excelLocation(highMuSeqdata, fl)
    fs.writeColorTxt(colorList, str(len(highMuSeqdata))+'integrations')
print '{} integrations are highMutation sequence...'.format(len(highMuSeqdata)) 


 
##rawData = fs.excludeLowPE(rawData, 1)
##print 'after excludeLowPE', len(rawData)
#rawData, excludeData = fs.excludeEndBP(rawData)
##print 'after excludeEndBP', len(rawData)
#
#
#seqResult = fs.extractRefSeq(HBV_refName, hg_refName, excludeData,fl)
#sortedSeqResult = fs.sortPECount(seqResult)
#
#
#fs.writeSeq2Csv('EndBP.csv', sortedSeqResult)
#locations = fs.excelLocation(sortedSeqResult, fl)
       