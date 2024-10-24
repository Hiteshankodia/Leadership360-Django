
from pydantic import BaseModel
class PreviewParticipantSurvey(BaseModel):
    participantid : int 
    surveyid : int 



class SaveParticipantSurvey(BaseModel):
    participantid : int 
    surveyid : int 
    companyid : int

class TeamPreviewParticipantSurvey(BaseModel):
    participantid : int 
    teammemberid : int 
    surveyid : int    