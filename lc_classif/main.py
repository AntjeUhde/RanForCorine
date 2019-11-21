# -*- coding: utf-8 -*-
"""
main.py: Random Forest classification (complete)

@author: Theresa Möller
"""

import data_cleaning as clean
import test_training_separation as tts
import randomforest_classifier as rf
import accuracy as acc
#from functions import importCSV
import os
import numpy as np
from sklearn import metrics as metrics

# IMPORT DATA
print("--- IMPORTING DATA ---")
cwd = os.getcwd()
clean.importCSV()
data_raw = clean.importCSV(cwd + '\\test_data\\classvalues_VH[168].csv')

# MISSING VALUES
print("--- ANALYZING MISSING VALUES ---")

data_clean = data_raw.replace(-99.0, np.NaN)
# count the number of NaN values
missing = clean.countMissingValuesTotal(data_raw)
print(str(missing) + " values are missing.")
# Impute missing values with mean in column
data_imputed = clean.imputeMean(data_clean)
print("Successfully imputed missing values.")

# TEST TRAINING
print("--- Test Training Split ---")
x_train, x_test, y_train, y_test = tts.splitData(
        data_imp, 
        "Label", 
        test_size=0.2, 
        random_state=245)

# RANDOM FOREST
base_model = rf.RandomForestClassifier()
rf.fitModel(base_model, x_train, y_train)
rf.predictModel(base_model, x_test)
