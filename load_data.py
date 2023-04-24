import pandas as pd


df=pd.read_excel("anime_ratings.xlsx") # Path of the file. 
df.to_pickle("data2.pkl")