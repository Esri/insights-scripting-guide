# A primer for Python Scripting in ArcGIS Insights (Part 1)
This repository contains the Python code samples used in the ESRI blog *A primer for Python Scripting in ArcGIS Insights*.

## To work with the scripts, you will also need:
- [Census API Key](https://www.census.gov/data/developers/guidance/api-user-guide.html)
- Kernel gateway to an environment that has the required Python3 dependencies installed (Documentation on how to setup a Kernel gateway [here]((https://github.com/Esri/insights-scripting-guide)) and list of dependencies [here](environment.yml))
- Zipped, cleaned census tract shapefile from this repo (Data sourced from [Census.gov](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html))
- Working knowledge of Python, and the Python libraries Pandas and Geopandas

## Repository content
    -`rest_api.py`
    
    -`config.py` (replace the key with your personal API key)
    -`census_tracts_poly.zip` Cleaned census tract shapefile
    -`morans_i.py`
    -`environment.yml`
