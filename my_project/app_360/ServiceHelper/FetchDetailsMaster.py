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
        


    def FetchState(self): 
        url = '/masterdata/fetchstate'
        response = self.apibaseobj.GetRequest(url)
        states = response.json()  
        return states