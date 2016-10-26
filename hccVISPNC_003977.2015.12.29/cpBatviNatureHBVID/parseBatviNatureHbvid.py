# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:43:22 2016
this file parse the BATVI.csv HBVID.csv NATURE.csv
@author: yanj
"""


def recurrentGene(fileName, byPoint = True):
    '''the file is from Ken with Header as column name'''
    from collections import defaultdict
    from operator import itemgetter
    import unicodecsv
    tally = defaultdict(list)
    count = 0
    with open(fileName, 'rb') as csvf:
        reader = unicodecsv.DictReader(csvf) 
        for row in reader:
            count += 1
            if row['Gene_Name'] != '' and row['Gene_Name'] != 'NA':
                if byPoint:
                    tally[row['Gene_Name']].append(('/').join([row['LIB'],row['Human'],row['Virus']]))
                else:
                    tally[row['Gene_Name']].append(row['LIB'])
    print 'finish parsing {} integrations...'.format(count)    
    result = [[key,sorted(set(sampleID)), len(set(sampleID))] for key, sampleID in tally.items()]   
    resultSorted = sorted(result, key = itemgetter(2,0), reverse = True) #sort on sample numver and genename
    if byPoint:
        outFName = fileName[:-4]+'_recurrGeneBypoint.csv'
    else:
        outFName = fileName[:-4]+'_recurrGene.csv'
    with open(outFName, 'wb') as outF:
        a = unicodecsv.writer(outF,delimiter = ',') 
        a.writerows([['geneName','sampleID/Human/Virus', 'totalLocations']]) 
        for rcGene in resultSorted:
            a.writerows([[rcGene[0],' **'.join(rcGene[1]), rcGene[2]]]) 
    print 'finish writing result to file: {}...'.format(outFName)            
    return

filePath = '/mnt/projects/yanj/hcc/hccVISPNC_003977.2015.12.29/cpBatviNatureHBVID/'
fileList = [filePath+'HBVID.csv', filePath+'BATVI.csv',\
            filePath+'BATVI-filter.csv', filePath+'NATURE.csv',filePath+'VISP819.csv']
recurrentGene(fileList[4])



    
    

