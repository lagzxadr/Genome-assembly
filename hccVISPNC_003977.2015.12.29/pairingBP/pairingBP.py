#!/mnt/software/unstowable/anaconda/bin/python
"""
Created on Tue Feb 23 10:52:41 2016
this program does the matching and pairing of break point
@author: yanj
"""
###############################################################################
def checkMatch(integration1, integration2, diff):
    '''check if the hbvStrand and hgStrand are complementary within the set of 
    data, integration1 and integration2 are dataEntry from rawData(extracted
    using extractInfoFromTxt) hbvStrand = dataEntry[0], hgStrand = dataEntry[3]'''
    Match = False
    matchDict = {'+':'-','-':'+'}
    if matchDict[integration1[0]] == integration2[0] and \
        matchDict[integration1[3]] == integration2[3]:
        if integration1[3] == '+' and int(integration1[4]) > int(integration2[4])\
            and abs(int(integration1[4]) - int(integration2[4])) < diff:
            Match = True 
        if integration1[3] == '-' and int(integration2[4]) > int(integration1[4])\
            and abs(int(integration1[4]) - int(integration2[4])) < diff:
            Match = True
    return Match
    
def checkMatch_wrongversion(integration1, integration2, diff):
    '''this wrong version does not consider the orientation of hg, do this to 
    check if the VISP output the wrong sign'''
    Match = False
    matchDict = {'+':'-','-':'+'}
    if matchDict[integration1[0]] == integration2[0] and \
        matchDict[integration1[3]] == integration2[3]: # sign complementary
        Match = True
#        if abs(int(integration1[4]) - int(integration2[4])) < diff:
#            Match = True 
#        if abs(int(integration1[4]) - int(integration2[4])) < diff:
#            Match = True
    return Match

def finding_pair(rawData, humanDiff):
    from itertools import combinations
    pairRes = []
    pairCount = 0
    chrNum = '1'
    chrData = []
    for data in rawData:
        if (data[2] != chrNum and chrData != []):
    #        print chrNum, len(chrData)        
            sampleIDs = sorted(set([chrData[i][9] for i in range(len(chrData))])) 
            # get the sampleIDs 
    #        print sampleIDs
            for sampleID in sampleIDs:
                sampleD = [d for d in chrData if d[9] == sampleID] # get data for certain sampleID
                if len(sampleD)> 1:
    #                print sampleID, ": ", len(sampleD), 'integrations'
                    for (i,j) in combinations(range(len(sampleD)),2):
                        if checkMatch(sampleD[i],sampleD[j], humanDiff):
                            pairCount += 1
                            pairRes.append((sampleD[i],sampleD[j]))
                            print 'chr',chrNum+': '+sampleID,' PE='+sampleD[j][7]+'/'+sampleD[i][7],' SP='+sampleD[j][8]+'/'+sampleD[i][8]
                            print '('+sampleD[i][3]+')_____|('+sampleD[i][0]+')-------|_____'
                            print sampleD[j][4]+'|'+sampleD[j][1]+'---'+sampleD[i][1]+'|'+sampleD[i][4]
                            print 
            chrNum = data[2]
            chrData = []
        chrData.append(data)
    #for last chromoson:
    #print chrNum, len(chrData)        
    sampleIDs = sorted(set([chrData[i][9] for i in range(len(chrData))]))
    #print sampleIDs
    for sampleID in sampleIDs:
        sampleD = [d for d in chrData if d[9] == sampleID]
    
        if len(sampleD)> 1:
    #       print sampleID, ": ", len(sampleD), 'integrations'
            for (i,j) in combinations(range(len(sampleD)),2):
                if checkMatch(sampleD[i],sampleD[j]):
                    pairCount += 1
                    pairRes.append((sampleD[i],sampleD[j]))
                    print 'chr'+chrNum+': '+sampleID
                    print '('+sampleD[i][3]+')_____|('+sampleD[i][0]+')-------|_____'
                    print sampleD[j][4]+'|'+sampleD[j][1]+'---'+sampleD[i][1]+'|'+sampleD[i][4]    
    
    chrNum = data[2] 
    return pairRes, pairCount
    
def plotPairCountvsDiff(diffs,pairCountRes, prefix = 'wrong_version_'):
    '''plot the # pairing vs loc diff'''          
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt    
    fig = plt.figure(1)        
    plt.plot (diffs, pairCountRes, 'ro',  alpha = 0.75)
    plt.xlabel('location difference on human DNA (bp)')
    plt.ylabel('Paired Break point')
    plt.savefig(prefix+'pairCountvsDiff',dpi=200) 
#    fig.close(1)     
    return     
    
###############################################################################    
import funcSum as fs
import os
from operator import itemgetter

writeBPList = False
writePairingSeq = False
plot = False
#diffs = [1]
diffs = [1,5,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,\
    5000,10000,50000,100000]
bpFilePath = '/mnt/projects/yanj/hcc/hccVISPNC_003977.2015.12.29/bpFiles/'
HBV_refName = '/mnt/projects/yanj/hcc/reference/NC_003977/NC_003977.fa'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
###############################################################################

filelist = os.listdir(bpFilePath)
filelist.sort() ##sort
#1. extract data
rawData = []
for f in filelist:
    bpFileName = bpFilePath + f
    data = fs.extractInfoFromTxt(bpFileName, [2,3,4,5,6,19,24,16,17])
    rawData.extend(data)    
rawData_filtered = rawData
#rawData_filtered = fs.excludeLowPE_v2(rawData, 1) 
#rawData_filtered, seqResult_filtered = fs.theSmallFilter(HBV_refName, hg_refName, rawData, 100)  
print 'finish filter  PE > 1 integrations...'  
print '{} integrations with PE > 1 are for analysis...'.format(len(rawData_filtered))
print '########################'
if writeBPList: 
    fs.writeExcelBPList(rawData_filtered, 'rawBPforHomer')  
    
###############################################################################

print 'no diff limitation on human DNA'   
    
#sort the rawData based on chr# and sampleID
rawData_filteredSorted = sorted(rawData_filtered, key = itemgetter(2,9,7,8), reverse = False)
pairCountRes = []    
for diff in diffs: 
    print 'start pairing break points...'
#    print 'the location difference on human DNA is at most {}bp'.format(diff)   
    pairRes, pairCount =  finding_pair(rawData_filteredSorted, diff)
    print 'pairing finished.' 
    print 'totally, {} pairing is found out of {} integrations.'. format(pairCount, len(rawData_filtered))
    pairCountRes.append(pairCount)  


if plot:
    plotPairCountvsDiff(diffs[:21], pairCountRes[:21])     
for (diff, pairc) in zip(diffs, pairCountRes):
    print pairc
###############################################################################

pairResAll = []
c1,c2,c3,c4 = 0,0,0,0
c00 = 0
c11 = 0
for pair in pairRes:
    pairResAll.append(pair[0])
    pairResAll.append(pair[1])    
    if (int(pair[0][1]) > 1750 and int(pair[0][1]) < 1850 and \
        int(pair[1][1]) >= 1850 and pair[0][0] == '+') or \
        (int(pair[1][1]) > 1750 and int(pair[1][1]) < 1850 and \
        int(pair[0][1]) >= 1850 and pair[0][0] == '-'):
        c3 += 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]
        
    elif (int(pair[0][1]) > 1750 and int(pair[0][1]) < 1850 and \
        int(pair[1][1]) >= 1850 and pair[0][0] == '-') or \
        (int(pair[1][1]) > 1750 and int(pair[1][1]) < 1850 and \
        int(pair[0][1]) >= 1850 and  pair[0][0] == '+'):
        c2 += 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]
    elif (int(pair[0][1]) > 1750 and int(pair[0][1]) < 1850 and \
        int(pair[1][1]) <= 1750 and pair[0][0] == '+') or \
        (int(pair[1][1]) > 1750 and int(pair[1][1]) < 1850 and \
        int(pair[0][1]) <= 1750 and  pair[0][0] == '-'):
        c1 += 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]
    elif (int(pair[0][1]) > 1750 and int(pair[0][1]) < 1850 and \
        int(pair[1][1]) <= 1750 and pair[0][0] == '-') or \
        (int(pair[1][1]) > 1750 and int(pair[1][1]) < 1850 and \
        int(pair[0][1]) <= 1750 and  pair[0][0] == '+'):
        c4 += 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]
        ###
    elif (int(pair[0][1]) > 1750 and int(pair[0][1]) < 1850 and    \
        int(pair[1][1]) > 1750 and int(pair[1][1]) < 1850):
        c00 += 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]  
    else: 
        c11+= 1
#        print 'chr'+pair[0][2]+': '+pair[0][9]
#        print '('+pair[0][3]+')_____|('+pair[0][0]+')-------|_____'
#        print pair[1][4]+'|'+pair[1][1]+'---'+pair[0][1]+'|'+pair[0][4]         
    
#print c00,c11,c1,c2,c3,c4 
#dif = 20: 1,8,3,1,7,0 total 20pair
#dif = 40: 2,14,11,3,11,0 total 41 pair
print '########################'
print '_____|~1800bp-----X|_________'
print '{} insertions are short insert with X < 1750bp'.format(c1)
print '{} insertions are short insert with X > 1850bp'.format(c2)
print '{} insertions are long insert with X < 1750bp'.format(c4)
print '{} insertions are long insert with X > 1850bp'.format(c3)
print '{} insertions are with 1750 bp < X < 1850bp'.format(c00)
print 'check BP around 1800 bp finished.'


###############################################################################
#check the MH
HBV_refName = '/mnt/projects/yanj/hcc/reference/NC_003977/NC_003977.fa'
hg_refName = '/mnt/projects/yanj/hcc/reference/human_g1k/human_g1k_v37.fasta'
fl = 100 # flanking region length
seqResult = fs.extractRefSeq(HBV_refName, hg_refName, pairResAll, fl)
if writePairingSeq:
    fs.writeSeq2Csv(str(len(seqResult))+'PairingBPSeq.csv', seqResult)
    colorList = fs.excelLocation(seqResult, fl)
    fs.writeColorTxt(colorList, str(len(seqResult))+'integrations')
        
    


