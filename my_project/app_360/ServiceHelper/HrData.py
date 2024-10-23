from app_360.ServiceHelper.ApiBase import ApiBase


class HrDataClass: 
    def __init__(self):
        self.apibaseobj = ApiBase()
         
    def FetchSurveyStatus(self, company_id): 
        data = {'companyid': int(company_id)}
        return self.apibaseobj.PostRequest(data = data, url = '/hrdatarouter/surveystatus', token = '')       
  
    def DownloadPDFSurveyDetails(self, company_id) : 
        data = {'companyid': int(company_id)}
        return self.apibaseobj.PostRequest(data = data, url = '/hrdatarouter/participant_survey_data_download', token = '') 
    
    def HRDashboardData(self, company_id) : 
        data = {'companyid': int(company_id)}
        return self.apibaseobj.PostRequest(data = data, url = '/hrdatarouter/hrdashboarddata', token = '') 
