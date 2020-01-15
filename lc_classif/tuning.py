# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:33:16 2019

@author: Theresa Möller
"""


from sklearn import ensemble as ensemble 
from sklearn.model_selection import RandomizedSearchCV

def RandomSearchCV(grid, x_train, y_train, n_iter=3, cv=3, random_state=42, n_jobs = -1):
    tune_model = ensemble.RandomForestClassifier()
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


def getParamsOfModel(model):
    params = model.get_params()
    return params