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

## Import data from CSV
#cwd = os.getcwd()
#data_raw = pd.read_csv(cwd + '\\test_data\\classvalues_VH[168].csv')
#print("Successfully imported data")
#
## Some inspection
#data_clean = data_raw.replace(-99.0, np.NaN)
## count the number of NaN values
#missing = countMissingValuesTotal(data_raw)
#print(str(missing) + " values are missing.")
#
## Impute missing values with mean in column (there are smarter imputation methods)
#data_imputed = imputeMean(data_clean)















