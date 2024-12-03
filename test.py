from bs4 import BeautifulSoup
import requests
import re

url = "https://www.bbcgoodfood.com/recipes/air-fryer-apple-pancakes"

html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

ingredients = soup.find_all('li', {'class': re.compile('ingredients-list__item.*')})
for ingredient in ingredients:
    print(ingredients.text)
# ingredient_list = [element.text for element in ingredients]
# for i in ingredient_list:
#     print(i)


# for element in soup.find_all("li", {'class': "ingredients-list__item list-item list-item--separator-top"}):
#     print(element.text)

methods = []
method_items = soup.find_all('li', {'class':'method-steps__list-item'})
# print("THE LI_TAGS ARE", li_tags)
for nested_soup in method_items:
    method = nested_soup.find_all('div', {'class':'editor-content'})
    for m in method: 
        p_tags = m.find_all('p')
        for p in p_tags:
            methods.append(str(p.text))



