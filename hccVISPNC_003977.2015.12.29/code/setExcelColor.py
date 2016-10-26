#!/bin/python/
"""
Created on Fri Feb 19 16:07:48 2016

@author: yanj
"""
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
    
def setExcelColor(muFileTxt, mhFileTxt, mFileTxt, nFileTxt, flankLen = 100):
    '''this function change to excel cell color to red, the location of the cell
    is indicated by the changecolorLocationList.txt'''
     
    from win32com.client import Dispatch
    xl= Dispatch("Excel.Application")
    xl.Visible = True # otherwise excel is hidden
    # newest excel does not accept forward slash in path
    wb = xl.Workbooks.Open(r'D:\dataFolder\HBV\mhData\hccVISP_003977.v2015.12.29\excelFiles\excel4Peiyong_shortSeq_777&380.xlsx')
    ws = wb.Worksheets("Sheet1")    
        
    #set bp to yellow
    ws.Range("{}:{},{}:{}".format(count2Col(flankLen-1), count2Col(flankLen-1),\
    count2Col(flankLen), count2Col(flankLen))).Interior.ColorIndex = 6 # set the breakpoint colomn yellow
    #set mu to blue
    blue_locf = open(muFileTxt,'r')    
    for line in blue_locf:
        loc = line.rstrip()
        ws.Range(loc).Interior.ColorIndex = 42
    blue_locf.close()
    #set mh to red
    red_locf = open(mhFileTxt,'r')
    for line in red_locf:
        loc = line.rstrip()
        ws.Range(loc).Interior.ColorIndex = 3
    red_locf.close()
#    set 'M' to black:
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
    
setExcelColor( '175integrations_blueList.txt','175integrations_redList.txt','175integrations_blackList.txt','175integrations_greyList.txt',500 )
#setExcelColor( 'T_blueList.txt','T_redList.txt','T_blackList.txt','T_greyList.txt',100 )

#setExcelColor( 'N_blueList.txt','N_redList.txt','N_blackList.txt','N_greyList.txt',100 )
#setExcelColor( 'NS_blueList.txt','NS_redList.txt','NS_blackList.txt','NS_greyList.txt',100 )
#setExcelColor( 'S_blueList.txt','S_redList.txt','S_blackList.txt','S_greyList.txt',100 )