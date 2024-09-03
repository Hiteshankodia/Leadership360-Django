from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.utility.utility import UtilityClass
from app_360.Schema.Team.invite import TeamMemberInviteSchema

class TeamInviteClass():
    def __init__(self):
        self.ApiBaseObj = ApiBase()
        

    def TeamInvite(self, teamMemberInviteSchema : TeamMemberInviteSchema, token): 
        data = self.ApiBaseObj.ToJSON(teamMemberInviteSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/teammember/invite', token=token)
        
        
        