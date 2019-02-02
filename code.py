#Import Required Libraries
from osgeo import gdal
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt
from numpy.random import randn
#Function Definition for NDVI calculation 
def calculate_NDVI(NewWorkingDir,RedBandImage,NIRBandImage):
    print '\nCurrent Working Directory: ', NewWorkingDir
    print 'Red Band Image: ', RedBandImage
    print 'NIR Band Image: ', NIRBandImage
    #Set Current Working Directory
    os.chdir(NewWorkingDir)
    #Read Red Band Image
    g = gdal.Open(RedBandImage)
    red = g.ReadAsArray()
    #Read NIR Band Image
    g = gdal.Open(NIRBandImage)
    nir = g.ReadAsArray()
    #Set datatype to float
    red = array(red, dtype = float)
    nir = array(nir, dtype = float)
    #Check condition
    check = np.logical_and ( red > 1, nir > 1 )
    #NDVI calculation formula
    ndvi = np.where ( check,  (nir - red ) / ( nir + red ), -999 )

    #NDVI result
    print "\n The NDVI values are as follows: \n",ndvi
    #Get transformation coefficients
    geo = g.GetGeoTransform()
    #Get image projection information
    proj = g.GetProjection()
    #Image size
    shape = red.shape
    #Get GDAL Driver 
    driver = gdal.GetDriverByName("GTiff")
    #Create the output NDVI image
    dst_ds = driver.Create( "ndvi.tif", shape[1], shape[0], 1, gdal.GDT_Float32)
    #Set the transformation coefficients of output image same as input images
    dst_ds.SetGeoTransform( geo )
    #Set the projection of output image same as input images
    dst_ds.SetProjection( proj )
    dst_ds.GetRasterBand(1).WriteArray(ndvi)
    #Get No of Pixels
    cols=dst_ds.RasterXSize
    rows=dst_ds.RasterYSize
    Pixels = cols*rows
    dst_ds = None

    print "\n NDVI saved in the respective folder"
    countHV = countV = countS = countW = countO = 0
    healthy_veg = []
    veg = []
    soil = []
    water = []
    others = []
    #Classification of various features based on NDVI values
    for i in range(ndvi.shape[1]):
       for j in range(ndvi.shape[0]):
           if ndvi[i,j] > 0.6:
               healthy_veg.append(ndvi[i,j])
               ndvi[i,j] = 1
               countHV = countHV + 1
           elif (ndvi[i,j] > 0.2 and ndvi[i,j] < 0.6):
               veg.append(ndvi[i,j])
               ndvi[i,j] = 2
               countV = countV + 1
           elif (ndvi[i,j]> 0.1 and ndvi[i,j] < 0.2):
               soil.append(ndvi[i,j])
               ndvi[i,j]=3
               countS = countS + 1
           elif (ndvi[i,j]>(-0.2) and ndvi[i,j] < 0.1):
               water.append(ndvi[i,j])
               ndvi[i,j]=4
               countW = countW + 1
           else:
               others.append(ndvi[i,j])
               ndvi[i,j]=5
               countO = countO + 1

    #Saving Classified results as New GeoTiff image
    dst_ds_classifiedImage = driver.Create( "ndviClassified.tif", shape[1], shape[0], 1, gdal.GDT_Float32)
    dst_ds_classifiedImage.SetGeoTransform( geo )
    dst_ds_classifiedImage.SetProjection( proj )
    dst_ds_classifiedImage.GetRasterBand(1).WriteArray(ndvi)
    dst_ds_classifiedImage = None
    print "\n Classified Image saved in the respective folder"
    
    #Number of pixels in image for each feature class           
    print "\nNo. of Healthy Vegetation Pixels in image = ", countHV
    print "No. of Vegetation Pixels in image = ", countV
    print "No. of Soil Pixels in image = ", countS
    print "No. of Water Pixels in image = ", countW
    print "No. of Other Pixels in image = ", countO
    print "\n After classifying into 5 different classes: \n ",ndvi

    
    # % calculation for Feature Cover
    
    l = (countHV/float(Pixels))*100
    print "% of Healthy Veg cover= ",l
    
    m = (countV/float(Pixels))*100
    print "% of Vegetation cover= ",m
    
    n = (countS/float(Pixels))*100
    print "% of Soil cover= ",n
    
    u = (countW/float(Pixels))*100
    print "% of Water cover= ",u

    v = (countO/float(Pixels))*100
    print "% of Other cover= ",v
    
    
    global HV
    global V
    global S
    global W
    global O
    #Storing count of each feature class in separate lists
    HV.append(l)
    V.append(m)
    S.append(n)
    W.append(u)
    O.append(v)
    #Plots
    x = ['1.Healthy_veg', '2.Veg', '3.Soil', '4.Water','5.Others']
##    y = [countHV,countV,countS,countW,countO]
##    plt.plot(x,y)
##    plt.title('Frequency Distribution of all Classes for '+ NewWorkingDir[-7:])
##    plt.xlabel("Classification")
##    plt.ylabel("Frequency")
##    plt.show()

    Percentage = (l,m,n,u,v)
    plt.bar(x,Percentage)
    plt.title('Percentage Distribution of all Classes for '+ NewWorkingDir[-7:])
    plt.xlabel("Classification")
    plt.ylabel("Percentage")
    plt.show()
    
    fig, ax = plt.subplots()
    cax = ax.imshow(ndvi, interpolation='nearest', cmap='RdYlGn_r')
    cbar = fig.colorbar(cax, ticks=[1,2,3,4,5])
    cbar.ax.set_yticklabels(['HealthyVeg', 'Veg', 'Soil', 'Water', 'Others'])
    plt.title('NDVI Image for '+ NewWorkingDir[-7:])
    plt.show()
    ##Function End

HV = []
V = []
S = []
W = []
O = []

#Initial parent working directory
WorkingDir = r'D:\SUMANA_module2\PSDII\Research_module_Project\Pune_Draught'
#Get list of folders inside the parent directory
FolderNames = os.listdir(WorkingDir)
print FolderNames
#Looping through each folder to get image files inside each folder
for folder in FolderNames:
    NewWorkingDir = WorkingDir+'\\'+folder
    FileNames = os.listdir(NewWorkingDir)
    print FileNames
    calculate_NDVI(NewWorkingDir,FileNames[1],FileNames[2])
##print 'Healthy Veg NDVI over years: ', HV
##print 'Veg NDVI over years: ', V
##print 'Soil NDVI over years: ', S
##print 'Water NDVI over years: ', W
    
#Temporal Curve plot for various features
plt.subplot(4,1,1)
plt.plot(FolderNames,HV)
plt.title("Percentage of Healthy Vegitation from 2008- 2016")
plt.ylim(0,100)
plt.subplot(4,1,2)
plt.plot(FolderNames,V)
plt.title("Percentage of Normal Vegitation from 2008- 2016")
plt.ylim(0,100)
plt.subplot(4,1,3)
plt.plot(FolderNames,S)
plt.ylim(0,100)
plt.title("Percentage of Soil from 2008- 2016")
plt.subplot(4,1,4)
plt.plot(FolderNames,W)
plt.ylim(0,100)
plt.title("Percentage of Water from 2008- 2016")
plt.tight_layout()
plt.show()


