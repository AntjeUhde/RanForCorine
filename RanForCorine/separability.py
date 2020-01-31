# -*- coding: utf-8 -*-
"""
separability.py: calculate class seperability from distance measures

@author: Theresa Möller
"""

from scipy.spatial import distance as dist
import numpy as np
import seaborn as sb
import pandas as pd

def calcClassHist(data, label_col="Label"):
    """
    calculate histograms per class

    Parameters
    ----------
    data: numpy.dataframe containing data        
    label_col: string name of label column

    Examples
    --------
    >>> plotResult([127, 455], base_prediction)

    Returns
    -------
    accuracy score of prediction
    """
    histograms = {}
    classes = data[label_col].unique()
    for class_name in classes:
        class_vals = data.loc[data[label_col] == class_name]
        class_vals = class_vals.drop(label_col, 1)
        hist, bins = np.histogram(class_vals)
        histograms[class_name] = hist
    return histograms


def calcSep(data, label_col="Label"):
    """
    calculate class seperability with different measures 
    (Euclidean, Manhatten, Chebyshev)

    Parameters
    ----------
    data: numpy.dataframe containing data        
    label_col: string name of label column

    Examples
    --------
    >>> class_seperability = calcSep(data_raw, "Label_nr")

    Returns
    -------
    dictionary of arrays containing distance measures for all classes
    """
    comparison = {}
    SCIPY_METHODS = {
	"Euclidean": dist.euclidean,
	"Manhattan": dist.cityblock,
	"Chebyshev": dist.chebyshev
    }
    histograms = calcClassHist(data, label_col)
    for (methodName, method) in SCIPY_METHODS.items():
        results = {}
        for (class_name, hist) in histograms.items():
            class_results = []
            for (n, nhist) in histograms.items():
                d = method(histograms[class_name], nhist)
                class_results.append(d)
            results[class_name] = class_results
        comparison[methodName] = results
    return comparison

def printHeatmap(class_sep, method):
    """
    print heatmap showing class distances

    Parameters
    ----------
    class_sep: result of calcSep()        
    method: "Euclidean", "Manhattan" or "Chebyshev"

    Examples
    --------
    >>> class_separability = calcSep(data_raw, "Label_nr")
    >>> printHeatmap(class_separability, "Euclidean")

    Returns
    -------
    Nothing
    """
    df = pd.DataFrame(class_sep[method])
    sb.heatmap(df, yticklabels=class_sep[method].keys())
