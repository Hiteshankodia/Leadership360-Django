from django.http import JsonResponse
from app_360.ServiceHelper.Teamsurvey import Survey
from django.shortcuts import render, redirect
from app_360.utility.utility import UtilityClass
from app_360.Schema.Team.survey import TeamFetchQuestionSchema
from app_360.Schema.Team.survey import TeamPreviewSurvey, TeamSubmitSurvey, TeamFetchAllSurveySchema, TeamSurveyUpdateStatusSchema
from app_360.Schema.Participant.survey import QuestionAnswerPair, UpdateSurveyAnswerTeam
import json

teamsurevyobj = Survey()
utilityobj = UtilityClass()

def TeamFetchQuestions(request, participantid = 0 , teamemberid = 0 , surveyid = 0 , page_number = 1):
    
    if participantid is None or participantid == 0:
        participantid = int(request.POST.get('hiddenstrpid', participantid))
   
      
    if teamemberid is None or teamemberid == 0 or teamemberid == '':
        teamemberid = int(request.POST.get('hiddentintteammemberid', teamemberid))
    

    milestone_message_index = int(request.POST.get('milestone_message_index', '0'))

    if surveyid is None or surveyid == 0 :
        surveyid = int(request.POST.get('hiddenintsurveyid', surveyid))
    

    if page_number == 1:
        page_number = int(request.POST.get('hiddenpage_number', page_number))
    

    record_count = 5
    
    miltestone_message_list = teamsurevyobj.FetchMilestoneMessage(surveyid)
    

    teamFetchQuestionSchema = TeamFetchQuestionSchema(
        participantid = participantid, 
        surveyid = surveyid, 
        record_count = record_count, 
        no_of_question = 10, 
        page_number = page_number, 
        teammemberid = teamemberid

    )

    question = teamsurevyobj.displayquestions(teamFetchQuestionSchema)
    
    
    show_submit_button = len(question) < record_count
    
    context = {
        'question': question, 
        'surveyid': surveyid,
        'page_number': page_number,
        'show_submit_button': show_submit_button, 
        'message' : miltestone_message_list[milestone_message_index]['message'],
        'miestone_index' : miltestone_message_list[milestone_message_index]['question_count'], 
        'milestone_message_index' : milestone_message_index, 
        'participantid' : participantid,
        'teammemberid' : teamemberid, 
        
    }
    
    if len(question) == 0: 
        
        teamPreviewSurvey = TeamPreviewSurvey(
                participantid = participantid, 
                surveyid = surveyid, 
                teammemberid = teamemberid) 
        return PreviewSurvey(request= request, teamPreviewSurvey = teamPreviewSurvey) 
    
    elif  ((int(page_number)-1) * record_count) == context['miestone_index'] :
        print(milestone_message_index) 
        context['milestone_message_index'] += 1 
        context["show_back_button"] = True
        return render(request, 'Team/milestone.html', context)
    
    else:
        if page_number > 1: 
            context["show_back_button"] = True
        return render(request, 'Team/survey.html', context)


def SaveAndFetchNextQuestions(request):
    print("SaveAND Fetch NExt Questions!")
    if request.method == 'POST':
        page_number = int(request.POST.get('hiddenpage_number', '1')) + 1 
        participantid = request.POST.get('hiddenstrpid', '')
        surveyid = request.POST.get('hiddenintsurveyid', '1')
        teammemberid = request.POST.get('hiddentintteammemberid')
        
        teamSurveyUpdateStatusSchema = TeamSurveyUpdateStatusSchema(
            participantid = participantid, 
            teammemberid = teammemberid,
            surveyid = surveyid, 
            status = 2
        )
        response = teamsurevyobj.TeamSurveyUpdateStatus(teamSurveyUpdateStatusSchema)
        if response['StatusCode'] == 1:
            question_responses = []

            # Loop through POST data to capture question responses
            for key, value in request.POST.items():
                if key.startswith('rdioAnswer_'):
                    question_id = int(key.split('_')[1])
                    answer_id = int(value)
                    presequence_id = int(request.POST.get(f'hiddenpresequenceid_{question_id}', ) or '0') + 1
                    question_responses.append({
                        "questionid": question_id,
                        "answerid": answer_id,
                        "presequencesurveyrequestid":  presequence_id
                    })

            # Construct survey data object
            survey_data = {
                "surveyid": surveyid,
                "participantid": participantid,
                "questionresponse": question_responses,
                "teammemberid": teammemberid
            }

           
            saved_status = teamsurevyobj.TeamSaveSurveyAnswers(survey_data)
            
            if saved_status['StatusCode'] == 1: 
                return TeamFetchQuestions(request,  participantid = participantid , teamemberid = teammemberid , surveyid = surveyid, page_number = page_number) 


def PreviewSurvey(request, teamPreviewSurvey : TeamPreviewSurvey):
    
    preview_survey = teamsurevyobj.TeamPreviewSurvey(teamPreviewSurvey)
    print(preview_survey)
    answer_options = {1 : 'Strongly Agree', 2 : 'Agree', 3 : 'Neutral', 4 : 'Disagree', 5 : 'Strongly Disagree'}
    context = {
        'preview_survey_data': preview_survey, 
        'enocded_pid' : teamPreviewSurvey.participantid,  
        'surveyid' : teamPreviewSurvey.surveyid,
        'teammemberid' : teamPreviewSurvey.teammemberid,
        'answer_options': answer_options,
    }

    return render(request, 'Team/survey_preview.html', context = context) 

def SubmitSurvey(request):  
    if request.method == 'POST':
        answers_json = request.POST.get('answers')
        surveyid = request.POST.get('hiddenintsurveyid')
        participantid = request.POST.get('hiddenstrpid')
        teammemberid = request.POST.get('hiddentintteammemberid')
        print(answers_json)
        # Update Survey Answers 
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
                    update_survey_answers = update_survey_answers = UpdateSurveyAnswerTeam(participantid=participantid,surveyid = surveyid, answers=answers_list, teammemberid = teammemberid)
                    teamsurevyobj.UpdateSurveyAnswer(update_survey_answers=update_survey_answers)
            except json.JSONDecodeError:
                # Handle JSON parsing errors
                return JsonResponse({'status': 'error', 'message': 'Invalid answers data format'}, status=400)
            
        

        teamSubmitSurvey = TeamSubmitSurvey(
                participantid = int(participantid), 
                surveyid = int(surveyid), 
                teammmeberid = int(teammemberid)
            )
        save_survey_status = teamsurevyobj.TeamSubmitSurvey(teamSubmitSurvey)

            
        if save_survey_status['StatusCode'] == 1:
            teamSurveyUpdateStatusSchema = TeamSurveyUpdateStatusSchema(
                participantid = participantid, 
                teammemberid = teammemberid,
                surveyid = surveyid, 
                status = 3
            )
            response = teamsurevyobj.TeamSurveyUpdateStatus(teamSurveyUpdateStatusSchema)
            if response['StatusCode'] == 1:
                return render(request, 'Team/AfterSurveyThankyou.html') 
        return render(request, 'Team/AfterSurveyThankyou.html')
