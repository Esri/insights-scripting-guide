"""
Copyright 2019 Esri

Licensed under the Apache License, Version 2.0 (the "License");

you may not use this file except in compliance with the License.

You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software

distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and

limitations under the License.​
"""


import csv
import pandas

country = []
exporter = []
recieved = []
lat = []
lng = []
exporterLat = []
exporterLng = []
geoDict = {}

def createFlatCSV():
    df = pandas.DataFrame(data={"Country": country,
                                "Amount": recieved,
                                "Lat": lat,
                                "Lng": lng,
                                "Exporter": exporter,
                               "ExporterLat": exporterLat,
                               "ExporterFromLng": exporterLng})

    df.to_csv("Horsemeat Link Table.csv", sep=',',index=False)
    return df


with open('Countries.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_num = 0
    for row in csv_reader:
        if(row_num != 0):
            geoDict.update({row[0]:{'lat':row[1], 'lng':row[2]}})
        row_num += 1


with open('Horsemeat Simple.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_num = 0
    header = []
    for row in csv_reader:
        j = 0
        if row_num == 0:
            header = row
            row_num += 1
        else:
            for j in range(43):
                if j >= 3:
                    country.append(row[0])
                    exporter.append(header[j])
                    recieved.append(row[j])
                    lat.append(row[43])
                    lng.append(row[44])
                    exporterLat.append(geoDict[header[j]]['lat'])
                    exporterLng.append(geoDict[header[j]]['lng'])
                j = j + 1
        row_num += 1
    df = createFlatCSV()

print(f'Processed {row_num} lines.')
print(df)
