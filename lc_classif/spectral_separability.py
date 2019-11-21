# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 10:08:09 2019

@author: there
"""
#######################
# Work in Progress
######################

# implement Battachariah distance or Jeffries-Matusita distance
#code from https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/

# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-d", "--dataset", required = True,
#	help = "Path to the directory of images")
#args = vars(ap.parse_args())
# 
# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves
index = {}
images = {}

## loop over the image paths
#for imagePath in glob.glob(args["dataset"] + "/*.png"):
#	# extract the image filename (assumed to be unique) and
#	# load the image, updating the images dictionary
#	filename = imagePath[imagePath.rfind("/") + 1:]
#	image = cv2.imread(imagePath)
#	images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
	# extract a 3D RGB color histogram from the image,
	# using 8 bins per channel, normalize, and update
	# the index
    
# step 1: calculate histogram for all classes (not with this function)
    # such dir die Werte einer Klasse aus dem DF
    # steck den Array in numpy.histogram
    # mach das für alle verfügbaren Klassen
	hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
	hist = cv2.normalize(hist, hist).flatten()
	index[filename] = hist

# METHOD #1: UTILIZING OPENCV
# initialize OpenCV methods for histogram comparison
OPENCV_METHODS = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Chi-Squared", cv2.HISTCMP_CHISQR),
	("Intersection", cv2.HISTCMP_INTERSECT),
	("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
 
# loop over the comparison methods
for (methodName, method) in OPENCV_METHODS:
	# initialize the results dictionary and the sort
	# direction
	results = {}
	reverse = False
 
	# if we are using the correlation or intersection
	# method, then sort the results in reverse order
	if methodName in ("Correlation", "Intersection"):
		reverse = True
for (k, hist) in index.items():
		# compute the distance between the two histograms
		# using the method and update the results dictionary
		d = cv2.compareHist(index["doge.png"], hist, method)
		results[k] = d
 
	# sort the results
	results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)