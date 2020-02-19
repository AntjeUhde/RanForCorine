# RanForCorine

This package uses machine learning for the land cover classification of 
Sentinel-1 data. It is the python programming project of Theresa Möller 
and Antje Uhde for the module Geo419 of the M.Sc. Geoinformatics course 
at the Friedrich-Schiller-University Jena.

Please note, that due to problems installing the correct GDAL using conda
this package can not be installed within an anaconda environment. We 
are currently working on a solution and will update as soon as possible.

Installation
------------
To use this package, download or clone the repo. In a cmd shell move to
the folder where setup.py is located and type `python setup.py sdist bdist_wheel` 
(make sure to have `setuptools wheel` installed, e.g. via pip). Type 
`pip install dist/RanForCorine-VERSION-py3-none-any.whl` (replace VERSION 
with the correct version number) in the cmd shell. GDAL 
needs to be installed separately due to a more complex installation process.
You can [download the wheel here.](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
Chose the correct version specified in the requirements.txt which fits 
your operating system. Use `pip install gdalfilename.whl`.
Make sure to update of the system environment variables
([check step 3 of this description](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows)).
Due it its dependency, the same accounts for rasterio, which can simply be 
installed using pip.
You should be good to go now!
If you want to use RanForCorine with conda there are some additional steps to follow.
First, move to the folder `ranforcorine-conda` and run `conda-build .` from an anaconda powershell.
After that you run `conda install --use-local RanForCorine` to finally install the package.

Land cover classification
-------------------------
See the jupyter notebook in */examples* for further information on how
to use this package.