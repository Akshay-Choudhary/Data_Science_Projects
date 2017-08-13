# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 21:49:24 2017

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
import csv
import urllib.request
import operator

def createLogFile():
    LOG_FILENAME ='logging_example.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)
    logging.info('-----------created log file---------------')
    return;

def readAndGenerateGrpah():
    os.chdir('C:\Samarth\Semester-4\ADS\Assignments\Assignment_02\Part1')
    logging.info("inside the readAndGenerateGrpah")
    #for year count
    ansDiction = {'2007': 0,'2008': 0,'2009': 0,'2010': 0,'2011': 0}
    
    #for state and year count
    # create and initialize the varibles for future use
    logging.info("create and initialize the varibles for future use")
    stateAndyearDic={}
    empTitleAndyearDic={}
    purposeAndyearDic={}
    varifiStatusAndyearDic={}
    amountAndYearDic={}
    roiAndyearDic={}
    deliquentAndYearDic={}
    
    print(os.getcwd())
    
    count=0;
    # open combine data file to read
    logging.info("open combine data file to read")
    with open('LoanoutFileDec.csv', 'rt',encoding="utf8") as fr:
         count=0
         skiprow=1
         
         # used reader function to read the file
         logging.info("used reader function to read the file")
         reader = csv.reader(fr, delimiter=',')
         blankRowCount=0
         # iterate over the reader to get each row
         for row in reader:
             global issue_d;
             global firstIndex;
             global year;
             
             # first two rows dont have required values,so will consider it
             # if the row is not require than will go to next step
             if(count<2):
                 count=count+1
                 continue;
             if(count>5):
                  break;
             if(len(row)==0):
                 blankRowCount=blankRowCount+1
                 continue;
             if(blankRowCount>2):
                 break;
             # if row[0] has 'Loans that do not meet the credit policy' then, then go to next row
             if(row[0]=='Loans that do not meet the credit policy'):
                 print(row[0]);
                 continue;
             
             # in every file at the end 'total' has given, if get the total then terminate it
             if "Total" in row[0]:
                 print(row[0])
                 break;
             # check the row length and condition setisfy than will go on to next step
             if(len(row)>16):
                 issue_d=row[15]
                 #print(issue_d)
                 firstIndex=issue_d.index('-')
                 monthVal=issue_d[0:firstIndex]
                 #q1=['Jan','Feb','Mar']
                 #q2=['Apr','May','Jun']
                 #q3=['Jul','Aug','Sep']
                 #q4=['Oct','Nov','Dec']
                 
                 #QuaterValue=""
                 #if monthVal in q1:
                 #    QuaterValue="Q1"
                 #elif monthVal in q2:
                 #    QuaterValue="Q2"
                 #elif monthVal in q3:
                 #    QuaterValue="Q3"
                 #elif monthVal in q4:    
                 #    QuaterValue="Q4"
                 
                 year=int(issue_d[firstIndex+1:len(issue_d)])
             
                  # add key in not present in dictionary and if present increase the count                
                  #yearAndQuater=year+QuaterValue
                 if year in ansDiction:
                    ansDiction[year] += 1
                 else:
                    ansDiction[year] = 1
             
                 #del ansDiction['2007']
                 #del ansDiction['2008']
                 #del ansDiction['2009']
                 #del ansDiction['2010']
                 #del ansDiction['2011']
             
             # to get the state and year wise details
             # to get the count of application per state in year
             if(len(row)>24):
                 
                 if year in stateAndyearDic:
                    stateAndCountDic=stateAndyearDic[year]
                    stateName=row[23]
                    if stateName=='':
                        stateName='unknown'
                    if stateName in stateAndCountDic:
                        stateAndCountDic[stateName] += 1
                    else:
                        stateAndCountDic[stateName] = 1
                    
                 else:
                    stateAndyearDic[year] = {}
               # end of state and year wise details
               
             # get the emp title and count  
             # get the emp title and count 
             if(len(row)>15):
                 empTitle=row[10]
                 if empTitle =='':
                     empTitle="Not Specified"
                 if year in empTitleAndyearDic:
                     empTitleAndCount=empTitleAndyearDic[year];                                       
                     if empTitle in empTitleAndCount:
                         empTitleAndCount[empTitle] += 1
                     else:
                         empTitleAndCount[empTitle] = 1
                 else:
                    empTitleAndyearDic[year] = {}
    
            # get the deliquent per year wise
             if(len(row)>21):
                if year in deliquentAndYearDic:
                    deliquentAndCount=deliquentAndYearDic[year]
                    deliquentVal=row[25]
                    deliquentStatus="no"
                    if deliquentVal=="":
                       deliquentVal='0'
                    if int(deliquentVal) >0:
                        deliquentStatus='yes'
                    else:
                        deliquentStatus='no'
                        
                    if deliquentStatus in deliquentAndCount:
                        deliquentAndCount[deliquentStatus]+=1
                    else:
                        deliquentAndCount[deliquentStatus]=1
                else:
                    deliquentAndYearDic[year]={'yes':0,'no':0}
            
            
            # purpose of people
            # add the values in dictionary
             if(len(row)>21):
                if year in purposeAndyearDic:
                    purposeAndCount=purposeAndyearDic[year]
                    purposeVal=row[20]
                    if purposeVal in purposeAndCount:
                        purposeAndCount[purposeVal]+=1
                    else:
                        purposeAndCount[purposeVal]=1
                else:
                    purposeAndyearDic[year]={}
            
            # % percentage of verified and not verified
             if(len(row)>20):            
                if year in varifiStatusAndyearDic:
                    varificationAndCount=varifiStatusAndyearDic[year]
                    varificationVal=row[14]
                    if varificationVal in varificationAndCount:
                        varificationAndCount[varificationVal]+=1
                    else:
                        varificationAndCount[varificationVal]=1
                else:
                    varifiStatusAndyearDic[year]={}
                
             # for load amout  over the year
             if(len(row)>20):            
                if year in amountAndYearDic:
                    loanAmountAndCount=amountAndYearDic[year]
                    strloanAmount=row[2]
                    loanAmount=int(strloanAmount)
                    
                    if loanAmount<=1000:
                        loanAmountAndCount['0-1000']+=1
                    elif loanAmount>1000 and loanAmount<=10000:
                        loanAmountAndCount['1001-10000']+=1
                    elif loanAmount>10000 and loanAmount<=20000:
                        loanAmountAndCount['10001-20000']+=1
                    elif loanAmount>20000 and loanAmount<=30000:
                        loanAmountAndCount['20001-30000']+=1
                    elif loanAmount>30000 and loanAmount<=40000:
                        loanAmountAndCount['30001-40000']+=1
                    elif loanAmount>40000 and loanAmount<=50000:
                        loanAmountAndCount['40001-50000']+=1
                    elif loanAmount>50000 and loanAmount<=90000:
                        loanAmountAndCount['50001-90000']+=1
                    elif loanAmount>90000 :   
                        loanAmountAndCount['50001-90000']+=1
                else:
                    amountAndYearDic[year]={'0-1000':0,'1001-10000':0,'10001-20000':0,'20001-30000':0,'30001-40000':0,'40001-50000':0,'50001-90000':0,'90000-above':0}
                
            # loan amout count, divide the loan amount in range
            # like 2500-10000 
            
            # ROI over the year
             if(len(row)>20):            
                if year in roiAndyearDic:
                    roiAndCount=roiAndyearDic[year]
                    strroiValue=row[6]
                    roiValue=float(strroiValue.replace("%",""))
                    if roiValue<=10:
                        roiAndCount['5-10']+=1
                    elif roiValue>10 and roiValue<=15:
                        roiAndCount['11-15']+=1
                    elif roiValue>15 and roiValue<=20:
                        roiAndCount['16-20']+=1
                    elif roiValue>20 and roiValue<=25:
                        roiAndCount['21-25']+=1
                    elif roiValue>25 and roiValue<=30:
                        roiAndCount['26-30']+=1
                    elif roiValue>30 and roiValue<=35:
                        roiAndCount['31-35']+=1
                    elif roiValue>35:
                        roiAndCount['35-above']+=1
                    
                else:
                    roiAndyearDic[year]={'5-10':0,'11-15':0,'16-20':0,'21-25':0,'26-30':0,'31-35':0,'35-above':0}
            
    
    logging.info("Start To create pie chart for purpose") 
    print("Start To create pie chart for purpose")
    #To create pie chart for purpose
    print(len(purposeAndyearDic))
    for yearkey, value in purposeAndyearDic.items():
        purAndCount=value
        labels=[]
        colors=['aqua','beige','coral','green','gold','fuchsia','indigo','lavender','yellowgreen']
                 #,'gray','indigo','ivory',
                #'khaki','lavender','lightblue','lime','magenta','orange',
                #'orchid','pink','red','salmon','tan','teal','violet','wheat','yellowgreen']
        values=[]
        purAndCountsorted = sorted(purAndCount.items(), key=operator.itemgetter(1))
        count=0;
        for key, value in purAndCount.items():
            print(key)
            if count>6:
                break;
            count=count+1
            labels.append(key)
            values.append(value)
        plt.style.use('ggplot')
        plt.pie(values, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=240)
        plt.axis('equal')
        #patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(labels, loc="best")
        plt.tight_layout()
        fig = plt.gcf()
        fig.set_size_inches(8,8) # or (4,4) or (5,5) or whatever
        plt.title("% share of loan purpose for year : "+str(yearkey),position=(0.5,1),bbox=dict(facecolor='0.8',), fontsize=15)
        graphName="purposeAndYear"+str(yearkey)+".png"
        plt.savefig(graphName)
        plt.close() 
        logging.info("end To create pie chart for purpose") 
        print("end To create pie chart for purpose")
        
    logging.info("Start To Number of application over the year graph") 
    print("Start To Number of application over the year graph")
    #code for Number of application over the year graph
    objects=[]
    performance = []
    ansDictionsorted = sorted(ansDiction.items(), key=operator.itemgetter(1))
    for key, value in ansDiction.items():
        objects.append(key)
        performance.append(int(value))
        
    y_pos = np.arange(len(objects))
    # set the color for graph
    colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    barlist=plt.bar(y_pos, performance, align='center', alpha=0.5,color=colors)
    plt.xticks(y_pos, objects)
    
    # set the y axix and title of graph
    plt.ylabel('Number of applications')
    plt.title('No. of loan applications over the years')
    plt.xlabel('year')
    
    # get the config of plt and set the size
    fig = plt.gcf()
    fig.set_size_inches(8,8)
    
    # set the graph name
    graphName="NumberOfApplications"+".png"
    
    # save the graph name and close the plt
    plt.savefig(graphName)
    plt.close()
    logging.info("end To Number of application over the year graph") 
    print("end To Number of application over the year graph")
    
    
    logging.info("start To create pie chart for ROI over year") 
    print("start To create pie chart for ROI over year")
    #code to create pie chart for ROI over year
    print(len(roiAndyearDic))
    #iterrate over the roiAndyearDic dictionary obj
    for yearkey, value in roiAndyearDic.items():
        # here value is type of dictionary type
        roiAndCount=value
        labels=[]
        # set the color of graph
        colors=['aqua','beige','coral','green','gold','fuchsia','indigo']
        values=[]
        count=0;
        # iterate over the object for calculation
        for key, value in roiAndCount.items():
            print(key)
            if count>6:
                break;
            count=count+1
            labels.append(key)
            values.append(value)
        plt.style.use('ggplot')
        plt.pie(values, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=240)
        plt.axis('equal')
        #patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(labels, loc="best")
        plt.tight_layout()
        # get the config and set the size
        fig = plt.gcf()
        fig.set_size_inches(8,8) # or (4,4) or (5,5) or whatever
        
        # set the titel of plot                   
        plt.title("% of loan catagory over year : "+str(yearkey),position=(0.5,1),bbox=dict(facecolor='0.8',), fontsize=15)
        
        # set the graph file name
        graphName="ROIAndYear"+str(yearkey)+".png"
        
        # save the plt and close
        plt.savefig(graphName)
        plt.close()
        logging.info("end To create pie chart for ROI over year") 
        print("end to create pie chart for ROI over year")
    
    
    #code to generate graph for Deliquent over the year
    
    logging.info("star tgenerate graph for Deliquent over the year") 
    print("start generate graph for Deliquent over the year") 
    # cleader and initialize variables for future use
    n_groups = 10
    means_frank1=[]
    means_guido1=[]
    yearValues=[]
    # to sort the values
    d = collections.OrderedDict(sorted(deliquentAndYearDic.items()))
    
    # iterate over the d dictionary
    for yearkey, value in d.items():
        roiAndCount=value
        totalCount=0;
        # loop to get the total count
        for key, value in roiAndCount.items():
            totalCount=totalCount+value;
        yearValues.append(yearkey)
        
        # loop to calculate the % 
        for key, value in roiAndCount.items():
            if key =='yes':
                percentVal=(value*100)/totalCount;
                means_frank1.append(percentVal)
            if key == 'no':
                percentVal=(value*100)/totalCount;
                means_guido1.append(percentVal)
         
    # create plot
    means_frank=(means_frank1)
    
    means_guido=(means_guido1)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
     
    # as we two values, below code set the color , label and other variables
    rects1 = plt.bar(index, means_frank, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Deliquent yes')
     
    rects2 = plt.bar(index + bar_width, means_guido, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Deliquent No')
     
    # set the x and y lables
    plt.xlabel('years')
    plt.ylabel('% numbers')
    
    # set the title 
    plt.title('Deliquent over years')
    plt.xticks(index + bar_width, yearValues)
    plt.legend()
    # get the config and set the size
    fig = plt.gcf()
    fig.set_size_inches(12,8)
    
    plt.tight_layout()
    # graph name 
    graphName="DeliquentpercentageoverYears"+str(yearkey)+".png"
    
    # save the lpt in file and close the plt
    plt.savefig(graphName)
    plt.close()
    logging.info("end tgenerate graph for Deliquent over the year") 
    print("end generate graph for Deliquent over the year") 
    
    #amountAndYearDic
    logging.info("start create pie chart for amount over year") 
    print("start create pie chart for amount over year") 
    #To create pie chart for amount over year
    print(len(roiAndyearDic))
    # iterate over the amountAndYearDic obj
    for yearkey, value in amountAndYearDic.items():
        # value obj is dictionary type
        roiAndCount=value
        labels=[]
        # set the colors for graph
        colors=['aqua','beige','coral','green','gold','fuchsia','indigo']
        values=[]
        count=0;
        # iterate over the roiAndCount items
        for key, value in roiAndCount.items():
            labels.append(key)
            values.append(value)
        plt.style.use('ggplot')
        plt.pie(values, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=240)
        plt.axis('equal')
        #patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(labels, loc="best")
        
        
        plt.tight_layout()
        # get the config of plt
        fig = plt.gcf()
        
        #set the size of plot
        fig.set_size_inches(8,8) # or (4,4) or (5,5) or whatever
        
        # set the title of plot
        plt.title("Loan amount catagory over year : "+str(yearkey),position=(0.5,1),bbox=dict(facecolor='0.8',), fontsize=15)
        
        # set graph name
        graphName="AmountAndYear"+str(yearkey)+".png"
        
        # save the graph in file
        plt.savefig(graphName)
        # close the plt
        plt.close()
        logging.info("end create pie chart for amount over year") 
        print("end create pie chart for amount over year") 
    
    #To create pie chart for varification over year
    
    logging.info("start pie chart for varification over year") 
    print("start pie chart for varification over year") 
    # iterate over the varifiStatusAndyearDic object
    for yearkey, value in varifiStatusAndyearDic.items():
        # here value is dictionary type
        roiAndCount=value
        labels=[]
        colors=['aqua','beige','coral']
        values=[]
        count=0;
        
        #iterate over the roiAndCount 
        for key, value in roiAndCount.items():
            labels.append(key)
            values.append(value)
        plt.style.use('ggplot')
        plt.pie(values, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=240)
        plt.axis('equal')
        #patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(labels, loc="best")
        plt.tight_layout()
        # get the configuration of plt
        fig = plt.gcf()
        # set the size of plot
        fig.set_size_inches(8,8) # or (4,4) or (5,5) or whatever
        
        # set the title of plt
        plt.title("Verification status over year : "+str(yearkey),position=(0.5,1),bbox=dict(facecolor='0.8',), fontsize=15)
        graphName="VarificationAndYear"+str(yearkey)+".png"
        
        # save the plt in file
        plt.savefig(graphName)
        
        #close the plot
        plt.close()
        logging.info("end pie chart for varification over year") 
        print("end pie chart for varification over year") 
        
        
    logging.info("start generate the csv file for state and count") 
    print("start generate the csv file for state and count")
    #To generate the csv file for state and count
    # cerate variable for header,yearAndCount, completedata
    headerNames=['year']
    YearAndCount=[]
    completeData=[]
    countforheader=0
    # iterate over the stateAndyearDic dictionary 
    for yearkey, value in stateAndyearDic.items():
        #here value is dictionary type
        stateAndCountDic=value
        
        # sort the dictionary value
        d = collections.OrderedDict(sorted(stateAndCountDic.items()))
        
        # append the year value in list
        YearAndCount.append(yearkey)
        
        #for add the header one time 
        totalCountOFrecordForAYear=0
        
        # iterate over the d dictionary that is sorted
        for statekey, value in d.items():
            
            if countforheader==0:
                headerNames.append(statekey);
            # get the total count to calculate the percentage
            totalCountOFrecordForAYear=totalCountOFrecordForAYear+value
        
        # iterate over the d dictionary to calculate the %    
        for statekey,value in d.items():
            percentVal=(float(value)/totalCountOFrecordForAYear)*100              
            YearAndCount.append(percentVal) 
            
        # if first time then will add values in list
        if countforheader==0:
            completeData.append(headerNames)
        countforheader=countforheader+1
        
        # added the complete data in list to create, dataframe
        completeData.append(YearAndCount)
        YearAndCount=[]
        
    # create data frame from completeData obj
    dfstateAndCount = pd.DataFrame(completeData)
    
    # to generate the output csv file.
    outStateFile = pd.DataFrame(dfstateAndCount)
    outPutfileName="LoanStateAndyears.csv"
    outStateFile.to_csv(outPutfileName,index=False)
    logging.info("end generate the csv file for state and count") 
    print("end generate the csv file for state and count")
    
if __name__ == "__main__":
    createLogFile()
    logging.info('After log file creation')
    
    logging.info('before graph generation')
    
    readAndGenerateGrpah()