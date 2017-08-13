## ============================= Classification ========================================= ##

gc()
## ======================================== Functions ======================================= ##

importcsv<-function(filename){
  # import csv
  df = read.table(filename, sep = ",", header = TRUE)
  return(df)
}

# Function to convert to factors and numeric
missingvalue<-function(ipdf){
    ipdf$Amount.Requested <- trunc(as.numeric(ipdf$Amount.Requested))
    ipdf$Debt.To.Income.Ratio <- as.numeric(ipdf$Debt.To.Income.Ratio) 
    ipdf$Employment.Length <- as.factor(ipdf$Employment.Length)
    ipdf$LoanStatus <- as.factor(ipdf$LoanStatus)
    ipdf$Score <- trunc(as.numeric(ipdf$Score))
    ipdf$State <- as.factor(ipdf$State)
    return(ipdf)
}

## ======================= script execution ========================================= ##

# rejected <- ("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/rejected.csv")
# accepted <- ("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/accepted.csv")
# accepteddf <- importcsv(accepted)
# rejecteddf <- importcsv(rejected)
# summary(rejecteddf)

loancsv <- ("/home/bhavik/ADS_FIles/Assignments/Asg2/Part2/LoanCombinedClean.csv")
# loandf <- importcsv(loancsv)
loandf <- read.csv(loancsv, sep = ",", header = TRUE)

# Remove any unwanted column if needed, optional step
loandf <- subset(loandf, select = -c(Loan.Title))

#Convert to numeric and factors
loandf$Amount.Requested <- as.numeric(loandf$Amount.Requested)
loandf$Debt.To.Income.Ratio <- as.numeric(loandf$Debt.To.Income.Ratio)
loandf$Employment.Length <- as.numeric(loandf$Employment.Length)
loandf$LoanStatus <- as.factor(loandf$LoanStatus)
loandf$Score <- trunc(as.numeric(loandf$Score))
loandf$State <- as.factor(loandf$State)

## ================================ Divide into Train and Test ================================ ##

samp_size <- floor(0.75 * nrow(loandf))
set.seed(12345)
train_loan <- sample(seq_len(nrow(loandf)), size = samp_size)
loandf.train <- loandf[train_loan, ]
loandf.test <- loandf[-train_loan, ]

## ================================ Logistic Regression ================================ ##

fit <- glm(LoanStatus ~ ., data=loandf.train, family = binomial(link = "logit"))
summary(fit)

test.prob <- predict(fit, loandf.test, type = 'response')
pred <- rep("Approved", length(test.prob))

pred[test.prob >= 0.5] <- "Rejected"

library(caret)
confusionMatrix(loandf.test$LoanStatus, pred)

# ROC curve
library(ROCR)
prediction <- prediction(test.prob, loandf.test$LoanStatus)
performance <- performance(prediction, measure = "tpr", x.measure = "fpr")

# summary plot output to pdf 
pdf("logreg_ROC.pdf",width=7,height=5)
plot(performance, main="ROC Curve", xlab="1-specificity", ylab="Sensitivity")
dev.off()

## ================================ Random Forest ================================ ##

rf = randomForest(LoanStatus ~ ., ntree = 100, data = loandf.train)

test.prob.rf <- predict(rf, loandf.test, type = 'response')
pred.rf <- rep("Approved", length(test.prob.rf))

pred.rf[test.prob.rf >= 0.5] <- "Rejected"

library(caret)
confusionMatrix(loandf.test$LoanStatus, pred.rf)

# ROC curve
library(ROCR)
prediction.rf <- prediction(test.prob.rf, loandf.test$LoanStatus)
performance.rf <- performance(prediction.rf, measure = "tpr", x.measure = "fpr")

# summary plot output to pdf 
pdf("rf_ROC.pdf",width=7,height=5)
plot(performance.rf, main="ROC Curve", xlab="1-specificity", ylab="Sensitivity")
dev.off()

# ================================ ANN starts ==================================== #

attach(loandf.train)
library(neuralnet)

train1 <- loandf.train

loanstat <- as.vector(train1$LoanStatus)
loanstat <- replace(loanstat, loanstat=="Approved", 1)
loanstat <- replace(loanstat, loanstat=="Rejected", 0)

loanstatus <- as.numeric(loanstat)
amtrequested <- c(train1$Amount.Requested)
emplength <- c(train1$Employment.Length)
dtiratio <- c(train1$Debt.To.Income.Ratio)
score <- c(train1$Score)
state <- as.numeric(train1$State)
train2 <- cbind(loanstatus,amtrequested,emplength,dtiratio,score,state)
summary(train2)
n <- colnames(train2)

f <- as.formula(paste("loanstatus ~", paste(n[!n %in% "loanstatus"], collapse = " + ")))
nn <- neuralnet(f, data = train2, hidden=c(4,4), linear.output=FALSE)

# summary for nn
nn.summary <- summary(nn)

# Confusion Matrix
nn.summary$result.matrix

# plot nn
plot(nn, main = "Neural Network",top =5)

# ================================ SVN starts ==================================== #

library(e1071)

svm.model <- svm(f, data = loandf.train, kernel = "linear", cost = 10)
summary(svm.model)

svm.test.prob <- predict(svm.model, loandf.test, type = 'response')
svm.pred <- rep("Approved", length(svm.test.prob))
svm.pred[svm.test.prob >= 0.5] <- "Rejected"

library(caret)
confusionMatrix(loandf.test$LoanStatus, svm.pred)

# ROC curve
library(ROCR)
prediction <- prediction(svm.test.prob, loandf.test$LoanStatus)
performance <- performance(prediction, measure = "tpr", x.measure = "fpr")

# summary plot output to pdf 
pdf("logreg_ROC.pdf",width=7,height=5)
plot(performance, main="ROC Curve", xlab="1-specificity", ylab="Sensitivity")
dev.off()

#===================================================================================================
