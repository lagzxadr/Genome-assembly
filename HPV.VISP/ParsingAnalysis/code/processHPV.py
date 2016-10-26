# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 10:37:54 2016

@author: yanj
processing HPV data
"""
import parseVispOutput as pv
import writeFile as wf


path =  '/mnt/projects/yanj/hcc/HPV.VISP/ParsingAnalysis/bpFiles/'  
parser = pv.parseVispOutput(path)     
parser.getAllData()
sortedData = parser.sortPE()[:4000]
print 'After selecting 4000 integrations:'
print 'the highest PE: ', sortedData[0]['PairedReadsCountWithPCRDup']
print 'the lowest PE: ', sortedData[-1]['PairedReadsCountWithPCRDup']
wf.writeBPLixt2txt(sortedData, 'tomergeHPVresult')
