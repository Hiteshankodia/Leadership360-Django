from django.shortcuts import render, redirect
from app_360.ServiceHelper.FetchDetailsMaster import FetchMasterData
import json
from app_360.ServiceHelper.ParticipantInviteServiceHelper import ParticipantInviteServiceHelperClass
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app_360.Schema.master_data import StateRequestSchema
from app_360.Schema.Participant.participant_invite import ParticipantInviteRequestSchema
import requests
#from fastapi.encoders import jsonable_encoder


fetchmasterobj = FetchMasterData()
participantInviteServiceHelperObj = ParticipantInviteServiceHelperClass()

def ParticipantDeatils(request):
    countries = fetchmasterobj.FetchCountry()
    context = {
        'countries': countries,
        'itereration' : range(1,6), 
        'departments' : ['HR', 'Data Science', 'Data Engineering', 'Softwares']
    }
    return render(request, 'Participant/invite.html', context)


def load_states(request):
    country_id = request.POST.get('country_id')
    states = fetchmasterobj.FetchState(country_id)
    return states
 


def save_data(request):
    if request.method == 'POST':
        names = request.POST.getlist('txtnamename')
        emails = request.POST.getlist('txtnameEmail')
        

        designations = request.POST.getlist('txtnamedesignation')
        departments = request.POST.getlist('intnamedepartment')
        locations = request.POST.getlist('txtnamelocation')
        
        dobs = request.POST.getlist('datenamedob')
        countries = request.POST.getlist('intnamecountry')
        states = request.POST.getlist('intnamestate')
        country_names = request.POST.getlist('country_name[]')  # Get country names
        state_names = request.POST.getlist('state_name[]')  # Get state names


        names = [name for name in names if name.strip()]
        




        print(names)
        participants = []
        for i in range(len(names)):
            participant = {
                'name': names[i],
                'designation': designations[i],
                'department': departments[i],
                'location': locations[i].upper(),
                'email': emails[i],
                'dob': dobs[i], 
                'country': country_names[i],
                'state': state_names[i],
                'country_id' : countries[i], 
                'state_id' : states[i]
            }
            participants.append(participant)
        print('participants', participants)
        context = {
            'participants': participants,
            
        }
        
        return render(request, 'Participant/preview.html', context)
    
def ParticipantInvite(request):
    print("participant invite")

    if request.method == 'POST':
        names = request.POST.getlist('names[]')
        designations = request.POST.getlist('designations[]')
        departments = request.POST.getlist('departments[]')
        locations = request.POST.getlist('locations[]')
        emails = request.POST.getlist('emails[]')
        dobs = request.POST.getlist('dobs[]')
        countries = request.POST.getlist('countries')
        states = request.POST.getlist('states')
        
        
        participants = []
        for i in range(len(names)):
            participant = {
                'name': names[i],
                'designation': designations[i],
                'department': departments[i],
                'location': locations[i].upper(),
                'email': emails[i],
                'dob': dobs[i], 
                'country_id': countries[i],
                'state_id': states[i],
                'country' : countries[i], 
                'dobs' : dobs[i]
            }
            participants.append(participant)
        print('After Preview - ')    
        print('participants', participants)

        # Convert participants list to desired format 
        data = []
        for participant in participants:
            data.append({
                "company_id": int(request.COOKIES.get('company_id')),
                "name": participant["name"],
                "email": participant["email"],
                "phone": '',
                "country_code": int(participant["country_id"]),
                "state": int(participant["state_id"]),
                "city": 1,
                "department": participant["department"],
                "experience": 0,
                "created_by": 2,
                "login_history_id": 0, 
                'dob' : participant["dobs"], 
                "designation" : participant['designation'], 
                "location" : participant["location"]
            })
        
        response = participantInviteServiceHelperObj.ParticipantInvite(data)
        response = response.json()
        # Print the response from the server
        print(response) 
        if response['StatusCode'] == 1:
            return render(request, 'Participant/thankyou.html')
        elif response['StatusCode'] == 2: 
            pass
            
         
