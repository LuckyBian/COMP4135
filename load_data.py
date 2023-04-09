import pandas as pd

df=pd.read_excel("data.xlsx") # Path of the file. 
df.to_pickle("data.pkl")