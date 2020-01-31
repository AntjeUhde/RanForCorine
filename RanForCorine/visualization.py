# -*- coding: utf-8 -*-
"""
visualization.py: visualizing the results of Random Forest image classification

@author: Theresa Möller, Antje Uhde
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Patch
import matplotlib as mpl
import numpy as np
import pandas as pd

def get_meta(number):
    """
    Retrieve the level 3 classname and official RGB value for each clc class.

    Parameters
    ----------
    number: int
        CLC_CODE of the class
    
    Examples
    --------
    >>> get_meta(111) 

    Returns
    -------
    Official RGB colors as (r,g,b)
    Level 3 name of the class
    """
    df=pd.read_csv(r'./data/clc_legend.txt', header=None)
    rgb=((df.loc[df[0]==number,1].values[0]/255),(df.loc[df[0]==number,2].values[0]/255),(df.loc[df[0]==number,3].values[0]/255))
    name=df.loc[df[0]==number,5].values[0]
    return rgb,name

def plotResult(prediction, imagedim = [127,455], fp=None):
    """
    Plot predicted image

    Parameters
    ----------
    prediction: array
        array with predicted labels        
    imagedim: list
        containing height and width of resulting image
    fp: str (optional)
        filepath to save the plot on disk

    Examples
    --------
    >>> plotResult([127, 455], base_prediction)

    Returns
    -------
    Nothing
    """
    grid = prediction.reshape((imagedim[0], imagedim[1]))
    values = np.unique(prediction.ravel())
    img = np.empty((grid.shape[0], grid.shape[1], 3))
    legend_elements=[]
    for i in values:
        # get the official Corine Land Cover RGB values and level 3 class name
        rgb,name=get_meta(i)
        img[np.where(grid==i)]=rgb
        legend_elements.append(
            Patch(facecolor=rgb, edgecolor=None,
                         label=name)
        )
    plt.imshow(img, interpolation='none')
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    plt.tight_layout()
    if fp != None:
        plt.savefig(fp)
    plt.show()
