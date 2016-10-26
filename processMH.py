# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:42:53 2016
this file batch process all the data from Peiyong
@author: yanj
"""

import funcSum as fs
import os

bpFilePath = os.getcwd()+'/bpFiles'
csvFilePath = os.getcwd()+'/csvFiles'
filelist = os.listdir(bpFilePath)
HBV_refName = '/home/yanj/AHLtest/reference/NC_003977/NC_003977.fa'
hg_refName = '/home/yanj/AHLtest/reference/human_g1k/human_g1k_v37.fasta'
#1. extract data
rawData = []
count = 0
for f in filelist:
    bpFileName = bpFilePath + '/' + f
    csvFileName = csvFilePath + '/' + f[:-2] + 'csv'
    fs.readVISPOutput(bpFileName, csvFileName)
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16])
    rawData.extend(data)
    
#2. filter data
rawData, excludedData = fs.excludeEndBP(rawData) # filter the BP close the start/end
seqResult = fs.extractRefSeq(HBV_refName, hg_refName, rawData)

excludeList1 = fs.shortSeqFilter(seqResult, 100) # filter short exp seq
seqResult = fs.filterData(seqResult,excludeList1)
rawData = fs.filterData(rawData,excludeList1)
# 
mutationLists = fs.checkMutation(seqResult) # filter mutation rate > 50%
mutationCount = fs.quantifyMutation(mutationLists)
excludeList2 = fs.highMutationFilter(mutationCount) 
seqResult = fs.filterData(seqResult, excludeList2)
rawData = fs.filterData(rawData,excludeList2)
#
mhLists = fs.checkMH(seqResult)
mhCount = fs.quantifyMH(mhLists)
excludeList3 = fs.highMHFilter(mhCount)
seqResult = fs.filterData(seqResult, excludeList3)
rawData = fs.filterData(rawData, excludeList3)

#3. sort data
sortedSeqResult = fs.sortPECount(seqResult)

#==============================================================================
# print len(sortedSeqResult)
# 
# uniqueintegration = fs.uniqueBP(rawData)
# print len(rawData)
# print len(uniqueintegration)
#==============================================================================
#==============================================================================
# #4. write to excel
# fs.writeSeq2Csv('88sampleIntegration_filter.csv', sortedSeqResult)
# #4 excel color issue
# muLists = fs.checkMutation(sortedSeqResult)
# mhLists = fs.checkMH(sortedSeqResult)
# blueLoc, redLoc = fs.excelLocation(muLists, mhLists)
# with open('blueList.txt','w') as bluef:
#     for blue in blueLoc:
#         bluef.writelines(str(blue)+'\n')
# with open('redList.txt','w') as redf:
#     for red in redLoc:
#         redf.writelines(str(red)+'\n')
# setExcelColor('blueList.txt','redList.txt')
#==============================================================================
        
#==============================================================================
# #5. plusminus distribution
# fs.plusMinusHist(rawData)
# 
# #6. mutation rate
# muLists = fs.checkMutation(sortedSeqResult)
# muC = fs.quantifyMutation(muLists)
# #6.1 plot the figure of mutation rate
# hbvMuperc, hgMuperc =  fs.mutationPerc(muC, sortedSeqResult, 100)
# fs. plotMutationBar(hbvMuperc, hgMuperc, 'mutationRate.png')
#==============================================================================

#==============================================================================
# mhonInte,inteCount = fs.assemblyData(sortedSeqResult, 100)
# mhonInteP = fs.chisquareTest(mhonInte,731)
# inteCountP = fs.chisquareTest(inteCount,731)
# fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,'numMHonInte.png')
# fs.Barplot_3samples_InteC(inteCount,inteCountP,'inteCount.png')
# print mhonInte
# print mhonInteP
# print
# print
# print inteCount
# print inteCountP
# 
#==============================================================================

#7. varying flanking region MH
flk = [20,30,40,50]
for f in flk:    
    cutAlnResult = fs.cutSeq(sortedSeqResult,f) # cut the result into certain flanking region
    mhonInte,inteCount = fs.assemblyData(cutAlnResult, f)
    mhonInteP = fs.chisquareTest(mhonInte,731)
    inteCountP = fs.chisquareTest(inteCount,731)
    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_numMHonInte.png')
    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_inteCount.png')
