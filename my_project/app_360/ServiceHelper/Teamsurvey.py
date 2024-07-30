from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema
from app_360.Schema.Team.survey import TeamFetchQuestionSchema, TeamMemberSurveyIds

class Survey: 
    def __init__(self): 
        self.ApiBaseObj = ApiBase()
        self.utilityobj = UtilityClass()
        
    def TeamMemberAssignSurvey(self, teamMemberSurveyIds : TeamMemberSurveyIds):
        data = self.ApiBaseObj.ToJSON(teamMemberSurveyIds)
        return self.ApiBaseObj.PostRequest(data = data, url = '/surveyteammember/teammemberassign', token='')
    

    def displayquestions(self, teamFetchQuestionSchema : TeamFetchQuestionSchema):
        print("Display questions Method! ") 
        data = self.ApiBaseObj.ToJSON(teamFetchQuestionSchema)
        return self.ApiBaseObj.PostRequest(data = data, url = '/surveyteammember/fetchQuestion', token='')
    
    
    def FetchMilestoneMessage(self, survey_id):
        data = {'surveyid': int(survey_id)}
        return self.ApiBaseObj.PostRequest(data = data, url = '/participantsurvey/fetchmilestonemessage', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3OTY1OTgsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.NUjCe1z4iX47nLrrOwdvw3mn8neVxV9lEQfWkVzGrjU')       
  