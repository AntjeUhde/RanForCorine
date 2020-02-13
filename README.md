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
needs to be installed separately due to a more complex installation process
if used in jupyter notebooks. Due it its dependency, the same accounts for
rasterio, which can simply be installed using pip.You should now be good
to go!

Land cover classification
-------------------------
See the jupyter notebook in */examples* for further information on how
to use this package.