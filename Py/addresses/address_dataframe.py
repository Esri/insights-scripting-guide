    import pandas as pd
    import numpy as np

    df = pd.DataFrame(np.array([
    ["1001 19th St North", "Arlington", "VA", "Esri R&D"],
    ["380 New York St", "Redlands", "CA", "Esri Headquarters"],
    ["920 SW #rd Avenue", "Portland", "OR", "Esri R&D"],
    ["75 Broad St", "New York City", "NY", "Esri Regional Office"]
    ]), columns=["Address", "City", "State", "Office"])
                  
    df