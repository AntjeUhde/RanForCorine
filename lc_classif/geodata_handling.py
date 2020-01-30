# -*- coding: utf-8 -*-
"""
geodata_handling.py: Operations on the geodata

@autor: Theresa Möller, Antje Uhde
"""
import gdal
import os
import rasterio as rio
import pandas as pd
import numpy as np
import osr
import sys

def read_file_gdal(fp,hdrp=None):
    """
    Open the specified file

    Parameters
    ----------
    fp: str
        Full file path to the file to be opened
    hdrp: str (optional) 
        Full file path to the hdr-file of an Envi file to be opened

    Examples
    --------
    >>> from lc_classif.geodata_handling import read_file_gdal
    >>> read_file_gdal(fp)

    Returns
    -------
    Gdal file object
        The data of the file
    """
    ds=gdal.Open(fp)
    if hdrp!=None:
        hdr=[h.rstrip('\n') for h in open(hdrp)][19::] # read the band names
        if ds==None:
            print("Import failed")
        else:
            print("file import done.")
        return ds,hdr
    else:
        if ds==None:
            print("Import failed")
        else:
            print("file import done.")
        return ds

def write_file_gdal(ds,outfn,ftype,hdrfp=None):
    """
    Write the passed GDAL file to disk

    Parameters
    ----------
    ds: GDAL file object
        File object containing the data to be written to disk
    outfn: str
        Full file path to the file to be written
    ftype: str  
        Filetype of the data
    hdrfp: String
        Filepath to the header-file of an ENVI dataset.

    Examples
    --------
    >>> from lc_classif.geodata_handling import write_file_gdal
    >>> write_file_gdal(data,fp,'GEOTiff')

    Returns
    -------
    Nothing
    """
    driver = gdal.GetDriverByName(ftype)
    cols = ds.RasterYSize
    rows = ds.RasterXSize
    bands = ds.RasterCount
    if hdrfp!=None:
        # read the band names
        hdr=[h.split(',') for h in open(hdrfp)][12::]
        hdr=hdr[0]
        hdr[0]=hdr[0].split('{')[1]
    if ftype=='GTIFF':
        dtype=gdal.GDT_UInt16 # set the data type
    elif ftype=='ENVI':
        dtype=gdal.GDT_Float32 # set the data type
    outds=driver.Create(outfn, rows, cols, bands, dtype) # create the output file
    outds.SetGeoTransform(ds.GetGeoTransform()) # set same geotransform as input
    outds.SetProjection(ds.GetProjection()) # set same projection as input
    for i in range(bands):
        print("Writing Band",i)
        band=ds.GetRasterBand(i+1).ReadAsArray()
        outds.GetRasterBand(i+1).WriteArray(band) # write the array into band of output image
        if ftype=='ENVI':
            outds.GetRasterBand(i+1).SetDescription(hdr[i]) # copy the band name

    outds.FlushCache() # saves to disk!!
    ds=None # close the data in memory
    outds = None
    print('file written to disk.')
    return

def adjust(fp1,fp2,epsg=None,write=False,outfp1=None,outfp2=None,hdrfp=None,subset=None):
    """
    Adjust ds2 to extend of ds1 and resample pixel size of ds1 to pixel size
    of ds2.

    Parameters
    ----------
    fp1: String
        Filepath to data-stack
    fp2: String
        Filepath to mask
    epsg: str (optional)
        EPSG-Code of the output array
    write: bool (optional)
        If True, transformed data is written to disk
    outfp1: String (optional)
        Filepath for the dataset to be written to desk
    outfp2: String (optional)
        Filepath for the dataset to be written to desk
    hdrfp: String (optional)
        Filepath to the header file of an ENVI dataset
    subset: List (optional)
        Both datasets are clipped to passed subset extend [minx,miny,maxx,maxy]

    Examples
    --------
    >>> from lc_classif.geodata_handling import adjust
    >>> adjust(fp_stack,fp_mask, epsg=32633, write=True, outfp1=outfnstack,outfp2=outfnmask,hdrfp=fp_hdr,subset=True)

    Returns
    -------
    Nothing
    """
    ds1=read_file_gdal(fp1) #open the S-1 dataset
    ds2=read_file_gdal(fp2) #open the mask

    # read metadata such as EPSG code and raster size
    proj_s1=osr.SpatialReference(wkt=ds1.GetProjection())
    epsg_s1=proj_s1.GetAttrValue('AUTHORITY',1)
    if epsg_s1==None and epsg!=None:
        epsg_s1=epsg
    gt_s1=ds1.GetGeoTransform()
    psize_s1=gt_s1[1]
    
    # read metadata such as EPSG code and raster size
    proj_mask=osr.SpatialReference(wkt=ds2.GetProjection())
    epsg_mask=proj_mask.GetAttrValue('AUTHORITY',1)
    gt_mask=ds2.GetGeoTransform()
    psize_mask=gt_mask[1]
    
    print("EPSG Code of the S-1 data is {}, of the mask is {}".format(epsg_s1,epsg_mask))
    print("Pixel size of the S-1 data is {}m, of the mask is {}m".format(psize_s1,psize_mask))
    print("Resampling the mask to CSR of stack and stack to GSD of mask.")

    if type(subset)==list:
        minx,miny,maxx,maxy=subset
    else:
        gt=ds1.GetGeoTransform()
        minx = gt[0]
        maxy = gt[3]
        maxx = minx + gt[1] * ds1.RasterXSize
        miny = maxy + gt[5] * ds1.RasterYSize

    # clip the mask data to the extend of the S-1 data and set 100m GSD
    ds1_res = gdal.Warp('', ds1, format='VRT', xRes=psize_mask, yRes=psize_mask, \
        outputType=gdal.GDT_Float32, outputBounds=[minx,miny,maxx,maxy])#, targetAlignedPixels=True) 
    ds2_res = gdal.Warp('', ds2, format='VRT',dstSRS='EPSG:{}'.format(epsg_s1), xRes=psize_mask, yRes=psize_mask, \
        outputType=gdal.GDT_Int16, outputBounds=[minx,miny,maxx,maxy])#, targetAlignedPixels=True)

    if ds1_res.RasterXSize!=ds2_res.RasterXSize or ds1_res.RasterYSize!=ds2_res.RasterYSize:
        print("something went wrong, returning.")
        return
    else:
        print("adjustment done.")
    if write==True:
        if outfp1==None and outfp2==None:
            print("No filepath specified, returning the dataset.")
        else:
            try:
                write_file_gdal(ds1_res,outfp1,ftype='ENVI',hdrfp=hdrfp)
            except:
                print("writing Sentinel-1 data failed")
            try:
                write_file_gdal(ds2_res,outfp2,ftype='GTIFF')
            except:
                print("writing mask data failed")
    return 

def split_classes(stackfp,maskfp,outfp):
    """
    Splits the given data into seperated classes based on a mask.

    Parameters
    ----------
    stackfp: String 
        Filepath to the Sentinel-1 data stack
    maskfp: String
        Filepath to the mask file
    outfp: String
        Filepath for the splitted data table to be written to disk.

    Examples
    --------
    >>> from lc_classif.geodata_handling import split_classes
    >>> split_classes(s1_stack_fp,mask_fp,out_fp)

    Returns
    -------
    Nothing
    """
    stack=rio.open(stackfp).read()
    mask=rio.open(maskfp).read()
    mask=mask[0]
    bands,rows,cols=stack.shape
    bands=None #not needed
    print('The data consists of',rows,'rows,',cols,'columns')

    df=pd.DataFrame()
    for i in range(10):
        if i == 0:
            labels=pd.Series(np.array(mask[:]).flat) # read the class labels once
            df['Label_nr'] = labels
        layer=pd.Series(np.array(stack[i,:]).flat) # all pixel values of this layer
        df['Band_{}'.format(i)]=layer

    df.to_csv(outfp, sep=';') # save table to disk
	
def importCSV(path):
    """
    Imports data from CSV file.

    Parameters
    ----------
    path: String 
        Filepath to the CSV file

    Examples
    --------
    >>> data = importCSV("C:/path-to-file/file-name.csv")
    
    Returns
    -------
    Pandas DataFrame
    """
    return pd.read_csv(path, sep=";", na_values=['-99.0'])
    print("Successfully imported data")

#TODO: write prediction array to disk as GeoTIFF
