# -*- coding: utf-8 -*-
"""
randomforest_classifier.py: implements the random forest classifier, it's 
fitting and prediction

@author: Theresa Möller
"""

# IMPORTS
from lc_classif.lc_classif import functions as f
from sklearn import ensemble as ensemble 
from sklearn.model_selection import RandomizedSearchCV
from sklearn.feature_selection import SelectFromModel

# FUNCTIONS
def RandomForestClassifier(max_depth, random_state, n_estimators):
    return f.RandomForestClassifier(max_depth,random_state, n_estimators)
    
def fitModel(model, x_train, y_train):
    f.fitModel(model, x_train, y_train)
    
def predictModel(model, x_test):
    return f.predictModel(model, x_test)

def selectImportantFeatures(model,x_train, y_train, x_test):
    sel = SelectFromModel(model)
    sel.fit(x_train, y_train)
    selected_feat= x_train.columns[(sel.get_support())]
    len(selected_feat)
    print(selected_feat)
    print(str(len(selected_feat)) + " features selected")
    # Transform the data to create a new dataset containing only the most important features
    # Note: We have to apply the transform to both the training X and test X data.
    x_important_train = sel.transform(x_train)
    x_important_test = sel.transform(x_test)
    return x_important_test, x_important_train

def tuneModel(grid, x_train, y_train, n_iter=3, cv=3, random_state=42, n_jobs = -1):
    tune_model = RandomForestClassifier(max_depth = 2, random_state = 1, n_estimators=100)
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    tune_model_random = RandomizedSearchCV(
            estimator = tune_model, 
            param_distributions = grid, 
            n_iter = n_iter, 
            cv = cv, 
            verbose = 2, 
            random_state = random_state, 
            n_jobs = n_jobs)
    # Fit the random search model
    tune_model_random.fit(x_train, y_train)
    best_random = tune_model_random.best_estimator_
    return best_random


def getParams(model):
    params = model.get_params()
    return params

def accuracyReport(prediction, y_test):
    return f.accuracyReport(prediction, y_test)

def printConfMatrix(conf_matrix, class_names):
    f.printConfMatrix(conf_matrix, class_names)
