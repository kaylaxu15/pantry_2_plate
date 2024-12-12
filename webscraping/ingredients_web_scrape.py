import re
import json
import requests
import pandas as pd

all_ingredients = []
alphabet = "abcdefghijklmnopqrstuvwxyz"

# webscraping standardized ingredients list
for letter in alphabet:
    page_num = 0
    while True:
        page_num += 1
        url = f"https://www.bbc.co.uk/food/ingredients/a-z/{letter}/{page_num}#featured-content"
        page = requests.get(url, allow_redirects=False)  # use `url` here, not `base_url`
        if page.status_code == 301 or page.status_code == 302:
            break
        if url == "https://www.bbc.co.uk/food/ingredients#featured-content":
            break

        html_doc = requests.get(url).text
        data = re.search(r"window\.__reactInitialState__ = (.*?);", html_doc).group(0)

        # Pattern to find all words starting with 'title'
        pattern = r"title\":\"[a-zA-Z ]+\","

        # Find all matches
        matches = re.findall(pattern, data)
        for match in matches[1:]:
            all_ingredients.append(match[8:-2])

df = pd.DataFrame(all_ingredients)
df.to_csv('webscraping/output/ingredients_list.csv', index=False)

