# -*- coding: utf-8 -*-
"""
this script is for study the distribution of BP
Created on Wed Feb 10 10:03:30 2016

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
N_filelist, T_filelist = fs.sepNT(filelist)
#fs.countBP(N_filelist, T_filelist, bpFilePath)
rawData, N_raw, T_raw = [], [], []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)

for f in N_filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    N_raw.extend(data)

for f in T_filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    T_raw.extend(data)


###############################################################################   
#%% 819 integrations   
print 'originally, there are {} integrations'.format(len(rawData))
filteredData = fs.excludeLowPE_v2(rawData, 1) # pls change the threshold
print 'after removing PE=1 integrations, {} are left.'.format(len(filteredData))
fs.plusMinusHist(filteredData,'819inte_')

print 'originally, there are {} integrations in Normal group'.format(len(N_raw))
filteredData_N = fs.excludeLowPE_v2(N_raw, 1) # pls change the threshold
print 'after removing PE=1 integrations, {} are left.'.format(len(filteredData_N))
fs.plusMinusHist(filteredData_N,'819inte_N_')

print 'originally, there are {} integrations'.format(len(T_raw))
filteredData_T = fs.excludeLowPE_v2(T_raw, 1) # pls change the threshold
print 'after removing PE=1 integrations, {} are left.'.format(len(filteredData_T))
fs.plusMinusHist(filteredData_T,'819inte_T_')


#%% 375 integrations
#rawData_filtered, seqResult_filtered = fs.theBigFilter(HBV_refName, hg_refName, rawData, 100)    
#fs.plusMinusHist(rawData_filtered,'375inte_')

#fs.writeExcelBPList(rawData_filtered, 'rawBP')    
#fs.repeatBP(rawData_filtered, 'rawBP')
#
#fs.writeBed(rawData_filtered, 'rawdata_hg.bed', 'rawdata_hbv.bed')
#print 'finish filter data...'
#N_rawData, T_rawData = fs.sepNTRawData(rawData_filtered)
#print len(N_rawData), len(T_rawData)
#fs.scatterPlot_PEvsBPlocation2group(T_rawData, N_rawData, 'tumor', 'normal','PEshortSeq')

