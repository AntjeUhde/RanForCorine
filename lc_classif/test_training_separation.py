# -*- coding: utf-8 -*-
"""
test_training_separation.py: separates test and training dataset

@author: Theresa Möller
"""

def imageSplit(
        data, 
        labelcol='Label_nr', 
        imagedim=[455,423], 
        testsize=0.3):
    """
    Split test and traing dataset taking the testsize proportion from the 
    top of the image as test dataset and the rest as training dataset

    Parameters
    ----------
    data: numpy.dataframe with data
    label_col: string, name of label column
    imagedim: list containing image size in width and height
    testsize: proportion of image to use for test dataset (values between 0 and 1)
    
    Examples
    --------
    >>> x_train, x_test, y_train, y_test = imageSplit(
            data_raw, 
            "Label_nr",
            [455, 423],
            0.2)

    Returns
    -------
    test and training datasets
    """
    row_count = round(imagedim[1] * testsize) * imagedim[0]
    x = data.drop(labelcol, axis=1)
    y = data[labelcol]    
    x_test = x.iloc[0:row_count] 
    x_train = x.iloc[row_count+1:x.shape[0]]
    y_test = y.iloc[0:row_count] 
    y_train = y.iloc[row_count+1:y.shape[0]]
    return x_train, x_test, y_train, y_test
