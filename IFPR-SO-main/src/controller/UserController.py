import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.UsersModel import usersModel


class UsersController:
    def __init__(self):
        self.usersModel = usersModel
    
    def signup(self, userName, password):
        try:
            userId = self.usersModel.create(userName, password)
            
            return userId
        
        except Exception as e:
            raise e         
        
    def signin(self, userName, password):
        try:
            userId = self.usersModel.authenticate(userName, password)
            
            return userId
        
        except Exception as e:
            raise e     
        
userController = UsersController()