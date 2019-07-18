import os
import datetime as dt
import pandas as pd
import numpy as np

# Download all years of snowfall data into a dictionary of dataframes
dfs_dict = {}
# URL to the snowfall data
url = "https://s3-us-west-1.amazonaws.com/python-and-r/ca_snow_feb_{}.csv"
# Years of interest
years = ["2017", "2018", "2019"]
# Get snowfall csv files for all years
csv_files = [url.format(year) for year in years]
# Build names for the dataframes for all the years
dfs = ["{}_{}".format("df", year) for year in years]

# List to hold the new column names
column_rename = {"GHCN ID": "GHCN_ID", "Station Name": "Station_Name"}

# Build the dict of dataframes for each year of interest
for df, file in zip(dfs, csv_files):
    # Read csv snowfall data into dataframe; skip first row containg title and description
    dfs_dict[df] = pd.read_csv(file, skiprows=1).rename(index=str, columns=column_rename)
    # Handle the date fields for later melting into dataframe rows
    dfs_dict[df].columns = ["{} {}".format(col, "".join(df.split("_")[1])) if col.startswith("Feb")
                            else col for col in dfs_dict[df].columns]
    # Replace "T" and "M" values with NaNs
    dfs_dict[df] = dfs_dict[df].replace("T", np.nan)
    dfs_dict[df] = dfs_dict[df].replace("M", np.nan)

# Concatenate all the year dataframes into one
snow_df = pd.concat([v for k, v in dfs_dict.items()], ignore_index=True, sort=False)

# Collect the id variable columns for the melt of dates to rows
id_vars = [col for col in snow_df.columns if not col.startswith("Feb")]
# Collect the date variables for the melt of dates to rows
date_vars = [col for col in snow_df.columns if col.startswith("Feb")]

# Create new dataframe with the dates to rows; Create Date and Snowfall columns
# and populate the corresponding values
new_snow_df = snow_df.melt(id_vars=id_vars, value_vars=date_vars, var_name="Date", value_name="Snowfall")

# Set Date column to datetime and do intitial format
new_snow_df["Date"] =  pd.to_datetime(new_snow_df["Date"], format="%b %d %Y")

# Final format of date values
new_snow_df["Date"] = new_snow_df["Date"].dt.strftime("%m/%d/%Y")

# Get columns of interest for final snowfall dataframe
final_columns = ["Station_Name", "Snowfall", "Date"]

# Create final snowfall dataframe with new columns of interest
final_snow_df = new_snow_df[final_columns].copy()

# View final snowfall dataframe 
final_snow_df

# Bring snowfall data into Insights
%insights_return(final_snow_df)


# Once in Insights you can convert the latitude and longitude values to geometry values (that are map ready) using enable location. 
