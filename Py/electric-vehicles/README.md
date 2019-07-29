## Explore Electric Vehicle Charging Stations

**Scrub nested JSON to desired format**

Data included in this sample contains automobile charging stations in JSON. While the original authors intended the data for https://openchargemap.org, it's useful to know how to scrub and clean data for use in other systems such as Insights for ArcGIS.

This sample contains two scripts and sample data. The first script _pretty prints_ JSON to the console to show the nested data.   

```
import json
import pprint

with open("https://raw.githubusercontent.com/Esri/insights-scripting-guide/master/Py/electric-vehicles/ev_stations.json", 'r') as f:
    data = f.read()
    json_data = json.loads(data)

pprint.pprint(json_data)

```


The second script flattens, manipulates, and simplifies the data in the nested JSON. It then converts the cleaned data into a panda data frame.

```
import urllib.request
import pandas as pd
 
with urllib.request.urlopen("https://raw.githubusercontent.com/Esri/insights-scripting-guide/master/Py/electric-vehicles/ev_stations.json") as url:
    data = url.read()
column_filter = ["ID", "Title", "Latitude", "Longitude"]
column_rename = {"Latitude": "Lat", "Longitude": "Lon"}
df = pd.read_json(data, orient="records")
ev_stations = pd.DataFrame.from_dict(elem for elem in df["AddressInfo"]).filter(items=column_filter).rename(index=str, columns=column_rename)
%insights_return(ev_stations)

 ```

 > To convert the data frame into an Insights dataset press ``` Ctrl/control + Alt/option + B ``` in a new cell. When the Insights magic command appears type the name of the data frame inside the parentheses and press ```Shift + Enter```.
