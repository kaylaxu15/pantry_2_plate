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

    # Extract main ingredient from given string
    def extract_ingredient(self, text):
        # print(text)
        text = text.split(" or ")[0]

        # String Removal
        text_cleaned = re.sub(
            r'\b(\w*\d+\w*|[¼½¾⅓⅔⅛⅜⅝⅞]|¼tsp|shakes|tbsp|tsp|cup|cups|g|kg|ml|l|oz|ounce|pinch|dash|bunch|slice|clove|cloves|can|cans|handful|stick|small|medium|large|hot|fresh|to taste|optional|few|extra|plus|more|leftover|good|shop-bought|homemade|ready-to-roll|broken|lengthways|stalks removed|roughly snapped|yolk|yolks|white|whites|fork|room|temperature|mins|pieces|pin|quarter|quaerters|water|boiling|bowl|freerange|very|soft|crosswise|bulb|end|half|semicircles|to|decorate|toasted|beaten|strong|veg|peeler|choice|cube|cubes|minute|minutes|skinless|bag|very|hole|topping|skinon|food|processor|liquid|if|intact|slices|slice|layer|layers|fingers|finger|one|ones|cordial|quarters|quarter|punnet|punnets|william|conference|it|may|be|little|hundred|thousand|drop|pen|paper|glue|skewer|chopstick|kitchen|pan|lid|sieve|glitter|string|parchment|case|cutter|template|hour|basin|flower|mould|ink|button|steamer|straw|truck|cardboard|stirrer|glas|nose|cutlery|flask|recipe|method|screwtop|tray|decoration|gasket|mouth|lustre|scotch|pipe|board|knife|spoon|mortar|½cmthick|round|thickly|then|ribbon|angle|cm|length|your|silver|serve|gold|reserve|kept|up|gift|lightly|writing|chunk|chunky|about|for|centre|down|the|middle|baton|weight|the|reserved|you|like|smoke|end|rest|sparkling|horizontally|hr|go|some|die|root|part|spring|top|mixture|giant|x|around|royal|each|litre|strength|an|supermarket|drizzle|silver|mixed|roasted|from|wheel|lukewarm|middle|quality|bite|size|bitesize|washed|both|selection|advance|shape|instruction|hold|bigger|eye|has|cheek|amount|possible|label|dust|freshly|tender|need|drain|ready|prepped|use|eat|at|icecold|way|rock|handful|tube|coarse|time|head|third|bulb|date|strip|shot|measure|pot|total|sweet|disc|block|matchstick|cover|core|drop|tip|rack|shin|sec|braising|drop|half|splash|bestquality|couple|pinch|green|eighth|skin|glutenfree|dry|only|long|baby|in|saltfree|smoke|shop|square|dried|grill|frozen|mince|semi-dried)\b',
            '', text, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(finely|roughly|thinly|coarsely|juiced|cut|into|wedges|rings|chopped|diced|minced|sliced|grated|peeled|halved|quartered|zested|seeds removed|to serve|shredded|ground|drained|torn|broken|snapped|stalk|stalks|florets|whole|works well)\b',
            '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(pack|packs|box|boxes|bottle|bottles|jar|jars|tin|tins|can|cans|container|containers|carton|cartons)\b',
            '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(r'\b(of|and|a|mix|any|such as|shop-bought|or)\b', '', text_cleaned, flags=re.IGNORECASE)  # Remove additional filler words
        text_cleaned = re.sub(r'\(.*?\)', '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(r'[^\w\s]', '', text_cleaned)
        text_cleaned = re.sub(r'\s+', ' ', text_cleaned).strip()
        
        # print(text_cleaned)

        doc = self.nlp(text_cleaned)

        candidates = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}]
        ingredient_phrase = " ".join(candidates).strip()

        matches = [ingredient for ingredient in self.known_ingredients if re.search(rf'\b{re.escape(ingredient)}\b', ingredient_phrase, flags=re.IGNORECASE)]
        if matches:
            matches.sort(key=len, reverse=True)
            return matches[0]

        if " " in text_cleaned:
            words = text_cleaned.split()
            for word in words:
                if word in self.known_ingredients:
                    return word
        return ingredient_phrase if ingredient_phrase else text_cleaned
    
    def handle_corner_cases(self, text):
        excluded_words = ['natural', 'scoop', 'horizontal', 'roasting', 'topping', 'equator', 'smooth', 'outer', 'rolling', 'whipping', 'piping', 'topping', 'shaving', 'single', 'segment', 'moisture', 'whirl', 'balloon', 'twig', 'topside', 'boiled', 'pouring', 'german', 'flaked', 'sundried', 'nest', 'teaspoon', 'tablespoon', 'mixing', 'scale', 'spatula', 'grater', 'grating', 'kettle', 'timer', 'jug', 'rack', 'square baking', 'opener', 'card', 'red card', 'tape', 'toilet roll', 'stencil', 'paintbrush', 'paint brush', 'paint gold leaf', 'fliptop', 'whisk', 'scissors', 'kitchen scissors', 'raw', 'regular', 'vegan', 'black', 'red', 'pink', 'purple', 'yellow', 'green', 'blue', 'sichuan', 'double', 'digestive', 'toothpick', 'woody end', 'spear woody end', 'conference', 'spicy green', 'king edward', 'eye aisle', 'quickcook green person', 'person', 'gel f', 'oven glove', 'glove', 'semiskimmed', 'brown', 'english']
        if text == "butternut":
            return "butternut squash"
        elif text == "parmigianoreggiano":
            return "parmigiano reggiano"
        elif text in excluded_words:
            return ''
        else:
            words = text.split()
            unique_words = []
            seen = set()

            for word in words:
                if word.lower() not in seen:
                    unique_words.append(word)
                    seen.add(word.lower())
            return " ".join(unique_words)
        


    
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
        list_recipe = ast.literal_eval(recipe)
        for ingredient in list_recipe:
            original_ingredient.append(ingredient)
            print(ingredient)
            main_ingredient = nlp_model.extract_ingredient(ingredient)
            print(main_ingredient)
            standardized_ingredient.append(main_ingredient)
