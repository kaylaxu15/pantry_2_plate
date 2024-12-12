import datetime
import time
import warnings
import os

import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')


def range_of_numbers(i, n):
    return list(range(i, n + 1))


def extract(pages, sleep_timer):
    def get_urls():
        # For now there is no use: later on, it can be used like this:
        # import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
# }

# response = requests.get('http://www.example.com', headers=headers)
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        
        urls_df = pd.DataFrame(columns=['recipe_urls'])

        for page in pages:
            time.sleep(sleep_timer)
            url = f'https://www.bbcgoodfood.com/search?page={page}'
            print(f"THE URL IS ############################################ {url}")
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])
            recipe_urls = recipe_urls[(recipe_urls.str.count("-") > 0)
                                      & (recipe_urls.str.contains("/recipes/") == True)
                                      & (recipe_urls.str.contains("category") == False)
                                      & (recipe_urls.str.contains("collection") == False)].unique()
            df = pd.DataFrame({"recipe_urls": recipe_urls})
            urls_df = pd.concat([urls_df, df], ignore_index=True)

        urls_df['recipe_urls'] = 'https://www.bbcgoodfood.com' + urls_df['recipe_urls'].astype(str)
        recipes_df = pd.DataFrame(
            columns=['title', 'difficulty', 'serves', 'rating', 'reviews', 'vegetarian', 'vegan', 'dairy_free', 'keto',
                     'gluten_free', 'prep_time', 'cook_time', 'ingredients', 'picture_url', 'methods'])
        list_urls = urls_df['recipe_urls'].to_list()
        return list_urls, urls_df, recipes_df

    def get_recipes(list_urls, urls_df, recipes_df):

        for i in range(len(list_urls)):
            time.sleep(sleep_timer)
            url = list_urls[i]
            print(f"THE ACTUAL URL FOR THE RECIPE IS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ {url}")

            url = url[url.rfind("https://"):]   # FIXME (deals with some http issues)
            
            html = requests.get(url)
            print(f"THE ACTUAL URL FOR THE RECIPE IS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ {url}")
            soup = BeautifulSoup(html.text, 'html.parser')

            try:
                recipe_title = soup.find('h1', {'class': 'heading-1'}).text
            except:
                recipe_title = np.nan
            try:
                difficulty = soup.find_all('div', {'class': 'icon-with-text__children'})[1].text
            except:
                difficulty = np.nan
            try:
                serves = soup.find_all('div', {'class': 'icon-with-text__children'})[2].text
            except:
                serves = np.nan
            try:
                rating = soup.find_all('span', {'class': 'sr-only'})[26].text
            except:
                rating = np.nan
            try:
                number_of_review = soup.find('span', {'class': 'rating__count-text body-copy-small'}).text
            except:
                number_of_review = np.nan
            try:
                times = soup.find_all('li', {'class': 'body-copy-small list-item'})

                if len(times) == 2:
                    for idx, time in enumerate(times):
                        t = time.find('time')
                        if idx == 0:
                            prep_time = t.text
                        else:
                            cook_time = t.text
            except:
                cook_time = np.nan
                prep_time = np.nan
                
            try: 
                images = soup.find_all('img', {'class':'image__img'})
                # print("THE LI_TAGS ARE", li_tags)
                for img in images:
                    title = img['title']

                    if title == recipe_title:
                        picture_url = img['src']
                    elif title == recipe_title + "s":
                        picture_url = img['src']

            except:
                picture_url = np.nan

            # add methods for recipes
            try: 
                methods = []
                method_items = soup.find_all('li', {'class':'method-steps__list-item'})
                # print("THE LI_TAGS ARE", li_tags)
                for nested_soup in method_items:
                    method = nested_soup.find_all('div', {'class':'editor-content'})
                    for m in method: 
                        p_tags = m.find_all('p')
                        for p in p_tags:
                            methods.append(str(p.text))

                print("METHODS IS !!!!!!!!!!!!!!!!!!!!", methods)
            except:
                methods = np.nan
            try:
                categories = soup.find_all('ul', {
                    'class': 'terms-icons-list d-flex post-header__term-icons-list mt-sm hidden-print list list--horizontal'})[
                    0].text
                if 'Vegetarian' in categories:
                    vegetarian = 'True'
                if not 'Vegetarian' in categories:
                    vegetarian = False
                if 'Vegan' in categories:
                    vegan = True
                if not 'Vegan' in categories:
                    vegan = False
                if 'Keto' in categories:
                    keto = True
                if not 'Keto' in categories:
                    keto = False
                if 'Dairy-free' in categories:
                    dairy_free = True
                if not 'Dairy-free' in categories:
                    dairy_free = False
                if 'Gluten-free' in categories:
                    gluten_free = True
                if not 'Gluten-free' in categories:
                    gluten_free = False
            except:
                vegetarian = False
                vegan = False
                keto = False
                dairy_free = False
                gluten_free = False

            
            i = 0
            ingredient_list = []
            ingredients = soup.find_all('li', {'class': re.compile('ingredients-list__item.*')})
            ingredient_list = [element.text for element in ingredients]

            print(f'Loaded recipe: {recipe_title}')
            new_row = pd.DataFrame([{'title': recipe_title, 'difficulty': difficulty, 'serves': serves, 'rating': rating,
                       'reviews': number_of_review, 'vegetarian': vegetarian, 'vegan': vegan, 'keto': keto,
                       'dairy_free': dairy_free, 'gluten_free': gluten_free, 'prep_time': prep_time, 'cook_time': cook_time,
                       'ingredients': ingredient_list, 'picture_url':picture_url, 'methods': methods}])
            recipes_df = pd.concat([recipes_df, new_row], ignore_index=True)
        recipes_df = recipes_df.join(urls_df)

        return recipes_df

    list_urls, urls_df, recipes_df = get_urls()
    recipes_df = get_recipes(list_urls, urls_df, recipes_df)
    return recipes_df


if __name__ == '__main__':
    # enter how many pages of recipes you would like to scrape
    pages = range_of_numbers(1, 250)
    # here you can change the amount of time between each request to scrape data
    sleep_timer = 0
    #week = datetime.datetime.now().strftime("%Y-%m-%d")

    # SCRAPE FOR THE REST OF THE PAGES
    print(f'Scraping {pages} pages from BBC good food')
    recipes_df = extract(pages, sleep_timer)
    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    recipes_df.to_csv(f'{output_dir}/recipes_data_2024-11-11.csv', index=False)
    print('Complete')