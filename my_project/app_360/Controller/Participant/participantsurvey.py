import base64
from django.shortcuts import HttpResponse, render, redirect
from app_360.ServiceHelper.ParticipantSurvey import ParticipantSurvey
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.participant_invite import ValidateParticipantDetailsSchema, CreateUserRequestSchema
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema
from urllib.parse import urlparse
from app_360.ServiceHelper.AuthServiceHelper import AuthServiceHelper 

participantobj = ParticipantSurvey()
utilityobj = UtilityClass()
authobj = AuthServiceHelper()

def fetchparticipantid(request, pid_encoded=1, surveyid=1):
    
    # Retrieve the participant ID from the GET or POST data
    pid_encoded = request.GET.get('pid', 'null')
    if pid_encoded == 'null':
        print("nUll")
        if request.method == 'POST':
            pid_encoded = request.POST.get('strnameparticipantid', 'null')
    
    # Get the full URL and extract the base URL
    full_url = request.build_absolute_uri()
    parsed_url = urlparse(full_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    
    # Fetch company ID using the base URL
    response_data = authobj.FetchCompanyid(base_url)
    company_id = response_data.get('companyid')
    
    # Prepare the participant ID and survey ID
    pid_encoded = str(pid_encoded.replace(' ', '+'))
    survey_id = request.POST.get('intnamesurveyid', surveyid)
    
    # Fetch participant ID and determine the response
    response_data = participantobj.fetchparticipantid(pid_encoded=pid_encoded)
    
    # Prepare the context for rendering the response
    context = {
        'pid_encoded': pid_encoded,
        'companyid': company_id,  # Use the fetched company_id
        'survey_id': survey_id
    }
    
    # Render the appropriate template based on the response status
    if response_data['StatusCode'] == 5:
        return redirect('index')
    else:
        return render(request, 'Participant/createuser.html', context=context)
    
    
         

def setpassword(request):
    print('setpassword')
    pid_encoded = request.POST.get('hiddenintparticipantid', '')
    company_id = request.POST.get('hiddenintcompanyid')
    date_of_birth = request.POST.get('datenamedob', '')
    email = request.POST.get('idemailemail', '')
    survey_id = request.POST.get('intnamesurveyid')
    
    #decode and user the participantid here
    participantid = utilityobj.decrypt(pid_encoded)
    validateParticipantDetailsSchema = ValidateParticipantDetailsSchema(
        email = email, 
        dob = date_of_birth, 
        participantid =  participantid, #encoded_pid 
        companyid = company_id   
    )

    context = {
    
            'pid_encoded': pid_encoded,
            'companyid' : company_id,  #hardcoded, 
            'email' : email, 
            'survey_id': survey_id, 
            'error_message' : ''
        }
    
    response = participantobj.CheckParticipantDetails(validateParticipantDetailsSchema)
    
    if response['StatusCode'] == 5:
        # Render the setpassword.html template
        return render(request, 'Participant/setpassword.html', context=context)
    else:
        
        context['error_message'] = 'The email or date of birth does not match'
        return render(request, 'Participant/createuser.html', context=context)


def save_password(request):
    print("save Password!")
    encoded_pid = request.POST.get('strnameparticipantid', '')
    company_id = request.POST.get('intnamecompanyid', '')
    password = request.POST.get('str_name_new_password')
    confirmpassword = request.POST.get('str_name_new_password')
    email = request.POST.get('emailnameemailid')
    survey_id = request.POST.get('intnamesurveyid')
    
    participantid = utilityobj.decrypt(encoded_pid)
    participantid = participantid
    context = {

            'encoded_pid': encoded_pid,  
            'survey_id' : survey_id,    
        }   
    createUserRequestSchema = CreateUserRequestSchema(
        participantid = participantid, 
        username = email, 
        password = password , 
        companyid = company_id
    )

    response = participantobj.CreateUser(createUserRequestSchema)
    participantSurvveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
        participantid = participantid, 
        surveyid = 1, 
        status = 1
    )
     
    participantobj.ParticipantUpdateSurveyStatus(participantSurvveyStatusUpdateSchema)

    if response['StatusCode'] == 1:
        return render(request, 'Participant/after_user_created.html', context = context) 
    else: 
        pass
    