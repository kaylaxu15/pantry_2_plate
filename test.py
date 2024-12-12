from bs4 import BeautifulSoup
import requests
import re
import numpy as np

url = "https://www.bbcgoodfood.com/recipes/mustard-apple-glazed-ham"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

# re.compile('ingredients-list__item .*')

ingredients = soup.find_all('li', {'class': re.compile('ingredients-list__item.*')})
for ingredient in ingredients:
    print(ingredient.text)
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

images = soup.find_all('img', {'class':'image__img'})
recipe_title = "Mustard & apple glazed ham"

found = False
picture_urls = []
for i in images:
    name = i['title']
    actual_words = recipe_title.split(' ')
    print("ACTUAL", actual_words[-1])
    print("TITLE", name)
    try: 
        itemname = i['data-item-name']
    except:
        itemname = ''

    image_url = i['src']
    
    if name == recipe_title:
        picture_urls.append(image_url)
        found=True
        print(recipe_title, ": ", image_url)
        break
    elif name == recipe_title + "s":
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif re.search(actual_words[-1], name, re.IGNORECASE):
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif re.search(actual_words[0], name, re.IGNORECASE):
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif re.search(actual_words[1], name, re.IGNORECASE): 
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif re.search(actual_words[0], itemname, re.IGNORECASE) or re.search(actual_words[-1], itemname, re.IGNORECASE):
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif name == recipe_title.replace("&", "and"):
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break
    elif name == recipe_title.replace("Air fryer", "Air-fryer"):
        picture_urls.append(image_url)
        found= True
        print(recipe_title, ": ", image_url)
        break


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

        





