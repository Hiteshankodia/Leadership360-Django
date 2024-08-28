from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema
from app_360.Schema.Participant.survey import  UpdateSurveyAnswers
class Survey: 
    def __init__(self): 
        self.ApiBaseObj = ApiBase()
        self.utilityobj = UtilityClass()
        

    def displayquestions(self, fetchQuestionRequestSchema : FetchQuestionRequestSchema, token ): 
        data = self.ApiBaseObj.ToJSON(fetchQuestionRequestSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/fetchQuestion', token=token)
        
    def SubmitSurvey(self, submitParticipantSurveyRequestSchema : SubmitParticipantSurveyRequestSchema, token):
        data = self.ApiBaseObj.ToJSON(submitParticipantSurveyRequestSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/submitParticipantSurvey', token = token)
    
    def SaveSurveyAnswers(self, survey_data, token):
        return self.ApiBaseObj.PostRequest(data = survey_data, url = '/participantsurvey/savequestions', token = token)
    
    def FetchMilestoneMessage(self, survey_id, token):
        data = {'surveyid': int(survey_id)}
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/fetchmilestonemessage', token = token)       
  
    def PreviewSurvey(self, previewParticipantSurvey, token ):
        data = self.ApiBaseObj.ToJSON(previewParticipantSurvey)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/previewParticipantSurvey', token = token)
    

    def ParticipantUpdateSurveyStatus(self, participantSurvveyStatusUpdateSchema : ParticipantSurvveyStatusUpdateSchema):
        data = self.ApiBaseObj.ToJSON(participantSurvveyStatusUpdateSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/updateSurveyStatus', token = '')
    
    def UpdateSurveyAnswer(self, update_survey_answers : UpdateSurveyAnswers): 
        data = self.ApiBaseObj.ToJSON(update_survey_answers)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/updatesurveyanswers', token = '')
    
        