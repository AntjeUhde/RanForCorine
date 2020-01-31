# -*- coding: utf-8 -*-
"""
feature_importance.py: implements feature selection and feature importance plot
for random forest models

@author: Theresa Möller
"""

from sklearn.feature_selection import SelectFromModel
import matplotlib.pyplot as plt
import numpy as np

def selectImportantFeatures(model,x_train, y_train, x_test):
    """
    Select important features and calculate new RF model

    Parameters
    ----------
    model: Random Forest Model the selection is based on
    x_train: training values dataset
    y_train: training labels dataset
    x_test: test values dataset

    Examples
    --------
    >>> x_important_train, x_important_test = 
        selectImportantFeatures(base_model, x_train, y_train, x_test)

    Returns
    -------
    new training datasets containing only values for selected features
    """
    sel = SelectFromModel(model)
    sel.fit(x_train, y_train)
    selected_feat= x_train.columns[(sel.get_support())]
    print(str(len(selected_feat)) + " features selected")
    print(selected_feat)
    x_important_train = sel.transform(x_train)
    x_important_test = sel.transform(x_test)
    return x_important_test, x_important_train

def importancePlot(model, features, feat_number=20):
    """
    Plot most important features in barplot.

    Parameters
    ----------
    model: Random Forest model
    features: list of features
    feat_number: int, number of features to show

    Examples
    --------
    >>> importancePlot(base_model, x_train.columns, 10)

    Returns
    -------
    Nothing
    """
    features = features
    importances = model.feature_importances_
    indices = np.argsort(importances)
    n = 0-feat_number

    plt.title('Feature Importances')
    plt.barh(range(len(indices[n:])), importances[indices[n:]], color='b', align='center')
    plt.yticks(range(len(indices[n:])), [features[i] for i in indices[n:]])
    plt.xlabel('Relative Importance')
    plt.show()

