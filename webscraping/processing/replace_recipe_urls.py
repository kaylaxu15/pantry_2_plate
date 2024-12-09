import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import re

def correct_url(df):
    picture_urls = []
    for idx, row in df.iterrows():
        url = row['recipe_urls']
        url = url[url.rfind("https://"):]   # FIXME (deals with some http issues)
        recipe_title = row['title'].lower()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        #print(recipe_title)  # debugging

        try: 
            images = soup.find_all('img', {'class':'image__img'})
            
            found = False
            for img in images:
                title = img['title'].lower()

                actual_words = recipe_title.split(' ')
                itemname = img['data-item-name']

                image_url = img['src']
                
                if title == recipe_title:
                    picture_urls.append(image_url)
                    found=True
                    print(idx,recipe_title, ": ", image_url)
                    break
                elif title == recipe_title + "s":
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif title == recipe_title.replace("&", "and"):
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif title == recipe_title.replace("Air fryer", "Air-fryer"):
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif re.search(actual_words[-1], title, re.IGNORECASE):
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif re.search(actual_words[0], title, re.IGNORECASE):
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif re.search(actual_words[1], title, re.IGNORECASE): 
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break
                elif re.search(actual_words[0], itemname, re.IGNORECASE) or re.search(actual_words[-1], itemname, re.IGNORECASE):
                    picture_urls.append(image_url)
                    found= True
                    print(idx, recipe_title, ": ", image_url)
                    break

            if not found:
                print(idx, "NOT FOUND ", recipe_title, ": ", image_url)
            
        except:
            picture_urls.append(np.nan)

    picture_urls = pd.Series(picture_urls)
    df['picture_url'] = picture_urls
    return df

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv')
new_df = correct_url(df)

new_df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/fixed-2024-11-27_final_recipes_servings_data.csv', index=False)