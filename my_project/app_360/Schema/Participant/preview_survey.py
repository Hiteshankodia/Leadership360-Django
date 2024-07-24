
from pydantic import BaseModel
class PreviewParticipantSurvey(BaseModel):
    participantid : int 
    surveyid : int 



class SaveParticipantSurvey(BaseModel):
    participantid : int 
    surveyid : int 