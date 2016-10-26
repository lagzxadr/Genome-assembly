#!/usr/bin/env python2.7
"""
Created on Mon Mar 07 14:31:54 2016

@author: yanj

real code for HPV
"""
import unicodecsv
import os
from operator import itemgetter
class parseVispOutput:
    
    def __init__(self, bpFilepath):
        self.bpFilePath = bpFilepath
        self.HPV_refName = '/mnt/projects/yanj/hcc/reference/HPV/HPVdb.fasta'
        self.hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
        self.srrIDName = '/mnt/projects/yanj/hcc/HPV.VISP/ParsingAnalysis/lib/srrID'
        self.rawData = []
        self.peFreq = []
        self.srrID = dict()
        
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
                
    def srr2SampleID(self):
#        srrID = dict()
        with open(self.srrIDName, 'r') as idF:
            for line in idF:
                if line.startswith('>'):
                    continue
                line = line.rstrip().split('\t')                
                if not (line[0] == '' and line[1] == ''):
                    self.srrID[line[1]] = line[0]
                                        
        
    
                
    def extractVISPInfo(self, bpFileName):
        inteRes = []
        peFreq = []
        self.srr2SampleID() # read the srr-ID relation
        print bpFileName
        with open(bpFileName, 'r') as dataF, open(bpFileName+'.csv', 'wb') as outF:
            a = unicodecsv.writer(outF, delimiter = ',')
            for line in dataF:
                line = line.rstrip().split('\t')
                a.writerow(line)
                
        with open(bpFileName+'.csv','rb') as dataF:            
            srr = bpFileName.split('/')[-1].split('.')[0]
            sampleID = self.srrID[srr]
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

    def sortPE(self):
        sortedData = sorted(self.rawData, key = itemgetter('PairedReadsCountWithPCRDup'), reverse = True)
        return sortedData
        
            
      
     
        
    