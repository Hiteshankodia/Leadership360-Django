from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper
from app_360.Schema.home import MyForm
from app_360.Schema.UserLoginSchema import UserLoginRequestSchema
from django.shortcuts import render, redirect, reverse
from app_360.utility.utility import UtilityClass
from app_360.Controller.survey.survey_ import FetchQuestions 
from app_360.Controller.survey.teamsurvey import TeamFetchQuestions
from app_360.Schema.Team.survey import TeamMemberSurveyIds, TeamFetchAllSurveySchema
from app_360.ServiceHelper.Teamsurvey import Survey
from app_360.ServiceHelper.ParticipantSurvey import ParticipantSurvey
from app_360.Controller.Team.inviteTeam import Beforeinvite
from django.shortcuts import HttpResponse
from urllib.parse import urlparse


participantsurveyobj = ParticipantSurvey()
surveyobj = Survey()
utilityobj = UtilityClass()
AuthServiceHelperobj = AuthServiceHelper()

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

def auth(request):
    if request.method == 'POST':
        print("Auth Method!")
        form = MyForm(request.POST)
        error_message = None
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            encoded_pid = request.POST.get('strnameparticipantid', '')
            surveyid = request.POST.get('intnamesurveyid', '')
            encoded_pid = str(encoded_pid.replace(' ', '+'))
            surveyid = 1
            print(username)
            print(password)
            print(encoded_pid)
            print(surveyid)

            userLoginRequestSchema = UserLoginRequestSchema(
                username=username,
                password=password,
                company_id=int(request.COOKIES.get('company_id'))
            )

            print("Auth Method!")
            print(encoded_pid)
            print(surveyid)
            
            try:
                token_details = AuthServiceHelperobj.Login(userLoginRequestSchema)
                print('token_details', token_details)
                print("-" * 30)
                
                access_token = token_details.get('access_token', None)

                print('access_token', access_token)
                if access_token:
                    # Create a response object to set the cookie
                    response = HttpResponse()
                    # Set the access_token in a cookie
                    response.set_cookie('access_token', access_token, max_age=18600)  # Cookie will expire in 1 hour
                    
                    # Continue processing based on role_id
                    role_id = token_details.get('role_id')
                    if role_id == 2:
                        response = redirect('thanksfrom360')
                        response.set_cookie('access_token', access_token, max_age=18600)  # Ensure the cookie is set
                        return response
                    
                    elif role_id == 3:
                        participantid = token_details['login_user_entity_id']
                        encoded_pid = utilityobj.encrypt(str(participantid)) 
                        print("participantid For now", participantid)
                        status = participantsurveyobj.FetchSurveyStatus(participantid)

                        print("FetchSurveyStatus", status)
                        
                        context = {
                            'encoded_pid': encoded_pid,
                            'surveyid': surveyid, 
                            'companyid': int(request.COOKIES.get('company_id'))
                        }
                        if status["status"] == "TeamInvite":
                            return Beforeinvite(request=request, encoded_pid=encoded_pid)
                        if status["status"] == "Assigned":
                            response = render(request, 'Participant/before_survey_message.html', context=context)
                            response.set_cookie('access_token', access_token, max_age=3600)  # Ensure the cookie is set
                            return response
                        elif status["status"] == "In Progress":
                            return FetchQuestions(request=request, encoded_pid=encoded_pid, survey_id=surveyid)
                        elif status["status"] == "Completed":
                            response = render(request, 'Survey/Thankyou.html', context=context)
                            response.set_cookie('access_token', access_token, max_age=3600)  # Ensure the cookie is set
                            return response

                    else:
                        response = redirect(reverse('index'))
                        response.set_cookie('access_token', access_token, max_age=3600)  # Ensure the cookie is set
                        return response
            except Exception as e:
                print(f"Error during login: {e}")
                error_message = "Invalid credentials, please try again."
            else:
                error_message = "Invalid credentials, please try again."
            
        # Render the login form with error message
        return render(request, 'Homepage/homepage.html', {'form': form, 'error_message': error_message})


#teammemberid : participantid : surveyid

def TeamMemberAssignSurvey(request):

    encoded_id = str(request.GET.get('id', None)) 
    encoded_id = str(encoded_id.replace(' ', '+'))
    print(encoded_id)
    id = utilityobj.decrypt(encoded_id)
    id_list = id.split(':')
    print(id_list)
    participantid = id_list[1]
    teammemberid = id_list[0]
    surveyid = id_list[2]
    teamMemberSurveyIds = TeamMemberSurveyIds(
        teammemberid  = teammemberid, 
        participantid = participantid, 
        surveyid = surveyid
    )
    #edited
    print('participantid')
    print(participantid)
    print(teammemberid)

    


    assign_survey = surveyobj.TeamMemberAssignSurvey(teamMemberSurveyIds=teamMemberSurveyIds)
    print(assign_survey)
    if assign_survey['StatusCode'] == 1:

        teamFetchAllSurveySchema = TeamFetchAllSurveySchema( 
            participantid = participantid, 
            teammemberid = teammemberid
        )
        
        status = surveyobj.FetchTeamSurveyStatus(teamFetchAllSurveySchema)
        print("FetchTeamSurveyStatus", status)
        

        full_url = request.build_absolute_uri()
        parsed_url = urlparse(full_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        print('Base URL:', base_url)
        
        # Fetch company ID using the base URL
        response_data = AuthServiceHelperobj.FetchCompanyid(base_url)
        company_id = response_data.get('companyid')
        print('Company ID:', company_id)

        context = {
            'participantid' : participantid,
            'teammemberid' : teammemberid,
            'surveyid': surveyid, 
            'companyid': company_id 
        }

        if status["status"] == "Assigned":
            return render(request, 'Team/before_survey_message.html', context=context) 
        
        elif status["status"]  == "In Progress":
            return TeamFetchQuestions(request = request, participantid = participantid, teamemberid = teammemberid, surveyid = surveyid, page_number = 1)
        
        elif status["status"] == "Completed":
            return render(request, 'Team/AfterSurveyThankyou.html', context = context)



def ParticipantSurveyAfterInvite(request):

    encoded_pid = request.GET.get('encoded_pid', None) 
    
    print('participantSurveyAfterInvite!')
    print(encoded_pid)
    context = {
            'encoded_pid': encoded_pid,
            'surveyid': 1, 
            'companyid': int(request.COOKIES.get('company_id'))
        }
    
    return render(request, 'Participant/before_survey_message.html', context=context) 