import base64
from django.shortcuts import HttpResponse, render, redirect
from app_360.ServiceHelper.ParticipantSurvey import ParticipantSurvey
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.participant_invite import ValidateParticipantDetailsSchema, CreateUserRequestSchema
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema

participantobj = ParticipantSurvey()
utilityobj = UtilityClass()



def fetchparticipantid(request, pid_encoded = 1, surveyid = 1):
    print('fetchparticipantid')
    pid_encoded = request.GET.get('pid', 'null')
    if pid_encoded == 'null':
        print("nUll")
        if request.method == 'POST':
            pid_encoded = request.POST.get('strnameparticipantid', 'null')
    
    survey_id = request.POST.get('intnamesurveyid', surveyid)
    company_id = int(request.COOKIES.get('company_id'))
    pid_encoded = str(pid_encoded.replace(' ', '+'))
    print('pid_encoded', pid_encoded)

    print(survey_id)
    response = participantobj.fetchparticipantid(pid_encoded=pid_encoded)
    print(response)   
    if response['StatusCode'] == 5:
        context = {

            'pid_encoded': pid_encoded,
            'companyid' : int(request.COOKIES.get('company_id')), 
            'survey_id' : survey_id
        }
        return render(request, 'Homepage/homepage.html', context) 
    
    else:
        context = {

            'pid_encoded': pid_encoded,
            'companyid' : int(request.COOKIES.get('company_id')), 
            'survey_id' : survey_id
        }
        return render(request, 'Participant/createuser.html', context=context)
         

def setpassword(request):
    print('setpassword')
    pid_encoded = request.POST.get('hiddenintparticipantid', '')
    company_id = request.POST.get('hiddenintcompanyid')
    date_of_birth = request.POST.get('datenamedob', '')
    email = request.POST.get('idemailemail', '')
    survey_id = request.POST.get('intnamesurveyid')
    print(pid_encoded)
    print(company_id)
    print(date_of_birth)
    print(email)    

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
    print(response)
    print('Check Participant Ran Successfully !')

    if response['StatusCode'] == 5:
        # Render the setpassword.html template
        return render(request, 'Participant/setpassword.html', context=context)
    else:
        print("here")
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
    print(encoded_pid)
    print(company_id)
    print(password)
    print(confirmpassword)
    print(email) 
    print('save_password!')
    
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
    print(survey_id)
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
    