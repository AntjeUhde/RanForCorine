import functions as f
import gdal
import pandas
import rasterio as rio
import sys

# split dataset into seperated classes and divide into training- and testdata

fp_stack=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP"
fp_hdr=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP.hdr"
fp_mask=r'D:\Master\Geo419\Projekt\mask_Curuai_resampled_TEST.tif'

stack=rio.open(fp_stack).read()
mask=rio.open(fp_mask).read()

pixel0=stack[:,0,0]
print("done")