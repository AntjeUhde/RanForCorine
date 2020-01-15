# -*- coding: utf-8 -*-
"""
main.py: Random Forest classification (complete)

@author: Theresa Möller
"""

import data_cleaning as clean
import test_training_separation as tts
import randomforest_classifier as rf
import accuracy as acc
import feature_importance as feat
import spectral_separability as spec
import descriptive_Stats as descr
import compress as comp
import tuning as tuning
#from functions import importCSV
import os
import numpy as np
from sklearn import metrics as metrics
from sklearn import ensemble as ensemble 

from sklearn.model_selection import RandomizedSearchCV

# IMPORT DATA ################################
print("--- IMPORTING DATA ---")
data_raw = clean.importCSV('C:\\Users\\there\\Documents\\Studium\\GEO419\\lc_classif\\lc_classif\\test_data\\classvalues_VV.csv')
print(data_raw.columns)
data_raw = data_raw.drop(data_raw.columns[0], axis=1) #remove index column

# FIRST IMPRESSIONS ##########################
class_count = descr.countPxlsPerClass(data_raw, "Label_nr")
class_count.plot.bar()

# MISSING VALUES #############################
print("--- ANALYZING MISSING VALUES ---")

data_clean = data_raw.replace(-99.0, np.NaN)
# count the number of NaN values
missing = clean.countMissingValuesTotal(data_raw)
print(str(missing) + " values are missing.")
# Impute missing values with mean in column
data_imputed = clean.imputeMean(data_clean)
print("Successfully imputed missing values.")

class_count = descr.countPxlsPerClass(data_imp, "Label_nr")
class_count.plot.bar()

# CLASS SEPARABILITY ##########################
print("--- ANALYZING CLASS SEPARABILITY ---")
histograms = spec.calcClassHist(data_imp, "Label_nr")
class_sep = spec.calcSep(histograms)
spec.printing(class_sep, "Euclidean")
# we decided to use following classes
sep_list = [112,211,231,311,312,523,512]

# prepare dataset for selected classes
data_comp = comp.compressClassesNull(data_imp, sep_list)
class_count_comp = descr.countPxlsPerClass(data_comp, "Label_new")
class_count_comp.plot.bar()

# CLASS SEPARABILITY
histograms2 = spec.calcClassHist(data_comp, "Label_new")
class_sep2 = spec.calcSep(histograms2)
spec.printing(class_sep2, "Euclidean")


# TEST TRAINING #################################
print("--- Test Training Split ---")
x_train, x_test, y_train, y_test = tts.splitData(
        data_comp, 
        "Label_new", 
        test_size=0.2, 
        random_state=245)


# RANDOM FOREST BASE MODEL ######################
print("--- CALCULATING BASE MODEL ---")
base_model = rf.RandomForestClassifier(max_depth=2, random_state=1, n_estimators=100)
rf.fitModel(base_model, x_train, y_train)
base_pred = rf.predictModel(base_model, x_test)

# ACCURACY
base_acc = acc.accuracyReport(base_pred, y_test)
print("Base model has accuracy of: " + str(base_acc)) # 0.65

# BASE MODEL TUNING
print("--- TUNING BASE MODEL ---")
base_params = rf.getParamsOfModel(base_model)
print(base_params)
max_depth_base = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth_base.append(None)
base_grid = {'n_estimators': [int(x) for x in np.linspace(start = 100, stop = 2000, num = 10)],
               'max_features': ['auto', 'sqrt'],
               'max_depth': max_depth_base}
best_base_model = rf.tuneModel(base_grid, x_train, y_train, n_jobs=1)
best_base_pred = rf.predictModel(best_base_model, x_test)
best_base_acc = acc.accuracyReport(best_base_pred, y_test)
print("Tuned base model has accuracy of: " + str(best_base_acc)) #0.993


# FEATURE SELECTION MODEL ##################################
print("--- SELECTING FEATURES ---")
x_important_test, x_important_train = feat.selectImportantFeatures(base_model, x_train, y_train, x_test)
sel_model = rf.RandomForestClassifier(max_depth=2, random_state=1, n_estimators=100)
rf.fitModel(sel_model, x_important_train, y_train)
sel_pred = rf.predictModel(sel_model, x_important_test)
sel_acc = acc.accuracyReport(sel_pred, y_test)
print("Model with selected features as accuracy of: " + str(sel_acc)) #0.67

# FEATURE SELECTION MODEL TUNING 
print("--- TUNING MODEL WITH SELECTED FEATURES ---")
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 10)]
# Number of features to consider at every split method
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth}

best_random = tuning.RandomSearchCV(random_grid, x_important_train, y_train)
best_random_pred = rf.predictModel(best_random, x_important_test)
best_random_acc = acc.accuracyReport(best_random_pred, y_test)
print("Tuned model with selected features has accuracy of: " + str(best_random_acc)) #0.993
