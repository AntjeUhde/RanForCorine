import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RanForCorine", 
    version="0.4.6",
    author="Theresa Möller, Antje Uhde",
    author_email='theresa.moeller@uni-jena.de, antje.uhde@uni-jena.de',
    license='MIT',
    description="A package to conduct Corine land cover classification using Sentinel-1 data and random forest classification.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntjeUhde/RanForCorine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.0',
    install_requires=['numpy==1.16.5',
                    'pandas==0.25.1',
                    'scikit-learn==0.21.3',
                    'matplotlib==3.1.1',
                    'scipy==1.10.0',
                    'seaborn==0.9.0']                  
    )