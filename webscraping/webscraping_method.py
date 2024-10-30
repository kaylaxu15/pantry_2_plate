import requests
from bs4 import BeautifulSoup

URL = "https://www.cnn.com/data/ocs/section/index.html:homepage1-zone-1/views/zones/common/zone-manager.izl"
response = requests.get(URL).json()["html"]
soup = BeautifulSoup(response, "html.parser")

for tag in soup.find_all(class_="recipe-method__list-item-text"):
    print(tag.text)