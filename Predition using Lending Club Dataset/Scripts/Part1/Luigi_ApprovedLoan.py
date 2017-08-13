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
from itertools import zip_longest


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

        # get the element by 'currentLoanStatsFileName' id
        elementValue=soup.find( id='currentLoanStatsFileName')

        # get the href value of element
        hrefValue=elementValue['href']

        # to get the common link from hrefValue
        commLink=hrefValue[0:hrefValue.index('3')]

        # get the current working directory
        CurrWorkingDir=os.getcwd();
        print(CurrWorkingDir)

        # add new path to it Part1
        pathForOutPut=CurrWorkingDir+'/'+"Part1"

        # check whether path is present or not
        if not os.path.exists(pathForOutPut):
            # will come if path is not present and will create path(folder)
            os.makedirs(pathForOutPut)
    
    

        # change the working dir to new path,(to generate the files under particular company folder)
        os.chdir(pathForOutPut)

        print("path")
        print(os.getcwd())

        #create dic for key value pair
        dict={"2007-2011":"3a.csv.zip","2012-2013":"3b.csv.zip","2014":"3c.csv.zip","2015":"3d.csv.zip",
              "2016 q1":"_2016Q1.csv.zip","2016 q2":"_2016Q2.csv.zip","2016 q3":"_2016Q3.csv.zip","2016 q4":"_2016Q4.csv.zip"}

        #commLink='https://resources.lendingclub.com/LoanStats'
        listofFinalLink=[]

        # iterate through the dictionary create the link and download the file in path.
        for key, value in dict.items():
            print(commLink+value)
            listofFinalLink.append(commLink+value)
            dlink=commLink+value
            zipres=urllib.request.urlopen(dlink)

            with ZipFile(BytesIO(zipres.read())) as zfile:
                zfile.extractall(pathForOutPut)
                print("Done")
       
        
        
        # output file name
        fileNameForOut="LoanoutFile.csv";

        #open the file with as w and newline=''
        f = open(fileNameForOut, 'w',newline='',encoding="utf8")
        writerFile = csv.writer(f)
        writerFile.writerow (["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","loan_status","pymnt_plan","url","desc","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","annual_inc_joint","dti_joint","verification_status_joint","acc_now_delinq","tot_coll_amt","tot_cur_bal","open_acc_6m","open_il_6m","open_il_12m","open_il_24m","mths_since_rcnt_il","total_bal_il","il_util","open_rv_12m","open_rv_24m","max_bal_bc","all_util","total_rev_hi_lim","inq_fi","total_cu_tl","inq_last_12m","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"])
        #created few variables that are required later    
        skiprow=2;
        firstFile=True
        singleFileData=[];

        #iterate over the files that are present at path
        for singleCsvFilename in os.listdir(pathForOutPut):
            print(singleCsvFilename)
            if ((singleCsvFilename !=fileNameForOut) and (singleCsvFilename.find('Reject')==-1)):
                 with open(singleCsvFilename, 'rt',encoding="utf8") as fr:
                     count=0
                     skiprow=1
                     reader = csv.reader(fr, delimiter=',')
                     blankRowCount=0
                     for row in reader:
                         # to escape the first two rows
                         if(count<2):
                             count=count+1
                             continue;
                         # to escape the row if row length is zero    
                         if(len(row)==0):
                             blankRowCount=blankRowCount+1
                             continue;

                         if(blankRowCount>2):
                             break;

                         # to escape the row that have 'Loans that do not meet the credit policy'
                         if(row[0]=='Loans that do not meet the credit policy'):
                             print(row[0]);
                             continue;

                         # to escape the row that have the text 'total'
                         if "Total" in row[0]:
                             print(row[0])
                             break;

                         # write the complete row data in file
                         writerFile.writerow(row)

        # after completion close the file
        f.close()
        print(os.getcwd())
        print(os.getcwd() + "/LoanoutFile.csv")
        
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part1/LoanoutFile.csv")

class CleanData(luigi.Task):
    
    def requires(self):
        return DownloadData()
    
    
    def run(self):
        
        loan_file_tmp = pd.read_csv(DownloadData().output().path, delimiter=",")
        # Handle Missing Data
        print("File Read")
        #Fill blank emp_title column with Employment Title Not Specified
        loan_file_tmp['emp_title'] = loan_file_tmp['emp_title'].fillna('Employment Title Not Specified')

        #Fill blank annual_inc column with median values
        loan_file_tmp['annual_inc'] = loan_file_tmp['annual_inc'].fillna(loan_file_tmp['annual_inc'].median())

        #Fill blank desc column with Description Not Specified
        loan_file_tmp['desc'] = loan_file_tmp['desc'].fillna('Description Not Specified')

        #Fill blank title column with Loan Title not specified 
        loan_file_tmp['title'] = loan_file_tmp['title'].fillna('Loan Title Not Specified')

        #Fill blank delinq_2yrscolumn with 0
        loan_file_tmp['delinq_2yrs'] = loan_file_tmp['delinq_2yrs'].fillna(0)

        #Fill blank inq_last_6mths column with 0
        loan_file_tmp['inq_last_6mths'] = loan_file_tmp['inq_last_6mths'].fillna(0)

        #Fill blank mths_since_last_delinq column with maximum value
        loan_file_tmp['mths_since_last_delinq'] = loan_file_tmp['mths_since_last_delinq'].fillna(loan_file_tmp['mths_since_last_delinq'].max())

        #Fill blank mths_since_last_record column with 0
        loan_file_tmp['mths_since_last_record'] = loan_file_tmp['mths_since_last_record'].fillna(0)

        #Fill blank open_acc column with 0
        loan_file_tmp['open_acc'] = loan_file_tmp['open_acc'].fillna(0)


        #Fill blank pub_rec columns with 0

        loan_file_tmp['pub_rec'] = loan_file_tmp['pub_rec'].fillna(0)


        # Strip % from values and copy the percentage values in the same column
        # Later fill blank values with median
        val = loan_file_tmp['revol_util'].str.split('%').str[0]
        loan_file_tmp['revol_util'] = val
        loan_file_tmp['revol_util'] = loan_file_tmp['revol_util'].fillna(loan_file_tmp['revol_util'].median())


        # Fill blank total_acc values column with 0

        loan_file_tmp['total_acc'] = loan_file_tmp['total_acc'].fillna(0)


        # Fill blank collections_12_mths_ex_med column with 0

        loan_file_tmp['collections_12_mths_ex_med'] = loan_file_tmp['collections_12_mths_ex_med'].fillna(0)


        # Fill blank mths_since_last_major_derog column with 0

        loan_file_tmp['mths_since_last_major_derog'] = loan_file_tmp['mths_since_last_major_derog'].fillna(0)


        # Fill blank annual_inc_joint column with 0

        loan_file_tmp['annual_inc_joint'] = loan_file_tmp['annual_inc_joint'].fillna(0)


        # Fill blank dti_joint column with 0

        loan_file_tmp['dti_joint'] = loan_file_tmp['dti_joint'].fillna(0)


        # Fill blank verification_status_joint column with N/A

        loan_file_tmp['verification_status_joint'] = loan_file_tmp['verification_status_joint'].fillna('N/A')


        # Fill blank acc_now_delinq column with 0

        loan_file_tmp['acc_now_delinq'] = loan_file_tmp['acc_now_delinq'].fillna(0)


        # Fill blank tot_coll_amt column with median values

        loan_file_tmp['tot_coll_amt'] = loan_file_tmp['tot_coll_amt'].fillna(loan_file_tmp['tot_coll_amt'].median())


        # Fill blank tot_cur_bal column with median values

        loan_file_tmp['tot_cur_bal'] = loan_file_tmp['tot_cur_bal'].fillna(loan_file_tmp['tot_cur_bal'].median())


        # Fill blank open_acc_6m column with median values

        loan_file_tmp['open_acc_6m'] = loan_file_tmp['open_acc_6m'].fillna(loan_file_tmp['open_acc_6m'].median())


        # Fill blank open_il_6m column with 0

        loan_file_tmp['open_il_6m'] = loan_file_tmp['open_il_6m'].fillna(0)


        # Fill blank acc_open_past_24mths column with 0

        loan_file_tmp['acc_open_past_24mths'] = loan_file_tmp['acc_open_past_24mths'].fillna(0)


        # Fill blank avg_cur_bal column with median values

        loan_file_tmp['avg_cur_bal'] = loan_file_tmp['avg_cur_bal'].fillna(loan_file_tmp['avg_cur_bal'].median())


        # Fill blank bc_open_to_buy column with median values

        loan_file_tmp['bc_open_to_buy'] = loan_file_tmp['bc_open_to_buy'].fillna(loan_file_tmp['bc_open_to_buy'].median())


        # Fill blank chargeoff_within_12_mths column with 0

        loan_file_tmp['chargeoff_within_12_mths'] = loan_file_tmp['chargeoff_within_12_mths'].fillna(0)


        # Fill blank delinq_amnt column with 0

        loan_file_tmp['delinq_amnt'] = loan_file_tmp['delinq_amnt'].fillna(0)


        # Fill blank mo_sin_old_il_acct column with 0

        loan_file_tmp['mo_sin_old_il_acct'] = loan_file_tmp['mo_sin_old_il_acct'].fillna(0)


        # Fill blank mo_sin_old_rev_tl_op column with 0

        loan_file_tmp['mo_sin_old_rev_tl_op'] = loan_file_tmp['mo_sin_old_rev_tl_op'].fillna(0)


        # Fill blank mo_sin_rcnt_rev_tl_op column with 0

        loan_file_tmp['mo_sin_rcnt_rev_tl_op'] = loan_file_tmp['mo_sin_rcnt_rev_tl_op'].fillna(0)


        # Fill blank mo_sin_rcnt_tl column with 0

        loan_file_tmp['mo_sin_rcnt_tl'] = loan_file_tmp['mo_sin_rcnt_tl'].fillna(0)


        # Fill blank mort_acc column with 0

        loan_file_tmp['mort_acc'] = loan_file_tmp['mort_acc'].fillna(0)


        # Fill blank mths_since_recent_bc with 0

        loan_file_tmp['mths_since_recent_bc'] = loan_file_tmp['mths_since_recent_bc'].fillna(0)


        # Fill blank mths_since_recent_inq with 0

        loan_file_tmp['mths_since_recent_inq'] = loan_file_tmp['mths_since_recent_inq'].fillna(0)


        # Fill blank mths_since_recent_revol_delinq with 0

        loan_file_tmp['mths_since_recent_revol_delinq'] = loan_file_tmp['mths_since_recent_revol_delinq'].fillna(0)


        # Fill blank num_accts_ever_120_pd with 0

        loan_file_tmp['num_accts_ever_120_pd'] = loan_file_tmp['num_accts_ever_120_pd'].fillna(0)


        # Fill blank num_actv_bc_tl with 0

        loan_file_tmp['num_actv_bc_tl'] = loan_file_tmp['num_actv_bc_tl'].fillna(0)


        # Fill blank num_actv_rev_tl with 0

        loan_file_tmp['num_actv_rev_tl'] = loan_file_tmp['num_actv_rev_tl'].fillna(0)


        # Fill blank num_bc_sats with 0

        loan_file_tmp['num_bc_sats'] = loan_file_tmp['num_bc_sats'].fillna(0)


        # Fill blank num_bc_tl with 0

        loan_file_tmp['num_bc_tl'] = loan_file_tmp['num_bc_tl'].fillna(0)


        # Fill blank num_il_tl with 0

        loan_file_tmp['num_il_tl'] = loan_file_tmp['num_il_tl'].fillna(0)


        # Fill blank num_op_rev_tl with 0

        loan_file_tmp['num_op_rev_tl'] = loan_file_tmp['num_op_rev_tl'].fillna(0)


        # Fill blank num_rev_accts with 0

        loan_file_tmp['num_rev_accts'] = loan_file_tmp['num_rev_accts'].fillna(0)


        # Fill blank num_rev_tl_bal_gt_0 column with 0

        loan_file_tmp['num_rev_tl_bal_gt_0'] = loan_file_tmp['num_rev_tl_bal_gt_0'].fillna(0)


        # Fill blank num_tl_120dpd_2m column with 0

        loan_file_tmp['num_tl_120dpd_2m'] = loan_file_tmp['num_tl_120dpd_2m'].fillna(0)


        # Fill blank num_tl_30dpd with 0

        loan_file_tmp['num_tl_30dpd'] = loan_file_tmp['num_tl_30dpd'].fillna(0)


        # Fill blank num_tl_90g_dpd_24m column with 0

        loan_file_tmp['num_tl_90g_dpd_24m'] = loan_file_tmp['num_tl_90g_dpd_24m'].fillna(0)


        # Fill blank num_tl_op_past_12m column with 0

        loan_file_tmp['num_tl_op_past_12m'] = loan_file_tmp['num_tl_op_past_12m'].fillna(0)


        # Fill blank num_op_rev_tl column with 0

        loan_file_tmp['num_op_rev_tl'] = loan_file_tmp['num_op_rev_tl'].fillna(0)


        # Fill blank pct_tl_nvr_dlq column with median values

        loan_file_tmp['pct_tl_nvr_dlq'] = loan_file_tmp['pct_tl_nvr_dlq'].fillna(loan_file_tmp['pct_tl_nvr_dlq'].median())


        # Fill blank percent_bc_gt_75 column with median values

        loan_file_tmp['percent_bc_gt_75'] = loan_file_tmp['percent_bc_gt_75'].fillna(loan_file_tmp['percent_bc_gt_75'].median())


        # Fill blank pub_rec_bankruptcies column with 0

        loan_file_tmp['pub_rec_bankruptcies'] = loan_file_tmp['pub_rec_bankruptcies'].fillna(0)


        # Fill blank tax_liens column with 0

        loan_file_tmp['tax_liens'] = loan_file_tmp['tax_liens'].fillna(0)


        # Fill blank tot_hi_cred_lim with median values

        loan_file_tmp['tot_hi_cred_lim'] = loan_file_tmp['tot_hi_cred_lim'].fillna(loan_file_tmp['tot_hi_cred_lim'].median())


        # Fill blank total_bal_ex_mort with median values

        loan_file_tmp['total_bal_ex_mort'] = loan_file_tmp['total_bal_ex_mort'].fillna(loan_file_tmp['total_bal_ex_mort'].median())


        # Fill blank total_bc_limit with median values

        loan_file_tmp['total_bc_limit'] = loan_file_tmp['total_bc_limit'].fillna(loan_file_tmp['total_bc_limit'].median())


        # Fill blank total_il_high_credit_limit with median values

        loan_file_tmp['total_il_high_credit_limit'] = loan_file_tmp['total_il_high_credit_limit'].fillna(loan_file_tmp['total_il_high_credit_limit'].median())

        print("Data filled")
        # Drop Columns that have significant proportion of values blank
        loan_file_tmp = loan_file_tmp.drop(['open_il_12m','open_il_24m','mths_since_rcnt_il','total_bal_il','il_util','open_rv_12m','open_rv_24m','max_bal_bc','all_util','inq_fi','total_cu_tl','inq_last_12m','bc_util','mths_since_recent_bc_dlq','last_pymnt_d','next_pymnt_d','last_credit_pull_d'], axis=1)

        #Convert Dataframe to CSV

        loan_file_tmp.to_csv(self.output().path)
    
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part1/CleanedFile.csv")

class FeatureSelection(luigi.Task):
    def requires(self):
        return CleanData()
    
    def run(self):
        loan_file_tmp = pd.read_csv(CleanData().output().path, delimiter=",")
        
        #Feature Selection
        
        year = loan_file_tmp['emp_length'].str.split(' y').str[0]
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

        loan_file_tmp['emp_ength'] = emp_length_years


        #New Column to identify % of active accounts 
        active_accounts = loan_file_tmp['open_il_6m'] + loan_file_tmp['num_actv_bc_tl'] + loan_file_tmp['num_actv_rev_tl']
        total_accounts = loan_file_tmp['num_il_tl'] + loan_file_tmp['num_bc_tl'] + loan_file_tmp['num_rev_accts']
        loan_file_tmp['% curr_active_accounts'] = (active_accounts/total_accounts) * 100

        acc_close_status = []
        # Based on active_accounts percentage categorise into Poor, Fair, Good and Excellent category
        for row in loan_file_tmp['% curr_active_accounts']:
            if row > 75:
                acc_close_status.append('Poor')
            elif row > 50:
                acc_close_status.append('Fair')
            elif row > 25:
                acc_close_status.append('Good')
            else:
                acc_close_status.append('Excellent')

        loan_file_tmp['Acc_Closure_Rate'] = acc_close_status



        # mths_since_last_major_derog

        dero_status = []

        #Since we are looking for just 6 months of data classify mths_since_last_major_derog column into Yes or No for last 6 months
        for row in loan_file_tmp['mths_since_last_major_derog']:
            if row > 180:
                dero_status.append('Yes')
            else:
                dero_status.append('No')

        loan_file_tmp['derogatory_account'] = dero_status


        #num_accts_ever_120_pd

        days_past_due = []
        #Classify num_accts_ever_120_pd into 120+_days_pastdue_account as 0 and 1.
        for row in loan_file_tmp['num_accts_ever_120_pd']:
            if row > 0:
                days_past_due.append(1)
            else:
                days_past_due.append(0)

        loan_file_tmp['120+_days_pastdue_account'] = days_past_due


        # Drop values that are not significant to contributing towards Interest Rate prediction.

        loan_file_tmp = loan_file_tmp.drop(['id','member_id','installment','grade','sub_grade','issue_d','loan_status','pymnt_plan','url','desc','title','zip_code','addr_state','earliest_cr_line','inq_last_6mths','mths_since_last_record','initial_list_status','out_prncp','out_prncp_inv','total_pymnt','total_pymnt_inv','total_rec_prncp','total_rec_int','total_rec_late_fee','recoveries','collection_recovery_fee','collections_12_mths_ex_med','policy_code','tot_coll_amt','tot_cur_bal','open_acc_6m','delinq_amnt','mo_sin_old_il_acct','mo_sin_old_rev_tl_op','mo_sin_rcnt_rev_tl_op','mo_sin_rcnt_tl','mths_since_recent_bc','mths_since_recent_inq','mths_since_recent_revol_delinq','num_accts_ever_120_pd','num_actv_bc_tl','num_actv_rev_tl','num_bc_sats','num_bc_tl','num_il_tl','num_op_rev_tl','num_rev_accts','num_rev_tl_bal_gt_0','num_sats','num_tl_120dpd_2m','num_tl_30dpd','num_tl_90g_dpd_24m','num_tl_op_past_12m','pub_rec_bankruptcies','tax_liens','% curr_active_accounts','mths_since_last_major_derog'], axis=1)
        loan_file_tmp.to_csv(self.output().path)

    
    def output(self):
        return luigi.LocalTarget("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part1/ProcessedFile.csv")




class UploadToS3(luigi.Task):
    awsKey = luigi.Parameter(config_path=dict(section='path', name='aws_key'))
    awsSecret = luigi.Parameter(config_path=dict(section='path', name='aws_secret'))

    def requires(self):
        return [FeatureSelection()]
  
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
        k.key = "PreProcessed_Data.csv"
        k.set_contents_from_filename("/home/akshay/Desktop/Assignment3_TestPart1/Luigi_Tasks/Part1/ProcessedFile.csv")
    

if __name__ == '__main__':
    luigi.run()
