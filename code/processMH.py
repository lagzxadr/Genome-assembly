# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:42:53 2016
this file batch process all the data from Peiyong
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
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)    
N_rawData = [] #normal sample
for f in N_filelist: 
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    N_rawData.extend(data)
   
T_rawData = [] #tumor sample
for f in T_filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    T_rawData.extend(data) 
    
includeList, notincludeList, include = fs.checkInclusive(T_rawData, N_rawData, False)

#2. filter data
#rawData, seqResult = fs.theBigFilter(HBV_refName, hg_refName, rawData, 100)    
#N_rawData, N_seqResult = fs.theBigFilter(HBV_refName, hg_refName, N_rawData, 100)
#T_rawData, T_seqResult = fs.theBigFilter(HBV_refName, hg_refName, T_rawData, 100)
S_rawData, S_seqResult = fs.theBigFilter(HBV_refName, hg_refName, notincludeList, 100)
NS_rawData, NS_seqResult = fs.theBigFilter(HBV_refName, hg_refName, T_rawData, 100)
print 'finish filter data...'   
#3. sort` data
#all_sortedSeqResult = fs.sortPECount(seqResult)
#N_sortedSeqResult = fs.sortPECount(N_seqResult)
#T_sortedSeqResult = fs.sortPECount(T_seqResult)
S_sortedSeqResult = fs.sortPECount(S_seqResult)
NS_sortedSeqResult = fs.sortPECount(NS_seqResult)
print 'finish sort data...'
#
#includeList, notincludeList, include = fs.checkInclusive(T_rawData, N_rawData, False)
#print len(includeList), ' BP are included in Tumor group'
#print len(notincludeList), ' BP are somatic'
#print len(S_rawData), len(NS_rawData)
##fs.plusMinusHist(NS_rawData, 'nonSomatic_')
#fs.plusMinusHist(S_rawData, 'somatic_')
#4. check if any duplite
S_uniqueintegration = fs.uniqueBP(S_rawData)
print 'Is there any dupli in N_group?-> ', len(S_rawData) > len(S_uniqueintegration)
print len(S_rawData), len(S_uniqueintegration)
NS_uniqueintegration = fs.uniqueBP(NS_rawData)
print 'Is there any dupli in T_group?-> ', len(NS_rawData) > len(NS_uniqueintegration)
print len(NS_rawData), len(NS_uniqueintegration)

#5. write to excel
#fs.writeSeq2Csv('allSampleBP.csv', all_sortedSeqResult)
#fs.writeSeq2Csv('normalSampleBP.csv', N_sortedSeqResult)
#fs.writeSeq2Csv('tumorSampleBP.csv', T_sortedSeqResult)
fs.writeSeq2Csv('nonsomaticSampleBP.csv', NS_seqResult)
fs.writeSeq2Csv('somaicSampleBP.csv', S_seqResult)

#4 excel color issue
#all_colorList = fs.excelLocation(all_sortedSeqResult, 100)
#fs.writeColorTxt(all_colorList, 'all_')
#N_colorList = fs.excelLocation(N_sortedSeqResult, 100)
#fs.writeColorTxt(N_colorList, 'N_')
#T_colorList = fs.excelLocation(T_sortedSeqResult, 100)
#fs.writeColorTxt(T_colorList, 'T_')

NS_colorList = fs.excelLocation(NS_seqResult, 100)
fs.writeColorTxt(NS_colorList, 'NS_')
S_colorList = fs.excelLocation(S_seqResult, 100)
fs.writeColorTxt(S_colorList, 'S_')                                
#5. plusminus distribution
#fs.plusMinusHist(rawData, 'all_')
#fs.plusMinusHist(N_rawData, 'normal_')
#fs.plusMinusHist(T_rawData, 'tumor_')


##6. mutation rate
#muLists = fs.checkMutation(N_sortedSeqResult)
#muC = fs.quantifyMutation(muLists)
##6.1 plot the figure of mutation rate
#hbvMuperc, hgMuperc =  fs.mutationPerc(muC, N_sortedSeqResult, 100)
#fs. plotMutationBar(hbvMuperc, hgMuperc, 'normal_mutationRate.png')
#
#muLists = fs.checkMutation(T_sortedSeqResult)
#muC = fs.quantifyMutation(muLists)
##6.1 plot the figure of mutation rate
#hbvMuperc, hgMuperc =  fs.mutationPerc(muC, T_sortedSeqResult, 100)
#fs. plotMutationBar(hbvMuperc, hgMuperc, 'tumor_mutationRate.png')
#

#mhonInte,inteCount = fs.assemblyData(N_sortedSeqResult, 100)
#mhonInteP = fs.chisquareTest(mhonInte,37)
#inteCountP = fs.chisquareTest(inteCount,37)
#fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,'numMHonInte.png')
#fs.Barplot_3samples_InteC(inteCount,inteCountP,'inteCount.png')
#print mhonInte
#print mhonInteP
#print
#print inteCount
#print inteCountP
#print 
#print
#mhonInte,inteCount = fs.assemblyData(T_sortedSeqResult, 100)
#mhonInteP = fs.chisquareTest(mhonInte,267)
#inteCountP = fs.chisquareTest(inteCount,267)
#print mhonInte
#print mhonInteP
#print
#print inteCount
#print inteCountP
#print
#print
#mhonInte,inteCount = fs.assemblyData(all_sortedSeqResult, 100)
#mhonInteP = fs.chisquareTest(mhonInte,375)
#inteCountP = fs.chisquareTest(inteCount,375)
#print mhonInte
#print mhonInteP
#print
#print inteCount
#print inteCountP
#print
#print

#==============================================================================
# #7. varying flanking region MH
# flk = [10,20,30]
# #for f in flk:    
# #    N_cutAlnResult = fs.cutSeq(N_sortedSeqResult,f) # cut the result into certain flanking region
# #    mhonInte,inteCount = fs.assemblyData(N_cutAlnResult, f)
# #    mhonInteP = fs.chisquareTest(mhonInte,37)
# #    inteCountP = fs.chisquareTest(inteCount,37)
# #    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_normal_numMHonInte.png')
# #    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_normal_inteCount.png')
# #    '''0.8,0.4   2,1'''
# #for f in flk:    
# #    T_cutAlnResult = fs.cutSeq(T_sortedSeqResult,f) # cut the result into certain flanking region
# #    mhonInte,inteCount = fs.assemblyData(T_cutAlnResult, f)
# #    mhonInteP = fs.chisquareTest(mhonInte,267)
# #    inteCountP = fs.chisquareTest(inteCount,267)
# #    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_tumor_numMHonInte.png')
# #    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_tumor_inteCount.png')
# #    '''5,2.5   16,8'''
# #important figure
# for f in flk:    
#     all_cutAlnResult = fs.cutSeq(all_sortedSeqResult,f) # cut the result into certain flanking region
#     mhonInte,inteCount = fs.assemblyData(all_cutAlnResult, f)
#     mhonInteP = fs.chisquareTest(mhonInte,len(all_sortedSeqResult))
#     inteCountP = fs.chisquareTest(inteCount,len(all_sortedSeqResult))
#     print 'fl = ', f
#     print mhonInte, mhonInteP
#     print
#     print inteCount, inteCountP
#     print
#     print
#     fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_all_numMHonInte.png')
#     fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_all_inteCount.png')
#     '''7,3.5   20,10'''
# 
#==============================================================================
#fs.inteCvsFlanklen(all_sortedSeqResult)
#==============================================================================
# # left/right side MH
# flk = [5,10,20,30]
# for f in flk:
#     all_cutAlnResult = fs.cutSeq(all_seqResult,f) # cut the result into certain flanking region
#     hbv_data,hg_data = fs.assemblyData_hbvhg(all_cutAlnResult, f)
#     hbv_mhonInteP = fs.chisquareTest(hbv_data[0],304)
#     hg_mhonInteP = fs.chisquareTest(hg_data[0],304)
# 
#     hbv_inteCountP = fs.chisquareTest(hbv_data[1],304)
#     hg_inteCountP = fs.chisquareTest(hg_data[1],304)
#     
#     fs.Barplot_3samples_mhonInteC(hbv_data[0], hbv_mhonInteP,str(f)+'hbv_all_numMHonInte.png')
#     fs.Barplot_3samples_mhonInteC(hg_data[0], hg_mhonInteP,str(f)+'hg_all_numMHonInte.png')
#     fs.Barplot_3samples_InteC(hbv_data[1], hbv_inteCountP,str(f)+'hbv_all_inteCount.png')
#     fs.Barplot_3samples_InteC(hg_data[1], hg_inteCountP,str(f)+'hg_all_inteCounte.png')
# 
# 
#==============================================================================
#