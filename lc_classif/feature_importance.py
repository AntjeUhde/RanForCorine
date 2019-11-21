# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:33:16 2019

@author: there
"""

#import functions as f
import data_cleaning as clean
from sklearn import model_selection as model_selection
#for classification_report
#for confusion_matrix
#for accuracy_score
from sklearn import metrics as metrics

# For the classifier
from sklearn import ensemble as ensemble 
# for RandomForestClassifier

# for Feature Selection
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC

# for hyperparameter tuning with cross calidation
from sklearn.model_selection import RandomizedSearchCV

import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV





#def splitTestTrain(x,y,size,random_state=245):
#    return model_selection.train_test_split(
#        x,y, size=size, random_state=random_state)


data = clean.data_imputed


# divide values and labels
col_names = list(data.columns)[1:214]
x = data.iloc[:,:-1].values
y = data["Label"]

if len(x) > 0:
    print("Done.")
    
    
# split test and training
# for train_test_split
# Split train and test dataset (20 % of dataset = test)
x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x,y, test_size=0.2, random_state=245)
print("Traingssamples: " + str(len(x_train)))
print("Testsamples: " + str(len(x_test)))


# create basic RF model
base_model = ensemble.RandomForestClassifier(max_depth=2, random_state=0, n_estimators=100)

# Model fit
base_model.fit(x_train, y_train)


# RECURSIVE FEATURE ELIMINATION
# Create the RFE object and compute a cross-validated score.
svc = SVC(kernel="linear")
# The "accuracy" scoring is proportional to the number of correct
# classifications
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2),
              scoring='accuracy')
rfecv.fit(x_train, y_train)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()



# Create a selector object that will use the random forest classifier to identify
# features that have an importance of more than 0.15
lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(x_train, y_train)
sfm = SelectFromModel(lsvc, prefit=True)
#sfm = SelectFromModel(base_model, threshold=0.02)

# Train the selector
#sfm.fit(x_train, y_train)
# Liste ausgewählter Features
#for feature_list_index in sfm.get_support(indices=True):
#    print(col_names[feature_list_index])

# Transform the data to create a new dataset containing only the most important features
# Note: We have to apply the transform to both the training X and test X data.
X_important_train = sfm.transform(x_train)
X_important_test = sfm.transform(x_test)

# Create a new random forest classifier for the most important features
clf_important = ensemble.RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)

# Train the new classifier on the new dataset containing the most important features
clf_important.fit(X_important_train, y_train)
# prediction
base_prediction = base_model.predict(x_test)
selfeat_prediction = clf_important.predict(X_important_test)

# accuracy - BASE MODEL
base_accuracy = metrics.accuracy_score(base_prediction, y_test)
base_conf_matrix = metrics.confusion_matrix(base_prediction, y_test)
base_classif_report = metrics.classification_report(base_prediction, y_test)

# accuracy - IMPORTANT FEATURES
selfeat_accuracy = metrics.accuracy_score(base_prediction, y_test)
selfeat_conf_matrix = metrics.confusion_matrix(base_prediction, y_test)
selfeat_classif_report = metrics.classification_report(base_prediction, y_test)

print("Base Accuracy: " + str(base_accuracy))
print("SelFeat Accuracy: " + str(selfeat_accuracy))














