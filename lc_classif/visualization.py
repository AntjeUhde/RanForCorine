# -*- coding: utf-8 -*-
"""
visualization.py: visualizing the results of Random Forest image classification

@author: Theresa Möller
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import numpy as np

def plotResult(prediction, imagedim = [127,455]):
    """
    Plot predicted image

    Parameters
    ----------
    prediction: 1d-array with predicted labels        
    imagedim: list containing height and width of resulting image

    Examples
    --------
    >>> plotResult([127, 455], base_prediction)

    Returns
    -------
    Nothing
    """
    grid = prediction.reshape((imagedim[0], imagedim[1]))
    values = np.unique(prediction.ravel())
    plt.figure(figsize=(8,4))
    im = plt.imshow(grid, interpolation='none')
    #TODO: sort list of unique values and get the corresponding CMYK colors
    # create custom colormap using matplotlib.colors.ListedColormap(['blue','black','red'])
    # pass on this colormap to the plotting function
    colors = [ im.cmap(im.norm(value)) for value in values]
    patches = [ mpatches.Patch(color=colors[i], 
                label="{l}".format(l=values[i]) ) for i in range(len(values)) ]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    plt.show()