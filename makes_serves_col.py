import pandas as pd
import numpy as np
import ast
import re

def makes_column(string):
    ret = None
    if string is np.nan:
        return ret
    if 'makes' in string.lower():
        
    string = string.split()
    for element in string:
        if element == "Serves":
            key = 'serves'
            
        elif element == "Makes":
            key = 'makes'
            
        else:
            try:
                int(element)
                dict[key] = element
                return dict
            except:
                pass
        
    return dict

def serves_column(string):


df = pd.read_csv('/Users/chaeyounglee/Desktop/Fall 2024/COS 333/princeton_plate_planner/webscraping/output/final_recipes_data_2024-11-01.csv')
df['serves_dict'] = df['serves'].apply(servings_to_dict)
df.to_csv('/Users/chaeyounglee/Desktop/Fall 2024/COS 333/princeton_plate_planner/webscraping/output/final_recipes_servings_data_2024-11-01.csv', index=False)