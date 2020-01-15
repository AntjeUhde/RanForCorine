# -*- coding: utf-8 -*-
"""
descriptive_Stats.py: First impressions on dataset
@autor: Theresa Möller
"""

#########################
# WORK IN PROGRESS
########################

import pandas as pd
import matplotlib.pyplot as plt

def countPxlsPerClass(data, label_col = "Label"):
    return data[label_col].value_counts()

def newData(data, label_col="Label"):
    classes = data[label_col].unique()
    df = pd.DataFrame()
    for cl in classes:
        d = classImpression(data, cl, label_col)
        sd = pd.Series(d.values.ravel())
        df[cl] = sd#pd.Series(np.random.randn(sLength), index=df1.index)
    return df

def classImpression(data, class_name, label_col = "Label"):
    d = data.loc[data[label_col] == class_name]
    d = d.drop(label_col, 1)
    return d

def plotHist(data, class_name, label_col="Label"):
    d = classImpression(data, class_name, label_col)
    sd = pd.Series(d.values.ravel())
    sd.plot.hist(bins=50)