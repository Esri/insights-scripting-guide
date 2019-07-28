%matplotlib inline
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parks = pd.read_csv("https://raw.githubusercontent.com/Esri/insights-scripting-guide/master/Py/parks/parks.csv")

x = parks["Year"]
y = np.vstack([parks["Badlands"], parks["GrandCanyon"], parks["BryceCanyon"]])
labels = ["Badlands", "GrandCanyon", "BryceCanyon"]
colors = ["green", "red", "blue"]
plt.stackplot(x, y, labels=labels, colors=colors, edgecolor="black")
plt.legend(loc=2)

plt.show()
