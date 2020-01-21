import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lc_classif", 
    version="0.0.1",
    author="Antje Uhde, Theresa Möller",
    description="A package to conduct Corine land cover classification using Sentinel-1 data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntjeUhde/lc_classif",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['gdal>=2.4.1',
                    'numpy>=1.16.1',
                    'pandas>=0.24.2',
                    'rasterio>=1.0.24'],
)