from pydantic import BaseModel 

class TeamFetchQuestionSchema(BaseModel):
    participantid : int 
    surveyid : int 
    record_count : int 
    no_of_question : int 
    page_number : int 
    teammemberid : int
 
class TeamMemberSurveyIds(BaseModel):
    participantid : int 
    teammemberid : int 
    surveyid : int 