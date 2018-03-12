#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
#********************************************************
FILE: SeasonComposites.py
AUTHOR: wellenbu
EMAIL: wle0001@uah.edu
MODIFIED BY: rlucey
EMAIL: rml0018@uah.edu
ORGANIZATION: SERVIR
CREATION DATE: 02/08/2018
LAST MOD DATE: 03/12/2018
PURPOSE: Utilizes GEE to aggragate quaterly means of a dataset, downloads and runs zonal statistics for an input polygon
DEPENDENCIES: pandas, numpy, rasterstats, urllib2, os, glob
NOTES: Earth Engine API must be installed and Google Earth Engine must be authorized
#********************************************************
"""

#import packages
import ee
import pandas as pd
import numpy as np
from rasterstats import zonal_stats
import urllib2
import os
import glob

#initialize the google earth engine python API
ee.Initialize()

#output directory
tifDir = '/Users/wellenbu/Documents/UAH/SPARROW/qtifs/'
#set to the HucGrids.csv file - which is a list of the grid IDs
gridCode = pd.read_csv(tifDir[:-6]+'HucGrids.csv')
#set to the zones for your zonal stats
shp = tifDir[:-6]+'USGSdata/Catchments_NHDPlusv2_Hydroregion03/Catchment_03NSW.shp'

# Define Date Variables 
startyear = 2001
endyear = 2017
startmonth = 1
endmonth = 12

# Get GEE date format
startdate = ee.Date.fromYMD(startyear,startmonth,1)
enddate = ee.Date.fromYMD(endyear,endmonth,31)


#Bounding Box for general SE domain
coords = [[-89.48,37.80], [-74.81,37.80], [-75.30,34.88], [-81.08,31.36],\
          [-79.23,24.94],[-82.59,24.94],[-84.67,28.46],[-89.30,28.49]]

bounds = ee.Geometry.Polygon(coords)

# Get EVI Collection filter for date and area
EVI = ee.ImageCollection('MODIS/MCD43A4_EVI')\
    .filter(ee.Filter.date(startdate, enddate))\
    .sort('system:time_start', False)\
    .filterBounds(bounds)

# Create DFs for each stat
meanDF = gridCode
minDF = gridCode
maxDF = gridCode
stdDF = gridCode


# Loop through year and quarter(JFM, AMJ, JAS, OND)
# quarter loop: [start month, end month, quarter]
for i in range(startyear,endyear+1):
    for q in [[1,3,1],[4,6,2],[7,9,3],[10,12,4]]:
        # name dir + q#_YEAR
        name = tifDir+'q'+str(q[2])+'_'+str(i)
        t1 = ee.Date.fromYMD(i,1,1)
        t2 = ee.Date.fromYMD(i,12,31)
        # Mean arcoss given quarter
        out = EVI.filterDate(t1,t2)\
            .filter(ee.Filter.calendarRange(q[0], q[1], 'month'))\
            .mean().rename('q'+str(q[2])+'_'+str(i))
        
        # Get download URL
        path = out.getDownloadUrl({
        'scale': 1000,
        'crs': 'EPSG:4326',
        'region': coords})
        
        # Read url and write as .zip
        html = urllib2.urlopen(path).read()
        
        File = open(name+'.zip', 'wb')
            
        File.write(html)
        File.close()
        
        print name
        # Open zip and rename .tif and .tfw
        os.system('unzip '+name+'.zip'+' -d '+tifDir)
        os.rename(glob.glob(tifDir+'*q'+str(q[2])+'_'+str(i)+'.tif')[0], name+'.tif')
        os.rename(glob.glob(tifDir+'*q'+str(q[2])+'_'+str(i)+'.tfw')[0], name+'.tfw')
        
        # Compute zonal stats base on provided polygon file (.shp)
        
        ras = name+'.tif'
        stats = zonal_stats(shp, ras, stats=['mean','min', 'max', 'std'],all_touched = True)
        
        # convert dict to DF and save as csv
        a = pd.DataFrame.from_dict(stats)
        # Add GridCodes
        a['GridCode'] = gridCode.iloc[:,0]
        #Rearrange Columns
        a = a[['GridCode','mean','min','max','std']]
        
        #saving single q file
        a.to_csv(name+'_EVI.csv')
        
        #Populated stat files 
        meanDF[name[-7:]] = a['mean']
        minDF[name[-7:]] = a['min']
        maxDF[name[-7:]] = a['max']
        stdDF[name[-7:]] = a['std']
        
        #sys.exit()

# save out total stat files
meanDF.to_csv(name+'_meanEVI.csv')  
minDF.to_csv(name+'_minEVI.csv')  
maxDF.to_csv(name+'_maxEVI.csv')  
stdDF.to_csv(name+'_stdEVI.csv')    
        
 
