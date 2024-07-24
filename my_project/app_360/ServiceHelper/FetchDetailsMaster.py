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
        if response.status_code == 200:
            countries = response.json()  
            print(countries)
            return countries
        else:
            print(f"Failed to fetch countries. Status code: {response.status_code}")


    def FetchState(self, country_id ):
          
        state_request = {'id': int(country_id)}  # Create StateRequestSchema with 'id'
        response = requests.post('http://localhost:5000/masterdata/fetchstate', json=state_request)
        response.raise_for_status()  # Raise exception for any HTTP error (4xx or 5xx)
        states = response.json()
        print(states)
        return JsonResponse(states, safe=False) 