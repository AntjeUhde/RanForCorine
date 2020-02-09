# -*- coding: utf-8 -*-
"""
accuracy.py: implements accuracy assessment and confusion matrix printing

@author: Theresa Möller
"""
# IMPORTS
import pandas as pd
from sklearn import metrics as metrics

# FUNCTIONS
def getAccuracy(prediction, y_test):
    """
    Returns overall accuracy of prediction

    Parameters
    ----------
    prediction: array
        1d-array with predicted labels
    y_test: array
        1d-array with ground-truth labels
        

    Examples
    --------
    >>> accuracy = getAccuracy(pred, y_test)

    Returns
    -------
    float
        accuracy score of prediction
    """
    accuracy = metrics.accuracy_score(y_test, prediction)
    return accuracy

def getConfMatrix(prediction, y_test):
    """
    Returns confusion matrix of prediction

    Parameters
    ----------
    prediction: array
        1d-array with predicted labels
    y_test: array
        1d-array with ground-truth labels

    Examples
    --------
    >>> conf_matrix = getConfMatrix(pred, y_test)

    Returns
    -------
    2d-array
        confusion matrix
    """
    conf_matrix = metrics.confusion_matrix(y_test, prediction)
    return conf_matrix

def printConfMatrix(conf_matrix, class_names):
    """
    Pretty printing of confusion matrix

    Parameters
    ----------
    conf_matrix: array
        confusion matrix to print
    class_names: list
        list of names of possible classes

    Examples
    --------
    >>> printConfMatrix(conf_matrix, class_names)

    Returns
    -------
    Nothing
    """
    cl_act = []
    cl_pred = []
    for cl in class_names:
        cl_act.append(str(cl) + " (act)")
        cl_pred.append(str(cl) + " (pred)")
    print(pd.DataFrame(conf_matrix, cl_act, cl_pred))
