from pydantic import BaseModel, EmailStr
from typing import List

class TeamMemberInvitedDetailSchema(BaseModel):
    name: str 
    email : EmailStr
    phone : str 
    location : str 
    designation : int 
    state : int 
    country : int 


class TeamMemberInviteSchema(BaseModel):
    participantid : int 
    teammembers : List[TeamMemberInvitedDetailSchema]    