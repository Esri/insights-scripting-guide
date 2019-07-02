## Slice and dice geographic data

**Review top and bottom items in your data**

Suppose you need to put together a few crude lists showing the top and bottom 25 places.  Let's say the task is related to total human population in zip codes.  Here's what you could do using python and r scripting in ArcGIS for Insights.

1) Open Insights for ArcGIS

2) Create a new Workbook

3) Click add and select Living Atlas and search for USA Zip Code Points

4) Add USA Zip Code Points to the Workbook

5) Open a new Script Console Window and choose Python

6) Now using the console create a variable named ```df = ``` and drag the Zip code layer dropping it to the right of the equal sign


	``` df = <ZipCode Layer - All Fields> ```

7) Next examine how the dataframe looks


	``` df.head() ```

8) Note there may be some unrealistic population values, such a population less than zero.  Let's clean that up.

	``` clean_df = df[df['POPULATION'] > 0] ```

9) Now find the top 25 zip codes with the largest population

	``` clean_df.nlargest(25, 'POPULATION') ```

10) Now find the bottom 25 zip codes with the smallest population

	``` clean_df.nsmallest(25, 'POPULATION') ```


 > PRO TIP:  To convert the data frame into an Insights dataset, press  ``` Ctrl/control + Alt/option + B ``` in a new cell.  When the Insights magic command appears type the name of the data frame inside the parentheses and press ```Shift + Enter```.
