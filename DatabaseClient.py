from pymongo import MongoClient
import pandas as pd
import ast
from bson import ObjectId

class DatabaseClient:
    
    def __init__(self):
        self.uri = "mongodb+srv://server:hHSsj4NSo5KqJcKB@princetonplateplanner.zggiw.mongodb.net/?retryWrites=true&w=majority&appName=PrincetonPlatePlanner"
        self.client = MongoClient(self.uri)
        self.db = self.client["PPP"]

    def insert_user(self, emailId, password, picture="", restrictions=[], inventory=[], favRecipes=[], wishList=[], completed=[]):
        if self.check_emailId_taken(emailId):
            return 1
        col = self.db["Users"]
        dict = {"emailId": emailId, "password": password, "picture": picture, "restrictions": restrictions, "inventory": inventory, "favRecipes": favRecipes, "wishList":wishList, "completed":completed}
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
    
    # return the favRecipes of a user
    def get_favRecipes(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId})
        if user:
            return user["favRecipes"]
        else:
            return None
        
    # remove a recipe from favorites
    def remove_favRecipe(self, emailId, recipe_id):
        col = self.db["Users"]
        col.update_one({"emailId": emailId}, {"$pull": {"favRecipes": recipe_id}})

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

    # return the completed recipeIDs of a user
    def get_completed(self, emailId):
        col = self.db["Users"]
        user = col.find_one({"emailId": emailId})
        if user:
            return user["completed"]
        else:
            return None
        
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
    
    def delete_all_recipes(self):
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
    
    def filter_recipes(self, skill=None, max_time=None):
        col = self.db["Recipes"] 
        query = {}
        if skill and max_time is not None:
            query = {"difficulty": {"$eq": skill}, "total_time": {"$lte": max_time}}
        elif skill:
            query = {"difficulty": {"$eq": skill}}
        elif max_time is not None:
            query = {"total_time": {"$lte": max_time}}
        results = col.find(query)
        return list(results)
    
    def get_recipes_missing_ingredients(self, number, ingredients):
        col = self.db["Recipes"]
        query = [{"$addFields": {"missing_count": {"$size": {"$filter": {"input": "$ingredients","as": "ingredient","cond": {"$not": {"$in": ["$$ingredient", ingredients]}}}}}}},{"$match": {"missing_count": number}}]
        return list(col.aggregate(query))
    
    def return_page_recipes(self, ingredients):
        recipes = []
        for i in range(5):
            recipes.extend(self.get_recipes_missing_ingredients(i, ingredients))
        return recipes
    
    
if __name__ == "__main__":
    db = DatabaseClient()
    # db.delete_all_ingredients()
    # db.delete_all_recipes()
    # recipes = db.get_recipes_ingredients(['cocoa powder'])
    # for recipe in recipes:
    #    print(db.return_recipe(recipe["_id"]))
    missing_recipes = db.return_page_recipes(['egg', 'butter'])
    for recipe in missing_recipes:
       print(recipe)
       print()
    # db.delete_all_recipes()
    #db.insert_user("Niru", "Basketball", "pic", ["vegan", "gluten-free"], ["apple", "banana"], ["recipe1", "recipe2"])
    # db.update_user_password("Niru", "Mahaniru1234")
    # print(db.get_user("Niru"))
    # db.delete_user("Niru")

    # # inserting the recipes into the database
    # df = pd.read_csv("webscraping/output/final_recipes_servings_data_2024-11-11.csv")

    # for row in df.iterrows():
    #     converted_ingredients = ast.literal_eval(row[1]["ingredients"])
    #     converted_methods = ast.literal_eval(row[1]["methods"])
    #     converted_standardized_ingredients_dict = ast.literal_eval(row[1]["standardized_ingredients_dict"])
    #     # print(converted_standardized_ingredients_dict)
    #     converted_servings_dict = ast.literal_eval(row[1]["serves_dict"])

    #     try:
    #         servings = converted_servings_dict['serves']
    #     except:
    #         servings = ''
        
    #     db.insert_recipe(row[1]["title"], row[1]["difficulty"], servings, row[1]["vegetarian"], row[1]["vegan"], row[1]["dairy_free"], row[1]["keto"], row[1]["gluten_free"], row[1]["prep_time"], row[1]["cook_time"], list(converted_standardized_ingredients_dict.keys()), row[1]["picture_url"], converted_standardized_ingredients_dict, converted_ingredients, row[1]["methods"], row[1]["recipe_urls"], row[1]["total_time"], row[1]["makes"], row[1]["servings"])