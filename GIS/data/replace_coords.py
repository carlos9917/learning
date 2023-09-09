# replace values of sogne polygon with utm coordinates
# https://stackoverflow.com/questions/55178112/update-values-in-geojson-file-in-python

import json
from pyproj import Transformer
from pprint import pprint
import sys
ifile="sogne.geojson"
with open(ifile, 'r') as f:
    data = json.load(f)

#this will make it look more readable
#with open("sogne_copy.json", 'w') as f:
#    json.dump(data, f, indent=2)
#sys.exit(0)
def latlon2utm(lat,lon):
    transformer=Transformer.from_crs(4258,25832,always_xy=True)
    for pt in transformer.itransform([(float(lon),float(lat))]):
        res='{:.6f} {:.6f}'.format(*pt)
    east,north=res.split()
    return east,north
for feature in data['features']:
    #if feature['geometry']['type'] == 'Polygon':
    coords = feature['geometry']['coordinates'][0]
    new_coords=[];
    for row in coords:
        #pprint(row)
        lon = row[0]
        lat = row[1] 
        z = row[2]
        e,n = latlon2utm(lat,lon)
        new_coords.append([float(n),float(e),z])
    #feature['geometry']['coordinates'][0].append(new_coords)
    feature['geometry']['coordinates'][0] = new_coords
    #if (feature['geometry']['type'] == 'LineString') & (len(feature['geometry']['coordinates']) >= 3):
    #    feature['geometry']['type'] = 'Polygon'
    #    feature['geometry']['coordinates'].append(feature['geometry']['coordinates'][0])
with open("sogne_utm.geojson", 'w') as f:
    json.dump(data, f, indent=2)
