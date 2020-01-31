# -*- coding: utf-8 -*-
"""
data_cleaning.py: Look for missing data and remove it.
@autor: Theresa Möller
"""

# IMPORTS
import numpy as np
import pandas as pd

# FUNCTIONS
def countMissingValuesTotal(data_raw, null_value):
    """
    Counts the missing values in a dataframe

    Parameters
    ----------
    data_raw: numpy.dataFrame 
        dataframe with values to analyze

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> countMissingValuesTotal(data)

    Returns
    -------
    absolute number of missing values
    """
    

    d_clean = data_raw.replace(null_value, np.NaN)
    return d_clean.isnull().sum().sum()

def imputeMean(data, clean=False, null_value=-99):
    """
    Imputes missing data with mean value of that column.

    Parameters
    ----------
    data: numypy.dataFrame with np.NaN values
        dataframe with missing values to impute

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> imputeMean(data)

    Returns
    -------
    dataframe with imputed data
    """
    if clean == True:
        data = data.replace(null_value, np.NaN)
    return data.fillna(data.mean())

def compressClasses(data, sep_list, label_col='Label', new_label_col='Label_new'):
    df_copy = data.copy()
    df_copy[new_label_col] = df_copy[label_col]
    df_copy.loc[~df_copy[new_label_col].isin(sep_list), new_label_col] = 0
    return df_copy