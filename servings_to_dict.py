import pandas as pd

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

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/final_recipes_data_2024-10-30.csv')
df['serves_dict'] = df['serves'].apply(servings_to_dict)
df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/finalfinal_recipes_data_2024-10-30.csv', index=False)