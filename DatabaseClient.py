from pymongo import MongoClient
import pandas as pd
import ast
from bson import ObjectId
import ssl
import json
import re
import NLP
import inflect

class DatabaseClient:
    
    def __init__(self):
        self.uri = "mongodb+srv://server:hHSsj4NSo5KqJcKB@princetonplateplanner.zggiw.mongodb.net/?retryWrites=true&w=majority&appName=PrincetonPlatePlanner"
        self.client = MongoClient(self.uri, ssl=True, tlsAllowInvalidCertificates=True)
        self.db = self.client["PPP"]

    def insert_user(self, emailId, password, picture="", restrictions=[], inventory=[], favRecipes=[], wishList=[], completed=[], groceryList=[], ratings={}):
        if self.check_emailId_taken(emailId):
            return 1
        col = self.db["Users"]
        dict = {"emailId": emailId, "password": password, "picture": picture, "restrictions": restrictions, "inventory": inventory, "favRecipes": favRecipes, "wishList":wishList, "completed":completed, "groceryList":groceryList, "ratings": ratings}
        col.insert_one(dict)
        return 0
        
    def delete_user(self, emailId):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.delete_one({"emailId": emailId})
        return 0
        
    def update_user_pic(self, emailId, picture):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"picture": picture}})
        return 0
        
    def update_user_restrictions(self, emailId, restrictions):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"restrictions": restrictions}})
        return 0
        
    def update_user_inventory(self, emailId, inventory):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"inventory": inventory}})
        return 0
    
    def get_user_inventory(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"inventory": 1})
        return user["inventory"] if user and "inventory" in user else []
    
        
    def update_user_password(self, emailId, password):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"password": password}})
        return 0
        
    def update_user_favRecipes(self, emailId, favRecipes):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"favRecipes": favRecipes}})
        return 0
    
    def get_user_favRecipes(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"favRecipes": 1})
        return user["favRecipes"] if user and "favRecipes" in user else []

        
    # remove a recipe from favorites
    def remove_favRecipe(self, emailId, recipe_id):
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$pull": {"favRecipes": recipe_id}})

    def get_user_grocerylist(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"groceryList": 1})
        return user["groceryList"] if user and "groceryList" in user else []
    
    def update_user_grocerylist(self, emailId, groceryList):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"groceryList": groceryList}})
        return 0

    def get_user_wishlist(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"wishList": 1})
        return user["wishList"] if user and "wishList" in user else []

    def update_user_wishlist(self, emailId, wishList):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"wishList": wishList}})
        return 0
    
    def update_user_completed(self, emailId, completed):
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"completed": completed}})
        return 0

    def get_user_completed(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"completed": 1})
        return user["completed"] if user and "completed" in user else []
    
    # adds user reviews as a field
    def add_user_reviews(self):
        users_collection = self.db["Users"]
        users_collection.update_many({}, {"$set":{"reviews": {}}})

    def update_user_reviews(self, emailId, new_dict):
        if self.check_emailId_taken(emailId) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"reviews": new_dict}})

    def get_user_reviews(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId}, {"reviews": 1})
        return user["reviews"] if user and "reviews" in user else {}
        
    def check_emailId_taken(self, emailId):
        col = self.db["Users"]
        return col.find_one({"emailId": emailId}) != None
    
    def get_user(self, emailId):
        col = self.db["Users"]
        return col.find_one({"emailId": emailId})
    
    def user_login_valid(self, emailId, password):
        col = self.db["Users"]
        if self.check_emailId_taken(emailId) == False:
            return "EmailId not found"
        user = col.find_one({"emailId": emailId, "password": password})
        if user == None:
            return "Password incorrect"
        return user
    
    def check_recipe_taken(self, title):
        col = self.db["Recipes"]
        return col.find_one({"title": title}) != None
    
    def return_recipe(self, recipe_id):
        col = self.db["Recipes"]
        if not ObjectId.is_valid(recipe_id):
            return None
        return col.find_one({"_id": ObjectId(recipe_id)})
    
    def return_recipe_wishlist(self, ingredients, recipe_id):
        col = self.db["Recipes"]
        if not ObjectId.is_valid(recipe_id):
            return None
        recipe = col.find_one({"_id": ObjectId(recipe_id)})
        matching_ingredients = []
        unmatching_ingredients = []
        for ingredient in recipe["ingredients"]:
            if ingredient in ingredients:
                matching_ingredients.append(ingredient)
            else:
                unmatching_ingredients.append(ingredient)
        recipe["matching_ingredients"] = matching_ingredients
        recipe["unmatching_ingredients"] = unmatching_ingredients
        recipe['missing_count'] = len(unmatching_ingredients)
        return recipe 
    
    def insert_recipe(self, title, difficulty, vegetarian, vegan, dairy_free, keto, gluten_free, ingredients, picture_url, actual_ingredients, methods, recipe_urls, total_time, makes, servings):
        
        col = self.db["Recipes"]
        if self.check_recipe_taken(title):
            return 1
        restrictions = []
        if vegetarian:
            restrictions.append("vegetarian")
        if vegan:
            restrictions.append("vegan")
        if dairy_free:
            restrictions.append("dairy-free")
        if keto:
            restrictions.append("keto")
        if gluten_free:
            restrictions.append("gluten-free")
        dict = {"title": title, "difficulty": difficulty, "restrictions": restrictions, "ingredients": ingredients, "picture_url": picture_url, "actual_ingredients":actual_ingredients, "methods":methods, "recipe_urls":recipe_urls, "total_time":total_time, "makes":makes, "servings":servings}
        col.insert_one(dict)
        for ingredient in ingredients:
            self.insert_ingredient(ingredient)
        return 0
    
    def delete_user_restrictions(self, emailId):
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$set": {"restrictions": []}})
    
    def delete_all_recipes(self):
        self.delete_all_ingredients()
        col = self.db["Recipes"]
        col.delete_many({})
        return 0
    
    def delete_all_ingredients(self):
        col = self.db["Ingredients"]
        col.delete_many({})
        return 0

    def delete_all_users(self):
        col = self.db["Users"]
        col.delete_many({})
        return 0
    
    def get_all_recipes(self):
        col = self.db["Recipes"]
        results = col.find()
        return list(results)
    
    def get_recipes_ingredients(self, ingredients):
        col = self.db["Recipes"]
        query = {"ingredients" : {'$all' : ingredients}}
        results = col.find(query)
        return list(results)
    
    def check_ingredient_taken(self, ingredient):
        col = self.db["Ingredients"]
        return col.find_one({"ingredient": ingredient}) != None
    
    def insert_ingredient(self, ingredient):
        if self.check_ingredient_taken(ingredient) == True:
            return 1
        col = self.db["Ingredients"]
        dict = {"ingredient":ingredient}
        col.insert_one(dict)
        return 0

    def get_all_ingredients(self):
        col = self.db["Ingredients"]
        results = col.find()
        return list(results)
    
    def get_pantry_ingredients(self):
        ingredient_dict = self.get_all_ingredients()
        return [item['ingredient'] for item in ingredient_dict]
    
    def filter_recipes(self, ingredients, skill=None, max_time=None, restrictions=[], search=''):
        col = self.db["Recipes"] 
        indicator = None 

        if not search:
            search = ''
        query = {}

        if skill == "Beginner":
            skill = "Easy"
        elif skill == "Intermediate":
            skill = "More effort"
        elif skill == "Advanced":
            skill = "A challenge"
        else:
            skill = None
        
        if skill is not None:
            query["difficulty"] = {"$eq": skill}
        if max_time is not None:
            query["total_time"] = {"$lte": max_time}
        if restrictions:
            query["restrictions"] = {"$all": restrictions}
        if search:
            query["title"] = {"$regex": search, "$options": "i"}
        
        count = col.count_documents(query)
        if count > 0:
            results = col.find(query)
            indicator = 0
        else:
            if skill == 'Easy':
                skill = ['Easy']
            elif skill == 'More effort':
                skill = ['Easy', 'More effort']
            elif skill == 'A challenge':
                skill = ['Easy', 'More effort', 'A challenge']

            if skill is not None:
                query["difficulty"] = {"$in": skill}
            if max_time is not None:
                query["total_time"] = {"$lte": max_time}
            if restrictions:
                query["restrictions"] = {"$all": restrictions}
            if search:
                query["title"] = {"$regex": search, "$options": "i"}
            count = col.count_documents(query)
            if count > 0:
                results = col.find(query)
                indicator = 1
            else:
                results = col.find(query)
                indicator = 2
        results = list(results)
        modified_results = []
        for recipe in results:
            matching_ingredients = []
            unmatching_ingredients = []
            for ingredient in recipe["ingredients"]:
                if ingredient in ingredients:
                    matching_ingredients.append(ingredient)
                else:
                    unmatching_ingredients.append(ingredient)
            recipe["matching_ingredients"] = matching_ingredients
            recipe["unmatching_ingredients"] = unmatching_ingredients
            recipe['missing_count'] = len(unmatching_ingredients)
            modified_results.append(recipe)
        return modified_results, indicator 
    
        
    def add_default_ingredients(self, ingredients):
        normalized_ingredients = set(ingredient.lower() for ingredient in ingredients if isinstance(ingredient, str))

        for ingredient in ingredients:
            if not isinstance(ingredient, str):
                continue  
            ingredient_lower = ingredient.lower()
            if "black peppercorn" not in ingredient_lower:
                normalized_ingredients.add("black peppercorn")
            if "sea salt" not in ingredient_lower:
                normalized_ingredients.add("sea salt")

        return normalized_ingredients
    
    def get_recipes_missing_ingredients(self, number, ingredients):
        col = self.db["Recipes"]
        updated_ingredients = self.add_default_ingredients(ingredients)

        query = [{"$addFields": {"missing_count": {"$size": {"$filter": {"input": "$ingredients","as": "ingredient","cond": {"$not": {"$in": ["$$ingredient",list(updated_ingredients)]}}}}}}},{"$match": {"missing_count": number}}]

        return list(col.aggregate(query))
    
    def return_page_recipes(self, ingredients):
        recipes = []
        modified_recipes = []
        updated_ingredients = self.add_default_ingredients(ingredients)

        for i in range(5):
            given_recipes = self.get_recipes_missing_ingredients(i, updated_ingredients)
            sorted_recipes = sorted(given_recipes, key=lambda x: len(x["ingredients"]), reverse=True)
            recipes.extend(sorted_recipes)
        for recipe in recipes:
            if int(recipe["missing_count"]) != len(recipe["ingredients"]):
                modified_recipes.append(recipe)
        return modified_recipes

    def get_recipes_missing_ingredients_rec(self, number, ingredients, skill=None, max_time=None, restrictions=[]):
        col = self.db["Recipes"]
        updated_ingredients = self.add_default_ingredients(ingredients)
        
        query = []
        
        filter = {}
        
        if skill is not None:
            filter["difficulty"] = {"$eq": skill}
        if max_time is not None:
            filter["total_time"] = {"$lte": max_time}
        if restrictions:
            filter["restrictions"] = {"$all": restrictions}
            
            
        if filter:
            query.append({"$match":filter})
        query.append({"$addFields":{"missing_count":{"$size":{"$filter": {"input": "$ingredients","as": "ingredient","cond": {"$not": {"$in": ["$$ingredient",list(updated_ingredients)]}}}}}}})
        query.append({"$match":{"missing_count":number}})

        return list(col.aggregate(query))
    
    def return_page_recipes_rec(self, ingredients, skill=None, max_time=None, restrictions=[]):
        recipes = []
        modified_recipes = []
        updated_ingredients = self.add_default_ingredients(ingredients)

        if skill == "Beginner":
            skill = "Easy"
        elif skill == "Intermediate":
            skill = "More effort"
        elif skill == "Advanced":
            skill = "A challenge"
        else:
            skill = None

        for i in range(5):
            given_recipes = self.get_recipes_missing_ingredients_rec(i, updated_ingredients, skill=skill, max_time=max_time, restrictions=restrictions)
            sorted_recipes = sorted(given_recipes, key=lambda x: len(x["ingredients"]), reverse=True)
            recipes.extend(sorted_recipes)
        for recipe in recipes:
            if int(recipe["missing_count"]) != len(recipe["ingredients"]):
                matching_ingredients = []
                unmatching_ingredients = []
                for ingredient in recipe["ingredients"]:
                    if ingredient in ingredients:
                        matching_ingredients.append(ingredient)
                    else:
                        unmatching_ingredients.append(ingredient)
                recipe["matching_ingredients"] = matching_ingredients
                recipe["unmatching_ingredients"] = unmatching_ingredients
                modified_recipes.append(recipe)
        return modified_recipes
    
if __name__ == "__main__":
    db = DatabaseClient()
    
    db.delete_all_users()
    
    db.delete_all_recipes()
    # inserting the recipes into the database
    df = pd.read_csv("webscraping/output/FINAL_recipes_servings_data.csv")
    nlp_model = NLP.NLP()
    p = inflect.engine()
    i = 0
    for row in df.iterrows():
        i += 1
        print(i / 6882)
        converted_ingredients = ast.literal_eval(row[1]["ingredients"])
        unique_ingredients = set()
        standardized_ingredients = []
        for ingredient in converted_ingredients:
            extracted_ingredient = nlp_model.extract_ingredient(ingredient).lower()
            extracted_ingredient = nlp_model.handle_corner_cases(extracted_ingredient)
            if extracted_ingredient != '':
                singular_ingredient = " ".join(word for word in extracted_ingredient.split())
                if singular_ingredient not in unique_ingredients:
                    unique_ingredients.add(singular_ingredient)
                    standardized_ingredients.append(singular_ingredient)

        converted_standardized_ingredients_dict = ast.literal_eval(row[1]["standardized_ingredients_dict"])
        converted_servings_dict = ast.literal_eval(row[1]["serves_dict"])

        try:
            servings = converted_servings_dict['serves']
        except:
            servings = ''

        methods = str(row[1]["methods"])

        methods = ast.literal_eval(methods)

        db.insert_recipe(row[1]["title"], row[1]["difficulty"], row[1]["vegetarian"], row[1]["vegan"], row[1]["dairy_free"], row[1]["keto"], row[1]["gluten_free"], standardized_ingredients, row[1]["picture_url"], converted_ingredients, methods, row[1]["recipe_urls"], int(row[1]["total_time"]), row[1]["makes"], row[1]["servings"])

    col = db.db["recipes"]
    col.create_index(["_id",1])