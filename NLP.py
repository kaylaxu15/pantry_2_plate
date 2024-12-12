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
            r'\b(\w*\d+\w*|[¼½¾⅓⅔⅛⅜⅝⅞]|¼tsp|shakes|tbsp|tsp|cup|cups|g|kg|ml|l|oz|ounce|pinch|dash|bunch|slice|can|cans|handful|stick|small|medium|large|hot|fresh|to taste|optional|few|extra|plus|more|leftover|good|shop-bought|homemade|ready-to-roll|broken|lengthways|stalks removed|roughly snapped|yolk|yolks|white|whites|fork|room|temperature|mins|pieces|pin|quarter|quaerters|water|boiling|bowl|freerange|very|soft|crosswise|bulb|end|half|semicircles|to|decorate|toasted|beaten|strong|veg|peeler|choice|cube|cubes|minute|minutes|skinless|bag|very|hole|topping|skinon|food|processor|liquid|if|intact|slices|slice|layer|layers|fingers|finger|one|ones|cordial|quarters|quarter|punnet|punnets|william|conference|it|may|be|little|hundred|thousand|drop|pen|paper|glue|skewer|chopstick|kitchen|pan|lid|sieve|glitter|string|parchment|case|cutter|template|hour|basin|flower|mould|ink|button|steamer|straw|truck|cardboard|stirrer|glas|nose|cutlery|flask|recipe|method|screwtop|tray|decoration|gasket|mouth|lustre|scotch|pipe|board|knife|spoon|mortar|½cmthick|round|thickly|then|ribbon|angle|cm|length|your|silver|serve|gold|reserve|kept|up|gift|lightly|writing|chunk|chunky|about|for|centre|down|the|middle|baton|weight|the|reserved|you|like|smoke|end|rest|sparkling|horizontally|hr|go|some|die|root|part|spring|top|mixture|giant|x|around|royal|each|litre|strength|an|supermarket|drizzle|silver|mixed|roasted|from|wheel|lukewarm|middle|quality|bite|size|bitesize|washed|both|selection|advance|shape|instruction|hold|bigger|eye|has|cheek|amount|possible|label|dust|freshly|tender|need|drain|ready|prepped|use|eat|at|icecold|way|rock|handful|tube|coarse|time|head|third|bulb|date|strip|shot|measure|pot|total|sweet|disc|block|matchstick|cover|core|drop|tip|rack|shin|sec|braising|drop|half|splash|bestquality|couple|pinch|green|eighth|skin|glutenfree|dry|only|long|baby|in|saltfree|smoke|shop|square|dried|grill|frozen|mince|semi-dried)\b',
            '', text, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(finely|roughly|thinly|coarsely|juiced|cut|into|wedges|rings|chopped|diced|minced|sliced|grated|peeled|halved|quartered|zested|seeds removed|to serve|shredded|ground|drained|torn|broken|snapped|stalk|stalks|florets|whole|works well|quantity|sprig|sprigs|similar-sized)\b',
            '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(
            r'\b(pack|packs|box|boxes|bottle|bottles|jar|jars|tin|tins|can|cans|container|containers|carton|cartons|litres|garnish|pickled|sprinkling|sheets)\b',
            '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(r'\b(of|and|a|mix|any|such as|shop-bought|or)\b', '', text_cleaned, flags=re.IGNORECASE)  # Remove additional filler words
        text_cleaned = re.sub(r'\(.*?\)', '', text_cleaned, flags=re.IGNORECASE)
        text_cleaned = re.sub(r'[^\w\s]', '', text_cleaned)
        text_cleaned = re.sub(r'\s+', ' ', text_cleaned).strip()

        doc = self.nlp(text_cleaned)
        
        multi_word_phrases = [
            chunk.text.lower() for chunk in doc.noun_chunks
        ]

        for phrase in multi_word_phrases:
            for ingredient in sorted(self.known_ingredients, key=len, reverse=True):  # Sort by length
                if ingredient.lower() == phrase:
                    return ingredient

        for phrase in multi_word_phrases:
            for ingredient in sorted(self.known_ingredients, key=len, reverse=True):  # Sort by length
                if ingredient.lower() in phrase:
                    return ingredient

        single_words = [token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"}]
        for word in single_words:
            for ingredient in sorted(self.known_ingredients, key=len, reverse=True):  # Sort by length
                if ingredient.lower() == word:
                    return ingredient

        return text_cleaned
    
    def handle_corner_cases(self, text):
        excluded_words = ['pizza', 'natural', 'scoop', 'horizontal', 'roasting', 'topping', 'equator', 'smooth', 'outer', 'rolling', 'whipping', 'piping', 'topping', 'shaving', 'single', 'segment', 'moisture', 'whirl', 'balloon', 'twig', 'topside', 'boiled', 'pouring', 'german', 'flaked', 'sundried', 'nest', 'teaspoon', 'tablespoon', 'mixing', 'scale', 'spatula', 'grater', 'grating', 'kettle', 'timer', 'jug', 'rack', 'square baking', 'opener', 'card', 'red card', 'tape', 'toilet roll', 'stencil', 'paintbrush', 'paint brush', 'paint gold leaf', 'fliptop', 'whisk', 'scissors', 'kitchen scissors', 'raw', 'regular', 'vegan', 'black', 'red', 'pink', 'purple', 'yellow', 'green', 'blue', 'sichuan', 'double', 'digestive', 'toothpick', 'woody end', 'spear woody end', 'conference', 'spicy green', 'king edward', 'eye aisle', 'quickcook green person', 'person', 'gel f', 'oven glove', 'glove', 'semiskimmed', 'brown', 'english']
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
    
    print(nlp_model.extract_ingredient("75g sweetened condensed milk"))
    print(nlp_model.extract_ingredient("5 tbsp olive oil plus extra to serve"))
    print(nlp_model.extract_ingredient("2 heaped tsp medium curry powder"))
    print(nlp_model.extract_ingredient("1 small butternut squash unpeeled and halved"))
    print(nlp_model.extract_ingredient("tsp white wine vinegar"))
    print(nlp_model.extract_ingredient("4 tbsp crème fraîche and grated chocolate, to serve"))
    print(nlp_model.extract_ingredient("6 tbsp chicken tikka masala paste"))
    print(nlp_model.extract_ingredient("160g edamame"))
    print(nlp_model.extract_ingredient("50g pickled jalapenos roughly chopped"))
    print(nlp_model.extract_ingredient("5 cloves"))
    print(nlp_model.extract_ingredient("1 small butternut squash unpeeled and halved"))
    print(nlp_model.extract_ingredient("tsp white wine vinegar"))
    print(nlp_model.extract_ingredient("4 tbsp crème fraîche and grated chocolate, to serve"))
    print(nlp_model.extract_ingredient("6 tbsp chicken tikka masala paste"))
    print(nlp_model.extract_ingredient("160g edamame"))
    print(nlp_model.extract_ingredient("50g pickled jalapenos roughly chopped"))
    print(nlp_model.extract_ingredient("5 cloves"))

