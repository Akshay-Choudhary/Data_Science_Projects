# -*- coding: utf-8 -*-

"""
Created on Fri Feb 24 09:11:02 2017

IMP :-  used method "max(set(list), key=list.count)" to calculate the mode. As this 
        method handles the error, if there are more than one Mode in output.


@author: Team 4
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import io
import urllib.request, urllib.parse, urllib.error
import csv
import zipfile
import statistics

url = 'https://www.sec.gov/data/edgar-log-file-data-set.html'

# Open URL in a new tab, if a browser window is already open.
#webbrowser.open_new_tab(url)

# Open URL in new window, raising the window if possible.
#webbrowser.open_new(url)

# enteredYear="2003"

# take the argument as the year for which the script needs to be executed
import sys
userInputarg = sys.argv[1]
enteredYear = userInputarg
#enteredYear="2003"
#create empty list to store file name
file_nameForLink =[]

# Scrape the HTML at the url
r = requests.get(url)

# Turn the HTML into a Beautiful Soup object
soup = BeautifulSoup(r.text, 'lxml')

tmpcheck=soup.find_all('a')

#print(tmpcheck)
print("========")

CurrWorkingDir=os.getcwd();
print(CurrWorkingDir)
pathForOutPut=CurrWorkingDir+'\\'+"Part2"

# check whether path is present or not
if not os.path.exists(pathForOutPut):
    # will come if path is not present and will create path(folder)
    os.makedirs(pathForOutPut)

# change the working dir to new path,(to generate the files under particular company folder)
os.chdir(pathForOutPut)

pathforOutputYearwise=pathForOutPut+ '\\'+ enteredYear

# check whether path is present or not
if not os.path.exists(pathforOutputYearwise):
    # will come if path is not present and will create path(folder)
    os.makedirs(pathforOutputYearwise)

# change the working dir to new path,(to generate the files under particular company folder)
os.chdir(pathforOutputYearwise)

linkForGivenYear=[]

# create all the link for given year
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr1/log"+ enteredYear+"0101.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr1/log"+ enteredYear+"0201.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr1/log"+ enteredYear+"0301.zip")

linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr2/log"+ enteredYear+"0401.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr2/log"+ enteredYear+"0501.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr2/log"+ enteredYear+"0601.zip")

linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr3/log"+ enteredYear+"0701.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr3/log"+ enteredYear+"0801.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr3/log"+ enteredYear+"0901.zip")

linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr4/log"+ enteredYear+"1001.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr4/log"+ enteredYear+"1101.zip")
linkForGivenYear.append("www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + enteredYear+ "/Qtr4/log"+ enteredYear+"1201.zip")

# file name for log file
logFileName="Asg1Q2log.txt"

# opens the log file
file =open(logFileName,"w")
 
file.write("***************************log file******************************\n") 
csvFileNames=[]
import datetime
import time

# get the time stamp and write in the file
currTime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(currTime)+ "starting downloading the file"+"\n")

# varibale to initialize with zero for loop through
i=0

# code to download the file and unzip it

while i< len(linkForGivenYear):
    print(linkForGivenYear[i])
    lastIndex=linkForGivenYear[i].rindex("/")
    totalLen=len(linkForGivenYear[i])
    fileName=linkForGivenYear[i][lastIndex+1:totalLen]
    print(fileName)
    
    # append the http to link. required it becasue of protocal
    url="http://"+linkForGivenYear[i]
    print(url)
    # replace the file extention with csv
    print(fileName.replace('zip','csv'))
    
    # append the file name in the list
    csvFileNames.append(fileName.replace('zip','csv'))
    urllib.request.urlretrieve(url, fileName)
    
    # code to extract the zip file and place in particular folder
    zip_ref = zipfile.ZipFile(pathforOutputYearwise+"/"+fileName, 'r')
    zip_ref.extractall(pathforOutputYearwise)
    zip_ref.close()
    i=i+1
    
    # get the time stamp and write in file
    currTime1=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(str(currTime)+ "completed downloading and unzip the files"+"\n")

# get the time stamp and write in file
currTime2=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(currTime2)+ "starting cleaning of data"+"\n")

# list to contain the clean data file name
listOfCleanFileName=[]
# Code to clean the data and create new files 

for singleCsvFilename in csvFileNames:
    
    # create new file with CD_with old file name
    newFileNameForCleanData="CD_"+singleCsvFilename
    
    # append the new file name in list
    listOfCleanFileName.append(newFileNameForCleanData)
    
    currTime12=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(str(currTime12)+ "   created new file for clean data "+ newFileNameForCleanData+"\n")
    
    # open the file to write, with newline="" for no blank line after after each row
    f = open(newFileNameForCleanData, 'w',newline='')
    writerSam = csv.writer(f)
     #compleRowData='ip','sa'
     
    # set the variables to zero for use
    initialRowCount=0
    noOfrowsinoutput=0
    fileSizeTotalSumCount=[0]
    fileSizeNumbers=0
    forCalculateAnyValueAndAppend=True
    listforCalculateModeOfCode=[]
         
    listforZone=[]
    listforidx=[]
    listfornorefer=[]
    listfornoAgent=[]
    listforFind=[]
    listforCrawler=[]
    listforBroser=[]
    print("singleCsvFilename-->"+singleCsvFilename)
    fordateRowCount=0
    
    # open the file as reader to read the data
    with open(singleCsvFilename, 'rt') as fr:
        reader = csv.reader(fr, delimiter=',')
        
        # iterate through all the rows
        for row in reader:
            #print("row Count -->"+str(len(row)))
            fordateRowCount=fordateRowCount+1
            
            # will break the loop if low length is zero
            if len(row)==0:
                break
            #break
            initialRowCount=initialRowCount+1
            #print("==============================")
            i=0
            allRowData=[]
            writedata=False
            while i < len(row):
                # resetting to true to add the values in list
                forCalculateAnyValueAndAppend=True
                
                # if the column 0,1,2,,4,5 are blank then will skip that row data
                if row[0]=="":
                    break
                if row[1]=="":
                    break
                if row[2]=="":
                    break
                if row[4]=="":
                    break
                if row[5]=="":
                    break
            
            # for Zone column          -------> taking Mode here
                if i==3:
                    if row[3]=="":
                        calculatedZoneMode=max(set(listforZone), key=listforZone.count)
                        allRowData.append(calculatedZoneMode)
                        forCalculateAnyValueAndAppend=False
                    else:
                        listforZone.append(row[3])
                    
                # for Code column            -------> taking Mode here
                if i==7:
                    if row[7]=="":
                        calculatedCodeMode=max(set(listforCalculateModeOfCode), key=listforCalculateModeOfCode.count)
                        allRowData.append(calculatedCodeMode)
                        forCalculateAnyValueAndAppend=False
                    else:
                        listforCalculateModeOfCode.append(row[7])
                
                    # for Size column              ---> taking mean 
                if i==8:
                    if row[8]=="":
                        sizemean=statistics.mean(fileSizeTotalSumCount)
                        allRowData.append(sizemean)
                        forCalculateAnyValueAndAppend=False
            

             # for IDX column                  -------> taking Mode here
                if i==9:
                    if row[9]=="":
                        calculatedIDX=max(set(listforidx), key=listforidx.count)
                        allRowData.append(calculatedIDX)
                        forCalculateAnyValueAndAppend=False
                else:
                     listforidx.append(row[9])
             
             # for norefer column               -------> taking Mode here
                if i==10:
                     if row[10]=="":
                         calculatedIDX=max(set(listfornorefer), key=listfornorefer.count)
                         allRowData.append(calculatedIDX)
                         forCalculateAnyValueAndAppend=False
                else:
                    listfornorefer.append(row[10])
              
             # for noagent column           -------> taking Mode here
                if i==11:
                     if row[11]=="":
                         calculatedNoAgent=max(set(listfornoAgent), key=listfornoAgent.count)
                         allRowData.append(calculatedNoAgent)
                         forCalculateAnyValueAndAppend=False
                else:
                     listfornoAgent.append(row[11])
                    
             # for find column             -------> taking Mode here
                if i==12:
                     if row[12]=="":
                         calculatedFind=max(set(listforFind), key=listforFind.count)
                         allRowData.append(calculatedFind)
                         forCalculateAnyValueAndAppend=False
                else:
                    listforFind.append(row[12])
               
                 # for crawler column         -------> taking Mode here
                if i==13:
                    if row[13]=="":
                        calculatedCrawler=max(set(listforCrawler), key=listforCrawler.count)
                        allRowData.append(calculatedCrawler)
                        forCalculateAnyValueAndAppend=False
                    else:
                        listforCrawler.append(row[13])
            
                # for browser column              -------> taking Mode here
                if i==14:
                    if row[14]=="":
                        #calculatedBrowser=max(set(listforBroser), key=listforBroser.count)
                        allRowData.append("NA")
                        forCalculateAnyValueAndAppend=False
                    else:
                        listforBroser.append(row[14])
                    

                if forCalculateAnyValueAndAppend==True:
                    allRowData.append(row[i]);
                                     
                writedata=True
                i=i+1
            #print(initialRowCount)
            if writedata==True:
                noOfrowsinoutput=noOfrowsinoutput+1
                
                if noOfrowsinoutput!=1 and row[8]!="" and isinstance(row[8], str) ==False:
                    fileSizeTotalSumCount.append(int(row[8]))
                    fileSizeNumbers=fileSizeNumbers+1
                    
                writerSam.writerow((allRowData))
    f.close()

print("initialRowCount-->"+str(initialRowCount))
print("noOfrowsinoutput-->"+str(noOfrowsinoutput))

currTime3=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(currTime3)+ "completed cleaning of data")

currTime4=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(currTime4)+ "starting mearging of data to one file")

# Code to merge the file and create one file 

print("csfFileName---->"+str(len(csvFileNames)))
allCSV_filesToCombine =listOfCleanFileName

header_saved = False

# Final file created after cleaning and merging individual 12 files for each month
summaryfile = "summaryResult.csv"

with open(summaryfile,'w') as fout:
    for filename in allCSV_filesToCombine:
        print(filename)
        currTime14=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        file.write(str(currTime14)+ "   working on mearging of data  "+filename +"  to one file"+"\n")
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                fout.write(header)
                header_saved = True
            for line in fin:
                fout.write(line)
                
print("====Done====")
    
currTime5=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(currTime5)+ "completed mearging of data to one file")

# Code to generate summary metrics from the resultant summary file
metricsFile = "Asg1Q2_metrics.csv"

import pandas as pd

# read the file and create data set
df = pd.read_csv(summaryfile)

df1 = pd.DataFrame(df.groupby(['cik'])[["ip"]].count())
df2 = pd.DataFrame(df.groupby(['cik'])[["size"]].sum())

# combine both the dataframe
final = pd.concat([df1, df2], axis=1)
final.columns = ['User Requests', 'Total File Size']

# sort the dataset
result = final.sort(['User Requests'], ascending=[0])

# generate the csv File
result.to_csv(metricsFile)

# Close the log file and 
file.close() 

# Code to connect S3 and upload the generated output and log files
'''
# Creating the connection 
import boto3
s3 = boto3.resource('s3')

# generate bucket name
bucket_name = "adsteam04" + "_" + enteredYear

# Creating the S3 bucket and upload the files to bucket
try:
    s3.create_bucket(Bucket=bucket_name)
    s3.Object(bucket_name, summaryfile).put(Body=open(summaryfile, 'rb'))
    s3.Object(bucket_name, logFileName).put(Body=open(logFileName, 'rb'))
    s3.Object(bucket_name, metricsFile).put(Body=open(metricsFile, 'rb'))
except Exception:
    print("Failed to make the S3 connection,please enter valid AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
''' 
# go back to the initial working directory and the end of the script        
os.chdir(CurrWorkingDir)

CurrWorkingDir1=os.getcwd();
print(CurrWorkingDir1)