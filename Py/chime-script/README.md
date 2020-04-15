# Insights CHIME Script v4


The Script allows for an entire states counties to be processed in one go.  Alternatively, there is a commented out section that can be used to process many states to the county level.  In the former case, only county name is required for an individual state, in the latter case, both state name and county name fields will be required.
 
1. Open Insights
2. Import the Florida Shape File (attached zip file)
3. Open the scripting console, connect to your Kernels
4. Import the CHIME (file contained in the compressed folder attached)
5. Using the data in the Florida Shape file DnD the following attributes to the first cell Line #495 before the comment
    1. Attributes: countyname, unacast_ch, hospitaliz, population, hospital_1
    2. Code before change: florida_df = #... ( DnD in front of the # sign)
    3. Code after change:  florida_df = FloridaCHIME ( 5 Fields)
6. Once step 5 is complete, run cell 1.  Wait for it to complete
7. Once cell 1 is complete running, execute cell 2
    1. This cell uses the magic command to load the merged dataset into Insights
8. Rename the “Layer” dataset that was added using the magic command to something relevant to your work
9. To add location to this field, you can enable location using the overflow menu on the newly added dataset and select geography, Select the FloridaCHIME Shape File added to Insights and the “CountyName field to match
Alternatively, you can use the “Create Relationship” feature to join the two datasets
10. Using the Geo-Enabled CHIME output, you can now have full interactivity between maps, charts, and tables against any of the supported types from the CHIME model
 
An image of the finished product: