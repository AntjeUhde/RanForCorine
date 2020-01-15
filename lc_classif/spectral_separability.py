# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 10:08:09 2019

@author: there
"""
#######################
# Work in Progress
######################

#code from https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/

from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd

def calcClassHist(data, label_col="Label"):
    histograms = {}
    classes = data[label_col].unique()
    for class_name in classes:
        class_vals = data.loc[data[label_col] == class_name]
        class_vals = class_vals.drop(label_col, 1)
        hist, bins = np.histogram(class_vals)
        histograms[class_name] = hist
    return histograms


def calcSep(histograms):
    comparison = {}
    SCIPY_METHODS = {
	"Euclidean": dist.euclidean,
	"Manhattan": dist.cityblock,
	"Chebyshev": dist.chebyshev
    }
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

def printing(comp, method):
    df = pd.DataFrame(comp[method])
    sb.heatmap(df, yticklabels=comp[method].keys())
