import json  
import pandas as pd  
from pandas.io.json import json_normalize  


fileNamePath = ""

with open(fileNamePath) as f:
    d = json.load(f)
df_steam = []
for i in range(len(d)):
    df_1 = json_normalize(d[i])
    df_steam.append(df_1)
df = pd.concat(df_steam)
df.to_csv(r''+fileNamePath)