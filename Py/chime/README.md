# Insights CHIME Script v4


The script allows for an entire states counties to be processed in one go.  Alternatively, there is a commented out section that can be used to process many states to the county level.  In the former case, only county name is required for an individual state, in the latter case, both state name and county name fields will be required.

If you don't have ArcGIS Insights, you can download Insights Desktop [here](https://www.esri.com/en-us/arcgis/products/arcgis-insights/resources/desktop-client-download).
 
1. Open Insights and create a new workbook
2. Click the _Add_ button and upload the Florida shapefile
3. Rename the uploaded dataset to FloridaCHIME
4. Open the scripting console and make a Jupyter Kernel Gateway connection
5. Import _CHIME.ipynb_ into the scripting console
6. Using the data in the FloridaCHIME drag and drop attributes below into the second cell (setting the variable named __florida_df__)
    1. Attributes: countyname, unacast_ch, hospitaliz, population, hospital_1
    2. Code before change: florida_df = #... ( DnD in front of the # sign)
    3. Code after change:  florida_df = FloridaCHIME ( 5 Fields)
7. Once step 5 is complete, run cell 1 and 2 to completion
8. Next execute cell 3
    1. This cell uses the magic command to load the merged dataset into Insights, ie ``` %insights_return(county_run_df) ```
9. After cell 3 executes a new layer will be added to the data pane, named "Layer".  Rename _Layer_ to _Florida_.
10. Next enable location on _Florida_, by clicking the ellipse and selecting _Enable Location_.  With the enable location dialog open, select the FloridaCHIME and choose the __CountyName__ field to match. 
11. Next drag and drop CHIME data fields from the datasets in the data pane to create interactive maps, charts, and tables

 
__Result image__

![Insights Scripting w/ CHIME ](screenshot.png)