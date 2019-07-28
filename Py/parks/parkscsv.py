"""
Copyright 2019 Esri

Licensed under the Apache License, Version 2.0 (the "License");

you may not use this file except in compliance with the License.

You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software

distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and

limitations under the License.​
"""


%matplotlib inline
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parks = pd.read_csv("parks.csv")

x = parks["Year"]
y = np.vstack([parks["Badlands"], parks["GrandCanyon"], parks["BryceCanyon"]])
labels = ["Badlands", "GrandCanyon", "BryceCanyon"]
colors = ["green", "red", "blue"]
plt.stackplot(x, y, labels=labels, colors=colors, edgecolor="black")
plt.legend(loc=2)

plt.show()

# create a card from the visualization by highlighting the output cell and
# clicking the create card button on the console