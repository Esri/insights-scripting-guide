# watershed-river-flow
This sample demonstrates the workflow for creating an ArcGIS Insights workbook from river flow (QR) monitoring data. This sample includes a brief walkthrough for creating a data assembly script to collate datasets downloaded in subsets.

The data collected for this exercise was downloaded from the [Grand River Conservation Authority (GRCA)](https://www.grandriver.ca/en/index.aspx) and their [monitoring datasets](https://data.grandriver.ca/downloads.html). This data is subject to their [Open Data License](https://data.grandriver.ca/docs/GRCA%20Open%20Data%20Licence%20v2.pdf).

## Requirements
To activate the ArcGIS Insights scripting environment, dig into this [annoucement](https://www.esri.com/arcgis-blog/products/insights/announcements/scripting-insights-arcgis/) and the associated [repo](https://github.com/Esri/insights-scripting-guide).

# Data Preparation
The purpose of this script is to collect and prepare the data required to conduct the analysis and author our workbook. The blog post walkthrough can be read [here](https://www.esri.com/arcgis-blog/products/insights/analytics/make-this-watershed-workbook-data-prep/).

The Jupyter Notebook that performs the data collation and prep is described below.

## Script Functions
1. The script processes a collection of River Flow `.csv` datasets downloaded to a local folder directory.
2. Transposes some of the metadata attributes from the file header into new columns.
3. Orders the fields.
4. Sets the column datatypes.
5. Sorts the dataframe.
6. Outputs the dataframe to the Insights datapane.
