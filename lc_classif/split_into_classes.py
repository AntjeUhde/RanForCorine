import functions as f

pols=['VH','VV']

# split dataset into seperated classes and divide into training- and testdata
for pol in pols:
    fp_stack=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018_100m".format(pol)
    # fp_hdr=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018_100m.hdr".format(pol)
    fp_mask=r"D:\Master\Geo419\Projekt\Daten\clc2018_vattenrike.tif"
    fp_legend=r"D:\Master\Geo419\Projekt\Daten\clc2018_clc2018_v2018_20_raster100m\Legend\CLC2018_CLC2018_V2018_20_QGIS.txt"
    fp_df=r"D:\Master\Geo419\Projekt\classvalues_{}.csv".format(pol)

    f.split_classes(fp_stack,fp_mask,fp_legend,fp_df)
    print("done")

mask=None 
stack=None 