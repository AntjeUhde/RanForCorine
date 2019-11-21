import gdal
import os
import rasterio as rio
import pandas as pd
import numpy as np
import osr
import sys
import numpy as np

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
        hdr[0]=hdr[0].split('{')[1]
        # print(hdr)
        # print(len(hdr))
        # print(hdr[0])
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

    if subset:
        # minx,miny,maxx,maxy=[444493.0,6207748.0,450572.0,6214642.0]
        minx,miny,maxx,maxy=[421900.0,6184700.0,467300.0,6227000.0]
    else:
        gt=ds1.GetGeoTransform()
        minx = gt[0]
        maxy = gt[3]
        maxx = minx + gt[1] * ds1.RasterXSize
        miny = maxy + gt[5] * ds1.RasterYSize
        # print(minx, miny)
    # resample the S-1 data to pixel size of the mask
    # ds2_res = gdal.Warp('', ds2, format='VRT', dstSRS='EPSG:{}'.format(epsg_s1),xRes=psize_s1, yRes=-psize_s1, \
    #     outputType=gdal.GDT_Int16)

    # clip the mask data to the extend of the S-1 data and set 100m GSD
    ds1_res = gdal.Warp('', ds1, format='VRT', xRes=psize_mask, yRes=psize_mask, \
        outputType=gdal.GDT_Float32, outputBounds=[minx,miny,maxx,maxy])#, targetAlignedPixels=True) 
    ds2_res = gdal.Warp('', ds2, format='VRT',dstSRS='EPSG:{}'.format(epsg_s1), xRes=psize_mask, yRes=psize_mask, \
        outputType=gdal.GDT_Int16, outputBounds=[minx,miny,maxx,maxy])#, targetAlignedPixels=True)

    # if necessary, cut the outer rows and columns to make sure, the output isn't bigger
    # than the input
    # gt2=ds2_res.GetGeoTransform()
    # redo=False
    # if minx>gt2[0]:
    #     minx=gt2[0]+psize_mask
    #     redo=True
    # if maxx<(gt2[0]+gt2[1]*ds2_res.RasterXSize):
    #     maxx=(gt2[0]+gt2[1]*ds2_res.RasterXSize)-psize_mask
    #     redo=True
    # if miny>(gt2[3]+gt2[5] * ds2_res.RasterYSize):
    #     miny=gt2[3]+gt2[5] * ds2_res.RasterYSize
    #     redo=True
    # if maxy<gt2[3]:
    #     maxy=gt2[3]-psize_mask
    #     redo=True
    # print(minx,miny,maxx,maxy)
    # gt2=None
    # if redo:
    #     ds1_out = gdal.Warp('', ds1_res, format='VRT', outputType=gdal.GDT_Float32, outputBounds=[minx,miny,maxx,maxy],\
    #         xRes=psize_mask, yRes=psize_mask,targetAlignedPixels=True) 
    #     ds2_out = gdal.Warp('', ds2_res, format='VRT', outputType=gdal.GDT_Int16, outputBounds=[minx,miny,maxx,maxy],\
    #         xRes=psize_mask, yRes=psize_mask,targetAlignedPixels=True)
    # else:
    #     ds1_out=ds1_res
    #     ds2_out=ds2_res

    if ds1_res.RasterXSize!=ds2_res.RasterXSize or ds1_res.RasterYSize!=ds2_res.RasterYSize:
        print("something went wrong, returning.")
        return
    else:
        print("adjustment done.")
    if write==True:
        if outfp1==None and outfp2==None:
            print("No filepath specified, returning the dataset.")
        else:
            # write_file_gdal(ds2_res,outfp2,ftype='GTIFF')
            # write_file_gdal(ds1_res,outfp1,ftype='ENVI',hdrfp=hdrfp)
            
            try:
                write_file_gdal(ds1_res,outfp1,ftype='ENVI',hdrfp=hdrfp)
            except:
                print("writing Sentinel-1 data failed")
            try:
                write_file_gdal(ds2_res,outfp2,ftype='GTIFF')
            except:
                print("writing mask data failed")
    return #ds1_out,ds2_out

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
    print(rows,'rows,',cols,'cols')

    # legend=pd.read_csv(legendfp, header = None)

    df=pd.DataFrame()
    for i in range(bands):
        if i == 0:
            labels=pd.Series(np.array(mask[:]).flat)
            # print(len(labels))
            df['Label_nr'] = labels
        layer=pd.Series(np.array(stack[i,:]).flat)
        # print(len(layer))
        df['Band_{}'.format(i)]=layer
        print('Layer',i) 

    # print(df.head())
    df.to_csv(outfp, sep=';')

def hist(fp):
    return
    
    
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
    Content of CSV file as numpy.dataFrame
    """
    return pd.read_csv(path)
    print("Successfully imported data")
    
def countMissingValuesTotal(data_raw):
    """
    Counts the missing values in a dataframe

    Parameters
    ----------
    data_raw: numypy.dataFrame 
        dataframe with values to analyze

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> countMissingValuesTotal(data)

    Returns
    -------
    absolute number of missing values
    """
    
    d_clean = data_raw.replace(-99.0, np.NaN)
    return d_clean.isnull().sum().sum()

def imputeMean(data, clean=False, null_value=-99):
    """
    Imputes missing data with mean value of that column.

    Parameters
    ----------
    data: numypy.dataFrame with np.NaN values
        dataframe with missing values to impute

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> imputeMean(data)

    Returns
    -------
    dataframe with imputed data
    """
    if clean == True:
        data = data.replace(null_value, np.NaN)
    return data.fillna(data.mean())

def splitData(data, labelcol, test_size=0.2, random_state=245):
    """
    Splits dataset in test and training dataset

    Parameters
    ----------
    data: numypy.dataFrame 
        dataframe with values to analyze
    labelcol: string
        name of column with class labels
    test_size: float
        portion of data to use as test dataset, default = 0.2
    random_state: int
        random integer number to secure reproducability

    Examples
    --------
    >>> data = numpy.dataframe()
    >>> splitData(data, "Labels", test_size=0.15, random_state=245)

    Returns
    -------
    test and training dataset für values and labels
    """
    # divide values and labels
#    col_names = list(data.columns)[startcol:endcol]
    x = data.drop(labelcol, axis=1)
#    x = data.iloc[:,:-1].values
    y = data[labelcol]
    if len(x) > 0:
        print("Done.")
    # Split train and test dataset (default 20 % of dataset = test)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
            x,y, test_size=test_size, random_state=random_state)
    print("Traingssamples: " + str(len(x_train)))
    print("Testsamples: " + str(len(x_test)))
    return x_train, x_test, y_train, y_test

def RandomForestClassifier(max_depth, random_state, n_estimators):
    return ensemble.RandomForestClassifier(
            max_depth=max_depth, 
            random_state=random_state, 
            n_estimators=n_estimators)
    
def fitModel(model, x_train, y_train):
    model.fit(x_train, y_train)
    
def predictModel(model, x_test):
    return model.predict(x_test)

def accuracyReport(prediction, y_test):
    accuracy = metrics.accuracy_score(prediction, y_test)
    conf_matrix = metrics.confusion_matrix(prediction, y_test)
    classif_report = metrics.classification_report(prediction, y_test)
    return accuracy, conf_matrix, classif_report

def printConfMatrix(conf_matrix, class_names):
    cl_act = []
    cl_pred = []
    for cl in class_names:
        cl_act.append(cl + " (act)")
        cl_pred.append(cl + " (pred)")
    print(pd.DataFrame(conf_matrix, cl_act, cl_pred))
