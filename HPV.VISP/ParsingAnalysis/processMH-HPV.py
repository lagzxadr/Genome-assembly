# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:42:53 2016
this file batch process all the data from Peiyong
@author: yanj
"""

import funcSumHPV as fs
import os

bpFilePath = os.getcwd()+'/bpFiles/'

filelist = os.listdir(bpFilePath)
filelist.sort()
HPV_refName = '/mnt/projects/yanj/hcc/reference/HPV/HPVdb.fasta'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
fl = 50
#1. extract data
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractVISPInfo(bpFileName)
    rawData.extend(data)
    
#print '{} integrations are extracted...'.format(len(rawData)) 
print '{} integrations with PE> 1 and SP != 0 for MH analysis...'.format(len(rawData))    
###############################################################################\

    
    
    
#==============================================================================
#     

# #rawData_bigFilter, seqResult = fs.theBigFilter(HPV_refName, hg_refName, rawData, fl) 
# 
# ##step1-> filter short exp seq
# excludeList1 = fs.shortSeqFilter_v2(rawData_filtered, fl) 
# rawData1 = fs.filterData(rawData_filtered,excludeList1)
# print '{} integrations left after removing short Seq...'.format(len(rawData1))
# 
# '''
# samtools faidx HPVdb.fasta "gi|13507120|gb|AF293961.1|HPV82":6991-7101
# '''
# 
# rawData_bigFilter, seqResult = fs.theBigFilter(HPV_refName, hg_refName, rawData1, fl) 
#==============================================================================

#print 'Initially {} integrations...'. format(len(rawData))
#rawData = fs.uniqueBP(rawData)
#print 'After removing repeate integration, there are {} integrations left...'.format(len(rawData))


#rawData = excludeLowPE(rawData, 1) # pls change the threshold
#print 'After removing PE = 1 and Spr = 0 integration, there are {} integrations left...'.format(len(rawData))
##extract the sequence
#seqResult =  extractRefSeq(HPV_refName, hg_refName, rawData, flankLen)

#print 'After removing short sequence, there are {} integrations left...'.format(len(rawData1))
##step2-> filter mutation rate > 50%
#mutationLists = checkMutation(seqResult1) 
#mutationCount = quantifyMutation(mutationLists)
#excludeList2 = highMutationFilter(mutationCount) 
#seqResult2 = filterData(seqResult1, excludeList2)
#rawData2 = filterData(rawData1,excludeList2)
#print 'After removing high mutation sequence, there are {} integrations left...'.format(len(rawData2))
##step3-> filter mh rate > 50%
#mhLists,_ = checkMH(seqResult2)
#mhCount = quantifyMH(mhLists)
#excludeList3 = highMHFilter(mhCount)
#seqResult3 = filterData(seqResult2, excludeList3)
#rawData3 = filterData(rawData2, excludeList3)  
#print 'After removing high MH sequence, there are {} integrations left...'.format(len(rawData3))
#excludeList4 = NatBPFilter(seqResult3)
#seqResult_filtered = filterData(seqResult3, excludeList4)
#rawData_filtered = filterData(rawData3, excludeList4) 
#print 'After removing "N" at human refseq integrations, there are {} integrations left..s.'.format(len(rawData3))   

#==============================================================================
# 
# 
# includeList, notincludeList, include = fs.checkInclusive(T_rawData, N_rawData, False)
# fs.scatterPlot_PEvsBPlocation2group(T_rawData, notincludeList, 'non-somatic', 'somatic','raw_')
# 
# #2. filter data
# #N_rawData, N_seqResult = fs.theBigFilter(HBV_refName, hg_refName, N_rawData, 100)
# #T_rawData, T_seqResult = fs.theBigFilter(HBV_refName, hg_refName, T_rawData, 100)
# S_rawData, S_seqResult = fs.theBigFilter(HBV_refName, hg_refName, notincludeList, 100)
# NS_rawData, NS_seqResult = fs.theBigFilter(HBV_refName, hg_refName, T_rawData, 100)
# print 'finish filter data...'   
# #3. sort` data
# #all_sortedSeqResult = fs.sortPECount(seqResult)
# #N_sortedSeqResult = fs.sortPECount(N_seqResult)
# #T_sortedSeqResult = fs.sortPECount(T_seqResult)
# #S_sortedSeqResult = fs.sortPECount(S_seqResult)
# #NS_sortedSeqResult = fs.sortPECount(NS_seqResult)
# #print 'finish sort data...'
# #fs.scatterPlot_PEvsBPlocation(rawData, 'all_')
# fs.scatterPlot_PEvsBPlocation2group(NS_rawData, S_rawData, 'non-somatic', 'somatic','afterFilter_')
# sortedData = fs.sortPEonRawData(rawData)
# print 'result: '
# for i in range(10):
#     print sortedData[i]
#==============================================================================
#
#includeList, notincludeList, include = fs.checkInclusive(T_rawData, N_rawData, False)
#print len(includeList), ' BP are included in Tumor group'
#print len(notincludeList), ' BP are somatic'
#print len(S_rawData), len(NS_rawData)
##fs.plusMinusHist(NS_rawData, 'nonSomatic_')
#fs.plusMinusHist(S_rawData, 'somatic_')
#4. check if any duplite
#S_uniqueintegration = fs.uniqueBP(S_rawData)
#print 'Is there any dupli in N_group?-> ', len(S_rawData) > len(S_uniqueintegration)
#print len(S_rawData), len(S_uniqueintegration)
#NS_uniqueintegration = fs.uniqueBP(NS_rawData)
#print 'Is there any dupli in T_group?-> ', len(NS_rawData) > len(NS_uniqueintegration)
#print len(NS_rawData), len(NS_uniqueintegration)

#5. write to excel
#fs.writeSeq2Csv('allSampleBP.csv', all_sortedSeqResult)
#fs.writeSeq2Csv('normalSampleBP.csv', N_sortedSeqResult)
#fs.writeSeq2Csv('tumorSampleBP.csv', T_sortedSeqResult)
#fs.writeSeq2Csv('nonsomaticSampleBP.csv', NS_sortedSeqResult)
#fs.writeSeq2Csv('somaicSampleBP.csv', S_sortedSeqResult)

#4 excel color issue
#all_colorList = fs.excelLocation(all_sortedSeqResult, 100)
#fs.writeColorTxt(all_colorList, 'all_')
#N_colorList = fs.excelLocation(N_sortedSeqResult, 100)
#fs.writeColorTxt(N_colorList, 'N_')
#T_colorList = fs.excelLocation(T_sortedSeqResult, 100)
#fs.writeColorTxt(T_colorList, 'T_')

#NS_colorList = fs.excelLocation(NS_sortedSeqResult, 100)
#fs.writeColorTxt(NS_colorList, 'NS_')
#S_colorList = fs.excelLocation(S_sortedSeqResult, 100)
#fs.writeColorTxt(S_colorList, 'S_')                                
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

#important figure
#7. varying flanking region MH
#flk = [10,20,30]
#for f in flk:    
#    S_cutAlnResult = fs.cutSeq(S_sortedSeqResult,f) # cut the result into certain flanking region
#    mhonInte,inteCount = fs.assemblyData(S_cutAlnResult, f)
#    mhonInteP = fs.chisquareTest(mhonInte,82)
#    inteCountP = fs.chisquareTest(inteCount,82)
#    print 'fl = ', f
#    print mhonInte, mhonInteP
#    print
#    print inteCount, inteCountP
#    print
#    print
#    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_somatic_numMHonInte.png')
#    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_sormatic_inteCount.png')
#    '''0.8,0.4   2,1'''
#for f in flk:    
#    NS_cutAlnResult = fs.cutSeq(NS_sortedSeqResult,f) # cut the result into certain flanking region
#    mhonInte,inteCount = fs.assemblyData(NS_cutAlnResult, f)
#    mhonInteP = fs.chisquareTest(mhonInte,294)
#    inteCountP = fs.chisquareTest(inteCount,294)
#    print 'fl = ', f
#    print mhonInte, mhonInteP
#    print
#    print inteCount, inteCountP
#    print
#    print
#    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_nonSomatic_numMHonInte.png')
#    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_nonSomatic_inteCount.png')
#    '''5,2.5   16,8'''

#for f in flk:    
#    all_cutAlnResult = fs.cutSeq(all_sortedSeqResult,f) # cut the result into certain flanking region
#    mhonInte,inteCount = fs.assemblyData(all_cutAlnResult, f)
#    mhonInteP = fs.chisquareTest(mhonInte,len(all_sortedSeqResult))
#    inteCountP = fs.chisquareTest(inteCount,len(all_sortedSeqResult))
#    print 'fl = ', f
#    print mhonInte, mhonInteP
#    print
#    print inteCount, inteCountP
#    print
#    print
#    fs.Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_all_numMHonInte.png')
#    fs.Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_all_inteCount.png')
#    '''7,3.5   20,10'''

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

