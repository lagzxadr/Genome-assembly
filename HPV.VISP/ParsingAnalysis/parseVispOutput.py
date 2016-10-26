#!/usr/bin/env python2.7
"""
Created on Mon Mar 07 14:31:54 2016

@author: yanj

real code for HPV
"""
import unicodecsv
import os
import csv
import numpy as np
from operator import itemgetter
class parseVispOutput:
    
    def __init__(self, bpFilepath):
        self.bpFilePath = bpFilepath
        self.HPV_refName = '/mnt/projects/yanj/hcc/reference/HPV/HPVdb.fasta'
        self.hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
        self.rawData = []
        self.peFreq = []
        
    def getAllData(self):       
        filelist = os.listdir(self.bpFilePath)
        filelist.sort()               
        for f in filelist:
            bpFileName = self.bpFilePath + f
            data,pe = self.extractVISPInfo(bpFileName)
            self.rawData.extend(data)
            self.peFreq.extend(pe)
        print '{} integrations with PE> 1 and SP != 0 are extracted for MH \
                analysis...'.format(len(self.rawData))  
                
    def extractVISPInfo(self, bpFileName):
        inteRes = []
        peFreq = []
        with open(bpFileName, 'r') as dataF, open(bpFileName+'.csv', 'wb') as outF:
            a = unicodecsv.writer(outF, delimiter = ',')
            for line in dataF:
                line = line.rstrip().split('\t')
                a.writerow(line)
                
        with open(bpFileName+'.csv','rb') as dataF:            
            sampleID = bpFileName.split('/')[-1].split('.')[0]
            reader = unicodecsv.DictReader(dataF)
            integrations = list(reader)
            for inte in integrations:
                inte['sampleID'] = sampleID
                inte['PositionVirus'] = int(inte['PositionVirus'])
                inte['PositionHuman'] = int(inte['PositionHuman'])
                inte['PairedReadsCountWithPCRDup'] = int(inte['PairedReadsCountWithPCRDup'])
                inte['SplitReadsCountWithPCRDup'] = int(inte['SplitReadsCountWithPCRDup'])
                if not (inte['PairedReadsCountWithPCRDup'] == 1 or \
                        inte['SplitReadsCountWithPCRDup'] == 0):
                    inteRes.append(inte) 
                    peFreq.append(inte['PairedReadsCountWithPCRDup'])
        os.remove(bpFileName+'.csv')
        return inteRes, peFreq
    
#    def getPeFreq(self):
#        self.getAllData()
#        x = np.array(self.peFreq)
#        b = np.linspace(1, np.max(x),100 )
#        hist, bin_edges = np.histogram(x, bins = b)
#        for (h, b) in zip(hist, bin_edges[:-1]):
#            print h,b
##        print hist
##        y = np.bincount(x)
##        ii = np.nonzero(y)[0]
##        for (pe, count) in zip(ii, y[ii]):
##            print pe, count
    def sortPE(self):
        self.getAllData()
        sortedData = sorted(self.rawData, key = itemgetter('PairedReadsCountWithPCRDup'), reverse = True)
        return sortedData
        
            
def writeExcelBPList(rawData, csvName):
    '''this function write the BP location into a csv, the rawData has to be 
    sorted based on the sampleID'''
    tmpData = sorted(rawData, key = itemgetter('sampleID', 'ChromosomeNameHuman',\
    'StrandHuman','PositionHuman'))
    with open(csvName + '.csv','wb') as outF:
        a = csv.writer(outF,delimiter = ',') 
        a.writerows([['sampleID', '#withinID','hg chr', 'hg strand', 'hg pos',\
        'virusType','HBV strand','HBV position','PEcount','Splitread']])

        sampleID = '*'
        for dataEntry in tmpData:
            if sampleID != dataEntry['sampleID']:
                count = 0
            sampleID = dataEntry['sampleID']
            count += 1
            a.writerow([sampleID, count, \
            dataEntry['ChromosomeNameHuman'], \
            dataEntry ['StrandHuman'], dataEntry['PositionHuman'],\
            dataEntry['ChromosomeNameVirus'].split('|')[-1],\
            dataEntry['StrandVirus'], dataEntry['PositionVirus'], \
            dataEntry['PairedReadsCountWithPCRDup'], \
            dataEntry['SplitReadsCountWithPCRDup']])
                                
    return        
     
        
        
        
path =  os.getcwd()+'/bpFiles/'       
parser = parseVispOutput(path)     
#parser.getAllData()
#parser.getPeFreq()
sortedData = parser.sortPE()[:4000]
print sortedData[-1]
writeExcelBPList(sortedData, 'topPE4000')


  
        
        
#bpFileName = 'SRR1610994.out.prediction.CAT1.bp'  
#integrations = extractVISPInfo(bpFileName)  
#print integrations[0]
#writePostxt(integrations)          
    
    
