import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.co.uk/food/recipes/tumbet_98868"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
instructions = []
for tag in soup.find_all('p', {'class': "recipe-method__list-item-text"}):
    instructions.append(tag.text)

