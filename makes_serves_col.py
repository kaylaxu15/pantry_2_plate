import pandas as pd
import numpy as np

def makes_column(string):
    if string is np.nan:
        return None
    if 'makes' in string.lower():
        string = string.replace('Makes', '')
        string = string.strip()
        return string
    return None

def serves_column(string):
    if string is np.nan:
        return None
    if 'serves' in string.lower():
        string = string.replace('Serves', '')
        string = string.strip()
        return string
    return None

df = pd.read_csv('webscraping/output/final_recipes_servings_data_2024-11-11.csv')
df['makes'] = df['serves'].apply(makes_column)
df['servings'] = df['serves'].apply(serves_column) 
df.to_csv('webscraping/output/final_recipes_servings_data_2024-11-27.csv', index=False)