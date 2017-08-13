# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 04:27:04 2017

@author: samar
"""

import requests
from lxml import html
import webbrowser
from bs4 import BeautifulSoup
import urllib
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import logging
import collections
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def createLogFile():
    LOG_FILENAME ='logging_example.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)
    logging.info('-----------created log file---------------')
    return;

def loginAndGetTable(session,uname,upassword):
    USERNAME = uname
    PASSWORD = upassword
    
    url ='https://freddiemac.embs.com/FLoan/secure/auth.php'
    
    logging.info('create the payload for first login page')
    
    payload = {'action':'auth.php',
           'username':USERNAME,
           'password':PASSWORD
              }
    
    print("Start login")
    logging.info('Post Request to open the link')
    a=session.post(url, data=payload,cookies={'from-my': 'browser'})
    
    
    secUrl="https://freddiemac.embs.com/FLoan/Data/download.php"
    
    logging.info('create the second payload for second login page')
    
    payloadSec = {
        'action': 'acceptTandC',
        'accept': 'Yes',
        'acceptSubmit':'Continue'
    }
    
    logging.info('Post request to open the second link')
    r = session.post(secUrl, data=payloadSec)
    
    logging.info('Convert into the BeautifulSoup object')
    soup = BeautifulSoup(r.text, 'lxml')
    #print("1.2")
    
    #Find the table based on the class="tableFile"
    logging.info('Find the table based on the class="tableFile"')
    table = soup.find(class_='table1')
    
    if table is None:
         print("Login fail, please check credentials")
         sys.exit("Login fail, please check credentials")
        
    #print(table)
    logging.info('Return the table value return to main function')
    return table;

def downloadFileAndExtract(mainTable,session):
    listforName=[]
    secUrl="https://freddiemac.embs.com/FLoan/Data/download.php"
    
    logging.info('inside the downloadFileAndExtract function')
    
    logging.info('create new path and create physiscal if not exists')
    CurrWorkingDir=os.getcwd();
    #print("CurrWorkingDir-->"+CurrWorkingDir)
    pathforOutputYearwise=CurrWorkingDir+"\\Part1"
    
    # check whether path is present or not
    if not os.path.exists(pathforOutputYearwise):
        # will come if path is not present and will create path(folder)
        os.makedirs(pathforOutputYearwise)
        logging.info('path was not present, created path')
        
    # change the working dir to new path,(to generate the files under particular company folder)
    os.chdir(pathforOutputYearwise)
    logging.info('changed the current Working dir'+str(pathforOutputYearwise))
    
    # code to create the link
    logging.info('Start to create the link , to download the file')
    for row in mainTable.find_all('tr')[1:]:
        # Create a variable of all the <td> tag pairs in each <tr> tag pair,
        col = row.find_all('td')
        #print("*************************")
        column_1 = col[0].findChildren()
        #print(column_1[0].get('href'))
        hrefValue=column_1[0].get('href')
        indexVal=hrefValue.index('?')
       
        rVal=hrefValue[indexVal:len(hrefValue)]
        if 'sample' in rVal:
            listforName.append(secUrl+rVal)
        
    logging.info('Start downloading file')   
    #code to download the file
    for link in listforName:
        fIndex=link.index('=')
        lIndex=link.index('&')
        fileName=link[fIndex+1:lIndex] +".zip"
        #print("file name-->"+fileName)
        #s.get(link)
        response=session.post(link)
        with ZipFile(BytesIO(response.content)) as zfile:
            zfile.extractall(pathforOutputYearwise)
    logging.info('completed downloading file') 
    print("completed downloading file")

def analysisOnOriginationFile():
    #print("3.1")
    completeData=[]
    rowDateForStateWise=["year","Quater"]
    completeDataStateDeliq=[]
    
    completeDataFirstTimeBuyer=[]
    
    rowData=["year","Quater","NumberOFAccount","ROIaVG","ROIMax","ROIlow","MostChanel","MostproductType","MostStateApplication","property Type","LoanPurpose","mostPopseller","serviceName"]
    quatersList=['Q1','Q2','Q3','Q4']
    completeData.append(rowData)
    sam=0
    forFirstTimebuyerHome=0
    #print("3.2")
    pathForOutPut=os.getcwd();
    for i in os.listdir(pathForOutPut):
        if "orig" in i:
            data = pd.read_csv(i,sep="|",header = None)
            
            
            #get the year from file name
            lastIndexof=i.rindex("_")
            indexoftxt=i.index(".")
            yearfromFile=i[lastIndexof+3:indexoftxt]
            #print(yearfromFile)
            #originYear=0,originQuater='q'
            i=0
            sumOfCreditScore=0
            rowCount=0
            #print("3.2.0")
            for index, row in data.iterrows():
                loanSQNumber=row[19]
                
                # if 'LOAN SEQUENCE NUMBER' is blank then will remove complete row 
                if loanSQNumber =="":
                    data=data.drop([index])
                else:
                    # calculate the quater from loanSQNumber number
                    originQuater=loanSQNumber[4:6]
                    
                    # calculate the year from loanSQNumber number
                    originYear=loanSQNumber[2:4]
                    if originYear !=yearfromFile:
                        originYear=yearfromFile
                    
                    # add year value in new column(column no 26)
                    data.set_value(index,'26',originYear)
                    
                    # add year value in new column(column no 27)
                    data.set_value(index,'27',originQuater)
                
                # code to change the year complete year.
                #print("3.2.1")
                if originYear=='99':
                    originYear='1999'
                else:
                    originYear=2000+int(originYear)
                
                #print("originYear--->"+str(originYear))
                #print("3.2.2")
                # fil the credit score with avg value
                
                strcreditScore=row[0]
                #print(str(strcreditScore))
                intgcreditScore=0;
                rowCount=rowCount+1
                
                #print("rowCount--->"+str(rowCount))  pandas.isnull(obj)[source]
                #print("3.2.3")
                if strcreditScore =="   " or pd.isnull(strcreditScore):
                   #print("strcreditScore--->"+strcreditScore
                   avgCreditScore=int(sumOfCreditScore)/int(rowCount)
                   #print("3.2.4")
                   creditScore=int(avgCreditScore)
                   #print("3.2.5")
                   data.set_value(index,'0',creditScore)
                   intgcreditScore=creditScore
                else:
                   #print("3.2.6")
                   sumOfCreditScore=sumOfCreditScore+int(strcreditScore);
                   #print("3.2.7")
                   intgcreditScore=int(strcreditScore)
                   #print("3.2.8")
                #if credit score higher than 700 than good credit score
                if intgcreditScore>=700:
                    data.set_value(index,'28','Y')
                else:
                    data.set_value(index,'28','N')
                    
            #print("3.3")
            for s in quatersList:
                
                # ...............................................................
                # dateframe for first quater loanSQNumber number
                q1DataFrame=data.loc[data['27']==s]
                
                #------------------------- for calulate the sampleQuaterAnalysis
                rowData=[]
                rowData.append(originYear)
                rowData.append(s)
                
                # get the count
                numOFInLoanSQInQ1=q1DataFrame[0].count()
                rowData.append(numOFInLoanSQInQ1)
                
               
                sumOfROI=q1DataFrame[12].sum()
            
                # cal the avg of Q1 ROI
                avgROIInQ1=sumOfROI/numOFInLoanSQInQ1;
                rowData.append(avgROIInQ1)
                
                # get the max value of column
                maxOfROI=q1DataFrame[12].max()
                rowData.append(maxOfROI)
                
                # get the low value of column
                lowOfROI=q1DataFrame[12].min()
                rowData.append(lowOfROI)
                
                #get the mode of Channel 
                mostChanelUsed=q1DataFrame[13].mode()
                rowData.append(mostChanelUsed.to_string().replace("0 ",""))
                
                #get most product type
                mostproductTypeUsed=q1DataFrame[15].mode()
                rowData.append(mostproductTypeUsed.to_string().replace("0 ",""))
                
                #get most property State
                mostStateUsed=q1DataFrame[16].mode()
                rowData.append(mostStateUsed.to_string().replace("0 ",""))
                
                #get property Type
                mostPropertyUsed=q1DataFrame[17].mode()
                rowData.append(str(mostPropertyUsed.to_string()).replace("0 ",""))
                
                #get loan Purpose
                mostPropertyUsed=q1DataFrame[20].mode()
                rowData.append(str(mostPropertyUsed.to_string()).replace("0 ",""))
                
                #get sellerName
                mostPropertyUsed=q1DataFrame[23].mode()
                rowData.append(str(mostPropertyUsed.to_string()).replace("0 ",""))
                
                #get serviceName
                mostPropertyUsed=q1DataFrame[24].mode()
                rowData.append(str(mostPropertyUsed.to_string()).replace("0 ",""))
                
                completeData.append(rowData)
                
                dictDataForStateWise=dict()
                #print("############################")
                # ------------------------- to calculate statewise application
                for index, row in q1DataFrame.iterrows():
                    stateName=row[16]
                    if stateName in dictDataForStateWise:
                        dictDataForStateWise[stateName] += 1
                    else:
                        dictDataForStateWise[stateName] = 1
                        #rowDateForStateWise.append(stateName)
                        
                d = collections.OrderedDict(sorted(dictDataForStateWise.items()))
                
                if sam==0:
                    rowDateForStateWise=["year","Quater"]
                    for key,value in d.items():
                        rowDateForStateWise.append(key)
                    completeDataStateDeliq.append(rowDateForStateWise)
                sam=sam+1    
                
                rowDateForStateWise=[originYear,s]
                #print("^^^^^^^^^^^^^^^------>"+str(originYear))
                for key,value in d.items():
                    percentVal=(float(value)/12500)*100
                    rowDateForStateWise.append(percentVal)
                completeDataStateDeliq.append(rowDateForStateWise)
                rowDateForStateWise=[]
                
                
                #-----------------------------------------------------
                # first Time home buyer
                #-----------------------------------------------------
                
                occupStatusDiction=dict()
                channelStatusDic=dict()
                ftBuyerCount=0
                
                for index, row in q1DataFrame.iterrows():
                    isFirstTimebuyer=row[2]
                    
                    # to get the count of first buyer
                    if isFirstTimebuyer=='Y' or isFirstTimebuyer=='y':
                        ftBuyerCount=ftBuyerCount+1
                    
                    occupStatus=row[7]
                    if occupStatus ==' ':
                        occupStatus='Unknown'
                        
                    # OCCUPANCY Status -increase the value amount and add key if not present in dictionary
                    if occupStatus in occupStatusDiction:
                       occupStatusDiction[occupStatus]+=1
                    else:
                       occupStatusDiction[occupStatus] = 1
                    
                    channelStatus=row[13]
                    if channelStatus ==' ':
                        channelStatus='Unknown'
                    
                    # Channel Status -increase the value amount and add key if not present in dictionary
                    if channelStatus in channelStatusDic:
                       channelStatusDic[channelStatus]+=1
                    else:
                       channelStatusDic[channelStatus] = 1
                
                #sort the dictionary based on key 
                d = collections.OrderedDict(sorted(occupStatusDiction.items()))
                d1 = collections.OrderedDict(sorted(channelStatusDic.items()))
                
                # add the headers  first time only
                if forFirstTimebuyerHome==0:
                    rowFtBuyer=['Year','Quater','First_Time_HomeBuyer']
                    for key,value in d.items():
                        rowFtBuyer.append(key)
                        
                    for key,value in d1.items():
                        rowFtBuyer.append(key)
                    completeDataFirstTimeBuyer.append(rowFtBuyer)
                        
                forFirstTimebuyerHome=forFirstTimebuyerHome+1
                
                # add values in list to write in final file
                rowFtBuyer=[originYear,s,ftBuyerCount]
                
                # add the dictionary values 
                for key,value in d.items():
                    rowFtBuyer.append(value)
                
                # add the dictionary values 
                for key,value in d1.items():
                    rowFtBuyer.append(value)
                    
                completeDataFirstTimeBuyer.append(rowFtBuyer)
                rowFtBuyer=[]
                
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!")       
    out = pd.DataFrame(completeData)
    outPutfileName="sampleQuaterAnalysis.csv"
    out.to_csv(outPutfileName,index=False)
    
    
    out1 = pd.DataFrame(completeDataStateDeliq)
    outPutfileNameSec="stateQuaterAnalysis.csv"
    out1.to_csv(outPutfileNameSec,index=False)
    
    
    out2 = pd.DataFrame(completeDataFirstTimeBuyer)
    outPutfileNameSec="firstTimeHomeBuyerAnalysis.csv"
    out2.to_csv(outPutfileNameSec,index=False)
    
    return out,out1,out2;
    
def analysisOnperformanceFile():
    completeDataForDelinq=[]
    completeDataForZeroBalanceCode=[]
    rowForZeroBalance=['year','ZERO BALANCE CODE(1)','ZERO BALANCE CODE(3)','ZERO BALANCE CODE(6)','ZERO BALANCE CODE(9)']
    
    completeDataForZeroBalanceCode.append(rowForZeroBalance)
    # work on performance file
    quatersList=['Q1','Q2','Q3','Q4']
    forAddDataFrame=0
    pathForOutPut=os.getcwd();
    for i in os.listdir(pathForOutPut):
        if "svcg" in i:
            #print("i value --->"+i)
            data = pd.read_csv(i,sep="|",names=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W'])
            #originYear=0,originQuater='q'
            i=0
            sumOfCreditScore=0
            rowCount=0
            
            for index, row in data.iterrows():
                loanSQNumber=row[0]
                
                # if 'LOAN SEQUENCE NUMBER' is blank then will remove complete row 
                if loanSQNumber =="":
                    data=data.drop([index])
                else:
                    # calculate the quater from loanSQNumber number
                    originQuater=loanSQNumber[4:6]
                    
                    # calculate the year from loanSQNumber number
                    originYear=loanSQNumber[2:4]
                    
                    # add year value in new column(column no 26)
                    data.set_value(index,'26',originYear)
                    
                    # add year value in new column(column no 27)
                    data.set_value(index,'27',originQuater)
                  
            for s in quatersList:
                rowData=[]
                rowData.append(originYear)
                # dateframe for first quater loanSQNumber number
                q1DataFrame=data.loc[data['27']==s]
                rowData.append(s)
                loanDelinQDiction=dict()
                #print("***********************")
                for index, row in q1DataFrame.iterrows():
                    loanSQNumber=row[0]
                    
                    #print("loanSQNumber--->"+loanSQNumber)
                    #print("loanDelinQDiction[loanSQNumber]-->"+loanDelinQDiction[loanSQNumber])
                    #print(loanDelinQDiction[loanSQNumber]==None)
                    
                    if loanSQNumber in loanDelinQDiction:
                        loanDelinQDiction[loanSQNumber]='N'
                    
                    
                    if row[3]!='R' and row[3]!='XX':
                        currDeliQuenctStatus=int(row[3])
                    
                    if(currDeliQuenctStatus>0):
                        loanDelinQDiction[loanSQNumber]='Y'
                
                totalDelinquishCounts=0
                
                #print("---------------------------")
                for key in loanDelinQDiction:
                    if loanDelinQDiction[key]=='Y':
                        totalDelinquishCounts=totalDelinquishCounts+1
                        
                pertotalDelinquishCounts=(float(totalDelinquishCounts)/float(q1DataFrame[0].count()))*100
                
                rowData.append(pertotalDelinquishCounts)
                completeDataForDelinq.append(rowData)
                
               
                #----------------------------------------------
                
             # Code to get row that have ZERO BALANCE CODE=9   
            filterdataForZero=data[(data.I== 9)]
            acount=filterdataForZero['A'].count()
            
            if forAddDataFrame==0:
                result=filterdataForZero
                forAddDataFrame=forAddDataFrame+1
            else:
                frames = [filterdataForZero, result]
                result = pd.concat(frames)
            
            # --------------------------------------------------
            # Get the count of different ZERO BALANCE CODE, year wise
            rowForZeroBalance=[]
            rowForZeroBalance.append(originYear)
            
            ZeroBalanceCodeForOne=data[(data.I== 1)]
            ZeroBalanceCodeForOneCount=ZeroBalanceCodeForOne['A'].count()
            rowForZeroBalance.append(ZeroBalanceCodeForOneCount)
            
            ZeroBalanceCodeForThree=data[(data.I== 3)]
            ZeroBalanceCodeForThreeCount=ZeroBalanceCodeForThree['A'].count()
            rowForZeroBalance.append(ZeroBalanceCodeForThreeCount)
            
            ZeroBalanceCodeForSix=data[(data.I== 6)]
            ZeroBalanceCodeForSixCount=ZeroBalanceCodeForSix['A'].count()
            rowForZeroBalance.append(ZeroBalanceCodeForSixCount)
            
            ZeroBalanceCodeForNine=data[(data.I== 9)]
            ZeroBalanceCodeForNineCount=ZeroBalanceCodeForNine['A'].count()
            rowForZeroBalance.append(ZeroBalanceCodeForNineCount)
            
            completeDataForZeroBalanceCode.append(rowForZeroBalance)
            
            
    outDelin = pd.DataFrame(completeDataForDelinq)
    outPutfileName="delinQuaterAnalysis.csv"
    outDelin.to_csv(outPutfileName,index=False)
    
    outForZeroNine = pd.DataFrame(result)
    outPutfileForZeroNine="FileForZeroBalanceCodeNine.csv"
    outForZeroNine.to_csv(outPutfileForZeroNine,index=False)
    
    outForZeroBalanceCode = pd.DataFrame(completeDataForZeroBalanceCode)
    outPutfileForBalanceCode="FileForZeroBalanceCode.csv"
    outForZeroBalanceCode.to_csv(outPutfileForBalanceCode,index=False)

def generateGraphROI(getfnCompleteData):  
    # function to generate the graph
    # data to plot
    Q1values = []
    Q2values = []
    Q3values = []
    Q4values = []
    #print("inside generateGraphROI")
    
    allQuaterValues=[]
    # iterate over the data frame and extract the information in quater list
    for index, row in getfnCompleteData.iterrows():
        quaterValue=row[1]
        
        if quaterValue=='Q1':
            Q1values.append(row[4])
            allQuaterValues.append(row[4])
        elif quaterValue=='Q2':
            Q2values.append(row[4])
            allQuaterValues.append(row[4])
        elif quaterValue=='Q3':
            Q3values.append(row[4])
            allQuaterValues.append(row[4])
        elif quaterValue=='Q4':
            Q4values.append(row[4])
            allQuaterValues.append(row[4])
    
    #print("Q1values->"+str(Q1values))
    #print("Q2values->"+str(Q2values))
    #print("Q3values->"+str(Q3values))
    #print("Q4values->"+str(Q4values))
    n_groups = len(Q1values)
    
    # create plot
    #fig, ax = plt.subplots()
    # Assign the howmany groups will be there
    index = np.arange(n_groups)
    bar_width = 0.2
    opacity = 0.9
    plt.figure(figsize=(13,5))
     
    rects1 = plt.bar(index, Q1values, bar_width,
                     alpha=opacity,
                     color='firebrick',
                     label='Q1')
     
    rects2 = plt.bar(index + bar_width, Q2values, bar_width,
                     alpha=opacity,
                     color='orange',
                     label='Q2')
    
    rects3 = plt.bar(index + bar_width + bar_width, Q3values, bar_width,
                     alpha=opacity,
                     color='yellowgreen',
                     label='Q3')
     
    rects4 = plt.bar(index + bar_width + bar_width + bar_width, Q4values, bar_width,
                     alpha=opacity,
                     color='deepskyblue',
                     label='Q4')
    
    # assign x axix the label
    plt.xlabel('Years 1999-2016')
    
    # Assign y axix label name
    plt.ylabel('ROI')
    
    plt.title('ROI over the Years')
    plt.yticks(index + bar_width+bar_width+bar_width, ['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
    plt.xticks(index + bar_width+bar_width+bar_width, ['99','00', '01', '02','03', '04', '05','06','07', '08','09', '10','11','12', '13', '14','15','16'])
    plt.legend()
     
    plt.tight_layout()
    plt.show()
    return allQuaterValues;

def lineGraphROI(allQuaterValuesCombine):
    plt.figure(figsize=(13,5))
    plt.plot(allQuaterValuesCombine)
    plt.ylabel('ROI')
    plt.xlabel('Year')
    plt.xticks(16, ['99','00', '01', '02','03', '04', '05','06','07', '08','09', '10','11','12', '13', '14','15','16'])
    plt.show()
    return;

def barGraphForFirstTimeBuyer(fnCompleteDataFirstTimeBuyer):
    Q1values = []
    Q2values = []
    Q3values = []
    Q4values = []
    #print("inside generateGraphROI")
    
    allQuaterValuesFirstTimeBuyer=[]
    # iterate over the data frame and extract the information in quater list
    for index, row in fnCompleteDataFirstTimeBuyer.iterrows():
        quaterValue=row[1]
        
        if quaterValue=='Q1':
            Q1values.append(row[2])
            allQuaterValuesFirstTimeBuyer.append(row[2])
        elif quaterValue=='Q2':
            Q2values.append(row[2])
            allQuaterValuesFirstTimeBuyer.append(row[2])
        elif quaterValue=='Q3':
            Q3values.append(row[2])
            allQuaterValuesFirstTimeBuyer.append(row[2])
        elif quaterValue=='Q4':
            Q4values.append(row[2])
            allQuaterValuesFirstTimeBuyer.append(row[2])
    '''
    print("Q1values->"+str(Q1values))
    print("Q2values->"+str(Q2values))
    print("Q3values->"+str(Q3values))
    print("Q4values->"+str(Q4values))
    '''
    n_groups = len(Q1values)
    
    # create plot
    #fig, ax = plt.subplots()
    # Assign the howmany groups will be there
    index = np.arange(n_groups)
    bar_width = 0.2
    opacity = 0.9
    plt.figure(figsize=(13,5))
     
    rects1 = plt.bar(index, Q1values, bar_width,
                     alpha=opacity,
                     color='firebrick',
                     label='Q1')
     
    rects2 = plt.bar(index + bar_width, Q2values, bar_width,
                     alpha=opacity,
                     color='orange',
                     label='Q2')
    
    rects3 = plt.bar(index + bar_width + bar_width, Q3values, bar_width,
                     alpha=opacity,
                     color='yellowgreen',
                     label='Q3')
     
    rects4 = plt.bar(index + bar_width + bar_width + bar_width, Q4values, bar_width,
                     alpha=opacity,
                     color='deepskyblue',
                     label='Q4')
    
    # assign x axix the label
    plt.xlabel('Years 1999-2016')
    
    # Assign y axix label name
    plt.ylabel('First Time Buyer')
    
    plt.title('First TimeHome buyer over the Years')
    plt.yticks(index + bar_width+bar_width+bar_width, ['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
    plt.xticks(index + bar_width+bar_width+bar_width, ['99','00', '01', '02','03', '04', '05','06','07', '08','09', '10','11','12', '13', '14','15','16'])
    plt.legend()
     
    plt.tight_layout()
    plt.show()
    return allQuaterValuesFirstTimeBuyer;

def lineGraphFirstTimeBuyer(allQuaterValuesCombineFirstBuy):
    plt.figure(figsize=(13,5))
    plt.plot(allQuaterValuesCombineFirstBuy)
    plt.ylabel('First Time Buyer')
    plt.xlabel('Year')
    #plt.xticks(16, ['99','00', '01', '02','03', '04', '05','06','07', '08','09', '10','11','12', '13', '14','15','16'])
    plt.show()
    return;  
        
def pieChartOCCUPANCYSTATUS(fnCompleteDataFirstTimeBuyer):
    
    #print(fnCompleteDataFirstTimeBuyer)
    year99for='1999'
    iValueFor99=0
    oValueFor99=0
    sValueFor99=0
    
    year15for='2015'
    iValueFor15=0
    oValueFor15=0
    sValueFor15=0
    
    for index, row in fnCompleteDataFirstTimeBuyer.iterrows():
        quaterValue=row[0]
        if year99for== quaterValue:
            iValueFor99=iValueFor99+row[3]
            print(iValueFor99)
            oValueFor99=oValueFor99+row[4]
            sValueFor99=sValueFor99+row[5]
            
        
        if year15for == str(quaterValue):
            print("inside condition")
            iValueFor15=iValueFor15+row[3]
            print(iValueFor15)
            oValueFor15=oValueFor15+row[4]
            print(oValueFor15)
            sValueFor15=sValueFor15+row[5]
        
    avgiValueFor99=iValueFor99/4;
    avgoValueFor99=oValueFor99/4
    avgsValueFor99=sValueFor99/4
    
    
    #print("for year 1999")
    totalfor99=avgiValueFor99+avgoValueFor99+avgsValueFor99
    
    percentivalue99=(avgiValueFor99/totalfor99)*100
    percentovalue99=(avgoValueFor99/totalfor99)*100
    percentsvalue99=(avgsValueFor99/totalfor99)*100
    
    sizesfor99=[]
    sizesfor99.append(percentivalue99)
    sizesfor99.append(percentovalue99)
    sizesfor99.append(percentsvalue99)        
                    
    labels = ['Investment', 'Owner Occupied', 'Second Home']
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.1, 0, 0)  # explode 1st slice
 
    # Plot
    plt.pie(sizesfor99, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=240)
    
    plt.axis('equal')
    plt.show()                
                
    # for year 15
    #print("for year 2015")
    avgiValueFor15=iValueFor15/4
    avgoValueFor15=oValueFor15/4
    avgsValueFor15=sValueFor15/4
    
    totalfor15=avgiValueFor15+avgoValueFor15+avgsValueFor15     
    #print(avgiValueFor15)
    #print(avgoValueFor15)
    #print(avgsValueFor15)
    #print("totalfor15-->"+str(totalfor15))
    
    percentivalue15=(avgiValueFor15/totalfor15)*100
    percentovalue15=(avgoValueFor15/totalfor15)*100
    percentsvalue15=(avgsValueFor15/totalfor15)*100
    
    sizesfor15=[]
    sizesfor15.append(percentivalue15)        
    sizesfor15.append(percentovalue15)
    sizesfor15.append(percentsvalue15)          
    
    labels = ['Investment', 'Owner Occupied', 'Second Home']
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.1, 0, 0)  # explode 1st slice
 
    # Plot
    plt.pie(sizesfor15, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
   
    plt.axis('equal')
    plt.show()
    
    # code to create the pieChartForChannel
def pieChartForChannel(fnCompleteDataFirstTimeBuyer):
    #print(fnCompleteDataFirstTimeBuyer)
    year99for='1999'
    bValueFor99=0
    cValueFor99=0
    rValueFor99=0
    tValueFor99=0
    
    year15for='2015'
    bValueFor15=0
    cValueFor15=0
    rValueFor15=0
    tValueFor15=0
    
    for index, row in fnCompleteDataFirstTimeBuyer.iterrows():
        quaterValue=row[0]
        if year99for== quaterValue:
            bValueFor99=bValueFor99+row[6]
            
            cValueFor99=cValueFor99+row[7]
            rValueFor99=rValueFor99+row[8]
            tValueFor99=tValueFor99+row[9]
        
        if year15for == str(quaterValue):
            #print("inside condition")
            bValueFor15=bValueFor15+row[6]
            #print(iValueFor15)
            cValueFor15=cValueFor15+row[7]
            #print(oValueFor15)
            rValueFor15=rValueFor15+row[8]
            tValueFor15=tValueFor15+row[9]
        
    avgbValueFor99=bValueFor99/4;
    avgcValueFor99=cValueFor99/4
    avgrValueFor99=rValueFor99/4
    avgtValueFor99=tValueFor99/4
    
    
    #print("for year 1999 channel")
    totalfor99=avgbValueFor99+avgcValueFor99+avgrValueFor99+avgtValueFor99
    
    percentbvalue99=(avgbValueFor99/totalfor99)*100
    percentcvalue99=(avgcValueFor99/totalfor99)*100
    percentrvalue99=(avgrValueFor99/totalfor99)*100
    percenttvalue99=(avgtValueFor99/totalfor99)*100
                    
    
    sizesfor99=[]
    sizesfor99.append(percentbvalue99)
    sizesfor99.append(percentcvalue99)
    sizesfor99.append(percentrvalue99)    
    sizesfor99.append(percenttvalue99)        
                    
    labels = ['Broker', 'Correspondent', 'Retail','TPO Not Specified']
    colors = ['gold', 'yellowgreen', 'lightcoral','deepskyblue']
    explode = (0.1, 0, 0,0)  # explode 1st slice
 
    # Plot
    plt.pie(sizesfor99, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=240)
    
    plt.axis('equal')
    plt.show()                
                
    # for year 15
    print("for year 2015 channel")
    avgbValueFor15=bValueFor15/4
    avgcValueFor15=cValueFor15/4
    avgrValueFor15=rValueFor15/4
    avgtValueFor15=tValueFor15/4
    
    totalfor15=avgbValueFor15+avgcValueFor15+avgrValueFor15+avgtValueFor15  
    
    print(avgbValueFor15)
    print(avgcValueFor15)
    print(avgrValueFor15)
    print(avgtValueFor15)
    #print("totalfor15-->"+str(totalfor15))
    
    percentbvalue15=(avgbValueFor15/totalfor15)*100
    percentcvalue15=(avgcValueFor15/totalfor15)*100
    percentrvalue15=(avgrValueFor15/totalfor15)*100
    percenttvalue15=(avgtValueFor15/totalfor15)*100
    
    sizesfor15=[]
    sizesfor15.append(percentbvalue15)        
    sizesfor15.append(percentcvalue15)
    sizesfor15.append(percentrvalue15)  
    sizesfor15.append(percenttvalue15)          
    
    labels = ['Broker', 'Correspondent', 'Retail','TPO Not Specified']
    colors = ['gold', 'yellowgreen', 'lightcoral','deepskyblue']
    explode = (0.1, 0, 0,0)  # explode 1st slice
 
    # Plot
    plt.pie(sizesfor15, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
   
    plt.axis('equal')
    plt.show()
    
if __name__ == "__main__":
    createLogFile()
    logging.info('After log file creation')
    
    logging.info('creating session for URL Login')
    session = requests.Session()
    uname=sys.argv[1]
    password=sys.argv[2]
    
    logging.info('calling loginAndGetTable function and passing session obj')
    mainTable=loginAndGetTable(session,uname,password)
    
    logging.info('calling downloadFileAndExtract function and passing mainTable and session obj')
    #downloadFileAndExtract(mainTable,session)
    
    os.chdir("C:\\Samarth\\Semester-4\\ADS\\Assignments\\Assignment_02_midterm\\Part1")
    logging.info('calling downloadFileAndExtract function and passing mainTable and session obj')
    fnCompleteData,fnCompleteDataStateDeliq,fnCompleteDataFirstTimeBuyer=analysisOnOriginationFile()
    
    tempfnCompleteData=fnCompleteData
    tempfnCompleteDataStateDeliq=fnCompleteDataStateDeliq
    tempfnCompleteDataFirstTimeBuyer=fnCompleteDataFirstTimeBuyer
    
    logging.info('calling downloadFileAndExtract function and passing mainTable and session obj')
    #analysisOnperformanceFile()
    
    logging.info('calling allQuaterValuesCombine function and passing tempfnCompleteData obj')
    allQuaterValuesCombine=generateGraphROI(tempfnCompleteData)
    
    logging.info('calling generateGraphROI function and passing allQuaterValuesCombine obj')
    lineGraphROI(allQuaterValuesCombine)
    
    logging.info('calling allQuaterValuesCombineFirstTimeBuyer function and passing allQuaterValuesCombine obj')
    allQuaterValuesCombineFirstTimeBuyer=barGraphForFirstTimeBuyer(fnCompleteDataFirstTimeBuyer)
    
    logging.info('calling generateGraphROI function and passing allQuaterValuesCombine obj')
    lineGraphFirstTimeBuyer(allQuaterValuesCombineFirstTimeBuyer)
    
    # pie chart for OCCUPANCY STATUS
    pieChartOCCUPANCYSTATUS(fnCompleteDataFirstTimeBuyer)
    
    pieChartForChannel(fnCompleteDataFirstTimeBuyer.fillna(0))
    
    