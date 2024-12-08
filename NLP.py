import spacy
import pandas as pd
import ast
import re

class NLP:
    # Load NLP Model and Get Ingredients
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        df = pd.read_csv("webscraping/output/ingredients_list.csv")
        self.known_ingredients = set(df["ingredients"].values.tolist())

    # Extract the main ingredient from a string
    def extract_ingredient(self, text):
        # Handle "or" logic by splitting and keeping the first part
        text = text.split(" or ")[0]

        # Remove numbers, fractions, units, and irrelevant descriptors
        text_cleaned = re.sub(
            r'\b(\w*\d+\w*|[¼½¾⅓⅔⅛⅜⅝⅞]|shakes|tbsp|tsp|cup|cups|g|kg|ml|l|oz|ounce|pinch|dash|bunch|slice|clove|cloves|can|cans|handful|stick|small|medium|large|hot|fresh|to taste|optional|few|extra|plus|more|leftover|good|shop-bought|homemade|ready-to-roll|broken|lengthways|stalks removed|roughly snapped)\b',
            '', text, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(finely|roughly|thinly|coarsely|juiced|cut|into|wedges|rings|chopped|diced|minced|sliced|grated|peeled|halved|quartered|zested|seeds removed|to serve|shredded|ground|drained|torn|broken|snapped|stalk|stalks|florets|whole|works well)\b',
            '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(pack|packs|box|boxes|bottle|bottles|jar|jars|tin|tins|can|cans|container|containers|carton|cartons)\b',
            '', text_cleaned, flags=re.IGNORECASE)  # Remove container-related words
        text_cleaned = re.sub(r'\b(of|and|a|mix|any|such as|shop-bought|or)\b', '', text_cleaned, flags=re.IGNORECASE)  # Remove additional filler words
        text_cleaned = re.sub(r'\(.*?\)', '', text_cleaned, flags=re.IGNORECASE)  # Remove parentheticals
        text_cleaned = re.sub(r'[^\w\s]', '', text_cleaned)  # Remove punctuation
        text_cleaned = re.sub(r'\s+', ' ', text_cleaned).strip()  # Remove extra spaces

        # Parse the cleaned text with spaCy
        doc = self.nlp(text_cleaned)

        # Extract nouns and proper nouns
        candidates = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}]
        ingredient_phrase = " ".join(candidates).strip()

        # Match against known ingredients, ensuring whole-word matches
        matches = [ingredient for ingredient in self.known_ingredients if re.search(rf'\b{re.escape(ingredient)}\b', ingredient_phrase, flags=re.IGNORECASE)]
        if matches:
            matches.sort(key=len, reverse=True)  # Sort by specificity
            return matches[0]

        # Fallback: Use the most relevant part of the cleaned text
        if " " in text_cleaned:
            words = text_cleaned.split()
            for word in words:
                if word in self.known_ingredients:
                    return word
        return ingredient_phrase if ingredient_phrase else text_cleaned
    
# Testing for accuracy
if __name__ == "__main__":
    nlp_model = NLP()
    
    df1 = pd.read_csv("webscraping/output/2024-11-27_final_recipes_servings_data.csv")
    recipe_list = df1["ingredients"].values.tolist()

    original_ingredient = []
    standardized_ingredient = []

    i = 0

    for recipe in recipe_list:
        i += 1
        # print(i/len(recipe_list))
        list_recipe = ast.literal_eval(recipe)  # Convert string to list of ingredients
        for ingredient in list_recipe:
            original_ingredient.append(ingredient)
            print(ingredient)
            main_ingredient = nlp_model.extract_ingredient(ingredient)
            print(main_ingredient)
            standardized_ingredient.append(main_ingredient)