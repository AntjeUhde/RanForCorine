# -*- coding: utf-8 -*-
"""
descriptive_Stats.py: First impressions on dataset
@autor: Theresa Möller
"""

#########################
# WORK IN PROGRESS
########################



def countPxlsPerClass(data, className):
    return data[className].value_counts()

import pandas as pd


# Import data from CSV
cwd = os.getcwd()
data_raw = pd.read_csv(cwd + '\\test_data\\classvalues_VH[168].csv')
print("Successfully imported data")

print(countPxlsPerClass(data_raw, 'Label'))