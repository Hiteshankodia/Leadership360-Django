from app_360.ServiceHelper.ApiBase import ApiBase
from app_360.Schema.master_data import StateRequestSchema
import requests
from django.http import JsonResponse


class FetchMasterData:
    def __init__(self):
        self.apibaseobj = ApiBase()
        
    def FetchCountry(self):
        url = '/masterdata/fetchcountry'
        response = self.apibaseobj.GetRequest(url)
        countries = response.json()  
        return countries
        


    def FetchState(self, country_id ): 
        state_request = {'id': int(country_id)}  
        url = ApiBase.GetBaseUrl(self)
        response = requests.post( url + '/masterdata/fetchstate', json=state_request)
        response.raise_for_status()  
        states = response.json()
        return JsonResponse(states, safe=False)  