import urllib
from io import BytesIO
import pandas as pd
import os
import numpy as np
import sys
import csv
import urllib.request
import configparser

import luigi
import io
import boto
import boto3
from luigi import configuration
#from azure.storage.blob import BlockBlobService
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


class DownloadData(luigi.Task):

    def run(self):
        CurrWorkingDir=os.getcwd();
        print(CurrWorkingDir)

        dlink="https://data.cityofnewyork.us/api/views/76xm-jjuj/rows.csv?accessType=DOWNLOAD";

        zipres=urllib.request.urlopen(dlink)
        fileNameForOut="DownloadedFile.csv";
        f = open(fileNameForOut, 'wb')

        f.write(zipres.read());

        f.close();
        
        rejectdf = pd.read_csv("DownloadedFile.csv")
        #select the sample 1500000 record
        finalOutRandom=rejectdf.sample(n=1500000)
        outPutfileNameSec="samplefinalOutFile.csv"
        


        
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/ADS/Final_Luigi/DownloadedFile.csv")
    
class TakeSample(luigi.Task):
    
    def requires(self):
        return DownloadData()
    
    def run(self):
        rejectdf = pd.read_csv(DownloadData().output().path, low_memory = False)
        #select the sample 1500000 record
        finalOutRandom=rejectdf.sample(n=1500000)
        outPutfileNameSec="SampleFile.csv"
        finalOutRandom.to_csv(outPutfileNameSec,index=False)
        
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/ADS/Final_Luigi/SampleFile.csv")
        
    
        
    
class CleanData(luigi.Task):
    def requires(self):
        return TakeSample()
    
    def run(self):
        
        df = pd.read_csv(TakeSample().output().path, low_memory = False)
        
        sample_df = df
        
        sample_df = sample_df.drop(['CAD_INCIDENT_ID','FIRST_HOSP_ARRIVAL_DATETIME','FIRST_TO_HOSP_DATETIME','ATOM'], axis =1)
        
        #Drop Remaining Empty rows since the ratio of them to the total is alomst negligible
        sample_df = sample_df.dropna(subset=['INCIDENT_TRAVEL_TM_SECONDS_QY'], how='any')
        sample_df = sample_df.dropna(subset=['INCIDENT_RESPONSE_SECONDS_QY'], how='any')
        sample_df = sample_df.dropna(subset=['FIRST_ACTIVATION_DATETIME'], how='any')
        sample_df = sample_df.dropna(subset=['INCIDENT_CLOSE_DATETIME'], how='any')
        sample_df = sample_df.dropna(subset=['ZIPCODE'], how='any')
        sample_df = sample_df.dropna(subset=['CITYCOUNCILDISTRICT'], how='any')
        sample_df = sample_df.dropna(subset=['COMMUNITYSCHOOLDISTRICT'], how='any')
        sample_df = sample_df.dropna(subset=['COMMUNITYDISTRICT'], how='any')
        sample_df['INCIDENT_DISPOSITION_CODE'] = sample_df['INCIDENT_DISPOSITION_CODE'].fillna(sample_df['INCIDENT_DISPOSITION_CODE'].max())
        
        #Derive Sev_Category_Level
        
        sev_level = []
        # Based on active_accounts percentage categorise into Poor, Fair, Good and Excellent category
        for row in df['FINAL_SEVERITY_LEVEL_CODE']:
            if row > 6:
                sev_level.append('Low')
            elif row > 3:
                sev_level.append('Med')
            else:
                sev_level.append('High')

        df['Call_Sev_Category'] = sev_level
        
        #Drop DateTime columns that would not help in identifying held indicator.
        sample_df = sample_df.drop(['INCIDENT_DATETIME','FIRST_ASSIGNMENT_DATETIME','FIRST_ACTIVATION_DATETIME','FIRST_ON_SCENE_DATETIME','INCIDENT_CLOSE_DATETIME'], axis =1)
        
        #Drop Location Columns 
        sample_df = sample_df.drop(['POLICEPRECINCT','CITYCOUNCILDISTRICT','COMMUNITYDISTRICT','COMMUNITYSCHOOLDISTRICT','CONGRESSIONALDISTRICT'], axis =1)
        
        
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/ADS/Final_Luigi/CleanedFile.csv")


class UploadToAzure(luigi.Task):
    #acc_name = luigi.Parameter(config_path=dict(section='path', name='accname'))
    #azure_Key = luigi.Parameter(config_path=dict(section='path', name='acckey'))

    def requires(self):
        return [CleanData()]

    #def output(self):
        #return luigi.contrib.s3.S3Target('s3://luigibucket857/clean.csv')

    def run(self):

	#Creating a connection
        #account = self.acc_name
        #access_key = self.azure_key
        
        block_blob_service = BlockBlobService(account_name='**********', account_key='**********************')
        block_blob_service.create_container('testcontainer')

        # upload the file to the blob
        block_blob_service.create_blob_from_path(
            'testcontainer',
            'Project_PreprocessedFile.csv',
            'CleanedFile.csv',
            content_settings=ContentSettings(content_type='application/CSV')
            )

#         #Creating a connection
#         access_key = self.awsKey
#         access_secret = self.awsSecret
#         conn = S3Connection(access_key, access_secret)

#         print("Connecting to S3 =======================>")

#         #Connecting to the bucket
#         bucket_name = "luigibucket857"
#         bucket = conn.get_bucket(bucket_name)

#         #Setting up the keys
#         k = Key(bucket)
#         k.key = "Downloaded_Data.csv"
#         k.set_contents_from_filename("/home/akshay/Desktop/ADS/Final_Luigi/DownloadedFile.csv")

#         print("Completed UploadToS3 Task =======================>")

    
   

    

if __name__ == '__main__':
    luigi.run()
