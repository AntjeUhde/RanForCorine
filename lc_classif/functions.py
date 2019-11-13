import gdal
import os
import rasterio as rio
import pandas as pd
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
    >>> from functions import read_file
    >>> read_file_gdal(fp)

    Returns
    -------
    Gdal file object
        The data of the file
    """
    ds=gdal.Open(fp)
    if hdrp!=None:
        hdr=[h.rstrip('\n') for h in open(hdrp)][19::]
            # print(hdr)
        if ds==None:
            print("Import failed")
            # return
        else:
            print("file import done.")
        return ds,hdr
    else:
        if ds==None:
            print("Import failed")
            # return
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
    >>> from functions import write_file_gdal
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
        # hdr=[h.rstrip('\t') for h in open(hdrfp)][12::]
        hdr=[h.split(',') for h in open(hdrfp)][12::]
        hdr=hdr[0]
        # print(hdr)
        # print(len(hdr))
        # return
    if ftype=='GTIFF':
        dtype=gdal.GDT_UInt16
    elif ftype=='ENVI':
        dtype=gdal.GDT_Float32
    # print(rows,cols,bands,dtype)
    outds=driver.Create(outfn, rows, cols, bands, dtype)
    # print(outds)
    outds.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
    outds.SetProjection(ds.GetProjection())##sets same projection as input
    for i in range(bands):
        print("Band",i)
        band=ds.GetRasterBand(i+1).ReadAsArray()
        # set values < -30 as no-data
        # band[band<-30]=None
        # band=band>-30
        # print(band)
        outds.GetRasterBand(i+1).WriteArray(band)
        if ftype=='ENVI':
            outds.GetRasterBand(i+1).SetDescription(hdr[i])

    outds.FlushCache() # saves to disk!!
    outds = None
    print('file written to disk.')
    return

def adjust(fp1,fp2, epsg=None, write=False, outfp1=None, outfp2=None,hdrfp=None, subset=None):
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
    subset: boolean (optional)
        If True, both datasets are clipped to predefined subset extend

    Examples
    --------
    >>> from bonds_functions import adjust
    >>> adjust(fp_stack,fp_mask, epsg=32633, write=True, outfp1=outfnstack,outfp2=outfnmask,hdrfp=fp_hdr,subset=True)

    Returns
    -------
    Gdal file object
        The transformed Sentinel-1 data
    Gdal file object
        The reprojected data of the mask
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
    # print(psize_stack,gt_s1[-5])
    
    # read metadata such as EPSG code and raster size
    proj_mask=osr.SpatialReference(wkt=ds2.GetProjection())
    epsg_mask=proj_mask.GetAttrValue('AUTHORITY',1)
    gt_mask=ds2.GetGeoTransform()
    psize_mask=gt_mask[1]
    
    print("EPSG Code of the S-1 data is {}, of the mask is {}".format(epsg_s1,epsg_mask))
    print("Pixel size of the S-1 data is {}m, of the mask is {}m".format(psize_s1,psize_mask))
    print("Resampling the mask to CSR of stack and stack to GSD of mask.")
    # resample the S-1 data to pixel size of the mask
    ds2_res = gdal.Warp('', ds2, format='VRT', dstSRS='EPSG:{}'.format(epsg_s1),xRes=psize_s1, yRes=-psize_s1, outputType=gdal.GDT_Int16)
    # read the S-1 data extend for clipping of mask
    
    if subset:
        minx,miny,maxx,maxy=[444493.0,6207748.0,450572.0,6214642.0]
    else:
        gt=ds1.GetGeoTransform()
        minx = gt[0]
        maxy = gt[3]
        maxx = minx + gt[1] * ds1.RasterXSize
        miny = maxy + gt[5] * ds1.RasterYSize
    # print(minx,maxx, miny, maxy)

    # clip the mask data to the extend of the S-1 data and set 100m GSD
    ds2_clip=gdal.Translate('', ds2_res, format='VRT', projWin = [minx, maxy, maxx, miny])
    ds1_clip=gdal.Translate('', ds1, format='VRT', projWin = [minx,maxy,maxx,miny])
    ds1_res = gdal.Warp('', ds1_clip, format='VRT', xRes=psize_mask, yRes=psize_mask, outputType=gdal.GDT_Float32) 
    ds2_res = gdal.Warp('', ds2_clip, format='VRT', xRes=psize_mask, yRes=psize_mask, outputType=gdal.GDT_Int16)

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
    return ds1_res,ds2_res

def split_classes(stackfp,maskfp,legendfp,outfp):
    """
    Splits the given data into seperated classes based on a mask.

    Parameters
    ----------
    stackfp: String 
        Filepath to the Sentinel-1 data stack
    maskfp: String
        Filepath to the mask file
    legendfp: String
        Filepath to the legend-CSV
    outfp: String
        Filepath for the splitted data table to be written to disk.

    Examples
    --------
    >>> from bonds_functions import split_classes
    >>> split_classes(s1_stack_fp,mask_fp, legend_fp,out_fp)

    Returns
    -------
    Nothing
    """
    stack=rio.open(stackfp).read()
    mask=rio.open(maskfp).read()
    mask=mask[0]
    bands,rows,cols=stack.shape
    print(rows,cols)

    legend=pd.read_csv(legendfp, header = None)
    # classes=legend[0]
    # labels=legend[5]        

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
        print("row", i)

    # print(df.head())
    df.to_csv(outfp, sep=';')