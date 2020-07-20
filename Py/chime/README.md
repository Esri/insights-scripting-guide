# ArcGIS Insights CHIME Script

Penn Medicine’s Predictive Healthcare Team adapted the susceptible, infected, and recovered (SIR) mathematical model, to create a new model it calls CHIME (COVID-19 Hospital Impact Model for Epidemics). The CHIME model provides up-to-date estimates of how many people will need to be hospitalized, and of that number how many will need ICU beds and ventilators.

The model uses a number of input parameters such as population size, percentage of infections, doubling time of the infection and, additionally can include impacts of physical distancing measure such as stay-at-home directives.

This implementation, for ArcGIS Insights, allows for modelling of a single region, in which one value is required for these fields:

### Fields / Column Names

| FIELD NAME           | DESCRIPTION   |
| ---------------------|:-------------:|
| countyname      | County name        |
| unacast_ch      | Doubling time in days (Contact Rate)                 |
| hospitaliz      | Currently hospitalized COVID-19 patients                 |
| population      | Regional population         |
| hospital_1      | Hospital market share (%)                |


* Implementing physical distancing and start date is optional


This script can also be used to model multiple regions at once, for example, all counties in a state (see, cells 4 and 5).  

If you don't have ArcGIS Insights, you can download Insights Desktop [here](https://www.esri.com/en-us/arcgis/products/arcgis-insights/resources/desktop-client-download).  
 
1. Open Insights and create a new workbook
2. Use the __Add__ button to upload a CSV containing the required fields and data _(see table above)_
3. Rename the uploaded dataset using CHIME as a suffex, ie. DataSet_CHIME
4. Open the scripting console and make a Jupyter Kernel Gateway connection
5. Import _CHIME.ipynb_ into the scripting console
6. Using the data in the DataSet_CHIME select these fields _countyname, unacast_ch, hospitaliz, population, hospital_1_ from the data pane and drag them into the second cell, setting the variable named __chime_df__
7. Once step 5 is complete, run cell 1 and 2 to completion
8. Next execute cell 3
    1. This cell uses the magic command to load the merged dataset into Insights, ie ``` %insights_return(county_run_df) ```
9. After cell 3 executes a new layer will be added to the data pane, named "Layer".  Rename _Layer_ to _Chime Estimates_.
10. Optional - If your workbook includes a spatial layer containing county names _(ie. County_Name)_, enable location on _Chime Estimates_, by clicking the ellipse and selecting __Enable Location__.  With the enable location dialog open, select your spatial layer and choose the _County_Name_ field to match. 
11. Next to create interactive maps, charts, and tables follow the step-by-step instructions in this [blog post](https://www.esri.com/arcgis-blog/products/insights/analytics/use-chime-arcgis-insights/)


Please log an issue, if you need assistance using this script or would like to offer feedback on how to make this resource more useful for people working in the front lines of epidemics.

 
__Example workbook with CHIME Estimates__

![Insights Scripting w/ CHIME ](screenshot.png)