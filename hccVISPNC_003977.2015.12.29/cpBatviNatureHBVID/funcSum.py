#!/usr/bin/env python2.7

"""
Created on Tue Jan 19 09:32:14 2016
this script pit the reference and experiment sequence together and highlight 
the mutations and the MH
@author: yanj
"""
def sepNT(filelist):
    '''this file seperate the notmal file name to the tumor file name.'''
    normal_filelist = []
    tumor_filelist = []
    for f in filelist:
        if 'N.' in f:
            normal_filelist.append(f)
        if 'T.' in f:
            tumor_filelist.append(f)
    return normal_filelist, tumor_filelist
    
    
def countBP(normal_filelist, tumor_filelist, filePath):
    '''this function write an excel file about the how many BP from normal 
    and tumor group'''
    import csv
    with open('normalBPStats.csv','wb') as outF:
        a = csv.writer(outF,delimiter = ',')
        a.writerows([['filename', '# of bp', '# of bp with PEreads >2',\
                    '# of bp with PEreads > 2 and splitreads !=0']])
        for fname in normal_filelist: 
            countBP, peR, spR = 0,0,0
            with open(filePath+fname, 'r') as bpF:
                for line in bpF:
                    if line.startswith('#'): continue
                    countBP += 1
                    line = line.rstrip().split('\t')
                    if int(line[16]) >2:
                        peR += 1
                        if int(line[17]) != 0:
                            spR += 1
            a.writerows([[fname, countBP, peR, spR]])
    with open('tumorBPstats.csv', 'wb') as outF:
        a = csv.writer(outF,delimiter = ',')
        a.writerows([['filename', '# of bp', '# of bp with PEreads >2',\
            '# of bp with PEreads > 2 and splitreads !=0']])
        for fname in tumor_filelist: 
            countBP, peR, spR = 0,0,0
            with open(filePath+fname, 'r') as bpF:
                for line in bpF:
                    if line.startswith('#'): continue
                    countBP += 1
                    line = line.rstrip().split('\t')
                    if int(line[16]) >2:
                        peR += 1
                        if int(line[17]) != 0:
                            spR += 1
            a.writerows([[fname, countBP, peR, spR]])
    return
            
    
def readVISPOutput(txtFileName, csvFileName):
    '''this file transfer the VISP result to the csv file for easily 
    visualization'''
    import csv
#    txtFileName = '75T.visp.out.prediction.CAT1.bp.txt'  # Peiyong's file
#    csvFileName = txtFileName[:-2]+'csv'
    with open(txtFileName,'r') as dataF, open(csvFileName,'wb') as outF:
        a = csv.writer(outF, delimiter = ',') 
        count = 0
        for line in dataF:
            count += 1
            line = line.rstrip().split('\t')
            a.writerows([line])
#    print 'txt file has been write to csv'
    return

#readVISPOutput('23N.out.prediction.CAT1.bp')
def extractInfoFromTxt(txtFileName, columnList):
    '''this function extract the data from the txt <fileName> 's <columnList>, 
    return the extracted data in a list'''
    rawData = []
    count = 0
    with open(txtFileName, 'r') as dataF:
        for line in dataF:
            count += 1
            if not count == 1:
                line = line.rstrip().split('\t')
                data = [line[i] for i in columnList]
                sampleID = txtFileName.split('/')[-1].split('.')[0]
                data.append(sampleID)
                rawData.append(data)
    return rawData
    
def writeBed(rawData, hgbedFileName, hbvbedFileName):
    sampleID = '*'
    hgbed = open(hgbedFileName, 'w')
    hbvbed = open(hbvbedFileName,'w')
    for dataEntry in rawData:
        #chrNum
#            if dataEntry[2] == 'X': 
#                chrNum = 'chr23'
#            elif dataEntry[2] == 'Y': 
#                chrNum = 'chr24'
        if dataEntry[2].startswith('GL'):
            chrNum = dataEntry[2]
        else:
            chrNum = 'chr'+dataEntry[2]
         #sampleID
        if sampleID != dataEntry[9]:
            count = 0
        sampleID = dataEntry[9]
        count += 1
        if dataEntry[8] == 0: #if split read == 0
            hgentry2write = chrNum + '\t' + str(int(dataEntry[4])-500)\
            + '\t' + str(int(dataEntry[4])+500) + '\t' + dataEntry[9] + '-' + \
            str(count) + '\t' + '*' + '\t' + dataEntry[3] + '\n'
            hgbed.write(hgentry2write)  
            
            hbventry2write = 'HBV\t' + str(int(dataEntry[1])-500)\
            + '\t' + str(int(dataEntry[1])+500) + '\t' + dataEntry[9] + '-' + \
            str(count) + '\t' + '*' + '\t' + dataEntry[0] + '\n'
            hbvbed.write(hbventry2write)
        else:
            hgentry2write = chrNum + '\t' + str(int(dataEntry[4])-1)\
            + '\t' + str(int(dataEntry[4])+1) + '\t' + dataEntry[9] + '-' + \
            str(count) + '\t' + '*' + '\t' + dataEntry[3] + '\n'
            hgbed.write(hgentry2write)
            
            hbventry2write = 'HBV\t' + str(int(dataEntry[1])-1)\
            + '\t' + str(int(dataEntry[1])+1) + '\t' + dataEntry[9] + '-' + \
            str(count) + '\t' + '*' + '\t' + dataEntry[0] + '\n'
            hbvbed.write(hbventry2write)
    hgbed.close()
    hbvbed.close()         
    return
    
def sepNTRawData(rawData):
    N_rawData, T_rawData = [], []
    N_rawData = [dataEntry for dataEntry in rawData if 'N' in dataEntry[9]]
    T_rawData = [dataEntry for dataEntry in rawData if 'T' in dataEntry[9]] 
    return N_rawData, T_rawData
    
def writeExcelBPList(rawData, excelName):
    '''this function write the BP location into a csv, the rawData has to be 
    sorted based on the sampleID'''
    import csv
    with open(excelName + '.csv','wb') as outF:
        a = csv.writer(outF,delimiter = ',') 
        a.writerows([['sampleID', '#withinID','PEcount','Splitread',\
        'HBV strand','HBV position','hg chr', 'hg strand', 'hg pos']])
        sampleID = '*'
        for dataEntry in rawData:
            if sampleID != dataEntry[9]:
                count = 0
            sampleID = dataEntry[9]
            count += 1
            a.writerows([[sampleID, count, dataEntry[7], dataEntry [8], \
            dataEntry[0], dataEntry[1], dataEntry[2], dataEntry[3], \
            dataEntry[4]]])
    return
            
    

    
def sortPEonRawData(rawData):
    '''this function sort the PE'''
    print rawData[0]
    from operator import itemgetter
    newData = []
    for i in range(len(rawData)):
        newData.append([rawData[i][0], int(rawData[i][1]), rawData[i][2],\
                rawData[i][3], int(rawData[i][4]), int(rawData[i][7])])
    print len(rawData), len(newData)

    print newData[0]
    sortedData = sorted(newData, key = itemgetter(5), reverse = True)
    return sortedData
    
    
def scatterPlot_PEvsBPlocation(rawData, prefix = ''):
    '''study the correlation between the PE reads and the BP location, 
    rawData is from extractInfoFromTxt'''
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    positiveStrandX = []
    positiveStrandY = []
    negtiveStrandX = []
    negtiveStrandY = []
    for dataEntry in rawData:
        if dataEntry[0] == '+':
            positiveStrandX.append(int(dataEntry[1]))
            positiveStrandY.append(int(dataEntry[7]))
        else:
            negtiveStrandX.append(int(dataEntry[1]))
            negtiveStrandY.append(int(dataEntry[7]))            
        
    fig = plt.figure(1)    
    ax = fig.add_subplot(111)
    
    plt.scatter (positiveStrandX, positiveStrandY, s = 20, color = 'r', \
    edgecolors = 'none', label = '+ strand', alpha = 0.75)
    plt.scatter (negtiveStrandX, negtiveStrandY, s = 20, color = 'g', \
    edgecolors = 'none', label = '- strand', alpha = 0.75)

    plt.xlabel('HBV coordinate')
    plt.ylabel('PE reads')
    ax.set_xlim([0,3300])
    plt.legend(loc = 'upper left',  frameon = True, fontsize = 12)
    plt.savefig(prefix+'scatter plot',dpi=400) 
    plt.close(1)     
    return

def scatterPlot_PEvsBPlocation2group(rawData_1, rawData_2, label_1 = '', label_2 = '', figNamePri = ''):
    '''study the correlation between the PE reads and the BP location, 
    rawData is from extractInfoFromTxt'''
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    g1_positiveStrandX, g1_positiveStrandY = [], []
    g1_negativeStrandX, g1_negativeStrandY = [], []
    g2_positiveStrandX, g2_positiveStrandY = [], []
    g2_negativeStrandX, g2_negativeStrandY = [], []    

    for dataEntry in rawData_1:
        if dataEntry[0] == '+':
            g1_positiveStrandX.append(int(dataEntry[1]))
            g1_positiveStrandY.append(int(dataEntry[7]))
        else:
            g1_negativeStrandX.append(int(dataEntry[1]))
            g1_negativeStrandY.append(int(dataEntry[7])) 
    
    for dataEntry in rawData_2:
        if dataEntry[0] == '+':
            g2_positiveStrandX.append(int(dataEntry[1]))
            g2_positiveStrandY.append(int(dataEntry[7]))
        else:
            g2_negativeStrandX.append(int(dataEntry[1]))
            g2_negativeStrandY.append(int(dataEntry[7])) 
            
    fig = plt.figure(1)    
    ax = fig.add_subplot(111)
    
    plt.scatter (g1_positiveStrandX, g1_positiveStrandY, s = 15, color = 'r', \
        edgecolors = 'none', label = label_1 + ' +strand', alpha = 0.75)
    plt.scatter (g1_negativeStrandX, g1_negativeStrandY, s = 15, color = 'g', \
        edgecolors = 'none', label = label_1 + ' -strand', alpha = 0.75)
    plt.scatter (g2_positiveStrandX, g2_positiveStrandY, s = 15, color = 'b', \
        edgecolors = 'none', label = label_2 + ' +strand', alpha = 0.75)
    plt.scatter (g2_negativeStrandX, g2_negativeStrandY, s = 15, color = 'c', \
        edgecolors = 'none', label = label_2 + ' -strand', alpha = 0.75)
    
    plt.xlabel('HBV coordinate')
    plt.ylabel('PE reads')
    ax.set_xlim([0,3300])
    plt.legend(loc = 'upper left',  frameon = True, fontsize = 12)
    plt.savefig(figNamePri+'_2 group scatter plot',dpi=400) 
    plt.close(1)     
    return
    
def uniqueBP(rawData):
    '''this functin count the unique BP (unique location on both virus and hg)'''
    requiredData = [dataEntry[:5] for dataEntry in rawData]
    uniqueData = [rawData[i] for i, e in enumerate(requiredData) if \
                requiredData.index(e) == i]
    return uniqueData
    
def repeatBP(rawData, excelprifix = ''):
    from collections import defaultdict
    import csv
    requiredData = [('.').join(dataEntry[:5]) for dataEntry in rawData]
    tally = defaultdict(list)
    for i, e in enumerate(requiredData):
        tally[e].append(rawData[i][9])
    result = ((key, locs) for key, locs in tally.items() if len(locs)>1 )
    with open(excelprifix+'_recurrentBP.csv', 'wb') as outF:
        a = csv.writer(outF,delimiter = ',') 
        a.writerows([['HBV strand','HBV position',\
        'hg chr', 'hg strand', 'hg pos', 'sampleIDs']])   
        for dup in result:
#            print dup
            BPposition = dup[0].split('.')
            BPposition.extend(dup[1])
            a.writerows([BPposition]) 
    return
    
def repeatHbvBP(rawData):
    
    return

def repeatHgBP(rawData):
    return
        

    
def checkInclusive(rawData_l, rawData_s, onlyHBVPos = True):
    '''this function check if the bp in rawData_s is included in rawData_l,
    if onlyHBVPos, check the position on HBV only, else check both HBV and 
    hg position
    rawData = [hbvStrand, hbvPos, hgChr, hgStrand, hgPos, hbvSeq, hgSeq, PEr, Sr]'''
    includeList, non_includeList = [], []
    include = False
    if onlyHBVPos:
        s_Data = [rawData_s[i][:2] for i in range(len(rawData_s))]
        l_Data = [rawData_l[i][:2] for i in range(len(rawData_l))]
    else:
        s_Data = [rawData_s[i][:5] for i in range(len(rawData_s))]
        l_Data = [rawData_l[i][:5] for i in range(len(rawData_l))]
        
    for i in range(len(s_Data)):
        if s_Data[i] in l_Data:
            includeList.append(rawData_s[i])
        else:
            non_includeList.append(rawData_s[i])
    if non_includeList == []:
        include = True
    return includeList, non_includeList, include
    
    
    
    
    
 
def classifyData(data):
    '''this function classify data based on the location of HBV integratio,
    category_1: 1600 < bp < 1900, category_2: the rest data.'''
#    bpList = getBP(data)
    cat_1 = []
    cat_2 = []
    for i in range(len(data)):
        if data[i][1] > 1600 and data[i][1] < 1900:
            cat_1.append(data[i])
        else:
            cat_2.append(data[i])
    return cat_1, cat_2
    
    
def excludeEndBP(rawData):
    '''this function exclude BP too close to start and too close to end, return
    the data after exclution and excluded data'''
    result = [dataEntry for dataEntry in rawData if not \
            (int(dataEntry[1]) > 3115 or int(dataEntry[1]) < 101)]
    excludedData = [dataEntry for dataEntry in rawData if \
            (int(dataEntry[1]) > 3115 or int(dataEntry[1]) < 101)]
    return result, excludedData
    
def excludeLowPE(rawData, PEreadsShreshold = 2):
    '''this function exclude BP with <PEreadsShreshold and 0 splitreads'''
    result = [dataEntry for dataEntry in rawData if \
            int(dataEntry[7]) > PEreadsShreshold and int(dataEntry[8]) != 0 ]   
    return result
    
def excludeLowPE_v2(rawData, PEreadsShreshold = 2):
    '''this function excludeBP with < PEreadsShreshold, nothing to do with
    splitreads'''
    result = [dataEntry for dataEntry in rawData if \
        int(dataEntry[7]) > PEreadsShreshold]   
    return result
    
def querySeq(faFileName, ID, startLoc, endLoc): 
    '''this function perform the sequence query using samtools, this function 
    only works on unix system, argument faFileName and ID are string, Loc is int'''
    from subprocess import check_output  
    command_line = \
    'samtools faidx '+faFileName+' '+ID+':'+str(startLoc)+"-"+str(endLoc)
    Seq = check_output(command_line, shell = True)
    return Seq

def extractRefSeq(hbvRefFile, hgRefFile, rawData, extractLen = 100):
    '''this function put the enquired comparable seqnence line by line and match 
    breankpoint in the middle, for both hg and hbv it enquire updownLen-bp sequence
    in both upstream and downstream. data is from excel file'''
    #from Bio import SeqIO
    from Bio.Seq import Seq
    result = []
#    print 'start extract reference sequence...'
    for i in range(len(rawData)):        
#        print '{}/{}'.format(i,len(rawData))
#        print rawData[i]
        hbvID = '"gi|21326584|ref|NC_003977.1|"'  #hbvID
        hgID = rawData[i][2] # hgID
        
         #truncate exp sequence
        if len(rawData[i][5])<extractLen: #hbv length <100
            expHbvSeq = 'M'*(extractLen-len(rawData[i][5])) + rawData[i][5]
        else:
            expHbvSeq = rawData[i][5][-extractLen:]
        
        if len(rawData[i][6])<extractLen: #hg length <100
            expHgSeq = rawData[i][6]+'M'*(extractLen-len(rawData[i][6]))
        else:
            expHgSeq = rawData[i][6][:extractLen]
              
        # extract reference sequence
        # HBV reference sequence
        if rawData[i][0] =='+':
            hbvEnqSeq = ''
            if int(rawData[i][1])<extractLen: #[3216+X-extL:3215]+[1:x+exL]               
                hbvSeq1 = querySeq(hbvRefFile, hbvID, int(rawData[i][1])+3216-extractLen, 3215)
                hbvSeq2 = querySeq(hbvRefFile, hbvID, 1, int(rawData[i][1])+extractLen)
                hbvSeq1 = hbvSeq1.split()
                hbvSeq2 = hbvSeq2.split()
                for j in range(1,len(hbvSeq1)):
                    hbvEnqSeq += hbvSeq1[j]
                for j in range(1,len(hbvSeq2)):
                    hbvEnqSeq += hbvSeq2[j] 
                hbvSeqName = '%d->3215->1->%d' % (int(rawData[i][1])+3216-extractLen, 
                                                  int(rawData[i][1])+extractLen)
            elif int(rawData[i][1])>3215-extractLen: #[x-extractLen+1:3215]+[1:x-3115] 
                hbvSeq1 = querySeq(hbvRefFile, hbvID, int(rawData[i][1])-extractLen+1, 3215)
                hbvSeq2 = querySeq(hbvRefFile, hbvID, 1, int(rawData[i][1])+extractLen-3215)
                hbvSeq1 = hbvSeq1.split()
                hbvSeq2 = hbvSeq2.split()
                for j in range(1,len(hbvSeq1)):
                    hbvEnqSeq += hbvSeq1[j]
                for j in range(1,len(hbvSeq2)):
                    hbvEnqSeq += hbvSeq2[j]
                hbvSeqName = '%d->3215->1->%d' % (int(rawData[i][1])-extractLen+1, \
                                                int(rawData[i][1])+extractLen-3215)
            else:
                hbvSeq = querySeq(hbvRefFile, hbvID, int(rawData[i][1])-extractLen + 1 ,\
                        int(rawData[i][1])+extractLen)
                hbvSeq = hbvSeq.split()
                for j in range(1,len(hbvSeq)):
                    hbvEnqSeq += hbvSeq[j] 
                hbvSeqName = '%d->%d' %(int(rawData[i][1])-extractLen +1, int(rawData[i][1])+extractLen)
            hbvSeq_record = Seq(hbvEnqSeq)
            hbvSeq_record = hbvSeq_record.upper()
#            print hbvSeq_record
        else: 
            
            if int(rawData[i][1]) < extractLen+1: #[1:x+99]+[3115+x:3215]
                hbvTempSeq1, hbvTempSeq2 = '',''
                hbvSeq1 = querySeq(hbvRefFile, hbvID, 1, int(rawData[i][1])+extractLen-1)
                hbvSeq2 = querySeq(hbvRefFile, hbvID, 3215-extractLen+int(rawData[i][1]), 3215)
                hbvSeq1 = hbvSeq1.split()
                hbvSeq2 = hbvSeq2.split() 
                for j in range(1,len(hbvSeq1)):
                    hbvTempSeq1 += hbvSeq1[j]
                hbvTempSeq_record1 = Seq(hbvTempSeq1)
                hbvTempSeq_record1 = hbvTempSeq_record1.upper().reverse_complement()
                for j in range(1,len(hbvSeq2)):
                    hbvTempSeq2 += hbvSeq2[j]
                hbvTempSeq_record2 = Seq(hbvTempSeq2)
                hbvTempSeq_record2 = hbvTempSeq_record2.upper().reverse_complement()
                hbvSeq_record = hbvTempSeq_record1 + hbvTempSeq_record2
                hbvSeqName = '%d->1->3215->%d' % (int(rawData[i][1])+extractLen-1, 3215-extractLen+int(rawData[i][1]))
            elif int(rawData[i][1]) > 3216-extractLen: #[1:x-3116] + [x-100:3215]
                hbvTempSeq1, hbvTempSeq2 = '',''
                hbvSeq1 = querySeq(hbvRefFile, hbvID, 1, int(rawData[i][1])+extractLen-3216)
                hbvSeq2 = querySeq(hbvRefFile, hbvID, int(rawData[i][1])-extractLen, 3215)
                hbvSeq1 = hbvSeq1.split()
                hbvSeq2 = hbvSeq2.split() 
                for j in range(1,len(hbvSeq1)):
                    hbvTempSeq1 += hbvSeq1[j]
                hbvTempSeq_record1 = Seq(hbvTempSeq1)
                hbvTempSeq_record1 = hbvTempSeq_record1.upper().reverse_complement()
                for j in range(1,len(hbvSeq2)):
                    hbvTempSeq2 += hbvSeq2[j]
                hbvTempSeq_record2 = Seq(hbvTempSeq2)
                hbvTempSeq_record2 = hbvTempSeq_record2.upper().reverse_complement()
                hbvSeq_record = hbvTempSeq_record1 + hbvTempSeq_record2
                hbvSeqName = '%d->1->3215->%d' % (int(rawData[i][1])+extractLen-3216, int(rawData[i][1])-extractLen)
            else:
                hbvEnqSeq = ''
                hbvSeq = querySeq(hbvRefFile, hbvID, int(rawData[i][1]) - extractLen, \
                        int(rawData[i][1]) + extractLen - 1)
                hbvSeq = hbvSeq.split()
                for j in range(1,len(hbvSeq)):
                    hbvEnqSeq += hbvSeq[j] 
                hbvSeq_record = Seq(hbvEnqSeq)
                hbvSeq_record = hbvSeq_record.upper().reverse_complement() 
                hbvSeqName = '%d->%d' %(int(rawData[i][1]) + extractLen - 1, 
                                        int(rawData[i][1]) - extractLen)
#            print hbvSeqName
#            print hbvSeq_record
        #hg reference sequence
        hgEnqSeq = ''
        if rawData[i][3] == '+':
             
            hgSeq = querySeq(hgRefFile, hgID, int(rawData[i][4])-extractLen, int(rawData[i][4])+extractLen-1)
            hgSeq = hgSeq.split()
            for j in range(1,len(hgSeq)):
                hgEnqSeq += hgSeq[j]
            hgSeq_record = Seq(hgEnqSeq)
            hgSeq_record = hgSeq_record.upper()  
        else:
             
            hgSeq = querySeq(hgRefFile, hgID, int(rawData[i][4])-extractLen+1, int(rawData[i][4]) + extractLen)
            hgSeq = hgSeq.split()
            for j in range(1,len(hgSeq)):
                hgEnqSeq += hgSeq[j]
            hgSeq_record = Seq(hgEnqSeq)
            hgSeq_record = hgSeq_record.upper().reverse_complement()        
#        print hgSeq
               
        alnSeq = [hbvSeqName + ' ' + 'exp_seq' + ' ' + hgSeq[0], \
            str(hbvSeq_record), expHbvSeq + expHgSeq, str(hgSeq_record), \
            int(rawData[i][7]), int(rawData[i][8]), rawData[i][9], \
            ('.').join(rawData[i][:5])]
        result.append(alnSeq)
    return result

def NatBPFilter(seqResult, flankLen = 100):
    '''if the hg reference has 'N' at the breakpoint, then remove'''
    excludeList = []
    for i in range(len(seqResult)):
        if seqResult[i][3][flankLen-1] == 'N' and seqResult[i][3][flankLen] == 'N':
            excludeList.append(i)    
    return excludeList
    
       
def sortPECount(seqResult):
    '''this functio sort the seqResult based on the PEcount seqResult[4].'''
    from operator import itemgetter
    sortedSeqResult = sorted(seqResult, key = itemgetter(4,5), reverse = True)
    return sortedSeqResult
    
    
def cutSeq(seqResult, flankingLen = 100):
    '''this function cut the length of the string to specific flanking region 
    length, specifric to VISP result'''
    import sys
    cutSeqResult = []
    if flankingLen > 100:
        print 'flankingRegionLength should less than 100'
        sys.exit()
    for BP in seqResult:
        hbvSeq = BP[1][100 - flankingLen : 100 + flankingLen ]
        expSeq = BP[2][100 - flankingLen : 100 + flankingLen ]
        hgSeq = BP[3][100 - flankingLen : 100 + flankingLen ]
        cutSeqBP = [BP[0], hbvSeq, expSeq, hgSeq]
        cutSeqResult.append(cutSeqBP)
    return cutSeqResult 

def shortSeqFilter(seqResult, flankingLen = 100):
    '''filter the integrations with too short sequence(too many 'M').###
    the excludeList will include some false positive, careful use!!!'''    
    excludeList = []
    threshold = float(flankingLen-40)/flankingLen # filter the inte with M over 60%
    for i in range(len(seqResult)):
        if seqResult[i][2][:flankingLen].count('M') > threshold * flankingLen or \
        seqResult[i][2][-1*flankingLen:].count('M') > threshold * flankingLen:
#        or seqResult[i][2][:flankingLen].count('N') > threshold * flankingLen or \
#        seqResult[i][2][-1*flankingLen:].count('N') > threshold * flankingLen:
            excludeList.append(i)    
    return excludeList
    
    
def writeSeq2Csv(csvFileName, seqResult):
    '''this function write the sequences to the excel files with location matched
    seqResult is returned by function extractRefSeq '''
    import csv
    with open(csvFileName,'wb') as outf:
        a = csv.writer(outf, delimiter = ',')
        count = 0
        for BP in seqResult: 
            count += 1
            a.writerows([['#'+str(count)+'_'+BP[6]+'_'+BP[7], BP[4], BP[5]]])
            
            seqID = BP[0].split() 			
            line1 = [seqID[0]]
            for nucli in BP[1]: 
                line1.append(nucli)				
            line2 = [seqID[1]]
            for nucli in BP[2]: 
                line2.append(nucli)	
            line3 = [seqID[2]]
            for nucli in BP[3]:
                line3.append(nucli)
            a.writerows([line1, line2, line3])  
    return

def plusMinusHist(rawData, fileNamePrefix = ''):
    '''this function do the first check of the dataset, which is to plot the 
    +/- fusion strand distribution. '''
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib. pyplot as plt 

    hbvPlus_hgPlus, hbvPlus_hgMinus, hbvMinus_hgPlus,  hbvMinus_hgMinus = \
    [], [], [], [] # from hg to HBV
    for dataEntry in rawData:
        if dataEntry[0] == '+' and dataEntry[3] == '+':
            hbvPlus_hgPlus.append(int(dataEntry[1]))
        if dataEntry[0] == '+' and dataEntry[3] == '-':
            hbvPlus_hgMinus.append(int(dataEntry[1]))            
        if dataEntry[0] == '-' and dataEntry[3] == '+':
            hbvMinus_hgPlus.append(int(dataEntry[1]))
        if dataEntry[0] == '-' and dataEntry[3] == '-':
            hbvMinus_hgMinus.append(int(dataEntry[1]))
            
    fig = plt.figure(1)
    _,_,patches = plt.hist([hbvPlus_hgPlus,hbvPlus_hgMinus],bins=50, histtype='bar', \
            rwidth=0.8, color = ['r','g'], label=['HBV+ hg+','HBV+ hg-'])
    plt.setp(patches, 'alpha', 0.75)
    plt.legend()
    ax = fig.add_subplot(111)
    ax.set_xlabel('HBV corrdinate')
    ax.set_ylabel('Number of HBV integration breakpoints')
    ax.set_autoscaley_on(False)
    ax.set_ylim([0,16])  
    ax.set_autoscalex_on(False)
    ax.set_xlim([0,3300])
    plt.savefig(fileNamePrefix+'plusHBVStrandHist.png',dpi=120)  
    
    fig = plt.figure(2)
    _,_,patches = plt.hist([hbvMinus_hgPlus,hbvMinus_hgMinus],bins=50, histtype='bar', \
            rwidth=0.8, color = ['r','g'], label=['HBV- hg+','HBV- hg-'])
    plt.setp(patches, 'alpha', 0.75)
    plt.legend()
    ax = fig.add_subplot(111)
    ax.set_xlabel('HBV corrdinate')
    ax.set_ylabel('Number of HBV integration breakpoints')
    ax.set_autoscaley_on(False)
    ax.set_ylim([0,16])    
    ax.set_autoscalex_on(False)
    ax.set_xlim([0,3300])
    plt.savefig(fileNamePrefix+'minusHBVStrandHist.png',dpi=120)  
    plt.close(1)
    plt.close(2)
    return
    
def checkMutation(seqResult, flankingLen = 100):
    mutationLists = []
    count = 0
    for BP in seqResult:
        count += 1
        hbv_mutation = [(i,j) for i,j in enumerate(zip(BP[1][:flankingLen], BP[2][:flankingLen])) \
                        if  (j[0] != j[1] and j[1] != 'M' and j[0] != 'N' and j[1] != 'N')]
                        #hbv_mutation: [(offset, (hbv_ref, hbv_exp))]
        hg_mutation = [(i,j) for i,j in enumerate(zip(BP[3][-flankingLen:], BP[2][-flankingLen:])) \
                        if  (j[0] != j[1] and j[1] != 'M' and j[0] !='N' and j[1] != 'N')]
                        #hg_mutation: [(offset, (hg_ref, hg_exp))]
        mutationLists.append([hbv_mutation, hg_mutation])
    return mutationLists
    
def quantifyMutation(mutationLists):
#    mutation = {'A>C/T>G': 0, 'A>G/T>C': 0, 'A>T/T>A': 0, 'C>A/G>T': 0, \
#                'C>G/G>C': 0, 'C>T/G>A': 0}
    mutationCount = []
    for integration_mutations in mutationLists:
        hbv_mutation = [0]*6
        hg_mutation = [0]*6
        for mu in integration_mutations[0]: # hbv_mutations
            if (mu[1][0] == 'A' and mu[1][1] == 'C') or\
                (mu[1][0] == 'T' and mu[1][1] == 'G'):
                hbv_mutation[0] += 1
            if (mu[1][0] == 'A' and mu[1][1] == 'G') or\
                (mu[1][0] == 'T' and mu[1][1] == 'C'):
                hbv_mutation[1] += 1
            if (mu[1][0] == 'A' and mu[1][1] == 'T') or\
                (mu[1][0] == 'T' and mu[1][1] == 'A'):
                hbv_mutation[2] += 1
            if (mu[1][0] == 'C' and mu[1][1] == 'A') or\
                (mu[1][0] == 'G' and mu[1][1] == 'T'):
                hbv_mutation[3] += 1   
            if (mu[1][0] == 'C' and mu[1][1] == 'G') or\
                (mu[1][0] == 'G' and mu[1][1] == 'C'):
                hbv_mutation[4] += 1 
                
            if (mu[1][0] == 'C' and mu[1][1] == 'T') or\
                (mu[1][0] == 'G' and mu[1][1] == 'A'):
                hbv_mutation[5] += 1 
        for mu in integration_mutations[1]: #hg_mutatios
            if (mu[1][0] == 'A' and mu[1][1] == 'C') or\
                (mu[1][0] == 'T' and mu[1][1] == 'G'):
                hg_mutation[0] += 1
            if (mu[1][0] == 'A' and mu[1][1] == 'G') or\
                (mu[1][0] == 'T' and mu[1][1] == 'C'):
                hg_mutation[1] += 1
            if (mu[1][0] == 'A' and mu[1][1] == 'T') or\
                (mu[1][0] == 'T' and mu[1][1] == 'A'):
                hg_mutation[2] += 1
            if (mu[1][0] == 'C' and mu[1][1] == 'A') or\
                (mu[1][0] == 'G' and mu[1][1] == 'T'):
                hg_mutation[3] += 1   
            if (mu[1][0] == 'C' and mu[1][1] == 'G') or\
                (mu[1][0] == 'G' and mu[1][1] == 'C'):
                hg_mutation[4] += 1 
            if (mu[1][0] == 'C' and mu[1][1] == 'T') or\
                (mu[1][0] == 'G' and mu[1][1] == 'A'):
                hg_mutation[5] += 1                 
        inteMutationCount = [hbv_mutation, hg_mutation]
        mutationCount.append(inteMutationCount)
    return mutationCount

def highMutationFilter(mutationCount,flankingLen = 100):
    '''create a filter remove hbv side mutaiton rate > 20%, hg side mutation 
    rate > 10% the index starts from 0 in the excludeList'''
    excludeList = []
    for i in range(len(mutationCount)):
        if sum(mutationCount[i][0]) > 0.2* flankingLen or sum(mutationCount[i][1]) > 0.1* flankingLen:
            excludeList.append(i)    
    return excludeList
       
def filterData(Data, excludeList):
    '''Data is a list of list, the data-entry/list's offset 
    in the excludeList will be excluded.'''
    updatedData = []
    for i in range(len(Data)):
        if i in excludeList:
            continue
        updatedData.append(Data[i])
    return updatedData

def mutationPerc(mutationCount, SeqResult, flankLen = 100):
    import numpy as np  
    #total length of nuclei sequence
    tot_hbvLen, tot_hgLen = 0,0
    for integration in SeqResult:
        tot_hbvLen += (flankLen-integration[2][:flankLen].count('M'))
        tot_hgLen += (flankLen-integration[2][-1*flankLen:].count('M'))    
    #sum the mutation within a sample
    hbv_mutation = [mutationCount[i][0] for i in range(len(mutationCount))]
    hg_mutaton = [mutationCount[i][1] for i in range(len(mutationCount))]
        
    resultMx = np.matrix(hbv_mutation)       
    hbv_numMu = list(resultMx.sum(axis=0).A1)
    
    resultMx = np.matrix(hg_mutaton)       
    hg_numMu = list(resultMx.sum(axis=0).A1)

    hbv_MuPerc = [float(numMu)/tot_hbvLen for numMu in hbv_numMu]
    hg_MuPerc = [float(numMu)/tot_hgLen for numMu in hg_numMu]
    return hbv_MuPerc, hg_MuPerc
    
def plotMutationBar(hbvMuPerc, hgMuPerc, figName):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    N = len(hbvMuPerc)
    ind = np.arange(N)
    width = 0.35
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    p1 = ax.bar(ind, hbvMuPerc, width, color = 'red', alpha = 0.75)
    p2 = ax.bar(ind + width, hgMuPerc, width, color = 'green', alpha = 0.75)
    xtickLabel = ['A>C/T>G', 'A>G/T>C', 'A>T/T>A', 'C>A/G>T','C>G/G>C', 'C>T/G>A']
    ax.set_xticks(ind + width)
    ax.set_xticklabels(xtickLabel)
    ax.set_xlabel('')
    ax.set_ylabel('Mutation rate (%)')
    ax.legend((p1[0],p2[0]),('HBV', 'Human'), loc = 'upper left')
    plt.savefig(figName,dpi=120) 
    plt.close(1)    
    return
        
def checkMH(seqResult, flankingLen = 100):
    MHLists = []
    count = 0    
    for BP in seqResult:
        count += 1
        hbv_MH = [(i,j) for i,j in enumerate(zip(BP[3][:flankingLen], BP[2][:flankingLen])) \
                if (j[0] == j[1] and j[0] !='N')]
        hg_MH = [(i,j) for i,j in enumerate(zip(BP[1][-1*flankingLen:],BP[2][-1*flankingLen:])) \
                if (j[0] == j[1] and j[0] != 'N')]
        MHLists.append([hbv_MH, hg_MH])
    return MHLists

def quantifyMH(MHLists):
    '''for generating filter'''
    MHCount = []
    for mh in MHLists:
        hbv_MHCount = len(mh[0])
        hg_MHCount = len(mh[1])
        MHCount.append([hbv_MHCount, hg_MHCount])
    return MHCount
    
def highMHFilter(MHCount,flankingLen = 100):
    '''create a filter base on the mutaiton rate > 50%, the index starts from 0
    in the excludeList'''
    excludeList = []
    for i in range(len(MHCount)):
        if MHCount[i][0] > 0.5* flankingLen or MHCount[i][1] > 0.5* flankingLen:
            excludeList.append(i)    
    return excludeList 

def theSmallFilter(HBV_refName, hg_refName, rawData, flankLen = 100):
    '''this viersion of filter is for study the BP distribution on HBV'''
    print len(rawData)
    rawData = excludeLowPE_v2(rawData, 1) # pls change the threshold
    print len(rawData)    
    #extract the sequence
    seqResult =  extractRefSeq(HBV_refName, hg_refName, rawData, flankLen)
    #step1-> filter short exp seq
    excludeList1 = shortSeqFilter(seqResult, flankLen) 
    seqResult1 = filterData(seqResult,excludeList1)
    rawData1 = filterData(rawData,excludeList1)
    print len(rawData1)
    
    #step2-> filter mutation rate > 50%
    mutationLists = checkMutation(seqResult1) 
    mutationCount = quantifyMutation(mutationLists)
    excludeList2 = highMutationFilter(mutationCount) 
    seqResult_filtered = filterData(seqResult1, excludeList2)
    rawData_filtered = filterData(rawData1,excludeList2)
    print len(rawData_filtered)  
    return rawData_filtered, seqResult_filtered
    
    
    
def theBigFilter(HBV_refName, hg_refName, rawData, flankLen = 100):
    '''this version of filter is for studying MH'''
    print len(rawData)
    rawData = uniqueBP(rawData)
    print len(rawData)
    rawData = excludeLowPE(rawData, 1) # pls change the threshold
    print len(rawData)
    #extract the sequence
    seqResult =  extractRefSeq(HBV_refName, hg_refName, rawData, flankLen)
    #step1-> filter short exp seq
    excludeList1 = shortSeqFilter(seqResult, flankLen) 
    seqResult1 = filterData(seqResult,excludeList1)
    rawData1 = filterData(rawData,excludeList1)
    print len(rawData1)
    #step2-> filter mutation rate > 50%
    mutationLists = checkMutation(seqResult1) 
    mutationCount = quantifyMutation(mutationLists)
    excludeList2 = highMutationFilter(mutationCount) 
    seqResult2 = filterData(seqResult1, excludeList2)
    rawData2 = filterData(rawData1,excludeList2)
    print len(rawData2)
    #step3-> filter mh rate > 50%
    mhLists = checkMH(seqResult2)
    mhCount = quantifyMH(mhLists)
    excludeList3 = highMHFilter(mhCount)
    seqResult3 = filterData(seqResult2, excludeList3)
    rawData3 = filterData(rawData2, excludeList3)  
    print len(rawData3)
    excludeList4 = NatBPFilter(seqResult3)
    seqResult_filtered = filterData(seqResult3, excludeList4)
    rawData_filtered = filterData(rawData3, excludeList4) 
    print len(rawData_filtered)     
    return rawData_filtered, seqResult_filtered
    
def checkMH_theratical(seqResult, flankingLen = 100):
    '''check the theratical MH using the break point location and sequence from
    reference genome.'''
    MHLists_theratical = []
    count = 0
    for BP in seqResult:
        count += 1
        hbv_MH_theratical = [(i,j) for i,j in enumerate(zip(BP[3][:flankingLen], BP[1][:flankingLen])) \
                if (j[0] == j[1] and j[0] !='N')]
        hg_MH_theratical = [(i,j) for i,j in enumerate(zip(BP[1][-1*flankingLen:],BP[3][-1*flankingLen:])) \
                if (j[0] == j[1] and j[1] != 'N')]
        MHLists_theratical.append([hbv_MH_theratical, hg_MH_theratical])
    return MHLists_theratical
    
def checkMH_expected(randSeqResult, flankingLen = 100):
    '''check the expected MH from the random sequence, the reandom sequence is 
    two line with 1st line virus, 2nd line hg.'''
    MHLists_expected = []
    count = 0
    for BP in randSeqResult:
        count += 1
        hbv_MH_theratical = [(i,j) for i,j in enumerate(zip(BP[1][:flankingLen], BP[2][:flankingLen])) \
                if (j[0] == j[1] and j[0] !='N')]
        hg_MH_theratical = [(i,j) for i,j in enumerate(zip(BP[1][-1*flankingLen:],BP[2][-1*flankingLen:])) \
                if (j[0] == j[1] and j[1] != 'N')]
        MHLists_expected.append([hbv_MH_theratical, hg_MH_theratical])        
    return MHLists_expected

def groupMHList(MHLists):
    '''this function group the MHLists, for easier view the length of the MH'''
    from itertools import groupby
    from operator import itemgetter
    groupMHLists = []
    for integration_mh in MHLists:
        hbv_mh, hg_mh = [],[]
        if integration_mh[0] == []:
            hbv_mh.append([])
        else:
            for k, g in groupby(enumerate(zip(*integration_mh[0])[0]), lambda (i, x): i-x):
                hbv_mh.append(map(itemgetter(1), g))
        if integration_mh[1] == []:
            hg_mh.append([])
        else:
            for k, g in groupby(enumerate(zip(*integration_mh[1])[0]), lambda (i, x): i-x):
                hg_mh.append(map(itemgetter(1), g)) 
        groupMHLists.append([hbv_mh, hg_mh])
    return groupMHLists
    
def combineGroupMHLists(groupMHLists, flankingLen = 100):
    '''this functin combine the hbv_mh with hg_mh, adjust hg_mh into proper 
    offset and address the break point cover both sides'''
    combinedGroupMHLists = []
    for inte_grp in groupMHLists:
#        print len(inte_grp)
        # check if the break point cover both sides
        if inte_grp[0] != [] and inte_grp[1] != [] and\
        (flankingLen-1) in inte_grp[0][-1] and 0 in inte_grp[1][0]:
            inte_grp[0][-1].extend(b+flankingLen for b in inte_grp[1][0])
            del inte_grp[1][0]
        combined_inte_grp = [inte_grp[0][i] for i in range(len(inte_grp[0]))]            
        for kmer in inte_grp[1]:
            combined_inte_grp.append([kmer[i]+flankingLen for i in range(len(kmer))])
        combinedGroupMHLists.append(combined_inte_grp)
    return combinedGroupMHLists
    
def kmerLenStats_KenVersion(lenStats):
    '''this function do the kmerStats with Ken's counting style, e.g. 
    if one integration has n5 MH = 5, then _kmerCount += n5 (k = 1,2,3,4)'''
#    print len(lenStats)    
    new_lenStats = []
    for stats in lenStats:
        stats[0] += stats[1]+stats[2]+stats[3]+stats[4]+stats[5]+stats[6]+stats[7]
        stats[1] += stats[2]+stats[3]+stats[4]+stats[5]+stats[6]+stats[7]
        stats[2] += stats[3]+stats[4]+stats[5]+stats[6]+stats[7]
        stats[3] += stats[4]+stats[5]+stats[6]+stats[7]
        stats[4] += stats[5]+stats[6]+stats[7]
        stats[5] += stats[6]+stats[7]
        stats[6] += stats[7] 
        new_lenStats.append([stats[i] for i in range(8)])
    return new_lenStats

def kmerLenStats(groupMHLists, flankingLen = 100):
    '''this function return the statistitcs of the groupResultLists to count 
    the number of kmer (k = 1-8) of each integration'''
    c_GroupMHLists = combineGroupMHLists(groupMHLists, flankingLen)    
    lenStats = []
    for inte_grp in c_GroupMHLists:                
        _1merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==1])
        _2merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==2])
        _3merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==3])
        _4merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==4])
        _5merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==5])
        _6merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==6])
        _7merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==7])
        _8merCount = len([Kmer for Kmer in inte_grp if len(Kmer)==8])
        lenStats.append([_1merCount, _2merCount, _3merCount, _4merCount,\
        _5merCount, _6merCount, _7merCount, _8merCount])
    lenStats = kmerLenStats_KenVersion(lenStats)
    return lenStats
    

    
def kmerLenStats_hbvhg(groupMHLists):
    '''this function count the number of kmer of each integration's left side 
    and right side seperately'''
    hbv_lenStats, hg_lenStats = [], []
    for inte_grp in groupMHLists:
        for i in [0,1]:
            _1merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==1])
            _2merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==2])
            _3merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==3])
            _4merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==4])
            _5merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==5])
            _6merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==6])
            _7merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==7])
            _8merCount = len([Kmer for Kmer in inte_grp[i] if len(Kmer)==8])
            if i == 0:
                hbv_lenStats.append([_1merCount, _2merCount, _3merCount, \
                _4merCount, _5merCount, _6merCount, _7merCount, _8merCount])
                hbv_lenStats = kmerLenStats_KenVersion(hbv_lenStats)
            else:
                hg_lenStats.append([_1merCount, _2merCount, _3merCount, \
                _4merCount, _5merCount, _6merCount, _7merCount, _8merCount])
                hg_lenStats = kmerLenStats_KenVersion(hg_lenStats)
    return hbv_lenStats, hg_lenStats   
    
def integrationCount(lenStats):
    ''' this function count the result from the kmerLenStats/ lmerLenStats_kenversion'''
    import numpy as np
    kmerList = np.array(zip(*lenStats))
    inteCount = [np.count_nonzero(arr) for arr in kmerList]
    return  inteCount
    
def mhonIntegration(groupMHLists,flankingLen = 100):
    ''' this function returns the list of integrations that contain MH on 
    breakpoint and classify the cases depends on the length of MH, the index 
    starts from 0'''
    mhonInteList = [[],[],[],[],[],[],[],[]]# put the offset of BP into length-according []
    mhcoverInteList = []    
    c_groupMHLists = combineGroupMHLists(groupMHLists,flankingLen)
    offset = -1
    for inte_grp in c_groupMHLists:
        offset += 1
        for Kmer in inte_grp:
            if (flankingLen-1 in Kmer) or (flankingLen in Kmer):
                for length in range(1,9):#test Kmer's length
                    if len(Kmer) == length:
                        mhonInteList[length-1].append(offset)
            if (flankingLen-1 in Kmer) and (flankingLen in Kmer):
                mhcoverInteList.append(offset)
    numMHonInte = [len(mhonInteList[i]) for i in range(len(mhonInteList))]   
    return [mhonInteList,mhcoverInteList], numMHonInte   

def mhonINtegration_hbvhg(groupMHLists,flankingLen = 100):
    hbv_mhonInteList = [[],[],[],[],[],[],[],[]]# put the offset of BP into length-according []
    hg_mhonInteList = [[],[],[],[],[],[],[],[]]    
    offset = -1
    for inte_grp in groupMHLists:
        if flankingLen-1 in inte_grp[0][-1]:
            for length in range(1,9):
                if len(inte_grp[0][-1]) == length:
                    hbv_mhonInteList[length-1].append(offset)
        if 0 in inte_grp[1][0]:
            for length in range(1,9):
                if len(inte_grp[1][0]) == length:
                    hg_mhonInteList[length-1].append(offset)
    hbv_numMHonInte = [len(hbv_mhonInteList[i]) for i in range(len(hbv_mhonInteList))]
    hg_numMHonInte = [len(hg_mhonInteList[i]) for i in range(len(hg_mhonInteList))]
    return hbv_numMHonInte, hg_numMHonInte 
    
def statsSummary(mhLists, flankingLen = 100):    
    groupMHLists = groupMHList(mhLists)
    lenStats = kmerLenStats(groupMHLists, flankingLen)
    inteCount = integrationCount(lenStats)
    _, mhonInte = mhonIntegration(groupMHLists, flankingLen)    
    return mhonInte, inteCount

def statsSummary_hbvhg(mhLists, flankingLen = 100):
    ''' adapted the 1st viersion to process the left/right side MH stats'''
    groupMHLists = groupMHList(mhLists)
    hbv_lenStats, hg_lenStats = kmerLenStats_hbvhg(groupMHLists) 
    hbv_inteCount = integrationCount(hbv_lenStats)
    hg_inteCount = integrationCount(hg_lenStats)
    hbv_numMHonInte, hg_numMHonInte = mhonINtegration_hbvhg(groupMHLists, flankingLen)
    return [hbv_numMHonInte,hbv_inteCount], [hg_numMHonInte,hg_inteCount]
    
    
    
def shuffleData(seqResult):
    '''this function decompose the alnBP into hg and hbv seqdata, randomly 
    shuffle the hg and hbv sequence, and recompose the data into the same format
    as alnResult, alnResult is output of function alignSeqBP '''
    from random import shuffle
    hg_Seqs = []
    hbv_Seqs = []
    randSeqResult = []
    for BP in seqResult:
        hbvID = BP[0].split(' ')[0]
        hbvSeq = BP[1]
        hgID = BP[0].split(' ')[2]
        hgSeq = BP[3]
        hbv_Seqs.append([hbvID, hbvSeq])
        hg_Seqs.append([hgID, hgSeq])
    shuffle(hbv_Seqs)
    shuffle(hg_Seqs)
    
    for (hbv_Seq, hg_Seq) in zip(hbv_Seqs, hg_Seqs):
        randAlnSeq = [hbv_Seq[0] + ' ' + hg_Seq[0], hbv_Seq[1], hg_Seq[1]]
        randSeqResult.append(randAlnSeq)
    return randSeqResult
    
def expectedStatsSummary(seqResult, flankingLen = 100):
    '''seqResult is from function extractRefSeq'''
    import numpy as np
    e_mhonInteCLists = []
    e_inteCLists = []        
    shuffleNum = 500
    for _ in range(shuffleNum):
        randSeqResult = shuffleData(seqResult)
        mhLists_expected = checkMH_expected(randSeqResult, flankingLen)
        e_mhonInteC, e_inteC = statsSummary(mhLists_expected, flankingLen)                
        e_mhonInteCLists.append(e_mhonInteC)
        e_inteCLists.append(e_inteC)
    
    Mx1 = np.matrix(e_mhonInteCLists)       
    sumMx1 = list(Mx1.sum(axis=0).A1)
    e_numMHonInteRes = [float(x)/shuffleNum for x in sumMx1]
    Mx2 = np.matrix(e_inteCLists)
    sumMx2 = list(Mx2.sum(axis=0).A1)
    e_InteCountresRes = [float(x)/shuffleNum for x in sumMx2]
    return e_numMHonInteRes, e_InteCountresRes

def expectedStatsSummary_hbvhg(seqResult, flankingLen = 100):
    '''seqResult is from function extractRefSeq, this function is for left/right 
    side statistics'''
    import numpy as np
    hbv_e_mhonInteCLists, hg_e_mhonInteCLists = [], []
    hbv_e_inteCLists, hg_e_inteCLists = [], []   
    shuffleNum = 500
    for _ in range(shuffleNum):
        randSeqResult = shuffleData(seqResult)
        mhLists_expected = checkMH_expected(randSeqResult, flankingLen)
        hbv_data, hg_data = statsSummary_hbvhg(mhLists_expected, flankingLen)                
        hbv_e_mhonInteCLists.append(hbv_data[0])
        hg_e_mhonInteCLists.append(hg_data[0])
        hbv_e_inteCLists.append(hbv_data[1])
        hg_e_inteCLists.append(hg_data[1])
        
    Mx1 = np.matrix(hbv_e_mhonInteCLists)       
    sumMx1 = list(Mx1.sum(axis=0).A1)
    hbv_e_numMHonInteRes = [float(x)/shuffleNum for x in sumMx1]
    
    Mx2 = np.matrix(hg_e_mhonInteCLists)       
    sumMx2 = list(Mx2.sum(axis=0).A1)
    hg_e_numMHonInteRes = [float(x)/shuffleNum for x in sumMx2]    
    
    
    Mx3 = np.matrix(hbv_e_inteCLists)
    sumMx3 = list(Mx3.sum(axis=0).A1)
    hbv_e_InteCountresRes = [float(x)/shuffleNum for x in sumMx3]
    
    Mx4 = np.matrix(hg_e_inteCLists)
    sumMx4 = list(Mx4.sum(axis=0).A1)
    hg_e_InteCountresRes = [float(x)/shuffleNum for x in sumMx4]    
    return [hbv_e_numMHonInteRes,hbv_e_InteCountresRes], \
            [hg_e_numMHonInteRes,hg_e_InteCountresRes]
            
            
def assemblyData(SeqResult, FlankingLen = 100):
    #the exp-ref result
    mhlists = checkMH(SeqResult,FlankingLen)
    mhonInteC, inteC = statsSummary(mhlists,FlankingLen)   
    # the ref-ref result
    mhlist_theratical = checkMH_theratical(SeqResult,FlankingLen)
    mhonInteC_thera, inteC_thera = statsSummary(mhlist_theratical,FlankingLen)
    #the expected result
    mhonInteC_expected, inteC_expected = expectedStatsSummary(SeqResult,FlankingLen)    
    #assembly
    mhonInteCData = [mhonInteC, mhonInteC_thera, mhonInteC_expected]
    inteCData = [inteC, inteC_thera, inteC_expected]   
    return mhonInteCData, inteCData

def assemblyData_hbvhg(SeqResult, FlankingLen = 100):
    mhlists = checkMH(SeqResult,FlankingLen)
    hbv_data, hg_data = statsSummary_hbvhg(mhlists,FlankingLen)
    mhlist_theratical = checkMH_theratical(SeqResult,FlankingLen)
    hbv_data_thera, hg_data_thera = statsSummary_hbvhg(mhlist_theratical,FlankingLen)
    hbv_data_e, hg_data_e = expectedStatsSummary_hbvhg(SeqResult, FlankingLen)
    #assembly
    hbv_mhonInteCData = [hbv_data[0], hbv_data_thera[0], hbv_data_e[0]]
    hg_mhonInteCData = [hg_data[0], hg_data_thera[0], hg_data_e[0]]
    hbv_inteCData = [hbv_data[1], hbv_data_thera[1], hbv_data_e[1]]
    hg_inteCData = [hg_data[1], hg_data_thera[1], hg_data_e[1]]
    return [hbv_mhonInteCData,hbv_inteCData],\
            [hg_mhonInteCData, hg_inteCData]

def chisquareTest(data,totalCount):
    '''do chisquare test of data, data is a list of list, the list inside is
    for test'''
#    print data
    from scipy.stats import chisquare 
    N = len(data) # number of data for test
    resultP = []
    for i in range(N-1):
        for j in range(i+1,N):
            P = []
            for k in range(len(data[0])):
                o = [data[i][k],totalCount - data[i][k]]
                e = [data[j][k], totalCount - data[j][k]]
                _,p = chisquare(o,f_exp = e)
                P.append(p)
            resultP.append(P)
    return resultP
    
def Barplot_3samples_mhonInteC(data, resultP, figureName):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    N = 7 #how many x column
    ind = np.arange(N)
    width = 0.2
    
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    p1 = ax.bar(ind, data[0][:7], width, color = 'indigo' , alpha = 0.75)
    p2 = ax.bar(ind + width, data[1][:7], width, color = 'blue', alpha = 0.75) 
    p3 = ax.bar(ind + 2*width, data[2][:7], width, color = 'powderblue', alpha = 0.75) 
    
    xtickLabel = ['1','2','3','4','5','6','7']
    ax.set_xticks(ind + 1.5*width)
    ax.set_xticklabels(xtickLabel)
    ax.set_xlabel('Match unit length (bp)')
    ax.set_ylabel('MH over the breakpoint')
    ax.legend((p1[0],p2[0], p3[0]),('Experiment-reference', 'Reference-reference', 'Expected'))
    
    height1 = [rect.get_height() for rect in p1]
    height2 = [rect.get_height() for rect in p2]
    height3 = [rect.get_height() for rect in p3]
    height = [height1,height2,height3]
    
    Mx = np.matrix(height)
    labelheight = list(Mx.max(axis = 0).A1)
    
#    for i in range(N):
#        ax.text(p2[i].get_x(),labelheight[i], 'p = %3.2e' % resultP[0][i],
#        ha = 'center', va = 'bottom')
    for i in range(N):
        ax.text(p2[i].get_x()+0.5*width,labelheight[i]+2, 'p = %2.1e' % resultP[1][i],
        ha = 'center', va = 'bottom', fontsize = 7)        
    for i in range(N):
        ax.text(p3[i].get_x(),labelheight[i]+0.5, 'p = %2.1e' % resultP[2][i],
        ha = 'center', va = 'bottom', fontsize = 7) 
    # the height is 7 and 2 for all data and nonSomatic data
    plt.savefig(figureName,dpi=120) 
    plt.close(1)    
    return
            
def Barplot_3samples_InteC(data, resultP, figureName):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    N = 7 #how many x column
    ind = np.arange(N)
    width = 0.2
    
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    p1 = ax.bar(ind, data[0][:7], width, color = 'indigo' , alpha = 0.75)
    p2 = ax.bar(ind + width, data[1][:7], width, color = 'blue', alpha = 0.75) 
    p3 = ax.bar(ind + 2*width, data[2][:7], width, color = 'powderblue', alpha = 0.75) 
    
    xtickLabel = ['1','2','3','4','5','6','7']
    ax.set_xticks(ind + 1.5*width)
    ax.set_xticklabels(xtickLabel)
    ax.set_xlabel('Match unit length (bp)')
    ax.set_ylabel('Number of Integrations')
    ax.legend((p1[0],p2[0], p3[0]),('Experiment-reference', 'Reference-reference', 'Expected'))
    
    height1 = [rect.get_height() for rect in p1]
    height2 = [rect.get_height() for rect in p2]
    height3 = [rect.get_height() for rect in p3]
    height = [height1,height2,height3]
    
    Mx = np.matrix(height)
    labelheight = list(Mx.max(axis = 0).A1)
    
    for i in range(N):
        ax.text(p2[i].get_x()+0.5*width,labelheight[i]+6, 'p = %2.1e' % resultP[1][i],
        ha = 'center', va = 'bottom',fontsize = 7)        
    for i in range(N):
        ax.text(p3[i].get_x(),labelheight[i]+2, 'p = %2.1e' % resultP[2][i],
        ha = 'center', va = 'bottom', fontsize = 7) 
    # the height is 20, 5 for all data and nonSomatic data 
    plt.savefig(figureName,dpi=120) 
    plt.close(1)    
    return    

def column(matrix, i):
    return [row[i] for row in matrix]
    
def inteCvsFlanklen(seqResult = ''):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
#    import numpy as np
    flk = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80]
    N = range(len(flk))
#    exp_ref, ref_ref, expected = [],[],[]
    _2bp, _3bp, _4bp, _5bp, _6bp, _7bp = [],[],[],[],[],[]
    for f in flk:    
        all_cutAlnResult = cutSeq(seqResult,f) # cut the result into certain flanking region
        _,inteCount = assemblyData(all_cutAlnResult, f)
#        A = np.array(inteCount)
        _2bp.append(column(inteCount, 1))
        _3bp.append(column(inteCount, 2))
        _4bp.append(column(inteCount, 3))
        _5bp.append(column(inteCount, 4))
        _6bp.append(column(inteCount, 5))
        _7bp.append(column(inteCount, 6))
    print '_2bp'
    print _2bp
    print '_3bp'
    print _3bp
    print '_4bp'
    print _4bp
    print '_5bp'
    print _5bp
    print '_6bp'
    print _6bp
    print '_7bp'
    print _7bp
#==============================================================================
#     _2bp = [[280, 275, 246.39], [322, 315, 301.144], [343, 343, 332.386], \
#     [363, 363, 360.922], [370, 370, 370.5], [375, 374, 373.526], \
#     [375, 375, 374.452], [375, 375, 374.766], [375, 375, 374.934], \
#     [375, 375, 374.974], [375, 375, 375.0]]
#     
#     _3bp = [[140, 134, 81.664], [168, 163, 117.232], [192, 189, 149.23], \
#     [228, 234, 200.87], [249, 254, 242.024], [283, 288, 272.5], \
#     [299, 304, 296.096], [312, 319, 313.394], [321, 331, 328.122], \
#     [332, 344, 338.756], [341, 352, 346.974]]
# 
#     _4bp = [[51, 49, 22.316], [65, 64, 33.444], [74, 73, 44.572], \
#     [97, 97, 66.226], [109, 108, 87.02], [123, 121, 105.268], \
#     [134, 135, 122.28], [147, 150, 138.55], [160, 166, 154.406], \
#     [168, 176, 168.406], [180, 191, 182.952]]
# 
#     _5bp = [[16, 17, 5.63], [22, 23, 8.448], [26, 27, 11.522], \
#     [30, 31, 18.076], [36, 36, 24.46], [37, 38, 30.386], \
#     [44, 45, 35.568], [47, 49, 41.676], [51, 52, 48.264], \
#     [56, 58, 53.112], [59, 62, 59.258]]
#     
#     _6bp = [[5, 7, 1.244], [7, 9, 2.008], [7, 9, 2.836], \
#     [8, 10, 4.508], [8, 11, 6.56], [8, 11, 8.29], \
#     [11, 14, 9.796], [12, 15, 11.44], [13, 16, 13.276], \
#     [14, 18, 14.818], [14, 19, 16.13]]
#     
#     _7bp = [[3, 4, 0.354], [4, 5, 0.488], [4, 5, 0.746], \
#     [5, 6, 1.226], [5, 6, 1.738], [5, 6, 2.28], \
#     [5, 6, 2.614], [5, 6, 2.96], [5, 6, 3.558], \
#     [5, 6, 3.872], [5, 6, 4.244]]
#==============================================================================

    
    xtickLabel = [str(f) for f in flk[::2]]

    fig = plt.figure(1, figsize = (12,8))    
    ax = fig.add_subplot(231)
    plt.plot(N, zip(*_2bp)[0], 'r--', linewidth = 2, label = 'exp_ref')
    plt.plot(N, zip(*_2bp)[1], 'b-', linewidth = 2, label = 'ref_ref')
    plt.plot(N, zip(*_2bp)[2], 'gs-.', linewidth = 2, label = 'expected')
    ax.invert_xaxis() 
    plt.title('MH length = 2 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)',fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left',  frameon = False, fontsize = 10)
    
    ax = fig.add_subplot(232)    
    plt.plot(N, zip(*_3bp)[0], 'r--', linewidth = 2,label = 'exp_ref')
    plt.plot(N, zip(*_3bp)[1], 'b-', linewidth = 2,label = 'ref_ref')
    plt.plot(N, zip(*_3bp)[2], 'gs-.',linewidth = 2,label = 'expected')
    ax.invert_xaxis()
    plt.title('MH length = 3 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)', fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left',  frameon = False, fontsize = 10)
    
    ax = fig.add_subplot(233)    
    plt.plot(N, zip(*_4bp)[0], 'r--', linewidth = 2,label = 'exp_ref')
    plt.plot(N, zip(*_4bp)[1], 'b-', linewidth = 2,label = 'ref_ref')
    plt.plot(N, zip(*_4bp)[2], 'gs-.',linewidth = 2,label = 'expected')
    ax.invert_xaxis()
    plt.title('MH length = 4 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)', fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left',  frameon = False, fontsize = 10)

    ax = fig.add_subplot(234)    
    plt.plot(N, zip(*_5bp)[0], 'r--', linewidth = 2,label = 'exp_ref')
    plt.plot(N, zip(*_5bp)[1], 'b-', linewidth = 2,label = 'ref_ref')
    plt.plot(N, zip(*_5bp)[2], 'gs-.',linewidth = 2,label = 'expected')
    ax.invert_xaxis()
    plt.title('MH length = 5 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)', fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left', frameon = False, fontsize = 10)
    
    ax = fig.add_subplot(235)    
    plt.plot(N, zip(*_6bp)[0], 'r--', linewidth = 2,label = 'exp_ref')
    plt.plot(N, zip(*_6bp)[1], 'b-', linewidth = 2,label = 'ref_ref')
    plt.plot(N, zip(*_6bp)[2], 'gs-.',linewidth = 2,label = 'expected')
    ax.invert_xaxis()
    plt.title('MH length = 6 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)', fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left', frameon = False, fontsize = 10)
    
    ax = fig.add_subplot(236)    
    plt.plot(N, zip(*_7bp)[0], 'r--',linewidth = 2, label = 'exp_ref')
    plt.plot(N, zip(*_7bp)[1], 'b-', linewidth = 2,label = 'ref_ref')
    plt.plot(N, zip(*_7bp)[2], 'gs-.',linewidth = 2,label = 'expected')
    ax.invert_xaxis()
    ax.set_ylim([0,7])
    plt.title('MH length = 7 bp', fontsize = 10)
    plt.xlabel('Flanking region size (bp)', fontsize = 8)
    plt.ylabel('Number of Integrations', fontsize = 8)
    ax.set_xticklabels(xtickLabel)
    plt.legend(loc = 'lower left',  frameon = False, fontsize = 10)
    
    plt.savefig('InteCount_vs_FlankingLen',dpi=400) 
#    plt.show()
    plt.close(1)     
    
    return
    
#inteCvsFlanklen()
    
def count2Col(idx):
    '''if index = 0, return B '''
    colName = ''    
    if idx < 25 and idx>-2:
        colName = chr(idx+66)
    elif idx < 701:
        col1 = chr(int((idx+1)/26)+64)
#        col2 = chr((idx+1)%26+65)
        col2 = count2Col((idx+1)%26-1)
        colName = col1+col2
    elif idx < 18277:
        col1 = chr(int((idx-25)/676)+64)
        col2 = count2Col((idx-25)%676+25)
        colName = col1+col2
    else:
        colName = 'unknown'       
    return colName
#==============================================================================
# # test
# print count2Col(0)
# print count2Col(99)  #CW
# print count2Col(100+0)  #CX
# print count2Col(100+100)
#==============================================================================

def findSectionOffsets(text, ch):
    '''find the all offset of ch match to text'''
    import re
    offset = []
    for m in re.finditer(ch, text):
        offset.append(m.start(0))
    return offset
    
def excelLocation(seqResult, flankLen = 100):
    '''this function loacte the MH on the excel file using the groupResultList,
    merList is obtained from the function kmerExactMatch'''
    mutationLists = checkMutation(seqResult, flankLen)
    MHLists = checkMH(seqResult, flankLen)
    mutationLocList = []
    MHLocList = []
    mBlackList, nGreyList = [], []
    count = 0
    for mutation in mutationLists:
        count += 1
        for mu in mutation[0]:
            colName = count2Col(mu[0])
            location1 = colName + str(count*4-2)
            location2 = colName + str(count*4-1)
            mutationLocList.append(location1)
            mutationLocList.append(location2) 
        for mu in mutation[1]:
            colName = count2Col(mu[0]+flankLen)
            location1 = colName + str(count*4-1)
            location2 = colName + str(count*4)            
            mutationLocList.append(location1)
            mutationLocList.append(location2)
    count = 0
    for MH in MHLists:
        count += 1
        for mh in MH[0]:
            colName = count2Col(mh[0])
            location1 = colName + str(count*4-1)
            location2 = colName + str(count*4)
            MHLocList.append(location1)
            MHLocList.append(location2)
        for mh in MH[1]:
            colName = count2Col(mh[0]+flankLen)            
            location1 = colName + str(count*4-2)
            location2 = colName + str(count*4-1)            
            MHLocList.append(location1)
            MHLocList.append(location2)
    count = 0
    for seq in seqResult:
        count += 1
        #find 'M'
        M_offset = findSectionOffsets(seq[2], 'M')
        for offset in M_offset:
            location1 = count2Col(offset) + str(count*4-2)
            location2 = count2Col(offset) + str(count*4-1)
            location3 = count2Col(offset) + str(count*4)
            mBlackList.append(location1)
            mBlackList.append(location2)
            mBlackList.append(location3)
        #find 'N'
        N_offset = findSectionOffsets(seq[2], 'N')
        for offset in N_offset:
            location = count2Col(offset) + str(count*4-1)
            nGreyList.append(location)
    return [mutationLocList, MHLocList, mBlackList, nGreyList]

def writeColorTxt(colorList, txtPrefix = ''):
    with open(txtPrefix+'_blueList.txt','w') as bluef:
        for blue in colorList[0]:
            bluef.writelines(str(blue)+'\n')
    with open(txtPrefix+'_redList.txt','w') as redf:
        for red in colorList[1]:
            redf.writelines(str(red)+'\n')
    with open(txtPrefix+'_blackList.txt', 'w') as greyf:
        for grey in colorList[2]:
            greyf.writelines(str(grey)+'\n')
    with open(txtPrefix+'_greyList.txt', 'w') as greyf:
        for grey in colorList[3]:
            greyf.writelines(str(grey)+'\n')        
    return
    
    
def setExcelColor(muFileTxt, mhFileTxt, mFileTxt, nFileTxt, flankLen = 100):
    '''this function change to excel cell color to red, the location of the cell
    is indicated by the changecolorLocationList.txt'''
     
    from win32com.client import Dispatch
    xl= Dispatch("Excel.Application")
    xl.Visible = True # otherwise excel is hidden
    # newest excel does not accept forward slash in path
    wb = xl.Workbooks.Open(r'D:\dataFolder\HBV\mhData\hccVISP_003977.v2015.12.29\excel4Peiyong_shortSeq.xlsx')
    ws = wb.Worksheets("Sheet2")    
        
#    #set bp to yellow
#    ws.Range("{}:{},{}:{}".format(count2Col(flankLen-1), count2Col(flankLen-1),\
#    count2Col(flankLen), count2Col(flankLen))).Interior.ColorIndex = 6 # set the breakpoint colomn yellow
#    #set mu to blue
#    blue_locf = open(muFileTxt,'r')    
#    for line in blue_locf:
#        loc = line.rstrip()
#        ws.Range(loc).Interior.ColorIndex = 42
#    blue_locf.close()
#    #set mh to red
#    red_locf = open(mhFileTxt,'r')
#    for line in red_locf:
#        loc = line.rstrip()
#        ws.Range(loc).Interior.ColorIndex = 3
#    red_locf.close()
    #set 'M' to black:
    black_locf = open(mFileTxt, 'r')
    for line in black_locf:
        loc = line.rstrip()
        ws.Range(loc).Interior.ColorIndex = 16
    black_locf.close()
    #set 'N' to grey
    grey_locf = open(nFileTxt, 'r')
    for line in grey_locf:
        loc = line.rstrip()
        ws.Range(loc).Interior.ColorIndex = 15
    grey_locf.close()
    
    wb.Save()
    wb.Close() 
    xl.Quit()
    return  
    
#setExcelColor( '777integrations_blueList.txt','777integrations_redList.txt','777integrations_blackList.txt','777integrations_greyList.txt',500 )
#setExcelColor( 'T_blueList.txt','T_redList.txt','T_blackList.txt','T_greyList.txt',100 )

#setExcelColor( 'N_blueList.txt','N_redList.txt','N_blackList.txt','N_greyList.txt',100 )
#setExcelColor( 'NS_blueList.txt','NS_redList.txt','NS_blackList.txt','NS_greyList.txt',100 )
#setExcelColor( 'S_blueList.txt','S_redList.txt','S_blackList.txt','S_greyList.txt',100 )


#test  


#==============================================================================
#5 mutation rate
#==============================================================================
# muLists = checkMutation(sortedSeqResult)
# muC = quantifyMutation(muLists)
# #5.1 plot the figure of mutation rate
# hbvMuperc, hgMuperc =  mutationPerc(muC, sortedSeqResult, 100)
# plotMutationBar(hbvMuperc, hgMuperc, 'mutationRate.png')
#==============================================================================

#6 MH
#==============================================================================
# mhonInte,inteCount = assemblyData(sortedSeqResult, 100)
# mhonInteP = chisquareTest(mhonInte,24)
# inteCountP = chisquareTest(inteCount,24)
# Barplot_3samples_mhonInteC(mhonInte, mhonInteP,'numMHonInte.png')
# Barplot_3samples_InteC(inteCount,inteCountP,'inteCount.png')
# print inteCount
# print inteCountP
#==============================================================================

#7 different flanking region
#==============================================================================
# flk = [20,30,40,50]
# for f in flk:    
#     cutAlnResult = cutSeq(sortedSeqResult,f) # cut the result into certain flanking region
#     mhonInte,inteCount = assemblyData(cutAlnResult, f)
#     mhonInteP = chisquareTest(mhonInte,24)
#     inteCountP = chisquareTest(inteCount,24)
#     Barplot_3samples_mhonInteC(mhonInte, mhonInteP,str(f)+'_numMHonInte.png')
#     Barplot_3samples_InteC(inteCount,inteCountP,str(f)+'_inteCount.png')
#==============================================================================
