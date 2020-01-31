import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RanForCorine", 
    version="0.0.1",
    author="Antje Uhde, Theresa Möller",
    description="A package to conduct Corine land cover classification using Sentinel-1 data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntjeUhde/RanForCorine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='=3.7',
    install_requires=['gdal==2.4.1',
                    'numpy==1.16.5',
                    'pandas==0.25.1',
                    'rasterio==1.0.24',
                    'sklearn==0.21.3',
                    'matplotlib==3.1.1',
                    'scipy==1.3.1',
                    'seaborn==0.9.0'],
    )