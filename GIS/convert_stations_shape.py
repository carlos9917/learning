import pandas as pd
import fiona
pointDf = pd.read_csv("data/vejvejr_stations.csv")
pointDf.columns =["SID","name","lon","lat"]

# define schema
schema = {
    'geometry':'Point',
    'properties':[('Name','str')]
}
# explore available drivers
#fiona.supported_drivers
#print(df_ll)

#open a fiona object
pointShp = fiona.open('data/vejvejr_stations_ll.shp', mode='w', driver='ESRI Shapefile', schema = schema, crs = "EPSG:4326")
#iterate over each row in the dataframe and save record
for index, row in pointDf.iterrows():
    rowDict = {
        'geometry' : {'type':'Point',
                     'coordinates': (row.lon,row.lat)},
        'properties': {'Name' : row.SID},
    }
    pointShp.write(rowDict)
#close fiona object
pointShp.close()
