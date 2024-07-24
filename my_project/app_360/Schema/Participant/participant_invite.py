from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date 

class EmployeeData(BaseModel):
    name: str
    designation: str
    department: int
    location: str
    email: str
    dob: str
    country: int
    state : int

class ParticipantInviteRequestSchema(BaseModel):
    company_id: Optional[int]
    name: str
    email: EmailStr
    phone: str  # Assuming a 10-digit phone number
    country_code: int
    state: int
    city: int
    department: str
    experience: float
    created_by: Optional[int]
    login_history_id: Optional[int]


class ValidateParticipantDetailsSchema(BaseModel):
    email: str
    dob: str
    participantid: int
    companyid: int


class CreateUserRequestSchema(BaseModel):
    participantid : int 
    username : str 
    password : str 
    companyid : int