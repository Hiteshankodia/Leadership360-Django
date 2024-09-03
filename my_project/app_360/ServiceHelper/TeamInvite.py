from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.utility.utility import UtilityClass
from app_360.Schema.Team.invite import TeamMemberInviteSchema
import requests
class TeamInviteClass():
    def __init__(self):
        self.ApiBaseObj = ApiBase()
        

    def TeamInvite(self, teamMemberInviteSchema : TeamMemberInviteSchema): 
        data = self.ApiBaseObj.ToJSON(teamMemberInviteSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/teammember/invite', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUyMzA4MjcsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.bx_4ccCt4BvkuTgLFkgQwdSU0JY3UCHjK5MVhJlWc5E')
        
        
        