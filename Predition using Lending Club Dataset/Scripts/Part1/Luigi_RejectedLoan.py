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
import sys
import csv
import urllib.request

import luigi
import io
import boto
import boto3
from luigi import configuration
from luigi.contrib.s3 import S3Target
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class DownloadData(luigi.Task):

    def run(self):
        url = 'https://www.lendingclub.com/info/download-data.action'

        # Scrape the HTML at the url
        r = requests.get(url)

        # Turn the HTML into a Beautiful Soup object
        soup = BeautifulSoup(r.text, 'lxml')

        elementValue=soup.find( id='currentRejectStatsFileName')

        hrefValue=elementValue['href']

        commLink=hrefValue[0:hrefValue.index('A')]

        CurrWorkingDir=os.getcwd();
        print(CurrWorkingDir)
        pathForOutPut=CurrWorkingDir+'/'+"Part2"

        # check whether path is present or not
        if not os.path.exists(pathForOutPut):
            # will come if path is not present and will create path(folder)
            os.makedirs(pathForOutPut)

        # change the working dir to new path,(to generate the files under particular company folder)
        os.chdir(pathForOutPut)

        print("path")
        print(os.getcwd())

        dict={"2007-2012":"A.csv.zip","2013-2014":"B.csv.zip","2015":"D.csv.zip","2016 -Q1":"_2016Q1.csv.zip","2016 -Q2":"_2016Q2.csv.zip",
        "2016 -Q3":"_2016Q3.csv.zip","2016 -Q4":"_2016Q4.csv.zip"}

        #commLink='https://resources.lendingclub.com/LoanStats'
        listofFinalLink=[]
        session = requests.Session()
        for key, value in dict.items():
            print(commLink+value)
            listofFinalLink.append(commLink+value)
            dlink=commLink+value
            zipres=urllib.request.urlopen(dlink)

            with ZipFile(BytesIO(zipres.read())) as zfile:
                zfile.extractall(pathForOutPut)
                print(pathForOutPut)
                print("Done")

        fileNameForOut="RejectLoanoutFile.csv";
        f = open(fileNameForOut, 'w',newline='',encoding="utf8")
        writerFile = csv.writer(f)
        writerFile.writerow(['Amount Requested','Application Date','Loan Title','Risk_Score','Debt-To-Income Ratio','Zip Code','State','Employment Length','Policy Code'])
        skiprow=2;
        firstFile=True
        singleFileData=[];

        for singleCsvFilename in os.listdir(pathForOutPut):
            print(singleCsvFilename)
            if (singleCsvFilename !=fileNameForOut and (singleCsvFilename.find('Loan')==-1)):
                 with open(singleCsvFilename, 'rt',encoding="utf8") as fr:
                     count=0
                     skiprow=1
                     reader = csv.reader(fr, delimiter=',')
                     blankRowCount=0
                     for row in reader:
                         if(count<2):
                             count=count+1
                             continue;
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
                         writerFile.writerow(row)


        f.close()
        print(os.getcwd())
        print(os.getcwd() + "/RejectLoanoutFile.csv")
        
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part2/RejectLoanoutFile.csv")

class CleanData(luigi.Task):
    
    def requires(self):
        return DownloadData()
    
    
    def run(self):
        loanReject_file_tmp = pd.read_csv(DownloadData().output().path, delimiter=",",low_memory = False)
        

        loanReject_file_tmp = loanReject_file_tmp.dropna(subset=['Risk_Score'], how='any')
        loanReject_file_tmp[:100000]
        loanReject_file_tmp['Loan Title'] = loanReject_file_tmp['Loan Title'].fillna('Loan Title Not Specified')
        
        loanReject_file_tmp['State'] = loanReject_file_tmp['State'].fillna('XX')
        
        MonthAndYear = []
        MonthAndYear = loanReject_file_tmp['Application Date'].str.split('/')
        loanReject_file_tmp['Year']= MonthAndYear.str[0]
        loanReject_file_tmp['Month']= MonthAndYear.str[1]
        loanReject_file_tmp['Date']= MonthAndYear.str[2]
        
        year = loanReject_file_tmp['Employment Length'].str.split(' y').str[0]
        emp_length_years = []

        for row in year:
            if row == '10+':
                emp_length_years.append('10')
            elif row == '< 1':
                emp_length_years.append('0')
            elif row == '1':
                emp_length_years.append('1')
            elif row == '2':
                emp_length_years.append('2')
            elif row == '3':
                emp_length_years.append('3')
            elif row == '4':
                emp_length_years.append('4')
            elif row == '5':
                emp_length_years.append('5')
            elif row == '6':
                emp_length_years.append('6')
            elif row == '7':
                emp_length_years.append('7')
            elif row == '8':
                emp_length_years.append('8')
            elif row == '9':
                emp_length_years.append('9')
            elif row == 'n/a':
                emp_length_years.append('0')

        loanReject_file_tmp['Employment Length'] = emp_length_years
        
        loanReject_file_tmp = loanReject_file_tmp.drop(['Application Date','Zip Code','Policy Code'],axis = 1)
        loanReject_file_tmp.to_csv(self.output().path)
    
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part2/CleanedFile.csv")
    
class UploadToS3(luigi.Task):
    awsKey = luigi.Parameter(config_path=dict(section='path', name='aws_key'))
    awsSecret = luigi.Parameter(config_path=dict(section='path', name='aws_secret'))

    def requires(self):
        return [CleanData()]
  
    #def output(self):
        #return luigi.contrib.s3.S3Target('s3://luigibucket857/clean.csv') 

    def run(self):

        #Creating a connection
        access_key = self.awsKey
        access_secret = self.awsSecret
        conn = S3Connection(access_key, access_secret)

        #Connecting to the bucket
        bucket_name = "luigibucket857"
        bucket = conn.get_bucket(bucket_name)

        #Setting up the keys
        k = Key(bucket)
        k.key = "Part2_Pre_ProcessedData.csv"
        k.set_contents_from_filename("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part2/CleanedFile.csv")
    

if __name__ == '__main__':
    luigi.run()
