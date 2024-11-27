import pandas as pd
import numpy as np
import ast
import re

# function to extact the servings from the serves column
def servings_to_dict(string):
    dict = {}
    print(string)
    if string is np.nan:
        return dict 
    if ("ml" in string) or ("g" in string):
        return dict
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

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv')
df['serves_dict'] = df['serves'].apply(servings_to_dict)
df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv', index=False)