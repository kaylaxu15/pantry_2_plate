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
            self.user = user
        
    