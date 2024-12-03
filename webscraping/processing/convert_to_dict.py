import pandas as pd
import ast
import re

def ingredients_to_dict(list):
    exclude = ['tbsp', 'tsp', 'g']
    dict = {}
    for element in list:
        # corner case
        if element.split(' ')[0] in exclude:
            element = "1 " + element

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

        if measurement == None and element.rfind("of a") != -1:
            measurement = element[:element.rfind("of a")] 
            print(measurement)

        if units != None:
            measurement += ' ' + units 
        dict[main_str] = measurement
    return dict

def match(dict, ingredient_list):
    ret_dict = {}
    for key, value in dict.items():
        matches = []
        for ingredient in ingredient_list:
            if ingredient in key:
                matches.append(ingredient)
        if matches:
            longest = max(matches, key=len) 
            ret_dict[longest] = value 
        else:
            continue
    return ret_dict

df_ingredient_list = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/ingredients_list.csv')
col_name = df_ingredient_list.columns.tolist()
concat_df = pd.DataFrame(col_name, columns=['ingredients'])
df_ingredient_list.columns = ['ingredients']
df_ingredient_list = pd.concat([concat_df, df_ingredient_list], ignore_index=True)
ingredient_list = df_ingredient_list['ingredients'].tolist()
ingredient_list = [ingredient.lower() for ingredient in ingredient_list]

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/output/recipes_data_2024-11-11.csv')
df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
df['ingredients_dict'] = df['ingredients'].apply(ingredients_to_dict)
df['standardized_ingredients_dict'] = df['ingredients_dict'].apply(match, args=([ingredient_list]))
df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv', index=False)