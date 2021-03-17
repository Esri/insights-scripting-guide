from libpysal.weights import Queen
from esda.moran import Moran

'''Make sure to replace the string by drag and dropping your data into line 5 before you run the script'''
gdf = "REPLACEWITHYOURFILE"
gdf.rename(columns = {"shape":"geometry"} , inplace = True)
gdf = gdf.dropna() #drop polys with no income data

'''Contiguity weights matrices define spatial connections through the existence of common boundaries. 
According to the queen method, two polygons need to share a point or more to be considered neighbors'''
w_queen = Queen.from_dataframe(gdf)
w_queen.transform = 'R'

'''Morans I is a number that will tell us if there is a spatial pattern or not. 
Closer to 1 indicates positive or -1 indicates negative relationship. 0 indicates random. Return results to dataframe'''
mi = Moran(gdf['b19013_001e'], w_queen)
result = pd.DataFrame([["Moran's I", mi.I],["P-value", mi.p_sim]], columns = ["Value", "Name"])

%insights_return(result)