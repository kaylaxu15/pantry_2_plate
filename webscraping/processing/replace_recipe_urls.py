import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import re

def correct_url(df):
    picture_urls = []
    for idx, row in df.iterrows():
        url = row['recipe_urls']
        title = row['title']
        
        #recipe_title = row['title'].lower()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        images = soup.find_all('img', {'class':'image__img'})
        pic_url = images[2]['src']
        picture_urls.append(pic_url)
        print(idx, title, pic_url)

        #print(recipe_title)  # debugging

        # try: 
        #     images = soup.find_all('img', {'class':'image__img'})
            
        #     found = False
        #     for idx, i in enumerate(images):
        #         name = i['title'].lower()
        #         actual_words = recipe_title.split(' ')

        #         try: 
        #             itemname = i['data-item-name']
        #         except:
        #             itemname = ''

        #         image_url = i['src']
                
        #         if name == recipe_title:
        #             picture_urls.append(image_url)
        #             found=True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif name == recipe_title + "s":
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif re.search(actual_words[-1], name, re.IGNORECASE):
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif re.search(actual_words[0], name, re.IGNORECASE):
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif re.search(actual_words[1], name, re.IGNORECASE): 
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif re.search(actual_words[0], itemname, re.IGNORECASE) or re.search(actual_words[-1], itemname, re.IGNORECASE):
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif name == recipe_title.replace("&", "and"):
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break
        #         elif name == recipe_title.replace("Air fryer", "Air-fryer"):
        #             picture_urls.append(image_url)
        #             found= True
        #             print(idx, recipe_title, ": ", image_url)
        #             break

        #     if not found:
        #         print(idx, "NOT FOUND ", recipe_title, ": ", image_url)
            
        # except:
        #     picture_urls.append(np.nan)

    picture_urls = pd.Series(picture_urls)
    df['picture_url'] = picture_urls
    return df

def correct_prep_cook(df):
    cook_times = []
    prep_times = []

    for idx, row in df.iterrows():

        url = row['recipe_urls']
        url = url[url.rfind("https://"):]   # FIXME (deals with some http issues)

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        #print(recipe_title)  # debugging

        times = soup.find_all('li', {'class': 'body-copy-small list-item'})
        if row['title'] == "Cheat's banana & peanut brittle ice cream":
            print(times)

        prep_times.append("Prep:0 min")
        cook_times.append("Cook:0 min")

        for idx, time in enumerate(times):
            t = time.find('time')
            if idx == 0:
                prep_time = t.text
                prep_times[-1] = "Prep:" + prep_time
            else:
                cook_time = t.text
                cook_times[-1] = "Cook:" + cook_time

        
        print(prep_times[-1], cook_times[-1])
        

    cook_times = pd.Series(cook_times)
    prep_times = pd.Series(prep_times)
    df['cook_time'] = cook_times
    df['prep_time'] = prep_times
    return df

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/FINAL_recipes_servings_data.csv')
#new_df = correct_prep_cook(df)
new_df = correct_url(df)
#new_df = correct_prep_cook(new_df)

new_df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/corrected_recipes_servings_data.csv', index=False)