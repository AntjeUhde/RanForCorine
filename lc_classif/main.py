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
data_raw = clean.importCSV(cwd + '\\test_data\\classvalues_VH[168].csv')

# MISSING VALUES
print("--- ANALYZING MISSING VALUES ---")
missing_count = clean.countMissingValuesTotal(data_raw, null_value=-99.0)
print(str(missing_count) + " values are missing.")
# Impute missing values with mean in column
data_imp = clean.imputeMean(data_raw, clean=True, null_value=-99.0)
print("Done imputing missing values.")

# TEST TRAINING
print("--- Test Training Split ---")
x_train, x_test, y_train, y_test = tts.splitData(
        data_imp, 
        "Label", 
        test_size=0.2, 
        random_state=245)

# RANDOM FOREST BASE MODEL
print("--- CALCULATE BASE MODEL ---")
base_model = rf.RandomForestClassifier(max_depth=2, random_state=1, n_estimators=100)
rf.fitModel(base_model, x_train, y_train)
base_pred = rf.predictModel(base_model, x_test)

# ACCURACY
acc, conf = acc.accuracyReport(base_pred, y_test)
print(acc)
print(conf)

# SHOW SPECTRAL SEPARABILITY

# FEATURE SELECTION MODEL

# CONCENTRATE ON SPECIAL CLASSES
