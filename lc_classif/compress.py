# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:03:24 2019

@author: there
"""

from lc_classif.lc_classif import data_cleaning as clean
from lc_classif.lc_classif import descriptive_Stats as stats
import numpy as np

#cwd = os.getcwd()
#df = clean.importCSV(cwd + '\\test_data\\classvalues_VV.csv')
#df = df.drop(df.columns[0], axis=1)
##a = a.drop(a.columns[0], axis=1)
#
## impute missing
#df.fillna(df.mean())

# get impression on class
#class_count = stats.countPxlsPerClass(df, "Label_nr")
#class_count.plot.bar()



#####################################
# COPY DF and pack classes
#####################################

# 100 - artificial, not discontinous
# 200 - other agricultural areas
# 300 - other forest and seminatural
# 400 - other wetlands
# 500 - other water bodies

#df_compressed = df.copy()
#label_list = df_compressed.Label_nr.unique()
#sep_list = [112,211,231,311,312,523,512]

def compressClasses(df_compressed, sep_list):
    for i in df_compressed["Label_nr"]:
        if i in sep_list:
            df_compressed["Label_new"] = i
        elif i < 200:
            df_compressed["Label_new"] = 100
        elif i < 300:
            df_compressed["Label_new"] = 200
        elif i < 400:
            df_compressed["Label_new"] = 300
        elif i < 500:
            df_compressed["Label_new"] = 400
        elif i > 500:
            df_compressed["Label_new"] = 500
    return df_compressed

def compressClassesNull(df, sep_list):
    df_copy = df.copy()
    df_copy['Label_new'] = df_copy["Label_nr"]
    df_copy.loc[~df_copy['Label_new'].isin(sep_list), 'Label_new'] = 0 #np.NaN
#    df_copy[mask] = 0
#        df_copy['Label_new'] = 0
    return df_copy
#    if df.loc[~df['column'].isin(list)]:
#        df.loc[~df['column'].isin(list)]["Label_new"] = 0
#    for i in df_compressed["Label_nr"]:
#        if i in sep_list:
#            df_compressed["Label_new"] = i
#        else:
#            df_compressed["Label_new"] = 0
#        

