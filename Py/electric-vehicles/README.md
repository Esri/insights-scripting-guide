## Explore Electric Vehicle Charging Stations

**Scrub nested JSON to desired format**

Data included in this sample contains automobile charging stations, expressed as JSON. While the original authors intended the data for https://openchargemap.org, it's useful to know how to scrub and clean data for use in other systems such as Insights for ArcGIS.

This sample contains two scripts and sample data.  To run the example, please know that the JSON data needs to be accessible to your Jupyter Kernel Gateway scripting environment.  Check out the _Pro Tip_ at the end of this page for making data accessible. 

The first script _pretty prints_ JSON to the console, revealing the nested nature of the data.  To the nested objects, look at each AddressInfo envelope. 


```
import json
import pprint

with open('ev_stations.json', 'r') as f:
    data = f.read()
    json_data = json.loads(data)

pprint.pprint(json_data)

```


The second script flattens the data and removes nested JSON elements.  It also simplifies the data removing unneeded fields.  Lastly, it converts the cleaned data into a panda data frame.

```

import pandas as pd

cleaned = []

with open('ev_stations.json') as file:
  data = json.load(file)
  
for d in data:
  cleaned.append({'ID': d['ID'],
 'Lat': d['AddressInfo']['Latitude'],
 'Lon': d['AddressInfo']['Longitude'],
 'Title': d['AddressInfo']['Title']})

ev_stations = pd.DataFrame.from_dict(cleaned, orient='columns')
ev_stations


 ```

  > PRO TIP:  To make file based data accessible to your Insights scripting environment move flat files into the directory where the Jupyter Kernel Gateway is running.  Than with Python or R data can be accessed using relative paths names.



 > PRO TIP:  To convert the data frame into an Insights dataset press  ``` Ctrl/control + Alt/option + B ``` in a new cell.  When the Insights magic command appears type the name of the data frame inside the parentheses and press ```Shift + Enter```.
