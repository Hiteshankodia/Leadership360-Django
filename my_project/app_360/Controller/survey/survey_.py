from app_360.Schema.Participant.survey import FetchQuestionRequestSchema, SubmitParticipantSurveyRequestSchema
from app_360.ServiceHelper.survey import Survey
from django.shortcuts import render, redirect
from app_360.Schema.Participant.save_survey import SaveQuestionRequestSchema, QuestionRequestSchema
from app_360.Schema.Participant.preview_survey import PreviewParticipantSurvey, SaveParticipantSurvey
from app_360.utility.utility import UtilityClass
from app_360.Schema.Participant.survey import ParticipantSurvveyStatusUpdateSchema 
from app_360.Schema.Participant.survey import QuestionAnswerPair, UpdateSurveyAnswers
import json
from django.http import JsonResponse

surveyobj = Survey()
utilityobj = UtilityClass()



def FetchQuestions(request, encoded_pid=None, survey_id =0 , page_number=1):

    milestone_message_index = int(request.POST.get('milestone_message_index', '0'))

    if encoded_pid is None:
        encoded_pid = request.POST.get('strnameparticipantid', encoded_pid)
    
    
    if survey_id == 0:
        survey_id = request.POST.get('intnamesurveyid', survey_id)
    
    
    if page_number == 1: 
        page_number = int(request.POST.get('hiddenpage_number', page_number)) 
    encoded_pid = str(encoded_pid.replace(' ', '+'))
    
    record_count = 5
 
    if encoded_pid:
        participant_id = utilityobj.decrypt(encoded_pid) 
    
    

    access_token = request.COOKIES.get('access_token')
    miltestone_message_list = surveyobj.FetchMilestoneMessage(survey_id = survey_id, token = access_token)
    

    fetchQuestionRequestSchema = FetchQuestionRequestSchema(
        participantid=participant_id,
        surveyid=survey_id,
        record_count=record_count,
        no_of_question=10,
        page_number=page_number
    )
    
    question = surveyobj.displayquestions(fetchQuestionRequestSchema = fetchQuestionRequestSchema, token = access_token)
    
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
        return PreviewSurvey(request=request, participantid=participant_id, surveyid=survey_id)
    
    elif ((int(page_number)-1) * record_count) == context['miestone_index'] :
        print(milestone_message_index) 
        context['milestone_message_index'] += 1 
        context["show_back_button"] = True
        return render(request, 'Survey/milestone_message.html', context)
    
    elif len(question) == 0: 
        return PreviewSurvey(request=request, participantid=participant_id, surveyid=survey_id)
    
    else:
        if page_number > 1: 
            context["show_back_button"] = True
        return render(request, 'Survey/survey2.html', context)
    


def SaveAndFetchNextQuestions(request):
    print("SaveAND Fetch NExt Questions!")
    if request.method == 'POST':
        page_number = int(request.POST.get('hiddenpage_number', '1')) + 1 
        enocded_pid = request.POST.get('hiddenstrpid', '')
        surveyid = request.POST.get('hiddenintsurveyid', '1')
        participant_id = utilityobj.decrypt(enocded_pid)
        
        #Update Participant Survey Status to Inprogress. 
        participantSurvveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
            participantid = participant_id, 
            surveyid = surveyid, 
            status = 2
        )
        response = surveyobj.ParticipantUpdateSurveyStatus(participantSurvveyStatusUpdateSchema)
        if response['StatusCode'] == 1:

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

            
            access_token = request.COOKIES.get('access_token')

            saved_status = surveyobj.SaveSurveyAnswers(survey_data = survey_data, token=access_token)
            if saved_status['StatusCode'] == 1: 
                return FetchQuestions(request, page_number=page_number, encoded_pid=enocded_pid, survey_id=surveyid)


def PreviewSurvey(request, participantid=0, surveyid=1):
    

    
    
    enocded_pid = request.POST.get('hiddenstrpid', '')
    surveyid = request.POST.get('hiddenintsurveyid', '1')
     
    participantid = utilityobj.decrypt(enocded_pid)
    
    previewParticipantSurvey = PreviewParticipantSurvey(
        participantid=participantid, 
        surveyid=surveyid
    )
    access_token = request.COOKIES.get('access_token')
    
    preview_survey = surveyobj.PreviewSurvey(previewParticipantSurvey=previewParticipantSurvey, token=access_token)
    
    print(preview_survey)


    answer_options = {1 : 'Strongly Agree', 2 : 'Agree', 3 : 'Neutral', 4 : 'Disagree', 5 : 'Strongly Disagree'}
    
    context = {
        'preview_survey_data': preview_survey,
        'enocded_pid': enocded_pid,
        'surveyid': surveyid,
        'answer_options': answer_options,
    }

    return render(request, 'Participant/preview_survey.html', context=context)




def SubmitSurvey(request):
    if request.method == 'POST':
        answers_json = request.POST.get('answers')
        surveyid = request.POST.get('hiddenintsurveyid')
        encoded_pid = request.POST.get('hiddenstrpid')
        participantid = utilityobj.decrypt(encoded_pid)

        if answers_json:
            try:
                # Parse and validate answers_json
                answers_list = json.loads(answers_json)
                if isinstance(answers_list, list) and all(isinstance(item, dict) for item in answers_list):
                    answers_list = [
                        QuestionAnswerPair(questionid=int(item["questionId"]), answerid=int(item["answerId"]))
                        for item in answers_list
                    ]

                    # Update survey answers
                    update_survey_answers = UpdateSurveyAnswers(participantid=participantid, surveyid=surveyid, answers=answers_list)
                    surveyobj.UpdateSurveyAnswer(update_survey_answers=update_survey_answers)
            except json.JSONDecodeError:
                # Handle JSON parsing errors
                return JsonResponse({'status': 'error', 'message': 'Invalid answers data format'}, status=400)
        
        # Submit the survey
        saveParticipantSurvey = SaveParticipantSurvey(
            participantid=participantid, 
            surveyid=surveyid, 
            companyid = int(request.COOKIES.get('company_id'))
        )
        access_token = request.COOKIES.get('access_token')
        save_survey_status = surveyobj.SubmitSurvey(submitParticipantSurveyRequestSchema=saveParticipantSurvey, token=access_token)
        
        # Update participant survey status to Inprogress
        participantSurveyStatusUpdateSchema = ParticipantSurvveyStatusUpdateSchema(
            participantid=participantid, 
            surveyid=surveyid, 
            status=3
        )
        surveyobj.ParticipantUpdateSurveyStatus(participantSurveyStatusUpdateSchema)

        if save_survey_status['StatusCode'] == 1:
            return render(request, 'Survey/Thankyou.html')
        else:
            # Handle the case where the survey submission fails
            return render(request, 'Survey/Error.html', {'message': 'There was an issue submitting the survey.'})
    
    # Handle non-POST requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
