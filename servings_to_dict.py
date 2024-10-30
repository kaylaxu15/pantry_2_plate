import pandas as pd
import ast
import re

# function to extact the servings from the serves column
def servings_to_dict(string):
    dict = {}
    if "ml" in string or "g" in string:
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

df = pd.read_csv('/Users/alineutetiwabo/Desktop/Fall 2024/COS333/princeton_plate_planner/webscraping/output/recipes_data_2024-10-22.csv')
df['serves_dict'] = df['serves'].apply(servings_to_dict)
df.to_csv('/Users/alineutetiwabo/Desktop/Fall 2024/COS333/princeton_plate_planner/webscraping/output/processedservings_recipes_data_2024-10-30.csv', index=False)