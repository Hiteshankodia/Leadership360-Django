from typing import List, Optional
from pydantic import BaseModel

class QuestionRequestSchema(BaseModel):
    questionid: int
    answerid: int
    presequencesurveyrequestid : int

class SaveQuestionRequestSchema(BaseModel):
    surveyid: int
    participantid : int 
    questionresponse: List[QuestionRequestSchema]
    teammemberid : Optional[int] = None