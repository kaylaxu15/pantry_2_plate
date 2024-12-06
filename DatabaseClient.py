from pymongo import MongoClient
import pandas as pd
import ast
from bson import ObjectId
import ssl
import json
import re

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
        if self.check_emailId_taken(emailId) == False:
            return 1
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
        return col.find_one({"_id": ObjectId(recipe_id)})
    
    def insert_recipe(self, title, difficulty, serves, vegetarian, vegan, dairy_free, keto, gluten_free, prep_time, cook_time, ingredients, picture_url, ingredients_dict, actual_ingredients, methods, recipe_urls, total_time, makes, servings):
        
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
        dict = {"title": title, "difficulty": difficulty, "servings": serves, "restrictions": restrictions, "prep_time": prep_time, "cook_time": cook_time, "ingredients": ingredients, "picture_url": picture_url, "ingredients_dict": ingredients_dict, "actual_ingredients":actual_ingredients, "methods":methods, "recipe_urls":recipe_urls, "total_time":total_time, "makes":makes, "servings":servings}
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
    
    
    def filter_recipes(self, skill=None, max_time=None, restrictions=[]):
        col = self.db["Recipes"] 
        query = {}
        if skill and max_time is not None:
            query = {"difficulty": {"$eq": skill}, "total_time": {"$lte": max_time}, "restrictions": {"$all": restrictions}}
        elif skill:
            query = {"difficulty": {"$eq": skill}, "restrictions": {"$all": restrictions}}
        elif max_time:
            query = {"total_time": {"$lte": max_time}, "restrictions": {"$all": restrictions}}
       
        results = col.find(query)
        return list(results) 
    
        
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

        query = [
            {
                "$addFields": {
                    "matching_ingredients": {
                        "$filter": {
                            "input": "$ingredients",
                            "as": "ingredient",
                            "cond": {"$in": ["$$ingredient", list(updated_ingredients)]}
                        }
                    },
                    "missing_ingredients": {
                        "$filter": {
                            "input": "$ingredients",
                            "as": "ingredient",
                            "cond": {"$not": {"$in": ["$$ingredient", list(updated_ingredients)]}}
                        }
                    },
                }
            },
            # Add a field to count missing ingredients
            {
                "$addFields": {
                    "missing_count": {"$size": "$missing_ingredients"}
                }
            },
            # Match recipes with the specified number of missing ingredients
            {
                "$match": {"missing_count": number}
            },
            # Project the desired fields
            {
                "$project": {
                    "_id": 0,
                    "recipe_name": 1,  # Include the recipe name
                    "matching_ingredients": 1,
                    "missing_ingredients": 1
                }
            }
        ]

        return list(col.aggregate(query))
    
    def return_page_recipes(self, ingredients):
        recipes = []
        modified_recipes = []
        updated_ingredients = self.add_default_ingredients(ingredients)

        for i in range(10):
            recipes.extend(self.get_recipes_missing_ingredients(i, updated_ingredients))
        for recipe in recipes:
            print("RECIPE", recipe)
            if int(recipe["missing_count"]) != len(recipe["ingredients"]):
                modified_recipes.append(recipe)
        return modified_recipes
    
if __name__ == "__main__":
    db = DatabaseClient()
    # db.delete_all_ingredients()
    # db.delete_all_recipes()
    # recipes = db.get_recipes_ingredients(['cocoa powder'])
    # for recipe in recipes:
    #    print(db.return_recipe(recipe["_id"]))
    # for recipe in missing_recipes:
    #    print(recipe)
    #    print()
    
    #db.insert_user("Niru", "Basketball", "pic", ["vegan", "gluten-free"], ["apple", "banana"], ["recipe1", "recipe2"])
    # db.update_user_password("Niru", "Mahaniru1234")
    # print(db.get_user("Niru"))
    # db.delete_user("Niru")

    # missing_recipes = db.return_page_recipes(['egg', 'butter'])
    # db.delete_all_recipes()
    # # inserting the recipes into the database
    # df = pd.read_csv("/Users/kaylaxu/princeton_plate_planner/webscraping/output/2024-11-27_final_recipes_servings_data.csv")

    # for row in df.iterrows():
    #     converted_ingredients = ast.literal_eval(row[1]["ingredients"])
    #     #converted_methods = ast.literal_eval(row[1]["methods"])
    #     converted_standardized_ingredients_dict = ast.literal_eval(row[1]["standardized_ingredients_dict"])
    #     converted_servings_dict = ast.literal_eval(row[1]["serves_dict"])

    #     try:
    #         servings = converted_servings_dict['serves']
    #     except:
    #         servings = ''


    #     methods = str(row[1]["methods"])
    #     # print(row[1]["title"])
    #     # print(methods)
    #     # regexp = re.compile(r"[a-z]+[\'][a-z]+")
    #     # methods = re.sub(r'(\w{2})\'([a-z]+)', r'\1\2', methods)
    #     # methods = methods.replace("\'", "\"")
  
    #     methods = ast.literal_eval(methods)

    #     db.insert_recipe(row[1]["title"], row[1]["difficulty"], servings, row[1]["vegetarian"], row[1]["vegan"], row[1]["dairy_free"], row[1]["keto"], row[1]["gluten_free"], row[1]["prep_time"], row[1]["cook_time"], ast.literal_eval(row[1]["standardized_ingredients"]), row[1]["picture_url"], 
    #                      converted_standardized_ingredients_dict, converted_ingredients, methods, 
    #                      row[1]["recipe_urls"], row[1]["total_time"], row[1]["makes"], row[1]["servings"])
    db.add_user_reviews()