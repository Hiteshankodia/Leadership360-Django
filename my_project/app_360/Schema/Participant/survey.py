from pydantic import BaseModel
class FetchQuestionRequestSchema(BaseModel):
    participantid : int 
    surveyid : int 
    record_count : int 
    no_of_question : int 
    page_number : int 


class SubmitParticipantSurveyRequestSchema(BaseModel):
    participantid : int 
    surveyid : int    

