from django.http import HttpResponse
from django.shortcuts import render

def set_participant_id(request, participantid: int):
    response = HttpResponse("Cookie is set!")
    response.set_cookie('participantid', participantid, max_age=3600)
    return response

def get_participant_id(request):
    participant_id = request.COOKIES.get('participantid')
    if participant_id:
        response_text = str(participant_id)
    else:
        response_text = "2"
    return HttpResponse(response_text)




'''from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from requests.exceptions import HTTPError
#from .ServiceHelper.AuthServiceHelper import ApiRequestHelper
from django.http import HttpRequest, JsonResponse
from pydantic import ValidationError
#from .Controller.authcontroller import AuthClass

#authobj = AuthClass()

def index(request):
    #return HttpResponse("Hello, world. This is my first Django app!")
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def call_fastapi_endpoint(data):
    print('Hello')

    url = 'http://localhost:5000/auth/token'  # Replace with your FastAPI endpoint URL
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(response)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return JSON response as Python dict
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None    
    


#api_helper = ApiRequestHelper()

# Example usage in a Django view
def apihelper(request : HttpRequest):
    if request.method == 'POST':
        form_data = request
        print(form_data)
        print(form_data.companyid)     
        data = {
            "username": form_data.username,
            "password": form_data.password, 
            "company_id": form_data.companyid
        }
        endpoint = 'http://localhost:5000/auth/token'  # Replace with your FastAPI endpoint URL
    
        # Call FastAPI endpoint
        #response_data = api_helper.PostRequest(endpoint ,data)
        #return response.json()
    return render(request, 'api.html')  
    

def auth(request  : HttpRequest):
    print('Views')
    if request.method == 'POST':
        form_data = request 
        #form_data = UserLoginRequestSchema(**request.POST.dict())

        print(form_data.username)
        
        #response = authobj.Auth(form_data)
    
    return render(request, 'api.html') 
'''