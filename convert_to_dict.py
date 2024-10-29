import pandas as pd
import ast
import re

def ingredients_to_dict(list):
    exclude = ['tbsp', 'tsp']
    dict = {}
    for element in list:
        units = None
        if 'plus' in element:
            element = element.split('plus')[0]
        if not element.isalnum():
            elements = [element.strip() for element in re.split(r'[^a-zA-Z\d\s\-\.]', element)]
            first_element = elements[0]
        else:
            first_element = element 
        main_str = ''
        measurement = None
        for word in first_element.split():
            if not bool(re.search(r'\d', word)):
                if word not in exclude:
                    main_str += word.strip() + ' '
                else:
                    units = word
            else:
                measurement = word
        main_str = main_str.strip()
        if main_str == '':
            continue
        if units != None:
            measurement += ' ' + units 
        dict[main_str] = measurement
    return dict

df = pd.read_csv('webscraping/output/recipes_data_2024-10-22.csv')
df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
df['ingredients_dict'] = df['ingredients'].apply(ingredients_to_dict)
df.to_csv('webscraping/output/processed_recipes_data_2024-10-22.csv', index=False)