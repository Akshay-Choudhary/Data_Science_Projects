# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 03:01:15 2017

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
    
    
    #for state and year count
    stateAndyearDicForReject={}
    
    
    print(os.getcwd())
    count=0;
    rejectAnsDiction={}
    counterFor2016=0;
    logging.info("read the file and calculate the data in dictionary")
    print("read the file")
    with open('RejectoutFileDec.csv', 'rt',encoding="utf8") as fr:
         count=0
         skiprow=1
         reader = csv.reader(fr, delimiter=',')
         blankRowCount=0
         for row in reader:
             global issue_d;
             global firstIndex;
             global year;
             
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
             if(row[0]=='Loans that do not meet the credit policy'):
                 print(row[0]);
                 continue;
                     
             if "Total" in row[0]:
                 print(row[0])
                 break;
            
             if((len(row)>5) and (not(row is None))):
                 issue_d=row[1]
                
                 firstIndex=issue_d.index('-')
                 year=issue_d[0:firstIndex]
                 if(year=='2016'):
                     counterFor2016=counterFor2016+1
                 if year in rejectAnsDiction:
                    rejectAnsDiction[year] += 1
                 else:
                    rejectAnsDiction[year] = 1
                 
                                    
             if(len(row)>6):
                 if year in stateAndyearDicForReject:
                    stateAndCountDicRej=stateAndyearDicForReject[year]
                    stateName=row[6]
                    if stateName in stateAndCountDicRej:
                        stateAndCountDicRej[stateName] += 1
                    else:
                        stateAndCountDicRej[stateName] = 1
                    
                 else:
                    stateAndyearDicForReject[year] = {}
             if counterFor2016>4769870:
                     break;
                 
                    
    logging.info("started creating graph for Rejected Number of applications")
    print("started creating graph for Rejected Number of applications")                
    objects=[]
    performance = []
    ansDictionsorted = sorted(rejectAnsDiction.items(), key=operator.itemgetter(1))
    for key, value in rejectAnsDiction.items():
        objects.append(key)
        performance.append(int(value))
        
    y_pos = np.arange(len(objects))
    colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    barlist=plt.bar(y_pos, performance, align='center', alpha=0.5,color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Rejected Number of applications')
    plt.xlabel('Years')
    plt.title('No. of loan applications over the years')
    
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    graphName="RejectedNumberOfApplications"+".png"
    plt.savefig(graphName)
    plt.close()
    logging.info("end creating graph for Rejected Number of applications")
    print("end creating graph for Rejected Number of applications") 

    
if __name__ == "__main__":
    createLogFile()
    logging.info('After log file creation')
    
    logging.info('before graph generation')
    
    readAndGenerateGrpah()
    