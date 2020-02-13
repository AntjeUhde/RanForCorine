# -*- coding: utf-8 -*-
"""
data_cleaning.py: Look for missing data and remove it.
@autor: Theresa Möller, Antje Uhde
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
    int
        absolute number of missing values
    """
    

    d_clean = data_raw.replace(null_value, np.NaN)
    return d_clean.isnull().sum().sum()

def imputeMean(data, clean=False, null_value=-99):
    """
    Imputes missing data with mean value of that column.

    Parameters
    ----------
    data: numpy.dataFrame with np.NaN values
        dataframe with missing values to impute

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> imputeMean(data)

    Returns
    -------
    numpy.dataFrame
        dataframe with imputed data
    """
    if clean == True:
        data = data.replace(null_value, np.NaN)
    copy_df=data.copy()
    return copy_df.T.fillna(data.mean(axis=1)).T#axis=1

def compressClasses(data, sep_list, label_col='Label', new_label_col='Label_new'):
    """
    Keeps classes from sep_list and compresses the rest to class 0

    Parameters
    ----------
    data: numpy.dataFrame with np.NaN values
        dataframe with all classes
    sep_list: array
        array containing names of classes to keep
    label_col: str (optional)
        name of label column
    new_label_col: str (optional)
        name of new label column

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> data_compressed_classes = compressClasses(data, [211,312])

    Returns
    -------
    numpy.dataFrame
        dataframe with compressed classes
    """
    df_copy = data.copy()
    df_copy[new_label_col] = df_copy[label_col]
    df_copy.loc[~df_copy[new_label_col].isin(sep_list), new_label_col] = 0
    return df_copy
