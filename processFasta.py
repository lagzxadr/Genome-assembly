#!/usr/bin/env python2.7
"""
Created on Fri Jan 22 11:02:51 2016

@author: yanj
"""
def helpFunc():
    print '''
processfasta.py: reads a FASTA file and builds a dictionary with all sequences 
bigger than a given length

processfasta.py [-h] [-l <length>] <filename>    
    -h          print this message
    -l <length> filter all sequences with a length smaller than <length>
                (default <length> =0)
 <filename>     the file has to be in FASTA format
 '''
 
import sys
import getopt

o,a = getopt.getopt(sys.argv[1:], 'l:h')
opts = {}
seqLen = 0


for k,v in o:
    opts[k] = v
if 'h' in opts.keys():
    helpFunc()
    sys.exit()
if len(a)< 1:
    helpFunc();sys.exit('input fasta file is missing!')
fileName = a[0]
if 'l' in opts.keys():
    if opts['l'] < 0:
        print "length of sequence should be positive!"; sys.exit(0)
    seqLen = opts['l']
    

try: 
    f = open(fileName)
except IOError:
    print "File %s does not exist!" % fileName
seqs = {}

f.readline()
lineLen = len(f.readline().rstrip())

f.seek(0,0)
for line in f:   
    line = line.rstrip()
    if line.startswith('>'):
        seqID= line.split()[0][1:]
        seqs[seqID] = ''
    else:
        line = line.rstrip()                  
        seqs[seqID] = seqs[seqID] + line
f.close()
        
