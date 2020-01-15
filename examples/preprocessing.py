import lc_classif.geodata_handling as f
import rasterio
from rasterio.enums import Resampling

pols=['VH','VV']

for pol in pols:
    fp_stack=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018".format(pol)
    fp_hdr=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018.hdr".format(pol)
    fp_mask=r"D:\Master\Geo419\Projekt\Daten\clc2018_clc2018_v2018_20_raster100m\CLC2018_CLC2018_V2018_20.tif"
    outfnstack=r'D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018_100m_test'.format(pol)
    outfnmask=r'D:\Master\Geo419\Projekt\Daten\clc2018_vattenrike_test.tif'

    # adjust pixel size and extend of S-1 data and mask
    # stack,mask=f.adjust(fp_stack,fp_mask, epsg=32633, write=True, outfp1=outfnstack,outfp2=outfnmask,hdrfp=fp_hdr,subset=False) #epsg=32633
    f.adjust(fp_stack,fp_mask, epsg=32633, write=False, outfp1=outfnstack,outfp2=outfnmask,hdrfp=fp_hdr,subset=False) #epsg=32633

stack=None
mask=None

##def main():
##
##    pol='VH'
##    
##    fp_stack=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018".format(pol)
##    fp_hdr=r"D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018.hdr".format(pol)
##    fp_mask=r"D:\Master\Geo419\Projekt\Daten\clc2018_clc2018_v2018_20_raster100m\CLC2018_CLC2018_V2018_20.tif"
##    outfnstack=r'D:\Master\Geo419\Projekt\Daten\Sweden_Vattenrike_{}_2018_100m'.format(pol)
##    outfnmask=r'D:\Master\Geo419\Projekt\Daten\clc2018_vattenrike.tif'
##    
##    # adjust pixel size and extend of S-1 data and mask
##    stack,mask=f.adjust(fp_stack,fp_mask, epsg=32633, write=True, outfp1=outfnstack,outfp2=outfnmask,hdrfp=fp_hdr,subset=False) #epsg=32633
##    
##    stack=None
##    mask=None
##
##if __name__ == '__main__':
##    main()
