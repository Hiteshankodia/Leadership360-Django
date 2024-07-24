
from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.Schema.UserLoginSchema import UserLoginRequestSchema

class AuthServiceHelper: 
    def __init__(self):
        self.ApiBaseObj = ApiBase()
    
    def Login(self, userLoginRequestSchema : UserLoginRequestSchema):
        data = self.ApiBaseObj.ToJSON(userLoginRequestSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/auth/token', token='')
        

 