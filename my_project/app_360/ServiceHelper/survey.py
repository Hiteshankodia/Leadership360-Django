from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema

class Survey: 
    def __init__(self): 
        self.ApiBaseObj = ApiBase()
        self.utilityobj = UtilityClass()
        

    def displayquestions(self, fetchQuestionRequestSchema : FetchQuestionRequestSchema): 
        data = self.ApiBaseObj.ToJSON(fetchQuestionRequestSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/fetchQuestion', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ1NTA0NzAsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.ZKoYbkMX7GMfnfHih-EmBpz-JylzAlqngHzGHNNwY6c')
        
    def SubmitSurvey(self, submitParticipantSurveyRequestSchema : SubmitParticipantSurveyRequestSchema):
        data = self.ApiBaseObj.ToJSON(submitParticipantSurveyRequestSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/submitParticipantSurvey', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3OTY1OTgsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.NUjCe1z4iX47nLrrOwdvw3mn8neVxV9lEQfWkVzGrjU')
    
    def SaveSurveyAnswers(self, survey_data):
        return self.ApiBaseObj.PostRequest(data = survey_data, url = '/participantsurvey/savequestions', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3OTY1OTgsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.NUjCe1z4iX47nLrrOwdvw3mn8neVxV9lEQfWkVzGrjU')
    
    def FetchMilestoneMessage(self, survey_id):
        data = {'surveyid': int(survey_id)}
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/fetchmilestonemessage', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3OTY1OTgsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.NUjCe1z4iX47nLrrOwdvw3mn8neVxV9lEQfWkVzGrjU')       
  
    def PreviewSurvey(self, previewParticipantSurvey):
        data = self.ApiBaseObj.ToJSON(previewParticipantSurvey)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/previewParticipantSurvey', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3OTY1OTgsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.NUjCe1z4iX47nLrrOwdvw3mn8neVxV9lEQfWkVzGrjU')
    

    def ParticipantUpdateSurveyStatus(self, participantSurvveyStatusUpdateSchema : ParticipantSurvveyStatusUpdateSchema):
        data = self.ApiBaseObj.ToJSON(participantSurvveyStatusUpdateSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/updateSurveyStatus', token = '')
    

        