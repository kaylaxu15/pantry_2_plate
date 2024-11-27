import pandas as pd
import ast
import re

# function to extact the servings from the serves column
def total_time(row):
    prep_time = row['prep_time']
    cook_time = row['cook_time']

    
    # Convert to string and handle NaN values
    prep_time = str(prep_time) if not pd.isna(prep_time) else ""
    cook_time = str(cook_time) if not pd.isna(cook_time) else ""
    
    index = prep_time.rfind("Total time") + len("Total time")
    if index != -1: 
        return prep_time[index + len("Total time"):]
    
    if cook_time == "":
        cook_time = 0
    elif 'h' in cook_time:
        cook_time = int(cook_time.split(' ')[0][5:]) * 60
    elif 'm' in cook_time:
        cook_time = int(cook_time.split(' ')[0][5:])
        
    if prep_time == "":
        prep_time = 0
    elif 'h' in prep_time:
        prep_time = int(prep_time.split(' ')[0][5:]) * 60
    elif 'm' in prep_time:
        prep_time = int(prep_time.split(' ')[0][5:])
    print("PREP", prep_time)
    print(prep_time + cook_time)
    return prep_time + cook_time

df = pd.read_csv('webscraping/output/2024-11-27_final_recipes_servings_data.csv')
df['total_time'] = df.apply(total_time, axis=1)
df.to_csv('webscraping/output/2024-11-27_final_recipes_servings_data.csv', index=False)