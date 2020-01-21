import lc_classif.geodata_handling as f
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys

pols=['VH','VV']

def hist(fp,fp_leg,outfp):

    df=pd.read_csv(fp, sep=';').drop('Unnamed: 0', axis=1)
    legend=pd.read_csv(fp_leg, header = None)

    classes=['Artificial surfaces','Agricultural areas','Forest and semi natural areas','Wetlands','Water bodies']
    class_colors=['magenta','r','g','c','b']

    df.loc[(df['Label_nr'] >= 100)&(df['Label_nr'] < 200),'Label']=classes[0]
    df.loc[(df['Label_nr'] >= 200)&(df['Label_nr'] < 300),'Label']=classes[1]
    df.loc[(df['Label_nr'] >= 300)&(df['Label_nr'] < 400),'Label']=classes[2]
    df.loc[(df['Label_nr'] >= 400)&(df['Label_nr'] < 500),'Label']=classes[3]
    df.loc[(df['Label_nr'] >= 500)&(df['Label_nr'] < 600),'Label']=classes[4]
    # print(df.head())
    # sys.exit()

    data=df['Label_nr'].value_counts()

    custom_palette={}
    for i in data.index:
        if int(i)>=100 and int(i)<200:
            custom_palette[i]=class_colors[0]
        elif int(i)>=200 and int(i)<300:
            custom_palette[i]=class_colors[1]
        elif int(i)>=300 and int(i)<400:
            custom_palette[i]=class_colors[2]
        elif int(i)>=400 and int(i)<500:
            custom_palette[i]=class_colors[3]
        elif int(i)>=500 and int(i)<600:
            custom_palette[i]=class_colors[4]

    labels=legend.loc[legend[0].isin(df['Label_nr']),:]

    sns.set()
    sns.set_style('darkgrid')
    fig,ax=plt.subplots(figsize=(20,15))
    # plt.figsize(15,10)
    sns.barplot(data.index, data.values, palette=custom_palette)
    ax.set_xticklabels(labels[5])
    plt.xticks(rotation=30, ha='right')
    legend_entries = [Line2D([0], [0], color=class_colors[0], lw=5),
                Line2D([0], [0], color=class_colors[1], lw=5),
                Line2D([0], [0], color=class_colors[2], lw=5),
                Line2D([0], [0], color=class_colors[3], lw=5),
                Line2D([0], [0], color=class_colors[4], lw=5)]
    plt.legend(legend_entries,classes)
    plt.savefig(outfp,bbox_inches='tight')
    # plt.show()
    plt.close()
    df=None
    return

def kernelplot(fp,fp_leg,outfp):
    #plot kernel density
    df=pd.read_csv(fp, sep=';').drop('Unnamed: 0', axis=1)
    # print(df[:5].head())
    legend=pd.read_csv(fp_leg, header = None)

    classes=['Artificial surfaces','Agricultural areas','Forest and semi natural areas','Wetlands','Water bodies']
    class_colors=['magenta','r','g','c','b']

    labels=list(legend.loc[legend[0].isin(df['Label_nr']),0])
    # print(type(labels))

    # sns.set(rc={'figure.figsize':(10,5)})
    # sns.set_style("whitegrid")

    for i in range(len(labels)-1):
        # print(type(labels[1]), type(df['Label_nr'][5]))
        # print(labels[i])
        class_vals=df.loc[df['Label_nr']==labels[i],'Band_0':].values.tolist()#.flatten()
        class_vals=[j for sub in class_vals for j in sub] 
        # print(type(class_vals))
        # print(class_vals.shape)
        sns.distplot(class_vals,hist=False,label=labels[i])#,color=colors[i]
        # class_vals=None
        print("Class {} done.".format(labels[i]))

    plt.xlim(-40,12)
    plt.legend(loc='upper right', ncol=2)
    plt.savefig(outfp)
    plt.show()
    plt.close()
    print("{} kernel density plot done.".format(pol))
    return

# create histogram of classes
for pol in pols:
    fp_table=r"D:\Master\Geo419\Projekt\classvalues_{}.csv".format(pol)
    fp_legend=r"D:\Master\Geo419\Projekt\Daten\clc2018_clc2018_v2018_20_raster100m\Legend\CLC2018_CLC2018_V2018_20_QGIS.txt"
    fp_out_kernel=r'D:\Master\Geo419\Projekt\kernel_density_{}.png'.format(pol)
    
    kernelplot(fp_table,fp_legend,fp_out_kernel)
    # f.hist(fp_table) 
    # sys.exit()

# fp_out=r'D:\Master\Geo419\Projekt\class_histogram.png'
# hist(fp_table,fp_legend,fp_out)