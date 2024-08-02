import base64
from django.shortcuts import HttpResponse, render, redirect
from app_360.ServiceHelper.ParticipantSurvey import ParticipantSurvey
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.participant_invite import ValidateParticipantDetailsSchema, CreateUserRequestSchema

participantobj = ParticipantSurvey()
utilityobj = UtilityClass()


def fetchparticipantid(request):
    print("HERE")
    pid_encoded = request.GET.get('pid', 'null')
    if pid_encoded == 'null' or pid_encoded == None or pid_encoded == 'None' or type(pid_encoded) == 'NoneType':
        pid_encoded = request.GET.get('strnameparticipantid')
    
    survey_id = request.POST.get('intnamesurveyid')
    company_id = 1
    print(pid_encoded)
    response = participantobj.fetchparticipantid(pid_encoded=pid_encoded)
    print(response)   
    if response['StatusCode'] == 5:
        context = {

            'encoded_pid': pid_encoded,
            'companyid' : 1, 
            'survey_id' : 1
        }
        return render(request, 'Homepage/homepage.html') 
    
    else:
        context = {

            'encoded_pid': pid_encoded,
            'companyid' : 1, 
            'survey_id' : 1
        }
        return render(request, 'Participant/createuser.html', context=context)
         

def setpassword(request):
    pid_encoded = request.POST.get('hiddenintparticipantid', '')
    company_id = request.POST.get('hiddenintcompanyid')
    date_of_birth = request.POST.get('datenamedob', '')
    email = request.POST.get('idemailemail', '')
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
            'email' : email
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
            'survey_id' : 1,    
        }   
    createUserRequestSchema = CreateUserRequestSchema(
        participantid = participantid, 
        username = email, 
        password = password , 
        companyid = company_id
    )

    response = participantobj.CreateUser(createUserRequestSchema)
     
    if response['StatusCode'] == 1:
        return render(request, 'Participant/after_user_created.html', context = context) 
    