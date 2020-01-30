# -*- coding: utf-8 -*-
"""
randomforest_classifier.py: implements the random forest classifier, it's 
fitting and prediction

@author: Theresa Möller
"""

# IMPORTS
from sklearn import ensemble as ensemble 

# FUNCTIONS
def RandomForestClassifier(max_depth, random_state, n_estimators):
    """
    Returns the Random Forest Classifier from scikit-learn

    Parameters
    ----------
    max_depth: int, maximal depth of each tree
    random_state: int, random number to unsure reproducability
    n_estimators: int, number of estimators

    Examples
    --------
    >>> base_model = RandomForestClassifier(2, 245, 100)

    Returns
    -------
    Random Forest model
    """
    rf = ensemble.RandomForestClassifier(
            max_depth=max_depth, 
            random_state=random_state, 
            n_estimators=n_estimators)
    return rf
    
def fitModel(model, x_train, y_train):
    """
    Implements scikit-learn's fit() for Random Forest Classifiers

    Parameters
    ----------
    model: Random Forest model to be fitted
    x_train: list of training values
    y_train: list of training labels

    Examples
    --------
    >>> model = RandomForestClassifier(2, 245, 50)
    >>> fitModel(model, x_train, y_train)

    Returns
    -------
    Nothing
    """
    model.fit(x_train, y_train)
    
def predictModel(model, x_test):
    """
    Implements scikit-learn's predict() for Random Forest Classifiers

    Parameters
    ----------
    model: Random Forest model
    x_test: list of test values

    Examples
    --------
    >>> pred = predictModel(base_model, x_test)

    Returns
    -------
    list of predicted labels
    """
    return model.predict(x_test)

