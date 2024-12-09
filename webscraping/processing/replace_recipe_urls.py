import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def correct_url(df):
    picture_urls = []
    for _, row in df.iterrows():
        url = row['recipe_urls']
        url = url[url.rfind("https://"):]   # FIXME (deals with some http issues)
        recipe_title = row['title']
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        #print(recipe_title)  # debugging

        try: 
            images = soup.find_all('img', {'class':'image__img'})
            
            found = False
            for img in images:
                title = img['title']
                words = title.split(' ')
                actual_words = recipe_title.split(' ')

                image_url = img['src']
                
                if title == recipe_title:
                    picture_urls.append(img['src'])
                    found=True
                    break
                elif title == recipe_title + "s":
                    picture_urls.append(img['src'])
                    found= True
                    break
                elif title == recipe_title.replace("&", "and"):
                    picture_urls.append(img['src'])
                    found= True
                    break
                elif title == recipe_title.replace("Air fryer", "Air-fryer"):
                    picture_urls.append(img['src'])
                    found= True
                    break
                elif title.index(words[:2]) == actual_words[:2]:
                    picture_urls.append(img['src'])
                    found= True
                    break


            if not found:
                print(recipe_title)

            
        except:
            picture_urls.append(np.nan)

    picture_urls = pd.Series(picture_urls)
    df['picture_url'] = picture_urls
    return df

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv')
new_df = correct_url(df)

new_df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/fixed-2024-11-27_final_recipes_servings_data.csv', index=False)