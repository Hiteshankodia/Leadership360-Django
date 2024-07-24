from pydantic import BaseModel
from datetime import date
from typing import List


class ParticipantInviteRequestSchema(BaseModel):
    name: List[str]
    designation: List[str]
    department: List[int]
    location: List[str]
    email: List[str]
    dob: List[date]
    country: List[int]
    state: List[int]

    