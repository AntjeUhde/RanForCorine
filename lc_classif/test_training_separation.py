# -*- coding: utf-8 -*-
"""
test_training_separation.py: separates test and training dataset

@author: Theresa Möller
"""

# IMPORTS
from lc_classif.lc_classif import functions as f

# FUNCTIONS
def splitData(data, labelcol, test_size=0.2, random_state=245):
    return f.splitData(data, labelcol, test_size=0.2, random_state=245)

#x_train, x_test, y_train, y_test = splitData(data,"Label", test_size=0.2, random_state=245)
