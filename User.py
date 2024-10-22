from DatabaseClient import DatabaseClient

class User:
    
    def __init__(self, emailId, password):
        self.db = DatabaseClient()
        user = self.db.user_login_valid(emailId, password)
        if user == "EmailId not found":
            raise Exception("EmailId not found")
        elif user == "Password incorrect":
            raise Exception("Password incorrect")
        else:
            self.emailId = emailId
            self.user = user
            
    def get_details(self):
        return self.user
        
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
        self.db.update_user_restrictions(self.emailId, restrictions)
        return 0
    
    def update_picture(self, picture):
        self.db.update_user_pic(self.emailId, picture)
        return 0
    
    def get_all_satisfied_recipes(self):
        pass
    
    def reset_password(self, new_password):
        self.db.update_user_password(self.emailId, new_password)
        return 0
    