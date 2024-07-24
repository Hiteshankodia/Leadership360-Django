from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper
from app_360.Schema.home import MyForm
from app_360.Schema.UserLoginSchema import UserLoginRequestSchema
from django.shortcuts import render, redirect, reverse
from app_360.utility.utility import UtilityClass

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
                    return redirect(reverse('participantinvite'))
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
