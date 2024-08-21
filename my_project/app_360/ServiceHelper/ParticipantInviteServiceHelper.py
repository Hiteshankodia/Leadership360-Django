#from app_360.Schema.Participant.participant_invite import ParticipantInviteSchema
from app_360.ServiceHelper.ApiBase import ApiBase
import json 
import requests

class ParticipantInviteServiceHelperClass: 
    def __init__(self):
        self.ApiBaseObj = ApiBase()
    

    def ParticipantInvite(self, data, token):
        json_data = json.dumps(data)
       
        
        
        url = ApiBase.GetBaseUrl(self) + '/participant/invite'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'  
        }

        response =  requests.post(url, headers=headers, data=json_data)
        print(response)
        return response
        

    