import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def correct_url(df):
    for _, row in df.iterrows():
        url = row['recipe_urls']
        recipe_title = row['title']
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        picture_urls = []

        try: 
            images = soup.find_all('img', {'class':'image__img'})
            # print("THE LI_TAGS ARE", li_tags)
            for img in images:
                title = img['title']

                if title == recipe_title:
                    picture_urls.append(img['src'])
                elif title == recipe_title + "s":
        
                    picture_urls.append(img['src'])
        except:
            picture_urls.append(np.nan)

    picture_urls = pd.Series(picture_urls)
    df['picture_urls'] = picture_urls
    return df

df = pd.read_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv')
new_df = correct_url(df)

new_df.to_csv('/Users/kaylaxu/princeton_plate_planner/webscraping/output/fixed-2024-11-27_final_recipes_servings_data.csv', index=False)