# -*- coding: utf-8 -*-
"""
descriptive_stats.py: First impressions on dataset

@autor: Theresa Möller
"""

import pandas as pd

def countPxlsPerClass(data, label_col = "Label"):
    """
    Counts amount of pixels per class label

    Parameters
    ----------
    data: numpy.dataframe with data
    label_col: string with name of label column

    Examples
    --------)
    >>> countPxlsPerClass(data, "Label_nr")

    Returns
    -------
    list of absolute value counts per class
    """
    return data[label_col].value_counts()

def classImpression(data, class_name, label_col = "Label"):
    """
    Return dataframe that contains only values of one class

    Parameters
    ----------
    data: numpy.dataframe with data
    class_name: name of class as its value (not necessarily a string)
    label_col: string, name of label column

    Examples
    --------
    >>> d = classImpression(data_raw, 211, "Label_nr")

    Returns
    -------
    dataframe containing all values of one class
    """
    d = data.loc[data[label_col] == class_name]
    d = d.drop(label_col, 1)
    return d

def plotHist(data, class_name, label_col="Label"):
    """
    Plot histogram for one class

    Parameters
    ----------
    data: numpy.dataframe with data
    class_name: name of class as its value (not necessarily a string)
    label_col: string, name of label column

    Examples
    --------
    >>> plotHist(data, 211, "Label_nr")

    Returns
    -------
    Nothing
    """
    d = classImpression(data, class_name, label_col)
    sd = pd.Series(d.values.ravel())
    sd.plot.hist(bins=50)
