from django.shortcuts import render, redirect
from app_360.ServiceHelper.FetchDetailsMaster import FetchMasterData
from django.conf import settings
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema 
from app_360.ServiceHelper.survey import Survey
from app_360.Schema.Team.invite import TeamMemberInvitedDetailSchema, TeamMemberInviteSchema
import requests
from app_360.ServiceHelper.TeamInvite import TeamInviteClass
from app_360.utility.utility import UtilityClass


surveyobj = Survey()
fetchmasterobj = FetchMasterData()
teamInviteobj = TeamInviteClass()
utilityobj = UtilityClass()


def Beforeinvite(request, encoded_pid):
    encoded_pid = request.GET.get('encoded_pid', encoded_pid)
    print(encoded_pid)  
    context = {
            'encoded_pid' : encoded_pid     
    }
        
    return render(request, "Team/before_invite.html", context=context)


def TeamFormDetails(request):
    
    pid_encoded = request.GET.get('encoded_pid', None)
    pid_encoded = str(pid_encoded.replace(' ', '+'))
    print('participantid in teamform details', pid_encoded)

    countries = fetchmasterobj.FetchCountry()
    context = {
        'countries': countries,
        'itereration' : range(1,9), 
        'teamtype':  (eval(settings.TEAM_TYPE)), 
        'encoded_pid' : pid_encoded
    }
    return render(request, 'Team/team_invite.html', context)


def load_states(request):
    country_id = request.POST.get('country_id')
    states = fetchmasterobj.FetchState(country_id)
    return states


def SaveData(request):
    if request.method == 'POST':
        pid_encoded = request.POST.get('strnameparticipantid', None)
        pid_encoded = str(pid_encoded.replace(' ', '+'))
        # Print encoded_pid for debugging purposes
        print(pid_encoded, "saveData")

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
        
        names = [name for name in names if name.strip()]
  
        TeamInviteList = []
        for i in range(len(names)): 
            teamdata = { 
                'name': names[i].upper(),
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
            'encoded_pid' : pid_encoded
             
        }
        
        return render(request, 'Team/invite_preview.html', context)


def TeamInvite(request):
    if request.method == 'POST':
        encoded_pid = request.POST.get('strnameparticipantid', None)
        encoded_pid = str(encoded_pid.replace(' ', '+'))
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
        
        names = [name for name in names if name.strip()]

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

        
        print("participantid in TeamInvite ", encoded_pid)
        encoded_pid = str(encoded_pid.replace(' ', '+'))
        participantid = utilityobj.decrypt(encoded_pid)

        teamMemberInviteSchema = TeamMemberInviteSchema(
            participantid=participantid,  # Set participant ID as needed
            teammembers=teammembers_list
        )
         
        print("Team Inivte Method!") 
        response = teamInviteobj.TeamInvite(teamMemberInviteSchema)
        print(response)
        if response.get('StatusCode') == 1: 
            
            participantSurvveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
            participantid = participantid, 
            surveyid = 1, 
            status = 1
            )

            context = {
            
            'encoded_pid' : encoded_pid
             
            }
            surveyobj.ParticipantUpdateSurveyStatus(participantSurvveyStatusUpdateSchema)
            return render(request, 'Participant/survey_now_or_later.html', context=context) 

        
 
    