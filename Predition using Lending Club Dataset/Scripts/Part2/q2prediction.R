gc()
## ======================================== Functions ========================================== ##

importcsv<-function(filename){
  # import csv
  df = read.csv(filename, sep = ",", header = TRUE)
  return(df)
}

tonumeric<-function(cleandf){
  cleandf$term <- as.numeric(cleandf$term)
  cleandf$home_ownership <- as.numeric(cleandf$home_ownership)
  cleandf$verification_status <- as.numeric(cleandf$verification_status)
  cleandf$purpose <- as.numeric(cleandf$purpose)
  cleandf$application_type <- as.numeric(cleandf$application_type)
  cleandf$Acc_Closure_Rate <- as.numeric(cleandf$Acc_Closure_Rate)
  cleandf$derogatory_account <- as.numeric(cleandf$derogatory_account)
  cleandf$addr_state <- as.numeric(cleandf$addr_state)
  return(cleandf)
}

## ================================== script execution ========================================= ##

acptloanscsv <- ("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/AcceptedLoansClean.csv")
acptloans <- importcsv(acptloanscsv)
str(acptloans)
test <- acptloans
test <- test[,-c(1,26)]
acptloans <- test
rm(test)

acptloans <- tonumeric(acptloans)

#============================= feature (variable) selection ================================================
library(leaps)

# exhaustive search --------------------------
features.ex <- regsubsets(int_rate ~ .,data=acptloans, nvmax = 12, really.big = T)
coef(features.ex,12)
ex.summary <- summary(features.ex)
names(ex.summary)
ex.summary$rss
ex.summary$adjr2
plot(ex.summary$adjr2, xlab = "Number of variables", ylab = "Adjusted R^2", type = "l")

# forward selection --------------------------
features.fwd <- regsubsets(int_rate ~ .,data=acptloans, nvmax = 12, method = "forward")
coef(features.fwd, 12)
fwd.summary <- summary(features.fwd)
names(fwd.summary)
fwd.summary$rss
fwd.summary$adjr2
plot(fwd.summary$adjr2, xlab = "Number of variables", ylab = "Adjusted R^2", type = "l")

# Backward selection --------------------------
features.bck <- regsubsets(int_rate ~ .,data=acptloans, nvmax = 12, method = "backward")
coef(features.bck, 12)
bck.summary <- summary(features.bck)
names(bck.summary)
bck.summary$rss
bck.summary$adjr2
plot(bck.summary$adjr2, xlab = "Number of variables", ylab = "Adjusted R^2", type = "l")

# Stepwise selection --------------------------
features.step <- regsubsets(int_rate ~ .,data=acptloans, nvmax = 12, method = "seqrep")
coef(features.step, 12)
step.summary <- summary(features.step)
names(step.summary)
step.summary$rss
step.summary$adjr2
plot(step.summary$adjr2, xlab = "Number of variables", ylab = "Adjusted R^2", type = "l")

library(mlbench)
library(caret)
correlationMatrix <- cor(acptloans[,1:44])
print(correlationMatrix)
highlyCorrelated <- findCorrelation(correlationMatrix, cutoff=0.75)
print(highlyCorrelated)

cols <- labels(coef(features.ex,12))
cols <- cols[cols != "(Intercept)"]
cols <- append(cols, "int_rate")
cols

# ================================ Split the data to train and test ==================================== #

samp_size <- floor(0.75 * nrow(acptloans))
set.seed(12345)
train_loan <- sample(seq_len(nrow(acptloans)), size = samp_size)
train.acptloans <- acptloans[train_loan, ]
test.acptloans <- acptloans[-train_loan, ]

# ================================ Linear Regression Algorithm ==================================== #

lm.f <- as.formula(paste("int_rate ~", paste(cols[!cols %in% "int_rate"], collapse = " + ")))
lm.full <- lm(lm.f,data=acptloans)
summary(lm.full)
plot(lm.full)

# ================================ Random forest starts ==================================== #
library(randomForest)

# RF model on test data 
rf.f <- as.formula(paste("int_rate ~", paste(cols[!cols %in% "int_rate"], collapse = " + ")))
rfmodel <- randomForest(rf.f, data = train.acptloans, ntree=8)

# RF summary output 
summary(rfmodel)

# RF importance of each predictor in the model 
imp <- importance(rfmodel)

# plot for imp predictors to pdf =============================
pdf("RF_top_predictors.pdf",width=7,height=5)
print("================= Top predictors to a pdf ================================= ")
plot(imp, main = "Influential Predictors", top = 5)
dev.off()

#Predict using the test data
rfpred <- predict(rfmodel, test.acptloans[,cols])

# prediction accuracy
accuracy(rfpred, q2orig1$origintrate)

# ================================ KNN starts ==================================== #

summary(train.acptloans)

library(caret)
require(class)

knn.f <- as.formula(paste("int_rate ~", paste(cols[!cols %in% "int_rate"], collapse = " + ")))
nrow(train.acptloans)
model.knn <- train(knn.f, data = train.acptloans, method = "knn", k = 3)

str(train.acptloans)

# print(model.knn)

# knn.pred <- predict(model.knn, q2orig1[,cols])
# accuracy(knn.pred, q2orig1$origintrate)

# validate the model
#validation<- validation[,orig1[c("creditscore", "maturitydate", "nofunits", "occstatus", "origupb", "origltv", "proptype", "loanpurpose" )]

# # predict the values
# predictions <- predict(model.knn, test[,1:8])

# # calculate the accuracy
# accuracy <- sum(predictions == q2orig1$origintrate)/nrow(q2orig1)

#=================================================== Manual Cluster ================================================

# North_East = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA']
# Mid_West = ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD']
# South = ['DE', 'FL', 'GA', 'MD', 'NC', 'SC' , 'VA', 'DC', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX']
# West = ['AZ', 'CO', 'ID', 'MT', 'NE', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']

splitdf <- acptloans
str(splitdf)

ne.df <- splitdf[splitdf$addr_state %in% c('CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'),]
nrow(ne.df)
unique(ne.df$addr_state)

midwest.df <- splitdf[splitdf$addr_state %in% c('IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'),]
nrow(midwest.df)
unique(midwest.df$addr_state)

south.df <- splitdf[splitdf$addr_state %in% c('DE', 'FL', 'GA', 'MD', 'NC', 'SC' , 'VA', 'DC', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'),]
nrow(south.df)
unique(south.df$addr_state)

west.df <- splitdf[splitdf$addr_state %in% c('AZ', 'CO', 'ID', 'MT', 'NE', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA'),]
nrow(west.df)
unique(west.df$addr_state)

nrow(splitdf)
nrow(ne.df) + nrow(midwest.df) + nrow(south.df) + nrow(west.df)

write.csv(ne.df, file = "nedf.csv", row.names = TRUE )
write.csv(midwest.df, file = "midwestdf.csv", row.names = TRUE)
write.csv(south.df, file = "southdf.csv", row.names = TRUE)
write.csv(west.df, file = "westdf.csv", row.names = TRUE)

# end of script execution, please review the output file and the and error logs for the exectuion steps
# ## ========================================== End of script ========================================= ##
