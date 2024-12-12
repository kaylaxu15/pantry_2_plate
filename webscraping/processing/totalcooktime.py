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
    
    # index = prep_time.rfind("Total time")
    # if index != -1: 
    #     return prep_time[index + len("Total time"):]
    
    if cook_time == "":
        cook_time = 0
    elif 'h' in cook_time:
        components = cook_time.split(' ')
        cook_time = int(components[0][5:]) * 60
        if len(components) > 2:
            cook_time += int(components[3])
            print(row['title'])
            print("COOK", cook_time)
        
    elif 'm' in cook_time:
        cook_time = int(cook_time.split(' ')[0][5:])
        
    if prep_time == "":
        prep_time = 0
    elif 'h' in prep_time:
        prep_comp = prep_time.split(' ')
        prep_time = int(prep_comp[0][5:]) * 60
        if len(prep_comp) > 2:
            prep_time += int(prep_comp[3])
            print(row['title'])
            print(prep_time)
        
        
    elif 'm' in prep_time:
        prep_comp = prep_time.split(' ')
        prep_time = int(prep_comp[0][5:])

    return prep_time + cook_time

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-12-11-final_recipes_servings_data.csv')

df['total_time'] = df.apply(total_time, axis=1)
df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/FINAL_recipes_servings_data.csv', index=False)