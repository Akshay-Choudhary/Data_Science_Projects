
# coding: utf-8

"""
Details :- Code perform the followinf task.
            A) Opne the first link and takes file names on the bases of 10-Q,k etc
            B) Create new URl and open it
            C) Get the particular tables using selectors and process on each, create dataframe and export to csv.
            D) Generate the log file.
            E) zip all the table files.
            F) Upload the files to AWS3 server.

Created on Sat Feb 18 18:04:23 2017

@author: Team 4( Samarth, Bhavik, Akshay)
"""

# BV start - code to parse the config file and generate the URL
import os
print("Script execution start")

cwd = os.getcwd()
inipath = cwd + "/edgar.ini"

# get the section name which is the company for which we need to run the script

import sys
userInputarg = sys.argv[1]

# read the path of the config file for the parser

import configparser
config = configparser.ConfigParser()

###config.read("/home/bhavik/Python3_home/notebooks/edgar.ini")
config.read(inipath)

# to display the sections in the config file
config.sections()

if userInputarg =="":
	section = "default"
else:
	section = userInputarg
  
# get CIK number from config file
cik = config.get(section,'cik')
# remove leading "0" from the CIK number 
ciktrim = cik.lstrip("0")

# get DAN number from config file
dan = config.get(section,'dan')
#remove "-" from the DAN number from the config file
dantrim = dan.replace("-","")

url_pre = 'https://www.sec.gov/Archives/edgar/data'
url_post = '-index.html'

# append all the part and create URL
url = url_pre + "/" + ciktrim + "/" + dantrim + "/" + dan + url_post

#url
print("starting code ---12345")

# BV - end code to parse the config file and generate the URL

import webbrowser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import io


#create empty list to store file name
file_nameForLink =[]

# Scrape the HTML at the url
r = requests.get(url)

# Turn the HTML into a Beautiful Soup object
soup = BeautifulSoup(r.text, 'lxml')

#Find the table based on the class="tableFile"
table = soup.find(class_='tableFile')

print('---------------')

#constant to compare and find the element
constantVal=['10-A','10-B','10-C','10-D','10-E','10-F','10-G','10-H','10-I','10-J','10-K','10-L','10-M','10-N','10-O','10-P','10-Q','10-R','10-S','10-T','10-U','10-V','10-W','10-X','10-Y','10-Z']

#iterate over all the rows and except first one
for row in table.find_all('tr')[1:]:
    
    # Create a variable of all the <td> tag pairs in each <tr> tag pair,
    col = row.find_all('td')

    # get the fourth td element and strip it
    column_1 = col[3].string.strip()
    
    #compare the col value and with constant value to get file name
    if column_1 in constantVal:
        #get the third column value, strip it and assign the value to variable
        column_2 = col[2].string.strip()
        
        #Append the file name in the array
        file_nameForLink.append(column_2)
    
#print(file_name)

# if the file is not present,Stop the program
import sys
if len(file_nameForLink)==0:
    print("Required file path not found")
    sys.exit("Error message-Required file path not found")

#get the last index of '/' in the first url
lastLocation=url.rindex('/')

# get the url part from 0th location to the last location of '/'
firstPartUrl=url[0:lastLocation]

# Append the common URl(firstpartUrl) and file name to get the secondURl.
secondURL=firstPartUrl+'/'+file_nameForLink[0]

# Optional statement -> To open the url in new Link...can remove it for multiple values
webbrowser.open_new(secondURL)
print('-----------------newURL-------------------')

# get the current working directory
CurrWorkingDir=os.getcwd();
                        
# print the working directory path on console
print (CurrWorkingDir)

# get the file name from file_nameForLink list
strTogetCMPName=file_nameForLink[0]

# find the location of 1 in file name
lastforCMP=strTogetCMPName.find('1')

# lastforCMP dont have any value then
if lastforCMP=="":
    companyName=strTogetCMPName[0:3]
else:
    # get the subString from 0th position to lastforCMP
    companyName=strTogetCMPName[0:lastforCMP]

# print the company name on console
print(companyName)


# Create the new path for working dir, append the company name in current workingDir
# *********** For Windows use '\\' to appennd the folder.   
#pathForOutPut=CurrWorkingDir+'\\'+companyName

#************ For Unix use '/' for append the folder
pathForOutPut=CurrWorkingDir+'/'+companyName

# check whether path is present or not
if not os.path.exists(pathForOutPut):
    # will come if path is not present and will create path(folder)
    os.makedirs(pathForOutPut)

# change the working dir to new path,(to generate the files under particular company folder)
os.chdir(pathForOutPut)

#------------------------------- second page extraction-----------------------

#get the second url
r1 = requests.get(secondURL)

# Turn the HTML into a Beautiful Soup object
soup1 = BeautifulSoup(r1.text, 'lxml')

# find all the table..
AlltableRec=soup1.find_all('table')
#print(tableRec[4])
print(len(AlltableRec))
print("Total Table found========")
requiredTableBasedOnDollarSign=[]

# code to select the tables based on the $ sign(if $ is present then will select the table)
for singleTable in AlltableRec:
    #print(singleTable)
    flagToGetTable=False
    for row in singleTable.find_all('tr')[1:]:
        
        # find all the tds of a row
        cols = row.find_all('td')
        for col in cols:
            tempforCheck=col.text.replace('\n','')
            if tempforCheck=="$":
                requiredTableBasedOnDollarSign.append(singleTable)
                flagToGetTable=True
                break
        if(flagToGetTable==True):
            break
    
totalTableFoundBasedOnDollarSign=len(requiredTableBasedOnDollarSign)
print("totalTableFound based on $ -->"+str(totalTableFoundBasedOnDollarSign))

# code to select the tables based on background color
requiredTableBasedOnBackGroundColor=[]

for singleTable in AlltableRec:
    #print(singleTable)
    flagToGetTable=False
    for row in singleTable.find_all('tr')[1:]:
        
        # find all the tds of a row
        cols = row.find_all('td')
        for col in cols:
            # to find the style value
            tempforCheckForStyle=col['style']
            #print(tempforCheckForStyle)
            #print("==============================")
            if 'background' in tempforCheckForStyle or 'background-color' in tempforCheckForStyle:
                #print("present")
                requiredTableBasedOnBackGroundColor.append(singleTable)
                flagToGetTable=True
                break
        if(flagToGetTable==True):
            break
    
totalTableFoundBasedOnbackGroundColor=len(requiredTableBasedOnBackGroundColor)
print("requiredTableBasedOnBackGroundColor-->"+str(totalTableFoundBasedOnbackGroundColor))


#************************************************************


finalSelectedTables=[]

# will get the max number of tables
if totalTableFoundBasedOnbackGroundColor > totalTableFoundBasedOnDollarSign:
    finalSelectedTables=requiredTableBasedOnBackGroundColor
else:
    finalSelectedTables=requiredTableBasedOnDollarSign


# initialize the variable with Zero
fileCount=0;

# create empty list to save the data
completeData=[]
fileNames= {'Name': 'Zara',companyName:0}

txtValueOFHeader=''

logFileName=companyName+"_logfile.txt"

file =open(logFileName,"w")
 
file.write("***************************log file******************************\n") 

tableNumber=1
file.write("Number of tables find -"+str(len(AlltableRec))+"\n")
# Iterate through all the tables
for tableRec in AlltableRec:
    
    # code to get file name
    
    file.write("Start processing on Table No - "+ str(tableNumber)+"\n")
    
    # get parent of the table 
    tableHeaderValue=tableRec.parent.parent
    
    # find all the element of the table
    tableHeaderValuechildren = tableHeaderValue.findChildren()
    
    
    file.write("Start Working on to get header vales for file name\n")
    
    # iterate over child and will work only first one. as used break to terminate the loop
    for childvalue in tableHeaderValuechildren:
        #print("***********************")
        allChildvaluesOFAParent=childvalue.findChildren()
        
        for temocheckChEl in allChildvaluesOFAParent:
            txtValueOFHeader=str(temocheckChEl.text.replace(' ','').strip())
            txtValueOFHeader=txtValueOFHeader.replace('\n','')
            txtValueOFHeader=txtValueOFHeader.strip().replace('-','')
            fileNamelen=len(txtValueOFHeader)
            if fileNamelen >21:
                txtValueOFHeader=txtValueOFHeader[0:20]
            #print("--------------------------------")
            if len(txtValueOFHeader) >2:
                if txtValueOFHeader in fileNames:
                    countValueOFFile=fileNames[txtValueOFHeader]
                    countValueOFFile=countValueOFFile+1
                    fileNames[txtValueOFHeader]=countValueOFFile
                    print("In if condition")
                    break
                else:
                    fileNames[txtValueOFHeader]=0
                    print("IN else condition")
                    break
        break
    # initialize the empty list
    rowData =[]
    file.write("completed Working on to get header vales for file name\n")
    print("+++++++++++++++++++++++++++++++++++++")
    
    file.write("Start Working on to date extraction from table\n")
    
    # Iterate through all the rows of table
    for row in tableRec.find_all('tr')[1:]:
        
        # find all the tds of a row
        cols = row.find_all('td')
        #print("a value--->"+str(a)+" ---col-->"+str(len(cols)))
        
        # Iterate through all the cols of table
        for col in cols:
            # get text value and replace the '\n' with ''(blank space) 
            tempforCheck=col.text.replace('\n','')
            
            
            # remove front and back space
            tempforCheck=tempforCheck.strip()
            
            # check the length, if length is greater than 1. it will return true.
            # place the condition to remove the blank tds(some tds dont have any value)
            if(len(tempforCheck) >1):
                tempforCheck=tempforCheck.replace('(','')
                tempforCheck=tempforCheck.replace(')','')
                # append the value in rowData list
                rowData.append(tempforCheck)
                     
        # Each td data value added to rowData. After executing all the cols,values are added to completeData list 
        completeData.append(rowData)
        #print("colfirst Value--->")
        # reinitialize the rowData , so remove all the old values
        rowData=[]
    #print(completeData) 
    
    file.write("Completed the data extraction from table and created the data set\n")
    
    out = pd.DataFrame(completeData)
    print('txtValueOFHeader-->'+txtValueOFHeader)
    
    if (len(txtValueOFHeader) <2):
        txtValueOFHeader=companyName
        fileCount=fileNames[companyName]
        fileNames[companyName]=fileCount+1
        
    else:
        fileCount=fileNames[txtValueOFHeader];
    
    # create the file name, to output the csv file
    fileName                                         =txtValueOFHeader+'_'+str(fileCount)+'.csv'
    #print(out)
    
    file.write("Created the file for table name as -"+fileName+"\n")
    # export the out dataframe in the file.and index =false to prevent index file in csv file.
    out.to_csv(fileName,index                        =False)
    
    file.write("Exported the dataset to csv\n")
    
    file.write("Completed processing on Table No - "+ str(tableNumber)+"\n")
    file.write("--------------------------------------------------------------------------------\n")
    file.write("--------------------------------------------------------------------------------\n")
    tableNumber                                      =tableNumber+1
    # reinitialize it to remove all old data
    completeData                                     =[]
    
    # to remove all the date of dataFrame
    out                                              =pd.DataFrame(completeData)
    
  
file.close() 

print("pathForOutPut-->"+pathForOutPut)

zipFileName='newfile.zip'

# to delete the old file
if os.path.exists(zipFileName):
   os.remove(zipFileName)

# code to zip the file 
import os , zipfile

newZip = zipfile.ZipFile(zipFileName,'a')

for i in os.listdir(pathForOutPut):
    if ((i !=zipFileName) and (i !=logFileName)):
        newZip.write(i,compress_type=zipfile.ZIP_DEFLATED)
newZip.close()


# BV S3 code

# Creating the connection 
import boto3
s3 = boto3.resource('s3')

# generate bucket name
bucket_name = "adsteam04" + "_" +companyName

try:
    # Creating the bucket
    s3.create_bucket(Bucket=bucket_name)
	#Upload to S3 bucket
	s3.Object(bucket_name, zipFileName).put(Body=open(zipFileName, 'rb'))
	s3.Object(bucket_name, logFileName).put(Body=open(logFileName, 'rb'))
except Exception:
    print("Failed to make the connection,please enter valid AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
    






