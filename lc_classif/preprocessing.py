import functions as f
import gdal
import sys


fp_stack=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP"
fp_hdr=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP.hdr"
fp_mask=r"D:\Master\HiWi_BONDS\Daten\LowerVarzeaHabitats_v2_MapArea01_.tif"
outfnmask=r'D:\Master\Geo419\Projekt\mask_Curuai_resampled_TEST.tif'

# read the data
# stack,hdr=f.read_file(fp_stack,hdrp=fp_hdr)
# mask=f.read_file(fp_mask)
# # print(mask)

# adjust pixel size and extend of S-1 data and mask
mask=f.adjust(fp_stack,fp_mask, epsg=4326, write=True, outfp=outfnmask)

# save the result to disk

# f.write_file(mask,outfnmask,'GTIFF')

# stack=None
# hdr=None
mask=None