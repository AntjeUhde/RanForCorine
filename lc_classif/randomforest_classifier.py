# -*- coding: utf-8 -*-
"""
randomforest_classifier.py: implements the random forest classifier, it's 
fitting and prediction

@author: Theresa Möller
"""

# IMPORTS
import functions as f

# FUNCTIONS
def RandomForestClassifier(max_depth, random_state, n_estimators):
    return f.RandomForestClassifier(max_depth,random_state, n_estimators)
    
def fitModel(model, x_train, y_train):
    f.fitModel(model, x_train, y_train)
    
def predictModel(model, x_test):
    return f.predictModel(model, x_test)
