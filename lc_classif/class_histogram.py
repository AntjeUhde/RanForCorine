import functions as f

pols=['VH','VV']

# create histogram of classes
for pol in pols:
    fp_table=r"D:\Master\Geo419\Projekt\classvalues_{}.csv".format(pol)

    f.hist(fp_table) 