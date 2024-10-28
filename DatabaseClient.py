from pymongo import MongoClient
import pandas as pd

class DatabaseClient:
    
    def __init__(self):
        self.uri = "mongodb+srv://server:hHSsj4NSo5KqJcKB@princetonplateplanner.zggiw.mongodb.net/?retryWrites=true&w=majority&appName=PrincetonPlatePlanner"
        self.client = MongoClient(self.uri)
        self.db = self.client["PPP"]

    def insert_user(self, emailId, password, picture, restrictions, inventory, favRecipes):
        if self.check_emailId_taken(emailId):
            return 1
        col = self.db["Users"]
        dict = {"emailId": emailId, "password": password, "picture": picture, "restrictions": restrictions, "inventory": inventory, "favRecipes": favRecipes}
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
    
    def insert_recipe(self, title, difficulty, serves, vegetarian, vegan, dairy_free, keto, gluten_free, prep_time, cook_time, ingredients, picture_url):
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
        dict = {"title": title, "password": difficulty, "servings": serves, "restrictions": restrictions, "prep_time": prep_time, "cook_time": cook_time, "ingredients": ingredients, "picture_url": picture_url}
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
        if self.check_ingredient_taken(ingredient) == False:
            return 1
        col = self.db["Ingredients"]
        dict = {"ingredient":ingredient}
        col.insert_one(dict)
        return 0

    def get_all_ingredients(self):
        col = self.db["Ingredients"]
        results = col.find()
        return list(results)
    
    
if __name__ == "__main__":
    db = DatabaseClient()
    # db.delete_all_recipes()
    # db.insert_user("Niru", "Basketball", "pic", ["vegan", "gluten-free"], ["apple", "banana"], ["recipe1", "recipe2"])
    # db.update_user_password("Niru", "Mahaniru1234")
    # print(db.get_user("Niru"))
    # db.delete_user("Niru")

    # inserting the recipes into the database
    df = pd.read_csv("webscraping/output/recipes_data_2024-10-22.csv")

    for row in df.iterrows():
        db.insert_recipe(row[1]["title"], row[1]["difficulty"], row[1]["serves"], row[1]["vegetarian"], row[1]["vegan"], row[1]["dairy_free"], row[1]["keto"], row[1]["gluten_free"], row[1]["prep_time"], row[1]["cook_time"], row[1]["ingredients"], row[1]["picture_url"])
        for ingredient_list in row[1]["ingredients"]:
            ingredients = ingredient_list.split(',')

            for ingredient in ingredients:
                db.insert_ingredient(ingredient)

        
    

    