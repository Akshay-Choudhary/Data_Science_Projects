import os
import pandas as pd

#=========================== Accepted Loans ===========================

# cols = ["id","member_id","loan_amnt","funded_amnt","funded_amnt_inv","term","int_rate","installment","grade","sub_grade","emp_title","emp_length","home_ownership","annual_inc","verification_status","issue_d","loan_status","pymnt_plan","url","desc","purpose","title","zip_code","addr_state","dti","delinq_2yrs","earliest_cr_line","fico_range_low","fico_range_high","inq_last_6mths","mths_since_last_delinq","mths_since_last_record","open_acc","pub_rec","revol_bal","revol_util","total_acc","initial_list_status","out_prncp","out_prncp_inv","total_pymnt","total_pymnt_inv","total_rec_prncp","total_rec_int","total_rec_late_fee","recoveries","collection_recovery_fee","last_pymnt_d","last_pymnt_amnt","next_pymnt_d","last_credit_pull_d","last_fico_range_high","last_fico_range_low","collections_12_mths_ex_med","mths_since_last_major_derog","policy_code","application_type","annual_inc_joint","dti_joint","verification_status_joint","acc_now_delinq","tot_coll_amt","tot_cur_bal","open_acc_6m","open_il_6m","open_il_12m","open_il_24m","mths_since_rcnt_il","total_bal_il","il_util","open_rv_12m","open_rv_24m","max_bal_bc","all_util","total_rev_hi_lim","inq_fi","total_cu_tl","inq_last_12m","acc_open_past_24mths","avg_cur_bal","bc_open_to_buy","bc_util","chargeoff_within_12_mths","delinq_amnt","mo_sin_old_il_acct","mo_sin_old_rev_tl_op","mo_sin_rcnt_rev_tl_op","mo_sin_rcnt_tl","mort_acc","mths_since_recent_bc","mths_since_recent_bc_dlq","mths_since_recent_inq","mths_since_recent_revol_delinq","num_accts_ever_120_pd","num_actv_bc_tl","num_actv_rev_tl","num_bc_sats","num_bc_tl","num_il_tl","num_op_rev_tl","num_rev_accts","num_rev_tl_bal_gt_0","num_sats","num_tl_120dpd_2m","num_tl_30dpd","num_tl_90g_dpd_24m","num_tl_op_past_12m","pct_tl_nvr_dlq","percent_bc_gt_75","pub_rec_bankruptcies","tax_liens","tot_hi_cred_lim","total_bal_ex_mort","total_bc_limit","total_il_high_credit_limit"]

accepteddf = pd.read_csv("LoanoutFile.csv", low_memory=False, usecols=[2,11,21,23,24,51,52])
accepteddf.columns = ["Amount Requested","Employment Length","Loan Title","State","Debt-To-Income Ratio","high","low"]

# accepteddf.columns = ["Amount Requested","Employment Length","Loan Title","State","Debt-To-Income Ratio","high","low"]
# accepteddf["Score"] = (accepteddf["high"] + accepteddf["low"])/2
# accepteddf["diff"] = (accepteddf["high"] - accepteddf["low"])
# accepteddf["diff"].unique()

accepteddf["Score"] = accepteddf["high"]
accepteddf = accepteddf.drop(["high","low"], axis = 1)
accepteddf["LoanStatus"] = "Approved"

accepteddf.dtypes

accepteddf.head()

#=========================== Rejected Loans ===========================

os.chdir("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/")
rejectdf = pd.read_csv("RejectLoanoutFile.csv", low_memory=False)

rejectdf = rejectdf.dropna(subset=['Risk_Score'], how='any')

MonthAndYear = []
MonthAndYear = rejectdf['Application Date'].str.split('-')
rejectdf['Year']= MonthAndYear.str[0]
rejectdf['Month']= MonthAndYear.str[1]
rejectdf['Date']= MonthAndYear.str[2]

rejectdf['Year'] = (rejectdf['Year']).astype(int)
rejectdf = rejectdf[rejectdf['Year'] > 2013]
new_risk_score = []
for row in rejectdf['Risk_Score']:
   newval = (((row - 501) * 550) / 489) + 300
   new_risk_score.append(newval)
rejectdf['Score'] = new_risk_score
rejectdf['Score'] = (rejectdf['Score'].round()).astype(int)

rejectdf["LoanStatus"] = "Rejected"

val = rejectdf["Debt-To-Income Ratio"].str.split('%').str[0]
rejectdf["Debt-To-Income Ratio"] = val

rejectdf = rejectdf.drop(['Application Date','Zip Code','Policy Code'],axis = 1)
rejectdf = rejectdf.drop(['Risk_Score','Year','Month','Date'], axis=1)

cols = ["Amount Requested","Employment Length","Loan Title","State","Debt-To-Income Ratio","Score","LoanStatus"]
rejectdf = rejectdf[cols]

rejectdf.isnull().sum()
rejectdf.head()

#=========================== Merge Files ===========================

# mergeddf = rejectdf.append(accepteddf)

mergeddf = pd.concat([accepteddf, rejectdf])

mergeddf.isnull().sum()

mergeddf["Loan Title"] = mergeddf["Loan Title"].fillna('Loan Title Not Specified')

mergeddf['State'] = mergeddf['State'].fillna('NA')

year = mergeddf['Employment Length'].str.split(' y').str[0]
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
   elif row == '0':
       emp_length_years.append('0')
   elif row == '10':
       emp_length_years.append('10')

mergeddf['Employment Length'] = emp_length_years

mergeddf['LoanStatus'].unique()

mergeddf.to_csv("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/LoanCombinedClean.csv", index = False)
