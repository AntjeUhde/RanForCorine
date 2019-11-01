import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.vrt import WarpedVRT
from rasterio import mask, MemoryFile
from affine import Affine
import gdal
import os
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
    >>> read_file(fp)

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
            sys.exit()
        else:
            print("file import done.")
            return ds,hdr
    else:
        if ds==None:
            print("Import failed")
            sys.exit()
        else:
            print("file import done.")
            return ds

def write_file(ds,outfn,ftype,hdr=None):
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
    hdr: list (optional)
        List of the band names to be written on the ENVI hdr file

    Examples
    --------
    >>> from bonds_functions import write_file
    >>> write_file(data,fp,'GEOTiff')

    Returns
    -------
    Nothing
    """
    driver = gdal.GetDriverByName(ftype)
    cols = ds.RasterYSize
    rows = ds.RasterXSize
    bands = ds.RasterCount
    if ftype=='GTIFF':
        dtype=gdal.GDT_UInt16
    elif ftype=='ENVI':
        dtype=gdal.GDT_Float32
    outds=driver.Create(outfn, rows, cols, bands, dtype)
    outds.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
    outds.SetProjection(ds.GetProjection())##sets same projection as input
    for i in range(bands):
        # print("Band",i)
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
    print('file wrote to disk.')
    return

def adjust(fp1,fp2, epsg=None, write=False, outfp=None):
    """
    Adjust ds2 to pixel size and extend of ds1

    Parameters
    ----------
    fp1: String
        Filepath to data-stack
    fp2: String
        Filepath to mask
    epsg: str (optional)
        EPSG-Code of the output array
    write: bool (optional)
        if True, transformed data is written to disk
    outfp: String (optional)
        Filepath for the dataset to be written to desk

    Examples
    --------
    >>> from bonds_functions import adjust
    >>> adjust(s1_stack_fp,mask_fp, write=True)

    Returns
    -------
    Gdal file object
        The reprojected and transformed data of the mask
    """
    ds1=read_file_gdal(fp1)
    ds2=read_file_gdal(fp2)
    print(ds2)
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
    print("Pixel size of the S-1 data is {}°, of the mask is {}m".format(psize_s1,psize_mask))
    print("Resampling the mask stack to CSR and GSD of S-1.")
    # resample the S-1 data to pixel size of the mask
    ds2_res = gdal.Warp('', ds2, format='VRT', dstSRS='EPSG:{}'.format(epsg_s1),
               outputType=gdal.GDT_Int16, xRes=psize_s1, yRes=psize_s1) #CSR transform: dstSRS='EPSG:{}'.format(epsg_s1),
    # read the S-1 data extend for clipping of mask
    gt=ds1.GetGeoTransform()
    minx = gt[0]
    maxy = gt[3]
    maxx = minx + gt[1] * ds1.RasterXSize
    miny = maxy + gt[5] * ds1.RasterYSize
    # print(minx,maxx, miny, maxy)
    # clip the mask data to the extend of the S-1 data
    ds2_clip=gdal.Translate('', ds2_res, format='VRT', projWin = [minx, maxy, maxx, miny])
    gt_clip=ds2_clip.GetGeoTransform()
    psize_clip=gt_clip[1]
    print("The new pixel size of the mask is {}°".format(psize_clip))
    print("adjustment done.")
    if write==True:
        if outfp==None:
            print("No filepath specified, returning the dataset")
        else:
            write_file(ds2_clip,outfp,ftype='GTIFF')
    return ds2_clip

def read_file_rio(fp):
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
    data=rio.open(fp)
    return data

def write_mem_raster(data, **profile):
    with MemoryFile() as memfile:
        with memfile.open(**profile) as dataset:  # Open as DatasetWriter
            dataset.write(data)

        with memfile.open() as dataset:  # Reopen as DatasetReader
            yield dataset  # Note yield not return

def reprojection(src, outpath, new_crs,cut=None):
    """
    take an input dataset and reproject it to a given CRS, return the new dataset
    #TODO: how to prevent rasterio from writing the reprojected data to disk?
    """

    dst_crs = new_crs 

    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    # print(width,height)
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rio.open(outpath, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            # print(dst.width,dst.height)
            reproject(
                source=rio.band(src, i),
                destination=rio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)
        return rio.open(outpath,'r')

def write_data(data,outpath, driver):
    kwargs={
        'driver': driver,
        'width': data.RasterXSize,
        'height': data.RasterYSize
    }
    with rio.open(outpath, 'w', **kwargs) as dst:
        for i in range(1,len(data)+1):
            reproject(
                source=rio.band(data.GetRasterBand(i).ReadAsArray(), i),
                destination=rio.band(dst, i))

