import datetime as dt
import pandas as pd
import os
from six.moves import urllib

year = "2019"

## Get the data from the web
path = "ca_snow_feb_{}.csv".format(year)
url = "https://s3-us-west-1.amazonaws.com/python-and-r/ca_snow_feb_{}.csv".format(year)
urllib.request.urlretrieve(url,path)

with open(path,'r') as f:
  text = f.readlines()[1:]
  text = ''.join([i for i in text])

## Write cleaned data to new CSV file
cleanedPath = "cln_{}".format(path)
with open(cleanedPath, "w+") as txtFile:
    print(text, file=txtFile)
    
df = pd.read_csv(cleanedPath, sep=',')

ndf = df.rename(index=str, columns={"GHCN ID": "GHCN_ID", "Station Name": "Station_Name"})
stations = ndf[['GHCN_ID','Station_Name', 'County', 'Elevation', 'Latitude', 'Longitude']]
stations

## Get yearly snowfall observations (find and replace, update columns and reshape the table)
import datetime as dt
import pandas as pd
import os
from six.moves import urllib

## Set year and state value
year = 2019

## Get the data from the web
path = "ca_snow_feb_{}.csv".format(year)
url = "https://s3-us-west-1.amazonaws.com/python-and-r/ca_snow_feb_{}.csv".format(year)
urllib.request.urlretrieve(url,path)

## Do find and replace on T and M values
with open(path,'r') as f:
  text = f.readlines()[1:]
  text = ''.join([i for i in text]).replace(",M", ",")
  text = ''.join([i for i in text]).replace(",T", ",")

## Write cleaned data to new CSV file
cleanedPath = "cln_{}".format(path)
with open(cleanedPath, "w+") as txtFile:
    print(text, file=txtFile)

## Read CSV file into a dataframe
df = pd.read_csv(cleanedPath, sep=',')

## Start reshaping the dataframe, begin by gathering the columns we want to use 
newCols = []
existingCols = df.columns.values.tolist()
for i in range (df.columns.size):
  if i < 6:
    if df.columns[i] == "Station Name":
      newCols.append("Station_Name")
newCols.append("Snowfall")
newCols.append("Date")

## Create a table with each observation and put it in it's own row
table = []
cols = df.columns.values.tolist()
for index, series in df.iterrows():
  attributes = []
  for idx, column in enumerate(df.columns):
    if idx < 6:
      if column == "Station Name":
        attributes.append(series[idx])
    if idx >= 6:
      date = dt.datetime.strptime("{}, {}".format(cols[idx], year),'%b %d, %Y')
      date = "{}/{}/{}".format(date.month, date.day, date.year)
      value = series[idx]
      row = attributes + [value, date]
      table.append(row)

## Now create the final reshaped table
df = pd.DataFrame(table, columns=newCols)

# Save table out as CSV
snow = os.path.join(os.getcwd(), "snow")
if not os.path.exists(snow):
    os.mkdir(snow)
filename = "final_{}".format(path)
path = os.path.join(os.getcwd(), "snow", filename)
df.to_csv(path, sep=',', encoding='utf-8')
df

## Merge all the data together (so we have 3 years of observations)
all_files = list(glob.glob('./snow/*.csv'))
df_list = []
for csv_file in all_files:
    df = pd.read_csv(csv_file)
    df_list.append(df)
concat_df = pd.concat(df_list, ignore_index=True, sort=False)
concat_csv = concat_df.to_csv('./snowall.csv', index=False)
outdf = pd.read_csv('./snowall.csv')
observations = outdf[['Station_Name','Snowfall', 'Date']]
observations

## Next load the data into Insights to do further analysis
%insights_return(observations)

## Once in Insights you can convert the latitude and longitude values to geometry values (that are map ready) using enable location.
