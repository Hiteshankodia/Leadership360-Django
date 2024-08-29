from pydantic import BaseModel
from typing import List

class FetchQuestionRequestSchema(BaseModel):
    participantid : int 
    surveyid : int 
    record_count : int 
    no_of_question : int 
    page_number : int 


class SubmitParticipantSurveyRequestSchema(BaseModel):
    participantid : int 
    surveyid : int    

class ParticipantSurvveyStatusUpdateSchema(BaseModel):
    participantid : int 
    surveyid : int 
    status : int

class QuestionAnswerPair(BaseModel):
    questionid: int
    answerid: int

class UpdateSurveyAnswers(BaseModel):
    participantid: int
    surveyid : int
    answers: List[QuestionAnswerPair]
    
class UpdateSurveyAnswerTeam(BaseModel):
    teammemberid : int 
    participantid: int
    answers: List[QuestionAnswerPair]    