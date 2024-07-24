from django.shortcuts import render, redirect
from app_360.ServiceHelper.FetchDetailsMaster import FetchMasterData
from django.conf import settings
import json
from app_360.Schema.Team.invite import TeamMemberInvitedDetailSchema, TeamMemberInviteSchema
import requests

fetchmasterobj = FetchMasterData()

def TeamFormDetails(request):
    countries = fetchmasterobj.FetchCountry()
    context = {
        'countries': countries,
        'itereration' : range(1,7), 
        'teamtype':  (eval(settings.TEAM_TYPE))
    }
    return render(request, 'Team/team_invite.html', context)


def load_states(request):
    country_id = request.POST.get('country_id')
    states = fetchmasterobj.FetchState(country_id)
    return states


def SaveData(request):
    if request.method == 'POST':
        names = request.POST.getlist('txtnamename')
        emails = request.POST.getlist('txtnameEmail')
        contacts = request.POST.getlist('txtnamecontact')
        locations = request.POST.getlist('txtnamelocation')
        teamtypes = request.POST.getlist('intnameteamtype')
        countries = request.POST.getlist('intnamecountry')
        states = request.POST.getlist('intnamestate')
        country_names = request.POST.getlist('country_name[]')
        state_names = request.POST.getlist('state_name[]')
        teamtype_name_list = []
        for i in teamtypes:
            teamtype_name_list.append(eval(settings.TEAM_TYPE)[int(i)])
        
 
        TeamInviteList = []
        for i in range(len(names)): 
            teamdata = { 
                'name': names[i],
                'email': emails[i],
                'contact': contacts[i], 
                'location': locations[i].upper(),
                'country': country_names[i],
                'state': state_names[i],
                'country_id' : countries[i], 
                'state_id' : states[i], 
                'teamtype_name' : teamtype_name_list[i], 
                'teamtype_id' : teamtypes[i]
            }
            TeamInviteList.append(teamdata)
        print('participants', teamdata) 
        context = {
            'TeamInviteList': TeamInviteList,
            
        }
        
        return render(request, 'Team/invite_preview.html', context)


def TeamInvite(request):
    if request.method == 'POST':
        names = request.POST.getlist('names[]')
        emails = request.POST.getlist('emails[]')
        contacts = request.POST.getlist('contacts[]')
        locations = request.POST.getlist('locations[]')
        teamtypes = request.POST.getlist('teamtypes[]')
        countries = request.POST.getlist('countries[]')
        states = request.POST.getlist('states[]')
        country_ids = request.POST.getlist('country_ids[]')
        state_ids = request.POST.getlist('state_ids[]')
        teamtype_ids = request.POST.getlist('teamtype_id[]')
        

        teammembers_list = []
        for i in range(len(names)):
            teammember_schema = TeamMemberInvitedDetailSchema(
                name=names[i].strip(),
                email=emails[i].strip(),
                phone=contacts[i].strip(),  # Assuming 'contacts' represent phone numbers
                location=locations[i].strip(),
                designation=int(teamtype_ids[i]),
                state=int(state_ids[i]),
                country=int(country_ids[i])
            )
            teammembers_list.append(teammember_schema)

        teamMemberInviteSchema = TeamMemberInviteSchema(
            participantid=23,  # Set participant ID as needed
            teammembers=teammembers_list
        )

        # Example of printing the converted schema
        data = teamMemberInviteSchema.json()    
        print(data)
        #json_data = json.dumps(data)

        # JWT token to append
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUyMzA4MjcsInN1YiI6IjEiLCJjb21wYW55X2lkIjoiMSIsImxvZ2luX3BlcnNvbl9uYW1lIjoiSGl0ZXNoIEFua29kaWEiLCJyb2xlX2lkIjoyLCJjb21wYW55X3VybCI6Imh0dHA6Ly8xMjcuMC4wLjEifQ.bx_4ccCt4BvkuTgLFkgQwdSU0JY3UCHjK5MVhJlWc5E"

        # Example of sending this JSON data to the server
        url = 'http://localhost:5000/teammember/invite'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'  # Append token as Authorization header
        }

        response =  requests.post(url, headers=headers, data=data)
        print(response)
        print(response.json)