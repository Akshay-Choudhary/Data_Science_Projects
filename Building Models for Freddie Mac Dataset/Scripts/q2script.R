setwd("/home/bhavik/ADS_FIles/Assignments/Midterm/Q2/historical_data1_2005_origination")
gc()

## ======================= import the required libraries ========================================= ##

library(sqldf)
library(data.table)
library(zoo)
library(forecast)
library(leaps)
library(randomForest)
library(caret)
require(class)
library(neuralnet)

# =========================== import First Quarter origination file ========================= ##

q12005orig = read.table("historical_data1_Q12005.txt", sep = "|" )
# set column names to the dataframe
names(q12005orig) <- c("creditscore","firstpymtdate","firsttimehome","maturitydate","msa","mortinsuperct","nofunits","occstatus","origcltv","dtiratio","origupb","origltv","origintrate","channel","ppmflag","prodtype","propstate","proptype","postalcode","loanseq","loanpurpose","origterm","nofborrowers","sellername","servicername","conformingflag")
# select rows for the model 
orig1 <- q12005orig[,c("creditscore","firsttimehome","maturitydate","msa", "nofunits", "occstatus", "origcltv","dtiratio","origupb","origltv", "origintrate", "propstate", "proptype", "loanpurpose", "origterm", "nofborrowers")]
#remove the bigger dataframe
rm(q12005orig)

## =========================== Data Wrangling First Quarter File ============================ ##

# select the credit score - mean ==============
creditscore <- orig1$creditscore
# fill credit score with mean values
orig1$creditscore <- trunc(na.aggregate(creditscore))
rm(creditscore)

# select first time home buyer - lcof ===========
orig1$firsttimehome[orig1$firsttimehome==""] <- NA
orig1$firsttimehome <- na.locf(orig1$firsttimehome)
orig1$firsttimehome <- as.numeric(orig1$firsttimehome)
str(orig1$firsttimehome)

# Select Maturity Date - as-is =====================

# select MSA - lcof =======================
orig1$msa <- na.locf(orig1$msa)

# select no of units - locf ========================
orig1$nofunits <- na.locf(orig1$nofunits)

# select occupancy status - locf ========================
orig1$occstatus <- na.locf(orig1$occstatus)
orig1$occstatus <- as.numeric(orig1$occstatus)
str(orig1$occstatus)

# select cltv - mean ========================
orig1$`origcltv` <- trunc(na.aggregate(orig1$`origcltv`))

# select dti - mean ========================
orig1$`dtiratio` <- trunc(na.aggregate(orig1$`dtiratio`))

# select upb - NA  ========================
orig1$origupb[orig1$origupb==""] <- NA

# select ltv - mean ========================
orig1$`origltv` <- trunc(na.aggregate(orig1$`origltv`))

# select orig interest rates - mean =========================
orig1$origintrate <- na.aggregate(orig1$origintrate)

# select property state - NA =========================
orig1$propstate[orig1$propstate==""] <- NA
orig1$propstate <- as.numeric(orig1$propstate)
str(orig1$propstate)

# select property type - lcof  =========================
orig1$proptype[orig1$proptype=="  "] <- NA
orig1$proptype <- na.locf(orig1$proptype)
orig1$proptype <- as.numeric(orig1$proptype)
str(orig1$proptype)

# # select loan seq number - as-is, NA if blank  =========================

# select loan purpose - locf  =========================
orig1$loanpurpose <- na.locf(orig1$loanpurpose)
orig1$loanpurpose <- as.numeric(orig1$loanpurpose)

# select loan term - mean ========================
orig1$origterm <- na.aggregate(orig1$origterm)
str(orig1$loanpurpose)

# select no of borrowers - lcof ========================
orig1$nofborrowers <- na.locf(orig1$nofborrowers)

# ====================== output the dataframe to csv =========================== ##
write.table(orig1, file = "step1_dataclean.csv", row.names = FALSE, col.names = TRUE, sep = "|", quote = FALSE)

# =========================== import Next Quarter origination file ========================= ##

q22005orig = read.table("historical_data1_Q22005.txt", sep = "|" )
names(q22005orig) <- c("creditscore","firstpymtdate","firsttimehome","maturitydate","msa","mortinsuperct","nofunits","occstatus","origcltv","dtiratio","origupb","origltv","origintrate","channel","ppmflag","prodtype","propstate","proptype","postalcode","loanseq","loanpurpose","origterm","nofborrowers","sellername","servicername","conformingflag")
# select rows for the model 
q2orig1 <- q22005orig[,c("creditscore","firsttimehome","maturitydate","msa", "nofunits", "occstatus", "origcltv","dtiratio","origupb","origltv", "origintrate", "propstate", "proptype", "loanpurpose", "origterm", "nofborrowers")]
rm(q22005orig)

## =========================== Missing Values for Next Quarter file ============================ ##

# select the credit score - mean ==============
creditscore <- q2orig1$creditscore
# fill credit score with mean values
q2orig1$creditscore <- trunc(na.aggregate(creditscore))
rm(creditscore)

# select first time home buyer - lcof ===========
#col_firsttimehome <- q2orig1$firsttimehome
q2orig1$firsttimehome[q2orig1$firsttimehome==""] <- NA
q2orig1$firsttimehome <- na.locf(q2orig1$firsttimehome)
q2orig1$firsttimehome <- as.numeric(q2orig1$firsttimehome)
str(q2orig1$firsttimehome)

# Select Maturity Date - as-is =====================

# select MSA - lcof =======================
#msa <- q2orig1$msa
q2orig1$msa <- na.locf(q2orig1$msa)

# select no of units - locf ========================
#units <- q2orig1$nofunits
q2orig1$nofunits <- na.locf(q2orig1$nofunits)

# select occupancy status - locf ========================
#occstatus <- q2orig1$occstatus
q2orig1$occstatus <- na.locf(q2orig1$occstatus)
q2orig1$occstatus <- as.numeric(q2orig1$occstatus)
str(q2orig1$occstatus)

# select cltv - mean ========================
#cltv <- q2orig1$`origcltv`
q2orig1$`origcltv` <- trunc(na.aggregate(q2orig1$`origcltv`))

# select dti - mean ========================
#dti <- q2orig1$`dtiratio`
q2orig1$`dtiratio` <- trunc(na.aggregate(q2orig1$`dtiratio`))

# select upb - NA  ========================
#upb <- q2orig1$origupb
q2orig1$origupb[q2orig1$origupb==""] <- NA

# select ltv - mean ========================
#ltv <- q2orig1$`origltv`
q2orig1$`origltv` <- trunc(na.aggregate(q2orig1$`origltv`))

# select orig interest rates - mean =========================
#intrates <- q2orig1$origintrate
q2orig1$origintrate <- na.aggregate(q2orig1$origintrate)

# select property state - NA =========================
#state <- q2orig1$propstate
q2orig1$propstate[q2orig1$propstate==""] <- NA
q2orig1$propstate <- as.numeric(q2orig1$propstate)
str(q2orig1$propstate)

# select property type - lcof  =========================
q2orig1$proptype[q2orig1$proptype=="  "] <- NA
q2orig1$proptype <- na.locf(q2orig1$proptype)
q2orig1$proptype <- as.numeric(q2orig1$proptype)
str(q2orig1$proptype)

# # select loan seq number - as-is, NA if blank  =========================
# q2orig1$loanseq[q2orig1$loanseq==""] <- NA

# select loan purpose - locf  =========================
#purpose <- q2orig1$loanpurpose
q2orig1$loanpurpose <- na.locf(q2orig1$loanpurpose)
q2orig1$loanpurpose <- as.numeric(q2orig1$loanpurpose)

# select loan term - mean ========================
#loanterm <- q2orig1$origterm
q2orig1$origterm <- na.aggregate(q2orig1$origterm)
str(q2orig1$loanpurpose)

# select no of borrowers - lcof ========================
#borrowers <- q2orig1$nofborrowers
q2orig1$nofborrowers <- na.locf(q2orig1$nofborrowers)

#======================================= Modelling ========================================= ##

# ----------------- Liner model execution ----------------------------#

# execute the model for all columns excluding interest rate and loansequence number 
lm.full <- lm(origintrate ~ creditscore + firsttimehome + maturitydate + msa + nofunits + occstatus + origcltv + dtiratio + origupb + origltv + propstate + proptype + loanpurpose + origterm + nofborrowers,data=orig1)
# summary output to console =============================
summary(lm.full)

# lm summary output to csv =============================
sink("prediction_execution.txt" , append = TRUE)
print("================= output of the lm() summary on full model ================================= ")
summary(lm.full)
sink()

# summary plot output to pdf =============================
pdf("lm_output_fullmodel.pdf",width=7,height=5)
print("================= output of the plot() to a pdf ================================= ")
plot(lm.full)
dev.off()

# run the full model on test data set =======================
library(forecast)
full.pred = predict(lm.full, q2orig1)

# lm prediction accuracy output to csv =============================
sink("prediction_execution.txt", append = TRUE)
print("================= output prediction accuracy of full model on test data ================================= ")
accuracy(full.pred, orig1$origintrate)
sink()

#============================= feature (variable) selection ================================================
library(leaps)

#  exhaustive search --------------------------
regfit.full <- regsubsets(origintrate ~ creditscore + firsttimehome + maturitydate + msa + nofunits + occstatus + origcltv + dtiratio + origupb + origltv + propstate + proptype + loanpurpose + origterm + nofborrowers,data=orig1, nvmax = 12, really.big = T )
sink("prediction_execution.txt", append = TRUE)
print("================= output of variable selection : exhaustive search ================================= ")
summary(regfit.full)
coef(regfit.full,11)
reg.summary <- summary(regfit.full)
names(reg.summary)
reg.summary$rss
reg.summary$adjr2
sink()

# exhaustive search plot output to pdf =============================
pdf("exhaustive_search.pdf",width=7,height=5)
print("================= output of the plot() to a pdf ================================= ")
plot(reg.summary$adjr2, xlab = "Number of variables", ylab = "Adjusted R^2", type = "l")
dev.off()

# forward selection --------------------------
regfit.fwd <- regsubsets(origintrate ~ creditscore + firsttimehome + maturitydate + msa + nofunits + occstatus + origcltv + dtiratio + origupb + origltv + propstate + proptype + loanpurpose + origterm + nofborrowers,data=orig1, nvmax = 8, method = "forward")
sink("prediction_execution.txt", append = TRUE)
print("================= output of variable selection : forward selection ================================= ")
F = summary(regfit.fwd)
F
coef(regfit.fwd, 8)
names(F)
F$rss
F$adjr2
sink()

# Backward selection --------------------------
regfit.bwd <- regsubsets(origintrate ~ creditscore + firsttimehome + maturitydate + msa + nofunits + occstatus + origcltv + dtiratio + origupb + origltv + propstate + proptype + loanpurpose + origterm + nofborrowers,data=orig1, nvmax = 8, method = "backward")
sink("prediction_execution.txt", append = TRUE)
print("================= output of variable selection : backward selection =================================")
B = summary(regfit.bwd)
B
coef(regfit.bwd, 8)
names(B)
B$rss
B$adjr2
sink()

# Stepwise selection --------------------------
regfit.step <- regsubsets(origintrate ~ creditscore + firsttimehome + maturitydate + msa + nofunits + occstatus + origcltv + dtiratio + origupb + origltv + propstate + proptype + loanpurpose + origterm + nofborrowers,data=orig1, nvmax = 8, method = "seqrep")
sink("prediction_execution.txt", append = TRUE)
print("================= output of variable selection : step selection =================================")
S = summary(regfit.step)
S
coef(regfit.step, 8)
names(S)
S$rss
S$adjr2
sink()

# ================================ save the above above 8 features (variables) obtained ==================================== #
cols1 <- labels(coef(regfit.step,8))
cols <- cols1[cols1 != "(Intercept)"]
cols <- append(cols, "origintrate")

# ================================ build the model using above 8 features (variables) ==================================== #
# ================================ Random forest starts ==================================== #

print("====================================== RANDOM FOREST ALGORITHM =========================================== ")

# RF model on test data =============================
rfmodel <- randomForest(origintrate ~ . , data = orig1[,cols], ntree=20)

# RF importance of each predictor in the model =============================
sink("prediction_execution.txt", append = TRUE)
print("================= Random forest importance of each predictor in the model ================================= ")
imp <- importance(rfmodel)
sink()

# plot for imp predictors to pdf =============================
pdf("RF_top_predictors.pdf",width=7,height=5)
print("================= Top predictors to a pdf ================================= ")
plot(imp, main = "Influential Predictors", top = 5)
dev.off()

# RF summary output to csv =============================
sink("prediction_execution.txt", append = TRUE)
print("================= Random forest summary on full model ================================= ")
summary(rfmodel)
sink()

#Predict using the test data
rfpred <- predict(rfmodel, q2orig1[,cols])

# prediction summary output to csv =============================
sink("prediction_execution.txt", append = TRUE)
print("=================================== output prediction summary of random forest on test data ================================= ")
accuracy(rfpred, q2orig1$origintrate)
sink()

# ================================ KNN regression starts ==================================== #

print("====================================== KNN regression Algorithm =========================================== ")

library(caret)
require(class)

model.knn <- train(origintrate ~ ., data = orig1, method = "knn")
print(model.knn)

# validate the model
validation<- validation[,orig1[c("creditscore", "maturitydate", "nofunits", "occstatus", "origupb", "origltv", "proptype", "loanpurpose" )]

# predict the values
predictions <- predict(model.knn, test[,1:8])

# calculate the accuracy 
accuracy <- sum(predictions == q2orig1$origintrate)/nrow(q2orig1)                        
                        
# ================================ ANN regression starts ==================================== #

print("====================================== ANN Algorithm =========================================== ")
attach(orig1)
library(neuralnet)

f <- as.formula(paste("origintrate ~", paste(cols[!cols %in% "origintrate"], collapse = " + ")))
nn <- neuralnet(f, data=orig1, hidden=10, linear.output=TRUE)
#plot(nn, main = "Neural Network",top =5)

# Matrix
nn$result.matrix

# plot for imp predictors to pdf =============================
pdf("NeuralNetwork_regresion.pdf",width=30,height=20)
print("================= Neural Network Plot ================================= ")
plot(nn, main = "Neural Network")
dev.off()

# predict values for test set
pr.nn <- compute(nn,q2orig1[c("creditscore", "maturitydate", "nofunits", "occstatus", "origupb", "origltv", "proptype", "loanpurpose" )])

#Calculate MSE
MSE.nn <- sum((pr.nn - q2orig1$origintrate)^2)/nrow(q2orig1)
