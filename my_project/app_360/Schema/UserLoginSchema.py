from pydantic import BaseModel

class UserLoginRequestSchema(BaseModel):
    username : str 
    password : str 
    company_id : int 