# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 10:10:58 2016

@author: yanj
"""
import csv
from operator import itemgetter

def writeBPList2csv(rawData, csvName):
    '''this function write the BP location into a csv'''
    tmpData = sorted(rawData, key = itemgetter('sampleID', 'ChromosomeNameHuman',\
    'PositionHuman'))            
    with open(csvName + '.csv','wb') as outF:
        a = csv.writer(outF,delimiter = ',') 
        a.writerows([['sampleID', '#withinID','hg chr', 'hg strand', 'hg pos',\
        'virusType','HBV strand','HBV position','PEcount','Splitread']])

        sampleID = '*'
        for data in tmpData:
            if sampleID != data['sampleID']:
                count = 0
            sampleID = data['sampleID']
            count += 1
            a.writerow([sampleID, count, \
            data['ChromosomeNameHuman'], \
            data ['StrandHuman'], data['PositionHuman'],\
            data['ChromosomeNameVirus'].split('|')[-1],\
            data['StrandVirus'], data['PositionVirus'], \
            data['PairedReadsCountWithPCRDup'], \
            data['SplitReadsCountWithPCRDup']])
                                
    return  
    
def writeBPLixt2txt(rawData, txtName):
    '''this function write the BP location into a txt, for comparison the 
    overlap between the visp result and the HPV paper'''
    tmpData = sorted(rawData, key = itemgetter('sampleID', 'ChromosomeNameHuman',\
    'PositionHuman')) 
    with open(txtName, 'w') as outF:
        sampleID = '*'
        for data in tmpData:
            if sampleID != data['sampleID']:
                count = 0
            sampleID = data['sampleID']
            count += 1
            
            str2write = data['sampleID'] + '\tchr' + \
            data['ChromosomeNameHuman']+'\t'\
            +'*\t'+str(data['PositionHuman'])+'\t'+str(count)+\
            '\t*\t*\t*\t*\t*\t*\t*\t*\t'+data['StrandHuman']+'\t'+\
             data['ChromosomeNameVirus'].split('|')[-1]+'\t'+\
             data['StrandVirus'] + '\t' + str(data['PositionVirus']) + '\t' + \
             str(data['PairedReadsCountWithPCRDup']) + '\t' + \
             str(data['SplitReadsCountWithPCRDup']) + '\n'

            
            outF.write(str2write)
            
    