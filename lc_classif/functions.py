import rasterio
import gdal
import os
import osr
import sys

def read_file(fp):
    """
    Open the specified file

    Parameters
    ----------
    fp: str
        Full file path to the file to be opened

    Examples
    --------
    >>> from bonds_functions import read_file
    >>> read_file(fp)

    Returns
    -------
    rasterio file object
        The data of the file
    """
    data=rasterio.open(fp)
    return data

stackfp=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP_mult_stats"
maskfp=r"D:\Master\HiWi_BONDS\Daten\LowerVarzeaHabitats_v2_MapArea01_.tif"

stack=read_file(stackfp)
mask=read_file(maskfp)

print("done")
stack=None
mask=None