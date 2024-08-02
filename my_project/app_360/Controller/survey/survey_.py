from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.ServiceHelper.survey import Survey
from django.shortcuts import render, redirect
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema, QuestionRequestSchema
from app_360.Schema.Participant.preview_survey import PreviewParticipantSurvey, SaveParticipantSurvey
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema 

surveyobj = Survey()
utilityobj = UtilityClass()



def FetchQuestions(request, page_number = 1, encoded_pid = 'IkAXfN6qGtab6aeQF2IqNdqPNCtPbagwGlx95sWFCX4=' , survey_id = 1):
    
    milestone_message_index = int(request.POST.get('milestone_message_index', '0'))
    encoded_pid = request.POST.get('hiddenstrpid', encoded_pid)  # Provide a default value if not found in POST data
    survey_id = request.POST.get('hiddenintsurveyid', survey_id)
    if page_number == 1: 
        page_number = int(request.POST.get('hiddenpage_number', page_number)) 
    
    print(f"Encoded PID: {encoded_pid}")
    print(f"Survey ID: {survey_id}") # Get survey_id as string
    print(encoded_pid) 
    print("Page Number", page_number) 
    record_count = 5
 
    if encoded_pid:
        participant_id = utilityobj.decrypt(encoded_pid) 
     # Or raise an exception or handle gracefully
         
    print(f"Participant ID: {participant_id}")
    print(f"Survey ID: {survey_id}")
    print(f"Page Number: {page_number}")

    #Update Participant Survey Status to Inprogress. 
    participantSurvveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
        participant_id = participant_id, 
        survey_id = survey_id, 
        status = 2
    )
    surveyobj.ParticipantUpdateSurveyStatus(participantSurvveyStatusUpdateSchema)


    miltestone_message_list = surveyobj.FetchMilestoneMessage(survey_id)
    print(f"Milestone Messages: {miltestone_message_list}")

    fetchQuestionRequestSchema = FetchQuestionRequestSchema(
        participantid=participant_id,
        surveyid=survey_id,
        record_count=record_count,
        no_of_question=5,
        page_number=page_number
    )

    question = surveyobj.displayquestions(fetchQuestionRequestSchema)
    print(f"Questions: {question}")
    
    show_submit_button = len(question) < record_count
    
    context = {
        'question': question,
        'encodedpid': encoded_pid,  
        'surveyid': survey_id,
        'page_number': page_number,
        'show_submit_button': show_submit_button, 
        'message' : miltestone_message_list[milestone_message_index]['message'],
        'miestone_index' : miltestone_message_list[milestone_message_index]['question_count'], 
        'milestone_message_index' : milestone_message_index
        
    }
    
    if len(question) == 0: 
        print("*" * 100)
        return PreviewSurvey(request=request, participantid=participant_id, surveyid=survey_id)
    
    elif  ((int(page_number)-1) * record_count) == context['miestone_index'] :
        print(milestone_message_index) 
        context['milestone_message_index'] += 1 
        return render(request, 'Survey/milestone_message.html', context)
    
        
    
    elif len(question) == 0: 
        print("*" * 100)
        return PreviewSurvey(request=request, participantid=participant_id, surveyid=survey_id)
    
    else:
        return render(request, 'Survey/survey2.html', context)
    


def SaveAndFetchNextQuestions(request):
    print("SaveAND Fetch NExt Questions!")
    if request.method == 'POST':
        page_number = int(request.POST.get('hiddenpage_number', '1')) + 1 
        enocded_pid = request.POST.get('hiddenstrpid', '')
        surveyid = request.POST.get('hiddenintsurveyid', '1')
        print(enocded_pid)
        participant_id = utilityobj.decrypt(enocded_pid)
        print(page_number)
        print(participant_id)
        print(surveyid)
        

        question_responses = []

        # Loop through POST data to capture question responses
        for key, value in request.POST.items():
            if key.startswith('rdioAnswer_'):
                question_id = int(key.split('_')[1])
                answer_id = int(value)
                presequence_id = int(request.POST.get(f'hiddenpresequenceid_{question_id}', '0') or '0')

                question_responses.append({
                    "questionid": question_id,
                    "answerid": answer_id,
                    "presequencesurveyrequestid": presequence_id
                })

        # Construct survey data object
        survey_data = {
            "surveyid": surveyid,
            "participantid": participant_id,
            "questionresponse": question_responses,
            "teammemberid": 0  # Adjust as per your data structure
        }

        print("Survey Data:", survey_data)
        saved_status = surveyobj.SaveSurveyAnswers(survey_data)
        if saved_status['StatusCode'] == 1: 
            return FetchQuestions(request, page_number=page_number, encoded_pid=enocded_pid)


def PreviewSurvey(request, participantid = 23 , surveyid = 1):
    print('PreviewSurvey ')
    enocded_pid = request.POST.get('hiddenstrpid', '')
    surveyid = request.POST.get('hiddenintsurveyid', '1')
     
    participantid = utilityobj.decrypt(enocded_pid)
    print(participantid)
    print(surveyid)
    previewParticipantSurvey = PreviewParticipantSurvey(
        participantid = participantid, 
        surveyid = surveyid
    )
    preview_survey = surveyobj.PreviewSurvey(previewParticipantSurvey)
    print(preview_survey) 
    
    print("Length of preview survey List", len(preview_survey))
    
    context = {
        'preview_survey_data': preview_survey, 
        'enocded_pid' : enocded_pid,  
        'surveyid' : surveyid 
    }

    return render(request, 'Participant/preview_survey.html', context = context) 

def SubmitSurvey(request):  
    print("Submit Survey!")
    surveyid = request.POST.get('hiddenintsurveyid')
    enocded_pid = request.POST.get('hiddenstrpid')
    participantid = utilityobj.decrypt(enocded_pid)

    saveParticipantSurvey = SaveParticipantSurvey(
            participantid = participantid, 
            surveyid = surveyid
        )
    save_survey_status = surveyobj.SubmitSurvey(saveParticipantSurvey)
    print(save_survey_status)
    participantid = utilityobj.decrypt(enocded_pid)


    #Update Participant Survey Status to Inprogress. 
    participantSurvveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
        participant_id = participantid, 
        survey_id = surveyid, 
        status = 3
    )
    surveyobj.ParticipantUpdateSurveyStatus(participantSurvveyStatusUpdateSchema)

    if save_survey_status['StatusCode'] == 1:
        return render(request, 'Survey/Thankyou.html') 
    return render(request, 'Survey/Thankyou.html')
