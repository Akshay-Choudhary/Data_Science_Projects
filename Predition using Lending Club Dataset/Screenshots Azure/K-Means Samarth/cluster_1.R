library(data.table)

importcsv<-function(filename){
  # import csv
  df = read.csv(filename, sep = ",", fill = TRUE, header = TRUE)
  return(df)
}

loancsv <- ("C:\\Samarth\\samarth_backup_4_10_2017\\Semester-4\\ADS\\Assignments\\Assignment_02\\Clustering\\AcceptedLoansClean.csv")
loandf <- importcsv(loancsv)

loandf_1=loandf

loandf_1 <- head(loandf,100000)

#loandf_1 <- subset(loandf_1, select = -c(emp_length))

loandf_1 <- subset(loandf_1, select = -c(verification_status_joint))
loandf_1 <- subset(loandf_1, select = -c(funded_amnt_inv))

loandf_1 <- subset(loandf_1, select = -c(fico_range_high))
loandf_1 <- subset(loandf_1, select = -c(mths_since_last_delinq))
loandf_1 <- subset(loandf_1, select = -c(pub_rec))
loandf_1 <- subset(loandf_1, select = -c(last_pymnt_amnt))
loandf_1 <- subset(loandf_1, select = -c(last_fico_range_high))
loandf_1 <- subset(loandf_1, select = -c(last_fico_range_low))
loandf_1 <- subset(loandf_1, select = -c(application_type))
loandf_1 <- subset(loandf_1, select = -c(annual_inc_joint))
loandf_1 <- subset(loandf_1, select = -c(verification_status_joint))
loandf_1 <- subset(loandf_1, select = -c(acc_now_delinq))
loandf_1 <- subset(loandf_1, select = -c(open_il_6m))
loandf_1 <- subset(loandf_1, select = -c(total_rev_hi_lim))


#loandf_1 <- subset(loandf_1, select = -c(acc_open_past_24mths))
loandf_1 <- subset(loandf_1, select = -c(bc_open_to_buy))
loandf_1 <- subset(loandf_1, select = -c(chargeoff_within_12_mths))
loandf_1 <- subset(loandf_1, select = -c(mort_acc))
loandf_1 <- subset(loandf_1, select = -c(pct_tl_nvr_dlq))
loandf_1 <- subset(loandf_1, select = -c(Acc_Closure_Rate))
#loandf_1 <- subset(loandf_1, select = -c(120+_days_pastdue_account))

#---------------added newly-----------------
loandf_1 <- subset(loandf_1, select = -c(open_acc))
loandf_1 <- subset(loandf_1, select = -c(revol_bal))
loandf_1 <- subset(loandf_1, select = -c(revol_util))
loandf_1 <- subset(loandf_1, select = -c(avg_cur_bal))
#loandf_1 <- subset(loandf_1, select = -c(percent_bc_gt_75))
loandf_1 <- subset(loandf_1, select = -c(tot_hi_cred_lim))
loandf_1 <- subset(loandf_1, select = -c(total_bal_ex_mort))
#loandf_1 <- subset(loandf_1, select = -c(total_bc_limit))
loandf_1 <- subset(loandf_1, select = -c(total_il_high_credit_limit))
loandf_1 <- subset(loandf_1, select = -c(derogatory_account))
loandf_1 <- subset(loandf_1, select = -c(fico_range_low))
loandf_1 <- subset(loandf_1, select = -c(loan_amnt))

loandf_1 <- subset(loandf_1, select = -c(emp_title))
loandf_1 <- subset(loandf_1, select = -c(emp_length))
loandf_1 <- subset(loandf_1, select = -c(dti))
loandf_1 <- subset(loandf_1, select = -c(delinq_2yrs))
#loandf_1 <- subset(loandf_1, select = -c(inq_last_6mths))


print(loandf_1$loan_amnt)

#loandf_1$loan_amnt <- as.integer(loandf_1$loan_amnt)
loandf_1$funded_amnt <- as.integer(loandf_1$funded_amnt)
loandf_1$term <- as.integer(as.factor(loandf_1$term))
loandf_1$int_rate <- as.integer(loandf_1$int_rate)
#loandf_1$emp_title <- as.integer(as.factor(loandf_1$emp_title))

#loandf_1$emp_length <- as.integer(loandf_1$emp_length)
loandf_1$home_ownership <- as.integer(as.factor(loandf_1$home_ownership))
loandf_1$annual_inc <- as.integer(loandf_1$annual_inc)
loandf_1$verification_status <- as.integer(as.factor(loandf_1$verification_status))
loandf_1$purpose <- as.integer(as.factor(loandf_1$purpose))

loandf_1$addr_state <- as.integer(as.factor(loandf_1$addr_state))

loandf_1$total_acc <- as.integer(loandf_1$total_acc)


loandf_1$inq_last_6mths <- as.integer(loandf_1$inq_last_6mths)
loandf_1$acc_open_past_24mths <- as.integer(loandf_1$acc_open_past_24mths)
loandf_1$percent_bc_gt_75 <- as.integer(loandf_1$percent_bc_gt_75)
loandf_1$total_bc_limit <- as.integer(loandf_1$total_bc_limit)
loandf_1$Score <- as.integer(loandf_1$Score)



#loandf_1$dti <- as.integer(loandf_1$dti)
#loandf_1$delinq_2yrs <- as.integer(as.factor(loandf_1$delinq_2yrs))
#----------------removed -------------
loandf_1$open_acc <- as.integer(loandf_1$open_acc)
loandf_1$revol_bal <- as.integer(loandf_1$revol_bal)
loandf_1$revol_util <- as.integer(loandf_1$revol_util)

loandf_1$avg_cur_bal <- as.integer(loandf_1$avg_cur_bal)
loandf_1$percent_bc_gt_75 <- as.integer(loandf_1$percent_bc_gt_75)
loandf_1$tot_hi_cred_lim <- as.integer(loandf_1$tot_hi_cred_lim)
loandf_1$total_bal_ex_mort <- as.integer(loandf_1$total_bal_ex_mort)
loandf_1$total_bc_limit <- as.integer(loandf_1$total_bc_limit)

loandf_1$total_il_high_credit_limit <- as.integer(loandf_1$total_il_high_credit_limit)
loandf_1$derogatory_account <- as.integer(loandf_1$derogatory_account)
loandf_1$fico_range_low <- as.integer(loandf_1$fico_range_low)
#--------------------end removed ------------------
summary(loandf_1)

iris # New dataset
?kmeans # What is kmean?



# ================================ K-Means Clustering ==================================== #

km.out <- kmeans(loandf_1,6,nstart=10) #nstart tells how many times algorithm
# starts from beginning since the final answers is related to initial assignments.
names(km.out)
km.out$centers # kmeans results
plot(loandf_1, col=(km.out$cluster), main="K-mean result with k=6") #Scatterplot matrix

km.out$centers
km.out$size

data1 <-loandf_1[km.out$cluster==1,]
print(length(data1$loan_amnt))
write.csv(data1, file="clusterData1.csv",row.names=FALSE)

data2 <-loandf_1[km.out$cluster==2,]
write.csv(data2, file="clusterData2.csv",row.names=FALSE)

data3 <-loandf_1[km.out$cluster==3,]
write.csv(data3, file="clusterData3.csv",row.names=FALSE)

data4 <-loandf_1[km.out$cluster==4,]
write.csv(data4, file="clusterData4.csv",row.names=FALSE)

data5 <-loandf_1[km.out$cluster==5,]
write.csv(data5, file="clusterData5.csv",row.names=FALSE)

data6 <-loandf_1[km.out$cluster==6,]
write.csv(data6, file="clusterData6.csv",row.names=FALSE)


