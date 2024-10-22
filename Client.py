from DatabaseClient import DatabaseClient
from User import User
import re

class Client:
    def __init__(self):
        self.db = DatabaseClient()
        self.user = None
        self.islogin = False
        
    def is_valid_email(self, emailId):
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', emailId)
        return valid
                
    def validate_email(self, emailId):
        pass
        
    def create_account(self, emailId, password):
        if not self.is_valid_email(emailId):
            print("Invalid Email")
            return 1
        return_code = self.db.insert_user(emailId, password, "", [], [], [])
        if return_code == 1:
            print("Email already taken")
            return 1
        print("Account Created")
        self.login(emailId, password)
        
    def login(self, emailId, password):
        self.user = User(emailId, password)
        self.islogin = True
        print("Login Successful")
        
    def delete_account(self):
        if self.islogin == False:
            return 1
        emailId = self.user.get_details()["emailId"]
        self.db.delete_user(emailId)
        print("Account Deleted")
        
        
if __name__ == "__main__":
    c = Client()
    c.create_account("Hello@gmail.com", "World")
    print(c.user.get_details())
    c.delete_account()
        
        
    
        
        
