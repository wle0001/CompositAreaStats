# CompositAreaStats
Composites data from Google Earth Engine (GEE) and provides areas statistics:

Utilizes GEE to aggregate quarterly means of a dataset, downloads and runs zonal statistics for an input polygon.

No installation is required, the application can be run directly by executing the SeasonComposites.py script.

It is assumed that the Earth Engine Python API is installed and Earth Engine is authorized as described [here](https://developers.google.com/earth-engine/python_install) via a docker container or [here](https://developers.google.com/earth-engine/python_install_manual) manually.

To run the script these modules need to be installed:
pandas, numpy, rasterstats, urllib2, os, glob

Hard code the following variables:

tifDir >  where you want to store the downloaded seasonal composites from GEE.

shp > set to the shapefile that your area statistics are based on .. the zones for your zonal statistics.

gridCodes > set to the HucGrids.csv file.

**The bounding box needs to extend beyond the shapefile boundaries.**
