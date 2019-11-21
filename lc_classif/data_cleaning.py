# -*- coding: utf-8 -*-
"""
data_cleaning.py: Look for missing data and remove it.
@autor: Theresa Möller
"""

# IMPORTS
from lc_classif.lc_classif import functions as f

# FUNCTIONS
def countMissingValuesTotal(data_raw, null_value=-99.0):
    return f.countMissingValuesTotal(data_raw, null_value)

def imputeMean(data, clean=False, null_value=-99.0):
    return f.imputeMean(data, clean, null_value)
    
def importCSV(path):
    return f.importCSV(path)
