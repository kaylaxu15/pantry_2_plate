from pymongo import MongoClient

class DatabaseClient:
    
    def __init__(self):
        self.uri = "mongodb+srv://server:hHSsj4NSo5KqJcKB@princetonplateplanner.zggiw.mongodb.net/?retryWrites=true&w=majority&appName=PrincetonPlatePlanner"
        self.client = MongoClient(self.uri)
        self.db = self.client["PPP"]

    def insert_user(self, username, password, picture, restrictions, inventory, favRecipes):
        if self.check_username_taken(username):
            return 1
        col = self.db["Users"]
        dict = {"username": username, "password": password, "picture": picture, "restrictions": restrictions, "inventory": inventory, "favRecipes": favRecipes}
        col.insert_one(dict)
        return 0
        
    def delete_user(self, username):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.delete_one({"username": username})
        return 0
        
    def update_user_pic(self, username, picture):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"username": username}, {"$set": {"picture": picture}})
        return 0
        
    def update_user_restrictions(self, username, restrictions):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"username": username}, {"$set": {"restrictions": restrictions}})
        
    def update_user_inventory(self, username, inventory):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"username": username}, {"$set": {"inventory": inventory}})
        
    def update_user_password(self, username, password):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"username": username}, {"$set": {"password": password}})
        
    def update_user_favRecipes(self, username, favRecipes):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        col.update_one({"username": username}, {"$set": {"favRecipes": favRecipes}})
        
    def check_username_taken(self, username):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        return col.find_one({"username": username}) != None
    
    def get_user(self, username):
        if self.check_username_taken(username) == False:
            return 1
        col = self.db["Users"]
        return col.find_one({"username": username})
    
if __name__ == "__main__":
    db = DatabaseClient()
    print(db.check_username_taken("Niru"))
    db.insert_user("Niru", "Basketball", "pic", ["vegan", "gluten-free"], ["apple", "banana"], ["recipe1", "recipe2"])
    db.update_user_password("Niru", "Mahaniru1234")
    print(db.get_user("Niru"))
    db.delete_user("Niru")
    