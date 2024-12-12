from bs4 import BeautifulSoup
import requests
import re
import numpy as np

# for small testing of webscraping before large scale webscraping
url = "https://www.bbcgoodfood.com/recipes/salted-caramel-burnt-basque-cheesecake-with-chocolate-sauce"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

ingredients = soup.find_all('li', {'class': re.compile('ingredients-list__item.*')})
for ingredient in ingredients:
    print(ingredient.text)

methods = []
method_items = soup.find_all('li', {'class':'method-steps__list-item'})
for nested_soup in method_items:
    method = nested_soup.find_all('div', {'class':'editor-content'})
    for m in method: 
        p_tags = m.find_all('p')
        for p in p_tags:
            methods.append(str(p.text))

images = soup.find_all({'class':'img'})


found = False
picture_urls = []

html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

for i in images:
    print(i)




times = soup.find_all('li', {'class': 'body-copy-small list-item'})

if len(times) == 2:
    for idx, time in enumerate(times):
        t = time.find('time')
        if idx == 0:
            prep_time = t.text
        else:
            cook_time = t.text

print(cook_time)
print(prep_time)

        





