import functions as f

fp_stack=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP"
# fp_hdr=r"D:\Master\HiWi_BONDS\Daten\S1_IW_VV_39_Curuai_dB_20_timestack_avg_SNAP.hdr"
fp_mask=r"D:\Master\HiWi_BONDS\Daten\LowerVarzeaHabitats_v2_MapArea01_.tif"
outfnmask=r'D:\Master\Geo419\Projekt\mask_Curuai_resampled_TEST.tif'

# adjust pixel size and extend of S-1 data and mask
mask=f.adjust(fp_stack,fp_mask, epsg=4326, write=True, outfp=outfnmask)

mask=None