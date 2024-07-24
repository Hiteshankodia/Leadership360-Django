from app_360.ServiceHelper.ApiBase import ApiBase
import requests
from django.http import JsonResponse
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.participant_invite import ValidateParticipantDetailsSchema, CreateUserRequestSchema

class ParticipantSurvey: 
    def __init__(self):
        self.ApiBaseObj = ApiBase()
        self.utilityobj = UtilityClass()
        

    def fetchparticipantid(self, pid_encoded):
        participantid = self.utilityobj.decrypt(pid_encoded)
        print('participantid', participantid)
        participantidrequest = {'participantid': int(participantid)}
        response = self.ApiBaseObj.PostRequest(data = participantidrequest, url='/participant/checkparticipantexist', token='')
        return response
    

    def CheckParticipantDetails(self,validateParticipantDetailsSchema : ValidateParticipantDetailsSchema):
        #participantid = self.utilityobj.decodedata(pid_encoded=pid_encoded)
        data = self.ApiBaseObj.ToJSON(validateParticipantDetailsSchema)
        print(data)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participant/verifyparticipantdetails', token='')
        

    def CreateUser(self, createUserRequestSchema : CreateUserRequestSchema):
        data = self.ApiBaseObj.ToJSON(createUserRequestSchema)
        print('Create User Date' , data)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participant/createuser', token='')
    
    

    