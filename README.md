# CompositAreaStats
Composites data from GEE and provides areas statistics:

Utilizes GEE to aggragate quaterly means of a dataset, dowloads and
runs zonal statistics for an input polygon.

No installtion is required, the application can be run directly by executing SeaonComposites.py script.

It is assumed Earth Engine Python API is installed and EE authorised as desribed [here](https://developers.google.com/earth-engine/python_install) via a docker container or [here](https://developers.google.com/earth-engine/python_install_manual) mannually.

To run the script these modules need to be installed:
pandas, numpy, rasterstats, urllib2, os, glob

Hard code the following varaibles:

tifDir >  where you want to store the downloaded seaonal composites from GEE

shp > set to the shapefile that your area stats are based on .. the zone of your zonal stats

gridCodes > set to the HucGrids.csv file

**The bounding box needs to extend beyond the shapefile boundaries.**
