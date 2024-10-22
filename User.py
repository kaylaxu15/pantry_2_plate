from DatabaseClient import DatabaseClient

class User:
    
    def __init__(self, username, password):
        self.db = DatabaseClient()
        user = self.db.user_login_valid(username, password)
        if user == "Username not found":
            raise Exception("Username not found")
        elif user == "Password incorrect":
            raise Exception("Password incorrect")
        else:
            self.username = username
            self.user = user
        
    def add_to_inventory(self, ingredientId):
        pass
    
    def remove_from_inventory(self, ingredientId):
        pass
    
    def complete_recipe(self, recipeId):
        pass
    
    def add_fav_recipe(self, recipeId):
        pass
    
    def remove_fav_recipe(self, recipeId):
        pass
    
    def update_restrictions(self, restrictions):
        self.db.update_user_restrictions(self.username, restrictions)
        return 0
    
    def update_picture(self, picture):
        self.db.update_user_pic(self.username, picture)
        return 0
    
    def get_all_satisfied_recipes(self):
        pass
    
    def reset_password(self, new_password):
        self.db.update_user_password(self.username, new_password)
        return 0
    