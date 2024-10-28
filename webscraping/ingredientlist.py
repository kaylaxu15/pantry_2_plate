import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://www.allrecipes.com/ingredients-a-z-6740416"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the section containing the ingredients
    ingredients_section = soup.find_all('li', class_='mntl-link-list__link type--dog-link type--dog-link') # or a element

    # Extract ingredient names
    ingredients = [ingredient.get_text(strip=True) for ingredient in ingredients_section]
    
    # Print the list of ingredient names
    for ingredient in ingredients:
        print(ingredient)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
