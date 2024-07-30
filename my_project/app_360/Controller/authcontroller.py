from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper
from app_360.Schema.home import MyForm
from app_360.Schema.UserLoginSchema import UserLoginRequestSchema
from django.shortcuts import render, redirect, reverse
from app_360.utility.utility import UtilityClass
from app_360.Controller.survey.teamsurvey import FetchQuestions
from app_360.Schema.Team.survey import TeamMemberSurveyIds
from app_360.ServiceHelper.Teamsurvey import Survey

surveyobj = Survey()
utilityobj = UtilityClass()
AuthServiceHelperobj = AuthServiceHelper()

def auth(request):
    form = MyForm(request.POST)
    error_message = None
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        encoded_pid = request.POST.get('strnameparticipantid', '')
        surveyid = request.POST.get('intnamesurveyid', '')
        userLoginRequestSchema = UserLoginRequestSchema(
            username=username,
            password=password,
            company_id=1
        )
        context = {
            'encoded_pid': encoded_pid,
            'surveyid': surveyid  # hardcoded
        }
        try:
            token_details = AuthServiceHelperobj.Login(userLoginRequestSchema)
            print('token_details', token_details)
            print("-" * 30)
            print('encoded_pid', encoded_pid)
            print('surveyid', surveyid)
            access_token = token_details.get('access_token', None)
            if access_token:
                # Saving to cookies in browser 
                utilityobj.SaveAccessToken(access_token)
                role_id = token_details.get('role_id')
                # Render different templates based on role_id
                if role_id == 2:
                    return redirect('thanksfrom360')
                elif role_id == 3:
                    return render(request, 'Participant/before_survey_message.html', context=context)
                else:
                    # Default redirect for other roles or if role_id is not recognized
                    return redirect(reverse('index'))
        except Exception as e:
            print(f"Error during login: {e}")
            error_message = "Invalid credentials, please try again."
        else:
            # If form is not valid (e.g., fields are empty or not properly formatted)
            error_message = "Invalid credentials, please try again."
        
    # Render the login form with error message
    return render(request, 'Homepage/homepage.html', {'form': form, 'error_message': error_message})

#teammemberid : participantid : surveyid

def TeamMemberAssignSurvey(request):
    encoded_id = str(request.GET.get('id', None)) 
    id = utilityobj.decrypt(encoded_id)
    id_list = id.split(':')
    print(id_list[0], id_list[1], id_list[2])

    teamMemberSurveyIds = TeamMemberSurveyIds(
        participantid  = id_list[0], 
        teammemberid = id_list[1], 
        surveyid = id_list[2]
    )
    
    #assign_survey = surveyobj.TeamMemberAssignSurvey(teamMemberSurveyIds=teamMemberSurveyIds)
    #print(assign_survey)
    #if assign_survey['StatusCode'] == '1': 
    return FetchQuestions(request = request, teamMemberSurveyIds = teamMemberSurveyIds, page_number = 1)
    
    
