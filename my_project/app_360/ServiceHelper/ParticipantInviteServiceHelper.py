#from app_360.Schema.Participant.participant_invite import ParticipantInviteSchema
from app_360.ServiceHelper.ApiBase import ApiBase
import json 
import requests

class ParticipantInviteServiceHelperClass: 
    def __init__(self):
        self.ApiBaseObj = ApiBase()
    

    def ParticipantInvite(self, data):
        json_data = json.dumps(data)

        # JWT token to append
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUyMzA4MjcsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.bx_4ccCt4BvkuTgLFkgQwdSU0JY3UCHjK5MVhJlWc5E"

        # Example of sending this JSON data to the server
        url = 'http://localhost:5000/participant/invite'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'  # Append token as Authorization header
        }

        return requests.post(url, headers=headers, data=json_data)

        #return self.ApiBaseObj.PostRequest(data = json_data, url = '/participant/invite', token=token)


    