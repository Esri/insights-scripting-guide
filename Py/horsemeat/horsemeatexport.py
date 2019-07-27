# import pandas
import pandas as pd

# Read horsemeat csv into a dataframe
df = pd.read_csv("Horsemeat Simple.csv")

# Create dataframe of exporter country with lat and lon
geo = df.loc[:, ["Country", "Lat", "Lon"]].rename(columns={"Lat": "Exporter_Lat",
                                                           "Lon": "Exporter_Lon"})

# Drop Received and Exported columns
df = df.drop(["Received", "Exported"], axis=1)

# Get columns for multi-index
idx = [col for col in df.columns if col in ("Country", "Lat", "Lon")]

# Set index to multi-index
m_df = df.set_index(idx)

# Stack dataframe columns and drop NAs if present
s_df = m_df.stack(dropna=True)

# Reset index to original to remove multi-index
l_df = s_df.reset_index()

# Rename columns for Exporter_Country and Amount
hm_df = l_df.rename(columns={"level_3": "Exporter_Country", 0: "Amount"})

# Remove all rows with zero amounts
hm_non_zero = hm_df[(hm_df != 0).all(1)]

# Join Exporter_Lat and Exporter_Lon
hm_export_df = hm_non_zero.join(geo.set_index("Country"), on="Exporter_Country")

# Display horse meat dataframe with Countries and Exporter Countries
hm_export_df

# Bring horsemeat data into Insights
%insights_return(hm_export_df)