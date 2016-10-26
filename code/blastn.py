#! usr/bin/env python2.7

"""
Created on Fri Jan 22 18:29:26 2016

@author: yanj


"""
def helpFunc():
      print '''
blastn.py: reads the DNA sequence and blast the sequence.

blastn.py [-h] <DNA sequene>
-h:              print this message
<DNA sequence>:  DNA sequence
'''
    
import sys
import getopt

print sys.argv
o,a = getopt.getopt(sys.argv[1:], 'h:e')
opts = {}
E_VALUE_THRESH = 0.01
for k,v in o:
    opts[k] = v
if 'h' in opts.keys():
    helpFunc(); sys.exit(0)
if len(a)< 1:
    helpFunc();sys.exit('input DNA string is missing!')
fasta_string = a[0]
if 'e' in opts.keys():
    if opts['e'] < 0:
        print "e value threshold should be positive!"; sys.exit(0)
    E_VALUE_THRESH = opts['l']

from Bio.Blast import NCBIWWW,NCBIXML
#fasta_string = open('myseq.fa').read()
#fasta_string = raw_input('please copy the DNA string here: ')
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
blast_record = NCBIXML.read(result_handle)

#E_VALUE_THRESH = 0.01
for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        if hsp.expect < E_VALUE_THRESH:
            print '******Alignment******'
            print 'sequence:', alignment.title
            print 'length: ', alignment.length
            print 'e value: ', hsp.expect
            print hsp.query
            print hsp.match
            print hsp.sbjct
            
