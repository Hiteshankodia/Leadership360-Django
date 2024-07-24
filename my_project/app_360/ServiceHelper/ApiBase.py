
from app_360.Schema.UserLoginSchema import UserLoginRequestSchema
from django.conf import settings
import requests
import json

class ApiBase: 
    def __init__(self):
        pass
         
    def ToJSON(self, userLoginRequestSchema : UserLoginRequestSchema):
        return userLoginRequestSchema.dict()

    def GetBaseUrl(self):
        return settings.AUTH_TOKEN_ENDPOINT 


    def PostRequest(self, data, url, token):
        endpoint = self.GetBaseUrl() + url
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        print(endpoint)

        response = requests.post(endpoint, json=data, headers=headers)
        #print('response', response)
        #print(response.json())  
        return response.json() 
    
    def GetRequest(self, url, token=None):
        endpoint = self.GetBaseUrl() + url
        print(endpoint)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        response = requests.get(endpoint, headers=headers)
        return response
    
    
    


   