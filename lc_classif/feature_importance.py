# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:33:16 2019

@author: there
"""

#import functions as f
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
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def selectImportantFeatures(model,x_train, y_train, x_test):
    sel = SelectFromModel(model)
    sel.fit(x_train, y_train)
    # Create a selector object that will use the random forest classifier to identify
    # features that have an importance of more than 0.15
#    lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(x_train, y_train)
#    sfm = SelectFromModel(lsvc, prefit=True)
    #sfm = SelectFromModel(base_model, threshold=0.02)
    
     #Train the selector
#    sfm.fit(x_train, y_train)
    # Liste ausgewählter Features
#    for feature_list_index in sel.get_support(indices=True):
#        print(col_names[feature_list_index])
    selected_feat= x_train.columns[(sel.get_support())]
    len(selected_feat)
    print(selected_feat)
    print(str(len(selected_feat)) + " features selected")
    
#    pd.series(sel.estimator_,feature_importances_,.ravel()).hist()
    
    # Transform the data to create a new dataset containing only the most important features
    # Note: We have to apply the transform to both the training X and test X data.
    x_important_train = sel.transform(x_train)
    x_important_test = sel.transform(x_test)
    return x_important_test, x_important_train



#
## Create a new random forest classifier for the most important features
#clf_important = ensemble.RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
#
## Train the new classifier on the new dataset containing the most important features
#clf_important.fit(X_important_train, y_train)
## prediction
#base_prediction = base_model.predict(x_test)
#selfeat_prediction = clf_important.predict(X_important_test)
#
## accuracy - BASE MODEL
#base_accuracy = metrics.accuracy_score(base_prediction, y_test)
#base_conf_matrix = metrics.confusion_matrix(base_prediction, y_test)
#base_classif_report = metrics.classification_report(base_prediction, y_test)
#
## accuracy - IMPORTANT FEATURES
#selfeat_accuracy = metrics.accuracy_score(base_prediction, y_test)
#selfeat_conf_matrix = metrics.confusion_matrix(base_prediction, y_test)
#selfeat_classif_report = metrics.classification_report(base_prediction, y_test)
#
#print("Base Accuracy: " + str(base_accuracy))
#print("SelFeat Accuracy: " + str(selfeat_accuracy))

