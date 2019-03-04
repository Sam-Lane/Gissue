import os
import requests

"""
https://github.com/settings/tokens
uses githubs oAuth tokens
"""

class Auth():
   
    def __init__(self):
        
        self.home = os.path.expanduser("~")
        self.gissueFile = os.path.join(self.home, ".gissue")

        if os.path.exists(self.gissueFile):
            with open(self.gissueFile, "r") as file:
                self.token = file.readline().strip()
        else:
            with open(self.gissueFile, "w"):
                pass


    def update_token(self, tokenStr):
        self.token = tokenStr
        with open(self.gissueFile, "w") as file:
            file.write(self.token)
            

    def get_token(self):
        return self.token

    def gen_token(self, username, passwd):
        url = "https://api.github.com/authorizations"
        payload = "{\n  \"scopes\": [\n    \"repo\"\n  ],\n  \"note\": \"Gissue\"\n}"
        

        response = requests.request("POST", url, data=payload, auth=(username, passwd))
        if response.status_code == 201:
            token = response.json()['token']
            self.update_token(token)
        elif response.status_code == 422:
            print('You already have a code\nTry going to Github and deleting Gissue key from your account')
        elif response.status_code == 401:
            print('Access Denied\nWrong username or password')
        else:
            print('Something went wrong')

