# -*- coding: utf-8 -*-
"""
accuracy.py: implements accuracy assessment and printing

@author: Theresa Möller
"""
# IMPORTS
import functions as f

# FUNCTIONS
def accuracyReport(prediction, y_test):
    return f.accuracyReport(prediction, y_test)

def printConfMatrix(conf_matrix, class_names):
    f.printConfMatrix(conf_matrix, class_names)