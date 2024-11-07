from DatabaseClient import DatabaseClient
from User import User
import re

class Client:
    def __init__(self):
        self.db = DatabaseClient()
        self.user = None
        self.islogin = False
        
    def is_valid_email(self, emailId):
        # Found from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/#
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
        user = self.db.user_login_valid(emailId, password)
        if user == "EmailId not found":
            raise Exception("EmailId not found")
        elif user == "Password incorrect":
            raise Exception("Password incorrect")
        else:
            self.user = user
        self.islogin = True
        print("Login Successful")
        
    def logout(self):
        if self.islogin == False:
            print("Not logged in")
            return 1
        self.user = None
        self.islogin = False
        print("Logout Successful")
        
    def delete_account(self):
        if self.islogin == False:
            print("Not logged in")
            return 1
        emailId = self.user.get_details()["emailId"]
        self.db.delete_user(emailId)
        print("Account Deleted")
        
        
if __name__ == "__main__":
    c = Client()
    c.create_account("Hello@gmail.com", "World")
    print(c.user.get_details())
    # c.logout()
    # c.logout()
    # c.delete_account()
    # c.login()
        
        
    
        
        
