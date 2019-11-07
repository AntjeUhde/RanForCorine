import functions as f
import gdal
import pandas as pd
import numpy as np
import rasterio as rio
import sys

# split dataset into seperated classes and divide into training- and testdata

fp_stack=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_VH_2018_100m"
# fp_hdr=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_VH_2018_100m.hdr"
fp_mask=r"D:\Master\Geo419\Projekt\Daten\clc2018_vattenrike.tif"
fp_legend=r"D:\Master\Geo419\Projekt\Daten\clc2018_clc2018_v2018_20_raster100m\Legend\CLC2018_CLC2018_V2018_20_QGIS.txt"
fp_df=r"D:\Master\Geo419\Projekt\classvalues_VH.csv"

def split_classes(stackfp,maskfp,legendfp,outfp):
    stack=rio.open(stackfp).read()
    mask=rio.open(maskfp).read()
    mask=mask[0]
    bands,rows,cols=stack.shape

    # legend=pd.r                                                                                                         c..............................................................................................................................................................................................................d[5]

    df=pd.DataFrame(columns=range(bands))
    count=0
    for i in range(rows):#rows
        for j in range(cols):#cols
            pixel=stack[:,i,j]
            pixel=pd.Series(pixel)
            df.loc[count,:bands]=pixel
            label=legend[5].loc[legend[0]==mask[i,j]].item()
            df.loc[count, 'Label'] = label
            count+=1
        # break

    print(df.head())
    # df.to_csv(outfp)

split_classes(fp_stack,fp_mask,fp_legend,fp_df)
print("done")

mask=None 
stack=None 